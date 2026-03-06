"""
CSV/Excel解析服务 - 支持多种券商交易记录导入

支持的券商:
- 同花顺 (tonghuashun)
- 国泰君安/国泰海通 (gtja)
- 国信证券 (guosen, Excel)
- moomoo (moomoo)
- 盈透证券 (ibkr)
- 通用格式 (generic)
"""

import csv
import pandas as pd
from typing import List, Dict, Any, Optional
from decimal import Decimal, InvalidOperation
from datetime import datetime
import io
import chardet
import re


class CSVParseError(Exception):
    """CSV解析错误"""
    pass


class BrokerTemplate:
    """券商CSV模板基类"""

    # 子类需要覆盖的属性
    COLUMN_MAPPING: Dict[str, str] = {}  # 券商列名 -> 系统字段名
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    REQUIRED_COLUMNS: List[str] = []  # 必填列
    # 是否允许在导入时用解析结果自动更新账户的“剩余资金/现金余额”
    # 某些券商导出的资金流水中余额字段并不可靠（或存在多口径），可在子类中关闭。
    IMPORT_CASH_BALANCE: bool = True

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.cash_balance: Optional[Decimal] = None
        self.cash_currency: Optional[str] = None

    def parse_file(self, filename: str, file_content: bytes) -> List[Dict[str, Any]]:
        """根据文件类型解析交易数据"""
        lower_name = (filename or "").lower()
        if lower_name.endswith(".csv"):
            return self.parse_csv(file_content)
        if lower_name.endswith(".xls") or lower_name.endswith(".xlsx"):
            return self.parse_excel(file_content)
        raise CSVParseError("仅支持CSV或Excel文件")

    def parse_csv(self, file_content: bytes) -> List[Dict[str, Any]]:
        """
        解析CSV文件并返回标准化的交易记录

        Args:
            file_content: CSV文件字节内容

        Returns:
            标准化的交易记录列表

        Raises:
            CSVParseError: CSV格式错误或必填字段缺失
        """
        self.errors = []
        try:
            # 自动检测编码
            encoding = self._detect_encoding(file_content)

            # 读取CSV
            df = pd.read_csv(
                io.BytesIO(file_content),
                encoding=encoding,
                skipinitialspace=True,
                dtype=str,
                keep_default_na=False
            )

            return self._parse_dataframe(df)
        except Exception as e:
            raise CSVParseError(f"CSV解析失败: {str(e)}")

    def parse_excel(self, file_content: bytes) -> List[Dict[str, Any]]:
        """解析Excel文件并返回标准化的交易记录"""
        raise CSVParseError("该券商模板暂不支持Excel导入")

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """
        解析单行数据为标准格式
        子类需要实现此方法
        """
        raise NotImplementedError

    def _parse_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析DataFrame为标准交易记录列表"""
        self._validate_columns(df)

        trades = []
        for idx, row in df.iterrows():
            try:
                trade = self.parse_row(row)
                if trade:  # 跳过空行
                    trades.append(trade)
            except Exception as e:
                self.errors.append({
                    'row': int(idx) + 2,  # +2 因为标题行且从1开始
                    'error': str(e)
                })

        return trades

    def _detect_encoding(self, file_content: bytes) -> str:
        """自动检测文件编码"""
        result = chardet.detect(file_content)
        encoding = result['encoding']

        # 常见中文编码处理
        if encoding and 'gb' in encoding.lower():
            return 'gbk'
        elif encoding and encoding.lower() in ['utf-8', 'utf-8-sig']:
            return 'utf-8-sig'
        else:
            # 默认尝试 utf-8
            return 'utf-8'

    def _validate_columns(self, df: pd.DataFrame):
        """验证必填列是否存在"""
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise CSVParseError(f"缺少必填列: {', '.join(missing_cols)}")

    def _safe_decimal(self, value: Any, default: Decimal = Decimal('0')) -> Decimal:
        """安全转换为Decimal"""
        try:
            if pd.isna(value) or value == '':
                return default
            # 移除逗号分隔符
            if isinstance(value, str):
                value = value.replace(',', '')
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return default

    def _safe_decimal_optional(self, value: Any) -> Optional[Decimal]:
        """安全转换为Decimal(允许空值)"""
        try:
            if pd.isna(value) or value == '':
                return None
            if isinstance(value, str):
                value = value.replace(',', '')
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None

    def _parse_datetime(self, date_str: str) -> datetime:
        """解析日期时间字符串"""
        try:
            return datetime.strptime(str(date_str).strip(), self.DATE_FORMAT)
        except ValueError:
            # 尝试其他常见格式
            for fmt in ['%Y/%m/%d %H:%M:%S', '%Y-%m-%d', '%Y/%m/%d']:
                try:
                    dt = datetime.strptime(str(date_str).strip(), fmt)
                    # 如果没有时间,设为09:30(开盘时间)
                    if fmt in ['%Y-%m-%d', '%Y/%m/%d']:
                        dt = dt.replace(hour=9, minute=30, second=0)
                    return dt
                except ValueError:
                    continue
            raise ValueError(f"无法解析日期时间: {date_str}")

    def _read_excel_dataframe(self, file_content: bytes) -> pd.DataFrame:
        """读取Excel文件为DataFrame,兼容文本导出的xls"""
        try:
            df = pd.read_excel(io.BytesIO(file_content), dtype=str, keep_default_na=False)
            if df.empty:
                raise CSVParseError("Excel内容为空")
            df.columns = [str(col).strip().replace('\ufeff', '') for col in df.columns]
            return df
        except Exception:
            df = self._read_excel_text_table(file_content)
            df.columns = [str(col).strip().replace('\ufeff', '') for col in df.columns]
            return df

    def _read_excel_text_table(self, file_content: bytes) -> pd.DataFrame:
        """解析文本形式的Excel导出(以制表符分隔)"""
        encoding = self._detect_encoding(file_content)
        text = file_content.decode(encoding, errors='ignore')
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            raise CSVParseError("Excel内容为空")

        reader = csv.reader(lines, delimiter='\t')
        rows = [[self._clean_cell(cell) for cell in row] for row in reader]
        if not rows:
            raise CSVParseError("Excel内容为空")

        header_row_idx: Optional[int] = None
        for idx, row in enumerate(rows[:50]):
            non_empty = [cell for cell in row if cell]
            if not non_empty:
                continue
            if len(non_empty) == 1 and non_empty[0].lower().startswith('sep='):
                continue
            if len(non_empty) < 3:
                continue
            joined = ''.join(non_empty)
            if any(token in joined for token in ('日期', '时间', '证券', '股票', '代码', '摘要', '业务')):
                header_row_idx = idx
                break

        if header_row_idx is None:
            header_row_idx = 0

        header_row = rows[header_row_idx]
        header_indices: List[int] = []
        header_names: List[str] = []
        seen: Dict[str, int] = {}
        for col_idx, raw_name in enumerate(header_row):
            name = (raw_name or "").strip()
            if not name:
                continue
            count = seen.get(name, 0) + 1
            seen[name] = count
            header_indices.append(col_idx)
            header_names.append(name if count == 1 else f"{name}_{count}")

        if not header_names:
            raise CSVParseError("未找到Excel表头")

        data_rows = []
        max_index = max(header_indices)
        for row in rows[header_row_idx + 1:]:
            if len(row) <= max_index:
                row = row + [''] * (max_index + 1 - len(row))
            record = {header_names[i]: row[header_indices[i]] for i in range(len(header_names))}
            if not any(str(v).strip() for v in record.values()):
                continue
            data_rows.append(record)
        return pd.DataFrame(data_rows)

    def _clean_cell(self, value: Any) -> str:
        """清理Excel单元格文本"""
        text = str(value).strip()
        if text.startswith('=\"') and text.endswith('\"'):
            text = text[2:-1]
        elif text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text.strip()


class TonghuashunTemplate(BrokerTemplate):
    """同花顺券商CSV模板解析器"""

    COLUMN_MAPPING = {
        '成交日期': 'trade_time',
        '证券代码': 'symbol',
        '证券名称': 'symbol_name',
        '买卖标志': 'side',
        '成交数量': 'quantity',
        '成交价格': 'price',
        '成交金额': 'amount',
        '手续费': 'fee',
        '成交编号': 'trade_id_external'
    }

    REQUIRED_COLUMNS = ['成交日期', '证券代码', '买卖标志', '成交数量', '成交价格']

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析同花顺CSV行"""
        # 跳过空行
        symbol_raw = row.get('证券代码')
        if pd.isna(symbol_raw) or str(symbol_raw).strip() == '':
            return None

        # 解析买卖方向
        side_text = str(row['买卖标志']).strip()
        if '买' in side_text or 'buy' in side_text.lower():
            side = 'buy'
        elif '卖' in side_text or 'sell' in side_text.lower():
            side = 'sell'
        else:
            raise ValueError(f"无法识别买卖标志: {side_text}")

        # 标准化股票代码
        symbol = self._normalize_symbol(str(row['证券代码']))

        # 解析数量和价格
        quantity = self._safe_decimal(row['成交数量'])
        price = self._safe_decimal(row['成交价格'])

        if quantity <= 0 or price <= 0:
            raise ValueError(f"数量或价格无效: quantity={quantity}, price={price}")

        # 计算成交金额(如果CSV中没有)
        amount_col = row.get('成交金额')
        if pd.notna(amount_col) and amount_col != '':
            amount = self._safe_decimal(amount_col)
        else:
            amount = quantity * price

        # 手续费
        fee = self._safe_decimal(row.get('手续费', 0))

        # 成交编号(用于去重)
        trade_id_external = str(row.get('成交编号', ''))
        if not trade_id_external or trade_id_external == 'nan':
            # 如果没有成交编号,生成唯一标识
            trade_id_external = f"{symbol}_{row['成交日期']}_{side}_{quantity}_{price}"

        # 解析时间
        trade_time = self._parse_datetime(row['成交日期'])

        # 构建标准交易记录
        trade = {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': f"导入自同花顺 - {row.get('证券名称', '')}"
        }

        return trade

    def _normalize_symbol(self, code: str) -> str:
        """
        标准化股票代码为交易所格式

        规则:
        - 6开头 -> 上海证券交易所 (.SH)
        - 0/3开头 -> 深圳证券交易所 (.SZ)

        Examples:
            '600000' -> '600000.SH'
            '000001' -> '000001.SZ'
            '300750' -> '300750.SZ'
        """
        code = str(code).strip()

        # 移除已有的交易所后缀
        if '.' in code:
            return code

        # 确保是6位数字
        if len(code) != 6 or not code.isdigit():
            raise ValueError(f"无效的股票代码: {code}")

        # 根据首位数字判断交易所
        if code.startswith('6'):
            return f"{code}.SH"  # 上海
        elif code.startswith('0') or code.startswith('3'):
            return f"{code}.SZ"  # 深圳
        else:
            # 其他情况默认深圳
            return f"{code}.SZ"


