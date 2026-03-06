"""
统一的交易导入服务

封装所有交易导入相关的逻辑:
1. 交易记录存储（包括去重）
2. 持仓计算（现货/合约自动识别）
3. 已平仓记录生成

使用这个服务可以确保交易导入后自动触发持仓计算，避免数据不一致。
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import logging

from ..models.trade import Trade as TradeModel
from ..models.trade_account import TradeAccount
from .position_service import PositionService

logger = logging.getLogger(__name__)


class TradeImportService:
    """统一的交易导入服务"""

    def __init__(self, db: Session):
        self.db = db
        self.position_service = PositionService(db)

    def import_trades(
        self,
        account_id: UUID,
        trades_data: List[Dict[str, Any]],
        sync_source: str = 'api'
    ) -> Dict[str, int]:
        """
        批量导入交易记录并自动计算持仓

        这是统一的入口方法，会自动处理:
        1. 交易记录去重（基于 trade_id_external）
        2. 批量插入交易记录
        3. 自动识别账户类型（现货/合约）
        4. 计算并更新持仓
        5. 生成已平仓记录

        Args:
            account_id: 交易账户ID
            trades_data: 交易数据列表，每个元素应包含:
                - symbol: 标的符号
                - side: 交易方向 (buy/sell)
                - quantity: 数量
                - price: 价格
                - trade_date: 交易时间
                - external_trade_id: 外部交易ID（可选，用于去重）
                - fee: 手续费（可选）
                - fee_currency: 手续费币种（可选）
                - position_side: 持仓方向（合约专用，LONG/SHORT）
                - leverage: 杠杆倍数（合约专用）
                - margin: 保证金（合约专用）
                - asset_class: 资产类别（可选）
            sync_source: 同步来源 (api/manual/import)

        Returns:
            统计信息字典:
            {
                'imported_count': 成功导入数量,
                'skipped_count': 跳过数量（重复）,
                'error_count': 失败数量,
                'affected_symbols': 受影响的标的列表
            }
        """
        logger.info(f"开始导入交易 - 账户: {account_id}, 记录数: {len(trades_data)}, 来源: {sync_source}")

        # 获取账户信息
        account = self.db.query(TradeAccount).filter(
            TradeAccount.id == account_id
        ).first()

        if not account:
            raise ValueError(f"Account not found: {account_id}")

        imported_count = 0
        skipped_count = 0
        error_count = 0
        affected_symbols = set()

        # 批量导入交易记录
        for trade_data in trades_data:
            try:
                # 检查是否已存在（基于 trade_id_external）
                external_id = trade_data.get('external_trade_id')
                if external_id:
                    existing = self.db.query(TradeModel).filter(
                        TradeModel.account_id == account_id,
                        TradeModel.trade_id_external == external_id
                    ).first()
                    if existing:
                        skipped_count += 1
                        continue

                # 创建交易记录
                trade = TradeModel(
                    account_id=account_id,
                    symbol=trade_data['symbol'],
                    side=trade_data['side'],
                    quantity=trade_data['quantity'],
                    price=trade_data['price'],
                    fee=trade_data.get('fee', 0.0),
                    fee_currency=trade_data.get('fee_currency', 'USD'),
                    trade_time=trade_data.get('trade_date') or datetime.utcnow(),
                    trade_id_external=external_id,
                    sync_source=sync_source,
                    notes=trade_data.get('notes', ''),
                    # 合约专用字段
                    position_side=trade_data.get('position_side'),
                    leverage=trade_data.get('leverage'),
                    margin=trade_data.get('margin')
                )
                self.db.add(trade)
                imported_count += 1
                affected_symbols.add(trade_data['symbol'])

            except Exception as e:
                logger.error(f"Error importing trade: {str(e)}")
                error_count += 1
                continue

        # 提交交易记录
        self.db.commit()

        logger.info(f"交易记录导入完成 - 导入: {imported_count}, 跳过: {skipped_count}, 错误: {error_count}")

        # 自动计算持仓（这会自动识别账户类型：现货/合约）
        try:
            logger.info(f"开始计算持仓 - 账户: {account_id}, 账户类型: {account.account_type}")
            self.position_service.calculate_positions_for_account(account_id)
            logger.info(f"持仓计算完成 - 账户: {account_id}")
        except Exception as e:
            logger.error(f"持仓计算失败 - 账户: {account_id}, 错误: {str(e)}", exc_info=True)
            # 持仓计算失败时抛出异常，让调用方知道
            raise Exception(f"Position calculation failed: {str(e)}")

        return {
            'imported_count': imported_count,
            'skipped_count': skipped_count,
            'error_count': error_count,
            'affected_symbols': list(affected_symbols)
        }

    def import_single_trade(
        self,
        account_id: UUID,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        trade_time: datetime,
        **kwargs
    ) -> TradeModel:
        """
        导入单条交易记录并更新持仓

        这是简化版本，适用于手动添加单条交易记录的场景

        Args:
            account_id: 交易账户ID
            symbol: 标的符号
            side: 交易方向 (buy/sell)
            quantity: 数量
            price: 价格
            trade_time: 交易时间
            **kwargs: 其他可选字段（fee, position_side, leverage等）

        Returns:
            创建的交易记录
        """
        # 使用批量导入方法
        trade_data = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'trade_date': trade_time,
            **kwargs
        }

        result = self.import_trades(
            account_id=account_id,
            trades_data=[trade_data],
            sync_source=kwargs.get('sync_source', 'manual')
        )

        if result['imported_count'] > 0:
            # 查询刚创建的交易记录
            trade = self.db.query(TradeModel).filter(
                TradeModel.account_id == account_id,
                TradeModel.symbol == symbol,
                TradeModel.trade_time == trade_time
            ).order_by(TradeModel.created_at.desc()).first()
            return trade
        else:
            raise ValueError("Failed to import trade")

    def recalculate_positions(self, account_id: UUID):
        """
        重新计算账户的所有持仓

        适用场景:
        1. 修复数据不一致问题
        2. 删除交易记录后
        3. 手动触发重算

        Args:
            account_id: 交易账户ID
        """
        logger.info(f"手动触发持仓重算 - 账户: {account_id}")
        self.position_service.calculate_positions_for_account(account_id)
        logger.info(f"持仓重算完成 - 账户: {account_id}")