class GTJATemplate(BrokerTemplate):
    """
    国泰君安资金股份流水CSV模板解析器

    券商导出的CSV格式(中文列名):
    - 交收日期: 交易日期 (YYYYMMDD)
    - 业务说明: 证券买入/证券卖出/港股通买入成交/港股通卖出成交
    - 证券代码: 股票代码
    - 证券名称: 股票名称
    - 成交价格: 成交价
    - 成交数量: 成交数量
    - 成交金额: 成交金额
    - 证券余额: 成交后持仓数量
    - 总佣金/印花税/过户费/其他费: 手续费构成
    """

    # 国泰君安/国泰海通资金流水中的“余额/剩余资金”口径可能不一致，导入时不自动更新账户余额，交由用户手动维护。
    IMPORT_CASH_BALANCE = False

    REQUIRED_COLUMNS = ['交收日期', '业务说明', '证券代码', '成交价格', '成交数量']
    EXCEL_REQUIRED_COLUMNS = ['交收日期', '摘要', '证券代码', '成交价格', '成交数量']
    EXCEL_DATE_COLUMNS = ['交收日期', '成交日期', '日期']
    EXCEL_SUMMARY_COLUMNS = ['摘要', '操作', '业务说明']
    EXCEL_PRICE_COLUMNS = ['成交价格', '成交均价', '成交价']
    EXCEL_FEE_COLUMNS = ['手续费', '印花税', '其他杂费', '过户费', '总佣金']

    def parse_excel(self, file_content: bytes) -> List[Dict[str, Any]]:
        """解析国泰君安/国泰海通导出的xls/xlsx"""
        self.errors = []
        try:
            df = self._read_excel_dataframe(file_content)
            self._normalize_excel_columns(df)
            self._extract_cash_balance_from_excel(df)
            return self._parse_excel_dataframe(df)
        except Exception as e:
            raise CSVParseError(f"Excel解析失败: {str(e)}")

    def _parse_excel_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析国泰君安/国泰海通资金流水查询导出的DataFrame"""
        # 有的导出和CSV列名一致（含“业务说明”），直接复用CSV逻辑
        if '业务说明' in df.columns:
            self._validate_columns(df)
            return self._parse_dataframe(df)

        missing_cols: List[str] = []
        if not any(col in df.columns for col in self.EXCEL_DATE_COLUMNS):
            missing_cols.append('交收日期/成交日期/日期')
        if not any(col in df.columns for col in self.EXCEL_SUMMARY_COLUMNS):
            missing_cols.append('摘要/操作/业务说明')
        for col in ['证券代码', '成交数量']:
            if col not in df.columns:
                missing_cols.append(col)
        if not any(col in df.columns for col in self.EXCEL_PRICE_COLUMNS):
            missing_cols.append('成交价格/成交均价/成交价')
        if missing_cols:
            raise CSVParseError(f"缺少必填列: {', '.join(missing_cols)}")

        trades: List[Optional[Dict[str, Any]]] = []
        refunded_contracts: set[str] = set()
        contract_trade_indices: Dict[str, List[int]] = {}
        for idx, row in df.iterrows():
            try:
                if self._is_subscription_refund_row(row):
                    contract_no = self._get_contract_no(row)
                    if contract_no:
                        refunded_contracts.add(contract_no)
                        for trade_idx in contract_trade_indices.get(contract_no, []):
                            trades[trade_idx] = None
                    continue

                if self._is_hk_duplicate_trade_row(row):
                    continue

                trade = self._parse_excel_row(row)
                if trade:
                    contract_no = self._get_contract_no(row)
                    if contract_no and contract_no in refunded_contracts and trade.get('side') == 'buy':
                        continue
                    trades.append(trade)
                    if contract_no:
                        contract_trade_indices.setdefault(contract_no, []).append(len(trades) - 1)
            except Exception as e:
                self.errors.append({
                    'row': int(idx) + 2,
                    'error': str(e)
                })
        return [trade for trade in trades if trade]

    def _get_contract_no(self, row: pd.Series) -> str:
        return str(row.get('合同编号', '')).strip()

    def _is_subscription_refund_row(self, row: pd.Series) -> bool:
        summary = str(
            row.get('摘要')
            or row.get('操作')
            or row.get('业务说明')
            or ''
        ).strip()
        return '申购资金返款' in summary

    def _is_hk_duplicate_trade_row(self, row: pd.Series) -> bool:
        summary = str(
            row.get('摘要')
            or row.get('操作')
            or row.get('业务说明')
            or ''
        ).strip()
        side = self._resolve_side(summary)
        if not side:
            return False

        market_name = str(row.get('市场名称', '')).strip()
        code = str(row.get('证券代码', '')).strip()
        is_hk_market = 'HK' in market_name or (code.isdigit() and len(code) == 5)
        if not is_hk_market:
            return False

        amount_value = self._safe_decimal(row.get('发生金额') or row.get('本次金额') or 0)
        stock_balance = self._safe_decimal(row.get('股票余额') or row.get('证券余额') or 0)
        return amount_value == 0 and stock_balance == 0

    def _parse_excel_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析资金流水查询(xls文本表格)单行"""
        summary = str(
            row.get('摘要')
            or row.get('操作')
            or row.get('业务说明')
            or ''
        ).strip()
        side = self._resolve_side(summary)
        if not side:
            return None

        symbol_raw = str(row.get('证券代码', '')).strip()
        if not symbol_raw or symbol_raw.lower() in ('nan', 'null', 'none'):
            return None

        symbol = self._normalize_symbol(symbol_raw)

        quantity = self._safe_decimal(row.get('成交数量'))
        price = self._safe_decimal(
            row.get('成交价格') or row.get('成交均价') or row.get('成交价')
        )
        if quantity <= 0 or price <= 0:
            return None

        gross = quantity * price
        amount_value = self._safe_decimal(row.get('发生金额') or row.get('本次金额') or 0)
        if amount_value != 0:
            amount = abs(amount_value)
            fee = amount - gross if side == 'buy' else gross - amount
            fee = abs(fee)
        else:
            amount = self._safe_decimal(row.get('成交金额', 0))
            if amount == 0:
                amount = gross
            fee = Decimal('0')

        if any(col in row.index for col in self.EXCEL_FEE_COLUMNS):
            fee_total = sum((self._safe_decimal(row.get(col, 0)) for col in self.EXCEL_FEE_COLUMNS), Decimal('0'))
            if fee_total > 0:
                fee = fee_total

        trade_time = self._parse_excel_trade_time(row)

        trade_id_external = str(row.get('成交编号', '')).strip()
        if not trade_id_external or trade_id_external == '0' or trade_id_external.lower() == 'nan':
            shareholder = str(row.get('股东代码') or row.get('股东帐户') or '').strip()
            contract_no = str(row.get('合同编号', '')).strip()
            trade_id_external = (
                f"gtja_{shareholder}_{contract_no}_{trade_time.strftime('%Y%m%d')}_{symbol}_{side}_"
                f"{quantity}_{price}_{amount}"
            )

        name = str(row.get('证券名称', '')).strip()
        if name.lower() == 'nan':
            name = ''

        notes_prefix = "导入自国泰海通"
        if name:
            notes = f"{notes_prefix} - {name} ({summary})"
        else:
            notes = f"{notes_prefix} ({summary})"

        return {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': notes.strip()
        }

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析国泰君安CSV行"""
        business = str(row.get('业务说明', '')).strip()
        side = self._resolve_side(business)
        if not side:
            return None

        symbol_raw = str(row.get('证券代码', '')).strip()
        if not symbol_raw or symbol_raw.lower() == 'nan':
            return None

        symbol = self._normalize_symbol(symbol_raw)

        quantity = self._safe_decimal(row.get('成交数量'))
        price = self._safe_decimal(row.get('成交价格'))

        if quantity <= 0 or price <= 0:
            raise ValueError(f"数量或价格无效: quantity={quantity}, price={price}")

        amount = self._safe_decimal(row.get('成交金额', 0))
        if amount == 0:
            amount = quantity * price

        total_commission = self._safe_decimal(row.get('总佣金', 0))
        stamp_tax = self._safe_decimal(row.get('印花税', 0))
        transfer_fee = self._safe_decimal(row.get('过户费', 0))
        other_fee = self._safe_decimal(row.get('其他费', 0))
        fee = total_commission + stamp_tax + transfer_fee + other_fee

        trade_time = self._parse_trade_datetime(row.get('交收日期'))

        account_no = str(row.get('资金账号', '')).strip()
        security_balance = self._safe_decimal(row.get('证券余额', 0))

        trade_id_external = (
            f"gtja_{account_no}_{trade_time.strftime('%Y%m%d')}_{symbol}_{side}_"
            f"{quantity}_{price}_{amount}_{security_balance}"
        )

        name = str(row.get('证券名称', '')).strip()
        if name.lower() == 'nan':
            name = ''
        if name:
            notes = f"导入自国泰君安 - {name} ({business})"
        else:
            notes = f"导入自国泰君安 ({business})"

        return {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': notes.strip()
        }

    def _resolve_side(self, business: str) -> Optional[str]:
        """根据业务说明解析买卖方向"""
        business = business.strip()
        mapping = {
            '证券买入': 'buy',
            '证券卖出': 'sell',
            '港股通买入成交': 'buy',
            '港股通卖出成交': 'sell',
        }
        if business in mapping:
            return mapping[business]
        if business.endswith('成交'):
            if '买入' in business:
                return 'buy'
            if '卖出' in business:
                return 'sell'
        if '买入' in business:
            return 'buy'
        if '卖出' in business:
            return 'sell'
        return None

    def _normalize_symbol(self, code: str) -> str:
        """标准化股票代码"""
        code = str(code).strip()
        if not code:
            raise ValueError(f"无效的股票代码: {code}")

        if '.' in code:
            return code.upper()

        if code.isdigit():
            if len(code) == 6:
                if code.startswith('6'):
                    return f"{code}.SH"
                if code.startswith('0') or code.startswith('3'):
                    return f"{code}.SZ"
            if len(code) == 5:
                return f"{code}.HK"

        return code.upper()

    def _parse_trade_datetime(self, date_str: Any) -> datetime:
        """解析交易日期为datetime"""
        date_str = str(date_str).strip()
        for fmt in [
            '%Y%m%d',
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y%m%d %H%M%S',
            '%Y%m%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
        ]:
            try:
                dt = datetime.strptime(date_str, fmt)
                if fmt in ['%Y%m%d', '%Y-%m-%d', '%Y/%m/%d']:
                    dt = dt.replace(hour=9, minute=30, second=0)
                return dt
            except ValueError:
                continue
        return self._parse_datetime(date_str)

    def _parse_excel_trade_time(self, row: pd.Series) -> datetime:
        """组合Excel成交日期和时间字段"""
        date_value = row.get('成交日期') or row.get('交收日期') or row.get('日期')
        time_value = row.get('成交时间') or row.get('时间')
        if date_value and time_value:
            date_text = str(date_value).strip()
            time_text = str(time_value).strip()
            if date_text and time_text:
                try:
                    return self._parse_trade_datetime(f"{date_text} {time_text}")
                except ValueError:
                    pass
        return self._parse_trade_datetime(date_value)

    def _extract_cash_balance_from_excel(self, df: pd.DataFrame) -> None:
        """尝试从资金流水查询导出的表中提取最新现金余额"""
        balance_candidates = ['剩余金额', '剩余资金', '资金余额', '余额', '可用资金', '资金本次余额']
        currency_candidates = ['币种', '币别', '币种名称']

        balance_col = next((col for col in balance_candidates if col in df.columns), None)
        if not balance_col:
            return
        currency_col = next((col for col in currency_candidates if col in df.columns), None)

        for _, row in df[::-1].iterrows():
            balance_value = self._safe_decimal_optional(row.get(balance_col))
            if balance_value is None:
                continue
            currency_value = row.get(currency_col) if currency_col else None
            currency_text = str(currency_value).strip() if currency_value else None
            self.cash_balance = balance_value
            self.cash_currency = currency_text or None
            return

    def _normalize_excel_columns(self, df: pd.DataFrame) -> None:
        """归一化Excel列名(去BOM/引号/单位括号)，提高兼容性"""
        rename_map: Dict[str, str] = {}
        for col in df.columns:
            name = self._clean_cell(col).replace('\ufeff', '').strip()
            name = re.sub(r'[（(].*?[）)]', '', name).strip()
            rename_map[col] = name
        df.rename(columns=rename_map, inplace=True)


class GuosenTemplate(BrokerTemplate):
    """
    国信证券资金流水/历史成交查询Excel模板解析器

    资金流水导出的Excel格式(中文列名):
    - 交收日期: 交易日期 (YYYYMMDD)
    - 证券代码: 股票代码
    - 证券名称: 股票名称
    - 成交数量: 成交数量
    - 成交价格: 成交价格
    - 摘要: 证券买入/证券卖出/新股申购等
    - 发生金额: 交易金额 (买入为负,卖出为正)
    - 成交编号: 成交编号
    - 成交日期: 成交日期

    历史成交查询导出的Excel格式(中文列名):
    - 成交日期: 交易日期 (YYYYMMDD)
    - 成交时间: 交易时间 (HHMMSS/HHMMSSff)
    - 证券代码: 股票代码
    - 证券名称: 股票名称
    - 买卖标志: 证券买入/证券卖出
    - 成交数量: 成交数量
    - 成交价格: 成交价格
    - 成交金额: 成交金额
    - 费用合计/印花税/标准手续费/过户费/清算费/交易规费/经手费/证管费/其他费/前台费: 手续费构成
    - 委托编号/合同编号: 可作为唯一成交标识
    """

    REQUIRED_COLUMNS = ['交收日期', '证券代码', '成交数量', '成交价格', '摘要']
    HISTORY_REQUIRED_COLUMNS = ['成交日期', '证券代码', '买卖标志', '成交数量', '成交价格']
    HISTORY_FEE_COLUMNS = [
        '印花税',
        '标准手续费',
        '过户费',
        '清算费',
        '交易规费',
        '经手费',
        '证管费',
        '其他费',
        '前台费',
    ]
    FEE_RATE = Decimal('0.0002')

    def parse_excel(self, file_content: bytes) -> List[Dict[str, Any]]:
        self.errors = []
        try:
            df = self._read_excel_dataframe(file_content)
            self._normalize_excel_columns(df)
            self._extract_cash_balance(df)
            return self._parse_dataframe(df)
        except Exception as e:
            raise CSVParseError(f"Excel解析失败: {str(e)}")

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析国信证券Excel行"""
        is_history = self._is_history_row(row)
        summary = str(row.get('摘要') or row.get('买卖标志') or '').strip()
        side = self._resolve_side(summary)
        if not side:
            return None

        symbol_raw = str(row.get('证券代码', '')).strip()
        if not symbol_raw or symbol_raw.lower() == 'nan':
            return None

        symbol = self._normalize_symbol(symbol_raw)

        quantity = self._safe_decimal(row.get('成交数量'))
        price = self._safe_decimal(row.get('成交价格'))

        if quantity <= 0 or price <= 0:
            raise ValueError(f"数量或价格无效: quantity={quantity}, price={price}")

        gross = quantity * price
        if is_history:
            amount = self._safe_decimal(row.get('成交金额', 0))
            if amount == 0:
                amount = gross
            amount = abs(amount)

            fee = self._extract_history_fee(row)
            if fee == 0 and amount != gross:
                fee = abs(amount - gross)

            trade_time = self._parse_history_trade_time(row)
            trade_id_external = str(
                row.get('成交编号')
                or row.get('合同编号')
                or row.get('委托编号')
                or ''
            ).strip()
            if not trade_id_external or trade_id_external == '0' or trade_id_external.lower() == 'nan':
                trade_id_external = (
                    f"guosen_{symbol}_{trade_time.strftime('%Y%m%d')}_{side}_"
                    f"{quantity}_{price}_{amount}"
                )
        else:
            amount_value = self._safe_decimal(row.get('发生金额', 0))
            if amount_value != 0:
                amount = abs(amount_value)
                fee = amount - gross if side == 'buy' else gross - amount
                fee = abs(fee)
            else:
                amount = gross
                fee = gross * self.FEE_RATE

            trade_time = self._parse_history_trade_time(row)

            trade_id_external = str(row.get('成交编号', '')).strip()
            if not trade_id_external or trade_id_external == '0' or trade_id_external.lower() == 'nan':
                trade_id_external = (
                    f"guosen_{symbol}_{trade_time.strftime('%Y%m%d')}_{side}_"
                    f"{quantity}_{price}_{amount}"
                )

        name = str(row.get('证券名称', '')).strip()
        if name.lower() == 'nan':
            name = ''
        if name:
            notes = f"导入自国信证券 - {name} ({summary})"
        else:
            notes = f"导入自国信证券 ({summary})"

        return {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': notes.strip()
        }

    def _extract_cash_balance(self, df: pd.DataFrame) -> None:
        balance_candidates = ['剩余金额', '剩余资金', '资金余额', '余额', '可用资金']
        currency_candidates = ['币种', '币别', '币种名称']

        balance_col = next((col for col in balance_candidates if col in df.columns), None)
        if not balance_col:
            return
        currency_col = next((col for col in currency_candidates if col in df.columns), None)

        for _, row in df[::-1].iterrows():
            balance_value = self._safe_decimal_optional(row.get(balance_col))
            if balance_value is None:
                continue
            currency_value = row.get(currency_col) if currency_col else None
            currency_text = str(currency_value).strip() if currency_value else None
            self.cash_balance = balance_value
            self.cash_currency = currency_text or None
            return

    def _resolve_side(self, summary: str) -> Optional[str]:
        """根据摘要解析买卖方向"""
        summary = summary.strip()
        if summary in ('新股申购', '申购还款'):
            return None
        if summary in ('买入', '证券买入'):
            return 'buy'
        if summary in ('卖出', '证券卖出'):
            return 'sell'
        if '买入' in summary:
            return 'buy'
        if '卖出' in summary:
            return 'sell'
        return None

    def _normalize_symbol(self, code: str) -> str:
        """标准化股票代码"""
        code = str(code).strip()
        if not code:
            raise ValueError(f"无效的股票代码: {code}")

        if '.' in code:
            return code.upper()

        if code.isdigit() and len(code) == 6:
            if code.startswith('6'):
                return f"{code}.SH"
            if code.startswith('0') or code.startswith('3'):
                return f"{code}.SZ"
            return code

        return code.upper()

    def _parse_trade_datetime(self, date_str: Any) -> datetime:
        """解析交易日期为datetime"""
        date_str = str(date_str).strip()
        for fmt in ['%Y%m%d', '%Y-%m-%d', '%Y/%m/%d', '%Y%m%d %H%M%S', '%Y%m%d %H:%M:%S']:
            try:
                dt = datetime.strptime(date_str, fmt)
                if fmt in ['%Y%m%d', '%Y-%m-%d', '%Y/%m/%d']:
                    dt = dt.replace(hour=9, minute=30, second=0)
                return dt
            except ValueError:
                continue
        return self._parse_datetime(date_str)

    def _normalize_excel_columns(self, df: pd.DataFrame) -> None:
        """归一化Excel列名(去BOM/引号/单位括号)，提高兼容性"""
        rename_map: Dict[str, str] = {}
        for col in df.columns:
            name = self._clean_cell(col).replace('\ufeff', '').strip()
            name = re.sub(r'[（(].*?[）)]', '', name).strip()
            rename_map[col] = name
        df.rename(columns=rename_map, inplace=True)

    def _is_history_dataframe(self, df: pd.DataFrame) -> bool:
        """判断是否为历史成交查询导出"""
        return '买卖标志' in df.columns or '成交时间' in df.columns or '费用合计' in df.columns

    def _is_history_row(self, row: pd.Series) -> bool:
        return '买卖标志' in row.index or '成交时间' in row.index or '费用合计' in row.index

    def _validate_columns(self, df: pd.DataFrame):
        """验证必填列是否存在(兼容两种导出格式)"""
        required = self.HISTORY_REQUIRED_COLUMNS if self._is_history_dataframe(df) else self.REQUIRED_COLUMNS
        missing_cols = [col for col in required if col not in df.columns]
        if missing_cols:
            raise CSVParseError(f"缺少必填列: {', '.join(missing_cols)}")

    def _parse_history_trade_time(self, row: pd.Series) -> datetime:
        """解析历史成交查询的成交日期/时间"""
        date_value = row.get('成交日期') or row.get('交收日期') or row.get('日期')
        time_value = row.get('成交时间') or row.get('时间')
        if date_value and time_value:
            date_text = str(date_value).strip()
            time_text = str(time_value).strip()
            if date_text and time_text:
                time_digits = re.sub(r'\D', '', time_text)
                if time_digits:
                    if len(time_digits) <= 6:
                        time_digits = time_digits.zfill(6)
                    else:
                        time_digits = time_digits.zfill(8)[:6]
                    time_text = f"{time_digits[0:2]}:{time_digits[2:4]}:{time_digits[4:6]}"
                else:
                    time_text = time_text.split('.')[0]
                try:
                    return self._parse_trade_datetime(f"{date_text} {time_text}")
                except ValueError:
                    pass
        return self._parse_trade_datetime(date_value)

    def _extract_history_fee(self, row: pd.Series) -> Decimal:
        """解析历史成交查询手续费"""
        fee_total = self._safe_decimal(row.get('费用合计', 0))
        if fee_total != 0:
            return abs(fee_total)
        fee_sum = sum((self._safe_decimal(row.get(col, 0)) for col in self.HISTORY_FEE_COLUMNS), Decimal('0'))
        return abs(fee_sum)


class MoomooTemplate(BrokerTemplate):
    """
    moomoo券商CSV模板解析器

    moomoo导出的CSV格式(中文列名):
    - 方向: 买入/卖出
    - 代码: 股票代码
    - 名称: 股票名称
    - 成交数量: 成交的股数
    - 成交价格: 成交价
    - 成交金额: 总成交额
    - 成交时间: 成交时间 (格式: 2025/10/28 10:23:54 (美东))
    - 合计费用: 总费用
    """

    REQUIRED_COLUMNS = ['方向', '代码', '成交数量', '成交价格', '成交时间']
    DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析moomoo CSV行"""
        # 跳过空行或没有代码的行
        if pd.isna(row.get('代码')) or not row.get('代码'):
            return None

        # 解析买卖方向
        side_text = str(row['方向']).strip()
        if '买' in side_text or 'buy' in side_text.lower():
            side = 'buy'
        elif '卖' in side_text or 'sell' in side_text.lower():
            side = 'sell'
        else:
            raise ValueError(f"无法识别买卖方向: {side_text}")

        # 提取股票代码
        symbol = str(row['代码']).strip()

        # 解析数量和价格
        quantity = self._safe_decimal(row['成交数量'])
        price = self._safe_decimal(row['成交价格'])

        if quantity <= 0 or price <= 0:
            raise ValueError(f"数量或价格无效: quantity={quantity}, price={price}")

        # 成交金额
        amount = self._safe_decimal(row.get('成交金额', 0))
        if amount == 0:
            amount = quantity * price

        # 手续费 (moomoo用"合计费用")
        fee = self._safe_decimal(row.get('合计费用', 0))

        # 解析成交时间 - 移除时区标记
        time_str = str(row['成交时间']).strip()
        # 移除时区标记,如 " (美东)" 或 " (EST)"
        if '(' in time_str:
            time_str = time_str.split('(')[0].strip()

        trade_time = self._parse_datetime(time_str)

        # 生成外部交易ID用于去重
        trade_id_external = f"moomoo_{symbol}_{time_str}_{side}_{quantity}_{price}"

        # 构建标准交易记录
        trade = {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': f"导入自moomoo - {row.get('名称', '')}"
        }

        return trade


class GenericTemplate(BrokerTemplate):
    """
    通用CSV模板 - 用于标准格式CSV

    期望列名 (可以是中文或英文):
    - date/日期/成交时间
    - symbol/代码/证券代码
    - side/方向/买卖
    - quantity/数量/成交数量
    - price/价格/成交价格
    - fee/手续费 (可选)
    """

    COLUMN_MAPPING = {
        # 中文列名
        '日期': 'trade_time',
        '成交时间': 'trade_time',
        '代码': 'symbol',
        '证券代码': 'symbol',
        '方向': 'side',
        '买卖': 'side',
        '数量': 'quantity',
        '成交数量': 'quantity',
        '价格': 'price',
        '成交价格': 'price',
        '手续费': 'fee',
        # 英文列名
        'date': 'trade_time',
        'time': 'trade_time',
        'symbol': 'symbol',
        'code': 'symbol',
        'side': 'side',
        'direction': 'side',
        'quantity': 'quantity',
        'amount': 'quantity',
        'price': 'price',
        'fee': 'fee',
    }

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析通用格式CSV行"""
        # 智能匹配列名
        mapped = self._auto_map_columns(row)

        if not mapped.get('symbol') or not mapped.get('trade_time'):
            return None

        # 解析方向
        side_text = str(mapped['side']).lower().strip()
        if 'buy' in side_text or '买' in side_text:
            side = 'buy'
        elif 'sell' in side_text or '卖' in side_text:
            side = 'sell'
        else:
            raise ValueError(f"无法识别买卖方向: {side_text}")

        quantity = self._safe_decimal(mapped['quantity'])
        price = self._safe_decimal(mapped['price'])
        fee = self._safe_decimal(mapped.get('fee', 0))

        if quantity <= 0 or price <= 0:
            raise ValueError(f"数量或价格无效")

        trade_time = self._parse_datetime(mapped['trade_time'])

        return {
            'symbol': str(mapped['symbol']).strip(),
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(quantity * price),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': f"{mapped['symbol']}_{trade_time.isoformat()}_{side}",
            'notes': '导入自通用CSV'
        }

    def _auto_map_columns(self, row: pd.Series) -> Dict[str, Any]:
        """自动匹配列名到标准字段"""
        mapped = {}
        for col_name, value in row.items():
            normalized_col = col_name.strip().lower()
            if normalized_col in self.COLUMN_MAPPING:
                field = self.COLUMN_MAPPING[normalized_col]
                mapped[field] = value
        return mapped


class IBKRTemplate(BrokerTemplate):
    """
    Interactive Brokers (盈透证券) CSV模板解析器

    IBKR导出的CSV格式(英文列名):
    - Symbol: 股票代码
    - Date/Time: 成交时间
    - Quantity: 成交数量(正数为买入,负数为卖出)
    - T. Price: 成交价格
    - Proceeds: 成交金额
    - Comm/Fee: 佣金/手续费
    """

    REQUIRED_COLUMNS = ['Symbol', 'Date/Time', 'Quantity', 'T. Price']
    DATE_FORMAT = '%Y%m%d %H:%M:%S'  # IBKR格式: 20231201 09:30:00

    def parse_row(self, row: pd.Series) -> Optional[Dict[str, Any]]:
        """解析IBKR CSV行"""
        # 跳过空行或没有代码的行
        if pd.isna(row.get('Symbol')) or not row.get('Symbol'):
            return None

        symbol = str(row['Symbol']).strip()

        # 解析数量(正数为买入,负数为卖出)
        quantity = self._safe_decimal(row['Quantity'])
        if quantity == 0:
            return None

        if quantity > 0:
            side = 'buy'
        else:
            side = 'sell'
            quantity = abs(quantity)  # 转为正数

        # 解析价格
        price = self._safe_decimal(row['T. Price'])
        if price <= 0:
            raise ValueError(f"价格无效: {price}")

        # 成交金额
        amount = self._safe_decimal(row.get('Proceeds', 0))
        if amount == 0:
            amount = quantity * price
        else:
            amount = abs(amount)  # IBKR的Proceeds可能为负数

        # 手续费
        fee = abs(self._safe_decimal(row.get('Comm/Fee', 0)))

        # 解析时间 - IBKR格式: 20231201 09:30:00 或 2023-12-01 09:30:00
        time_str = str(row['Date/Time']).strip()
        # 处理可能的分隔符
        time_str = time_str.replace('-', '').replace(':', '').replace(' ', '')
        # 重新格式化为标准格式
        if len(time_str) >= 14:
            formatted_time = f"{time_str[:4]}-{time_str[4:6]}-{time_str[6:8]} {time_str[8:10]}:{time_str[10:12]}:{time_str[12:14]}"
        else:
            formatted_time = time_str

        trade_time = self._parse_datetime(formatted_time)

        # 生成外部交易ID
        trade_id_external = f"ibkr_{symbol}_{time_str}_{side}_{quantity}_{price}"

        return {
            'symbol': symbol,
            'side': side,
            'quantity': float(quantity),
            'price': float(price),
            'amount': float(amount),
            'fee': float(fee),
            'trade_time': trade_time.isoformat(),
            'trade_id_external': trade_id_external,
            'notes': f"导入自Interactive Brokers"
        }


# 券商模板注册表
BROKER_TEMPLATES = {
    'tonghuashun': TonghuashunTemplate,
    'gtja': GTJATemplate,
    'guosen': GuosenTemplate,
    'moomoo': MoomooTemplate,
    'ibkr': IBKRTemplate,
    'generic': GenericTemplate,
}


def get_parser(broker_template: str = 'tonghuashun') -> BrokerTemplate:
    """
    获取指定券商的CSV解析器

    Args:
        broker_template: 券商模板名称

    Returns:
        BrokerTemplate实例

    Raises:
        ValueError: 不支持的券商模板
    """
    if broker_template not in BROKER_TEMPLATES:
        raise ValueError(
            f"不支持的券商模板: {broker_template}. "
            f"支持的模板: {', '.join(BROKER_TEMPLATES.keys())}"
        )

    return BROKER_TEMPLATES[broker_template]()
