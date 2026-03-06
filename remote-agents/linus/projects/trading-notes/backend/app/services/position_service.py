"""
持仓计算服务

从交易记录计算持仓,而不是直接从交易所获取持仓数据。
这样可以确保数据的一致性和可追溯性。
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from collections import defaultdict
import logging

from ..models.trade import Trade as TradeModel
from ..models.position import Position as PositionModel
from ..models.trade_account import TradeAccount as TradeAccountModel
from ..models.closed_position import ClosedPosition as ClosedPositionModel

logger = logging.getLogger(__name__)


class PositionService:
    """持仓计算服务"""

    def __init__(self, db: Session):
        self.db = db

    def _get_realized_pnl_from_closed_records(
        self,
        account_id: UUID,
        symbol: str
    ) -> tuple[Optional[Decimal], Decimal, Decimal]:
        """
        从 closed_positions 表汇总已实现盈亏

        Returns:
            (final_price, realized_pnl, realized_pnl_percent)
        """
        closed_records = self.db.query(ClosedPositionModel).filter(
            ClosedPositionModel.account_id == account_id,
            ClosedPositionModel.symbol == symbol
        ).all()

        if closed_records:
            # 汇总所有已平仓记录
            total_realized_pnl = sum(Decimal(str(r.realized_pnl)) for r in closed_records)
            total_cost = sum(Decimal(str(r.entry_price)) * Decimal(str(r.quantity)) for r in closed_records)

            # 计算总盈亏率
            realized_pnl_percent = (total_realized_pnl / total_cost * 100) if total_cost > 0 else Decimal('0')

            # 使用最后一笔卖出的价格作为 final_price
            last_closed = max(closed_records, key=lambda x: x.close_time)
            final_price = last_closed.exit_price

            return (final_price, total_realized_pnl, realized_pnl_percent)
        else:
            return (None, Decimal('0'), Decimal('0'))

    def _create_closed_position_record(
        self,
        account_id: UUID,
        symbol: str,
        position_type: str,
        position_side: Optional[str],
        closed_quantity: Decimal,
        entry_price: Decimal,
        exit_price: Decimal,
        open_time: datetime,
        close_time: datetime,
        leverage: Optional[Decimal] = None,
        margin_used: Optional[Decimal] = None,
        total_fees: Decimal = Decimal('0')
    ) -> ClosedPositionModel:
        """
        创建已平仓记录

        Args:
            account_id: 账户ID
            symbol: 标的符号
            position_type: 持仓类型 (spot/futures)
            position_side: 持仓方向 (LONG/SHORT/None)
            closed_quantity: 平仓数量
            entry_price: 开仓价(成本价)
            exit_price: 平仓价(卖出价)
            open_time: 开仓时间
            close_time: 平仓时间
            leverage: 杠杆倍数
            margin_used: 占用保证金
            total_fees: 手续费

        Returns:
            创建的已平仓记录
        """
        # 计算持仓天数
        holding_days = (close_time - open_time).days if open_time else None

        # 计算盈亏
        if position_type == 'spot':
            # 现货: (卖出价 - 成本价) * 数量
            realized_pnl = (exit_price - entry_price) * closed_quantity - total_fees
            # 盈亏百分比: 盈亏 / 成本
            cost_value = entry_price * closed_quantity
            realized_pnl_percent = (realized_pnl / cost_value * 100) if cost_value > 0 else Decimal('0')
            roe_percent = None

        elif position_type == 'futures':
            # 合约盈亏取决于方向
            if position_side == 'LONG':
                # 多头: (平仓价 - 开仓价) * 数量
                realized_pnl = (exit_price - entry_price) * closed_quantity - total_fees
            elif position_side == 'SHORT':
                # 空头: (开仓价 - 平仓价) * 数量
                realized_pnl = (entry_price - exit_price) * closed_quantity - total_fees
            else:
                realized_pnl = Decimal('0')

            # 盈亏百分比: 基于开仓价值
            entry_value = entry_price * closed_quantity
            realized_pnl_percent = (realized_pnl / entry_value * 100) if entry_value > 0 else Decimal('0')

            # ROE: 基于保证金
            if margin_used and margin_used > 0:
                roe_percent = (realized_pnl / margin_used * 100)
            else:
                roe_percent = None
        else:
            realized_pnl = Decimal('0')
            realized_pnl_percent = Decimal('0')
            roe_percent = None

        # 创建平仓记录
        closed_position = ClosedPositionModel(
            account_id=account_id,
            symbol=symbol,
            position_type=position_type,
            position_side=position_side,
            quantity=closed_quantity,
            entry_price=entry_price,
            exit_price=exit_price,
            leverage=leverage,
            margin_used=margin_used,
            realized_pnl=realized_pnl,
            realized_pnl_percent=realized_pnl_percent,
            roe_percent=roe_percent,
            open_time=open_time,
            close_time=close_time,
            holding_days=holding_days,
            total_fees=total_fees
        )

        self.db.add(closed_position)
        return closed_position

    def generate_closed_positions_from_trades(self, account_id: UUID):
        """
        从交易记录生成已平仓记录

        遍历所有交易记录,在每次卖出时创建 ClosedPosition 记录。
        这个方法应该在导入交易或同步交易后调用。

        注意: 此方法会清空该账户的所有已平仓记录并重新生成,
        确保数据准确性。

        Args:
            account_id: 交易账户 ID
        """
        # 获取账户信息
        account = self.db.query(TradeAccountModel).filter(
            TradeAccountModel.id == account_id
        ).first()

        if not account:
            return

        # 清空该账户的已平仓记录
        self.db.query(ClosedPositionModel).filter(
            ClosedPositionModel.account_id == account_id
        ).delete()

        # 获取所有交易记录,按时间排序
        trades = self.db.query(TradeModel).filter(
            TradeModel.account_id == account_id
        ).order_by(TradeModel.trade_time).all()

        # 根据账户类型选择处理方法
        if account.is_futures_account():
            self._generate_closed_positions_futures(account_id, trades)
        else:
            self._generate_closed_positions_spot(account_id, trades)

        self.db.commit()

    def _generate_closed_positions_spot(self, account_id: UUID, trades: List[TradeModel]):
        """
        为现货交易生成已平仓记录

        现货逻辑:
        - 跟踪每个标的的持仓成本和数量
        - 每次卖出时,创建一条 ClosedPosition 记录
        - 使用 FIFO (先进先出)计算成本价
        """
        # 按标的分组跟踪持仓
        positions_tracker = {}  # symbol -> {quantity, avg_cost, first_buy_time}

        for trade in trades:
            symbol = trade.symbol

            if symbol not in positions_tracker:
                positions_tracker[symbol] = {
                    'quantity': Decimal('0'),
                    'avg_cost': Decimal('0'),
                    'first_buy_time': None
                }

            tracker = positions_tracker[symbol]
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_fee = Decimal(str(trade.fee)) if trade.fee else Decimal('0')

            if trade.side == 'buy':
                # 买入: 更新平均成本
                old_quantity = tracker['quantity']
                old_cost = tracker['avg_cost']

                # 加权平均成本 (包含手续费)
                cost_with_fee = trade_price + (trade_fee / trade_quantity if trade_quantity > 0 else Decimal('0'))

                if old_quantity > 0:
                    new_avg_cost = (old_quantity * old_cost + trade_quantity * cost_with_fee) / (old_quantity + trade_quantity)
                else:
                    new_avg_cost = cost_with_fee
                    tracker['first_buy_time'] = trade.trade_time

                tracker['quantity'] = old_quantity + trade_quantity
                tracker['avg_cost'] = new_avg_cost

            elif trade.side == 'sell':
                # 卖出: 创建平仓记录
                if tracker['quantity'] > 0:
                    closed_quantity = min(trade_quantity, tracker['quantity'])

                    # 创建平仓记录
                    self._create_closed_position_record(
                        account_id=account_id,
                        symbol=symbol,
                        position_type='spot',
                        position_side=None,
                        closed_quantity=closed_quantity,
                        entry_price=tracker['avg_cost'],
                        exit_price=trade_price,
                        open_time=tracker['first_buy_time'],
                        close_time=trade.trade_time,
                        total_fees=trade_fee
                    )

                    # 更新跟踪器
                    tracker['quantity'] -= closed_quantity

                    if tracker['quantity'] <= 0:
                        tracker['quantity'] = Decimal('0')
                        tracker['avg_cost'] = Decimal('0')
                        tracker['first_buy_time'] = None

    def _generate_closed_positions_futures(self, account_id: UUID, trades: List[TradeModel]):
        """
        为合约交易生成已平仓记录

        合约逻辑:
        - 跟踪每个标的的多空持仓
        - 平仓时创建 ClosedPosition 记录
        """
        # 按标的分组跟踪持仓
        positions_tracker = {}  # symbol -> {quantity, entry_price, first_open_time, leverage, margin}

        for trade in trades:
            symbol = trade.symbol

            if symbol not in positions_tracker:
                positions_tracker[symbol] = {
                    'quantity': Decimal('0'),  # 正=多头,负=空头
                    'entry_price': Decimal('0'),
                    'first_open_time': None,
                    'leverage': trade.leverage or Decimal('1'),
                    'total_margin': Decimal('0')
                }

            tracker = positions_tracker[symbol]
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_fee = Decimal(str(trade.fee)) if trade.fee else Decimal('0')
            trade_margin = Decimal(str(trade.margin)) if trade.margin else Decimal('0')

            old_quantity = tracker['quantity']
            old_entry_price = tracker['entry_price']

            # 根据position_side和side判断操作
            if trade.position_side == 'LONG':
                if trade.side == 'buy':
                    # 开多/加多
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    if abs_old_qty > 0 and old_quantity > 0:
                        # 加多仓
                        tracker['entry_price'] = (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                    else:
                        # 新开多仓
                        tracker['entry_price'] = trade_price
                        tracker['first_open_time'] = trade.trade_time

                    tracker['quantity'] = new_quantity
                    tracker['total_margin'] += trade_margin

                elif trade.side == 'sell':
                    # 平多
                    if old_quantity > 0:
                        closed_quantity = min(trade_quantity, old_quantity)
                        margin_per_unit = tracker['total_margin'] / old_quantity if old_quantity > 0 else Decimal('0')

                        # 创建平仓记录
                        self._create_closed_position_record(
                            account_id=account_id,
                            symbol=symbol,
                            position_type='futures',
                            position_side='LONG',
                            closed_quantity=closed_quantity,
                            entry_price=old_entry_price,
                            exit_price=trade_price,
                            open_time=tracker['first_open_time'],
                            close_time=trade.trade_time,
                            leverage=tracker['leverage'],
                            margin_used=closed_quantity * margin_per_unit,
                            total_fees=trade_fee
                        )

                        # 更新跟踪器
                        tracker['quantity'] -= closed_quantity
                        tracker['total_margin'] -= closed_quantity * margin_per_unit

                        if tracker['quantity'] <= 0:
                            tracker['quantity'] = Decimal('0')
                            tracker['total_margin'] = Decimal('0')
                            tracker['first_open_time'] = None

            elif trade.position_side == 'SHORT':
                if trade.side == 'sell':
                    # 开空/加空
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    if abs_old_qty > 0 and old_quantity < 0:
                        # 加空仓
                        tracker['entry_price'] = (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                    else:
                        # 新开空仓
                        tracker['entry_price'] = trade_price
                        tracker['first_open_time'] = trade.trade_time

                    tracker['quantity'] = -new_quantity
                    tracker['total_margin'] += trade_margin

                elif trade.side == 'buy':
                    # 平空
                    if old_quantity < 0:
                        closed_quantity = min(trade_quantity, abs(old_quantity))
                        margin_per_unit = tracker['total_margin'] / abs(old_quantity) if old_quantity != 0 else Decimal('0')

                        # 创建平仓记录
                        self._create_closed_position_record(
                            account_id=account_id,
                            symbol=symbol,
                            position_type='futures',
                            position_side='SHORT',
                            closed_quantity=closed_quantity,
                            entry_price=old_entry_price,
                            exit_price=trade_price,
                            open_time=tracker['first_open_time'],
                            close_time=trade.trade_time,
                            leverage=tracker['leverage'],
                            margin_used=closed_quantity * margin_per_unit,
                            total_fees=trade_fee
                        )

                        # 更新跟踪器
                        tracker['quantity'] += closed_quantity
                        tracker['total_margin'] -= closed_quantity * margin_per_unit

                        if tracker['quantity'] >= 0:
                            tracker['quantity'] = Decimal('0')
                            tracker['total_margin'] = Decimal('0')
                            tracker['first_open_time'] = None

    def calculate_positions_for_account(self, account_id: UUID) -> List[PositionModel]:
        """
        从交易记录计算指定账户的所有持仓

        支持现货和合约两种模式:
        - 现货: quantity > 0, average_cost
        - 合约(单向持仓): quantity可正负, entry_price, 多空通过正负区分

        算法:
        1. 获取账户类型(现货/合约)
        2. 获取账户的所有交易记录(按时间排序)
        3. 根据账户类型调用不同的计算方法
        4. 保存计算结果到 positions 表
        5. 生成已平仓记录

        Args:
            account_id: 交易账户 ID

        Returns:
            计算后的持仓列表
        """
        # 获取账户信息判断类型
        account = self.db.query(TradeAccountModel).filter(
            TradeAccountModel.id == account_id
        ).first()

        if not account:
            return []

        # 获取所有交易记录,按时间排序
        trades = self.db.query(TradeModel).filter(
            TradeModel.account_id == account_id
        ).order_by(TradeModel.trade_time).all()

        # 生成已平仓记录（必须先生成，因为 calculate 需要查询这些数据）
        try:
            self.generate_closed_positions_from_trades(account_id)
        except Exception as e:
            logger.error(f"生成已平仓记录失败 - 账户: {account_id}, 错误: {str(e)}", exc_info=True)
            raise

        # 根据账户类型选择计算方法
        try:
            if account.is_futures_account():
                result = self._calculate_futures_positions(account_id, trades)
            else:
                result = self._calculate_spot_positions(account_id, trades)
        except Exception as e:
            logger.error(f"计算持仓失败 - 账户: {account_id}, 类型: {'futures' if account.is_futures_account() else 'spot'}, 错误: {str(e)}", exc_info=True)
            raise

        return result

    def _calculate_spot_positions(
        self,
        account_id: UUID,
        trades: List[TradeModel]
    ) -> List[PositionModel]:
        """
        计算现货持仓 (保持原有逻辑)

        Args:
            account_id: 账户ID
            trades: 交易记录列表

        Returns:
            持仓列表
        """
        # 按标的分组计算持仓
        positions_data = {}  # symbol -> position data

        for trade in trades:
            symbol = trade.symbol

            if symbol not in positions_data:
                positions_data[symbol] = {
                    'quantity': Decimal('0'),
                    'total_cost': Decimal('0'),
                    'first_buy_time': None,
                }

            position = positions_data[symbol]
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_fee = Decimal(str(trade.fee)) if trade.fee else Decimal('0')

            if trade.side == 'buy':
                # 买入: 增加持仓
                old_quantity = position['quantity']
                old_total_cost = position['total_cost']

                # 计算新的总成本 (包含手续费)
                new_cost = (trade_quantity * trade_price) + trade_fee
                position['total_cost'] = old_total_cost + new_cost
                position['quantity'] = old_quantity + trade_quantity

                # 记录第一次买入时间
                if position['first_buy_time'] is None:
                    position['first_buy_time'] = trade.trade_time

            elif trade.side == 'sell':
                # 卖出: 减少持仓
                position['quantity'] = position['quantity'] - trade_quantity

                # 按照比例减少总成本
                if position['quantity'] > 0:
                    cost_ratio = (position['quantity'] + trade_quantity) / position['quantity']
                    position['total_cost'] = position['total_cost'] / cost_ratio
                else:
                    # 全部卖出,清空成本
                    position['total_cost'] = Decimal('0')
                    position['first_buy_time'] = None

        # 保存或更新持仓记录
        result_positions = []

        for symbol, data in positions_data.items():
            quantity = data['quantity']

            # 查找或创建持仓记录
            position = self.db.query(PositionModel).filter(
                PositionModel.account_id == account_id,
                PositionModel.symbol == symbol
            ).first()

            # 持仓清零: 标记为已清仓
            if quantity <= 0:
                trades_for_symbol = [t for t in trades if t.symbol == symbol]
                last_sell_time = max(
                    (t.trade_time for t in trades_for_symbol if t.side == 'sell'),
                    default=None
                )
                last_trade_time = max(
                    (t.trade_time for t in trades_for_symbol),
                    default=None
                )
                fallback_close_time = last_sell_time or last_trade_time or datetime.utcnow()

                if position:
                    # 从 closed_positions 表汇总已实现盈亏和数量
                    closed_records = self.db.query(ClosedPositionModel).filter(
                        ClosedPositionModel.account_id == account_id,
                        ClosedPositionModel.symbol == symbol
                    ).all()

                    if closed_records:
                        # 汇总所有已平仓记录
                        total_closed_quantity = sum(Decimal(str(r.quantity)) for r in closed_records)
                        total_realized_pnl = sum(Decimal(str(r.realized_pnl)) for r in closed_records)
                        total_cost = sum(Decimal(str(r.entry_price)) * Decimal(str(r.quantity)) for r in closed_records)
                        total_proceeds = sum(Decimal(str(r.exit_price)) * Decimal(str(r.quantity)) for r in closed_records)

                        # 计算总盈亏率
                        realized_pnl_percent = (total_realized_pnl / total_cost * 100) if total_cost > 0 else Decimal('0')

                        # 使用最后一笔卖出的价格作为 final_price
                        last_closed = max(closed_records, key=lambda x: x.close_time)
                        final_price = last_closed.exit_price
                        closed_at_time = last_closed.close_time or fallback_close_time
                    else:
                        total_closed_quantity = Decimal('0')
                        total_realized_pnl = Decimal('0')
                        realized_pnl_percent = Decimal('0')
                        final_price = None
                        closed_at_time = fallback_close_time

                    # 标记为已清仓，保存总的清仓数量
                    position.quantity = total_closed_quantity
                    position.is_closed = True
                    position.closed_at = closed_at_time
                    position.final_price = final_price
                    position.realized_pnl = total_realized_pnl
                    position.realized_pnl_percent = realized_pnl_percent
                    position.unrealized_pnl = Decimal('0')
                    position.unrealized_pnl_percent = Decimal('0')
                    if position.first_buy_time:
                        position.holding_days = (closed_at_time - position.first_buy_time).days
                    result_positions.append(position)
                else:
                    # 创建已清仓的持仓记录（保留历史）
                    # 从交易记录中提取信息
                    trades_for_symbol = [t for t in trades if t.symbol == symbol]
                    buy_trades = [t for t in trades_for_symbol if t.side == 'buy']

                    # 计算历史成本价
                    if buy_trades:
                        total_qty = sum(Decimal(str(t.quantity)) for t in buy_trades)
                        total_cost = sum(Decimal(str(t.quantity)) * Decimal(str(t.price)) for t in buy_trades)
                        average_cost = total_cost / total_qty if total_qty > 0 else Decimal('0')
                        first_buy_time = min(t.trade_time for t in buy_trades)
                    else:
                        average_cost = Decimal('0')
                        first_buy_time = None

                    # 计算持仓天数（从第一次买入到清仓）
                    closed_at_time = fallback_close_time
                    if first_buy_time:
                        holding_days = (closed_at_time - first_buy_time).days
                    else:
                        holding_days = None

                    # 从 closed_positions 表汇总已实现盈亏和数量
                    closed_records = self.db.query(ClosedPositionModel).filter(
                        ClosedPositionModel.account_id == account_id,
                        ClosedPositionModel.symbol == symbol
                    ).all()

                    if closed_records:
                        # 汇总所有已平仓记录
                        total_closed_quantity = sum(Decimal(str(r.quantity)) for r in closed_records)
                        total_realized_pnl = sum(Decimal(str(r.realized_pnl)) for r in closed_records)
                        total_cost_closed = sum(Decimal(str(r.entry_price)) * Decimal(str(r.quantity)) for r in closed_records)

                        # 计算总盈亏率
                        realized_pnl_percent = (total_realized_pnl / total_cost_closed * 100) if total_cost_closed > 0 else Decimal('0')

                        # 使用最后一笔卖出的价格作为 final_price
                        last_closed = max(closed_records, key=lambda x: x.close_time)
                        final_price = last_closed.exit_price
                        closed_at_time = last_closed.close_time or fallback_close_time
                    else:
                        total_closed_quantity = Decimal('0')
                        total_realized_pnl = Decimal('0')
                        realized_pnl_percent = Decimal('0')
                        final_price = None
                        closed_at_time = fallback_close_time

                    if first_buy_time:
                        holding_days = (closed_at_time - first_buy_time).days
                    else:
                        holding_days = None

                    position = PositionModel(
                        account_id=account_id,
                        symbol=symbol,
                        position_type='spot',
                        quantity=total_closed_quantity,
                        average_cost=average_cost,
                        first_buy_time=first_buy_time,
                        holding_days=holding_days,
                        is_closed=True,
                        closed_at=closed_at_time,
                        final_price=final_price,
                        realized_pnl=total_realized_pnl,
                        realized_pnl_percent=realized_pnl_percent,
                        unrealized_pnl=Decimal('0'),
                        unrealized_pnl_percent=Decimal('0')
                    )
                    self.db.add(position)
                    result_positions.append(position)
                continue

            # 计算平均成本
            average_cost = data['total_cost'] / quantity if quantity > 0 else Decimal('0')

            if position:
                # 更新现有持仓
                position.position_type = 'spot'
                position.quantity = quantity
                position.average_cost = average_cost
                position.first_buy_time = data['first_buy_time']
                position.is_closed = False  # 重新开仓
                position.closed_at = None
                position.update_holding_days()
            else:
                # 创建新持仓
                position = PositionModel(
                    account_id=account_id,
                    symbol=symbol,
                    position_type='spot',
                    quantity=quantity,
                    average_cost=average_cost,
                    first_buy_time=data['first_buy_time'],
                    is_closed=False
                )
                position.update_holding_days()
                self.db.add(position)

            result_positions.append(position)

        # 提交所有更改
        self.db.commit()

        return result_positions

    def _calculate_futures_positions(
        self,
        account_id: UUID,
        trades: List[TradeModel]
    ) -> List[PositionModel]:
        """
        计算合约持仓 (单向持仓模式)

        单向持仓逻辑:
        - quantity > 0: 多头持仓
        - quantity < 0: 空头持仓
        - position_side根据quantity正负自动设置

        交易类型:
        - position_side=LONG + side=buy: 开多/加多
        - position_side=LONG + side=sell: 平多
        - position_side=SHORT + side=sell: 开空/加空
        - position_side=SHORT + side=buy: 平空

        Args:
            account_id: 账户ID
            trades: 交易记录列表

        Returns:
            持仓列表
        """
        positions_data = {}  # symbol -> position data

        for trade in trades:
            symbol = trade.symbol

            if symbol not in positions_data:
                positions_data[symbol] = {
                    'quantity': Decimal('0'),  # 正=多头,负=空头
                    'entry_price': Decimal('0'),  # 开仓均价
                    'total_margin': Decimal('0'),  # 累计保证金
                    'leverage': trade.leverage or Decimal('1'),
                    'first_open_time': None,
                    'last_trade_time': None,
                }

            position = positions_data[symbol]
            position['last_trade_time'] = trade.trade_time
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_margin = Decimal(str(trade.margin)) if trade.margin else Decimal('0')

            old_quantity = position['quantity']
            old_entry_price = position['entry_price']

            # 根据position_side和side判断操作类型
            if trade.position_side == 'LONG':
                if trade.side == 'buy':
                    # 开多/加多仓
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    # 更新加权平均开仓价
                    if abs_old_qty > 0 and old_quantity > 0:
                        # 已有多头,加仓
                        position['entry_price'] = (
                            (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                        )
                    else:
                        # 新开多头
                        position['entry_price'] = trade_price
                        position['first_open_time'] = trade.trade_time

                    position['quantity'] = new_quantity
                    position['total_margin'] += trade_margin

                elif trade.side == 'sell':
                    # 平多仓
                    new_quantity = old_quantity - trade_quantity

                    if new_quantity >= 0:
                        # 部分平仓,保持多头
                        position['quantity'] = new_quantity
                        # 按比例减少保证金
                        if old_quantity > 0:
                            position['total_margin'] *= (new_quantity / old_quantity)
                    else:
                        # 多头平完并反向开空
                        position['quantity'] = new_quantity
                        position['entry_price'] = trade_price
                        position['total_margin'] = trade_margin
                        position['first_open_time'] = trade.trade_time

            elif trade.position_side == 'SHORT':
                if trade.side == 'sell':
                    # 开空/加空仓
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    # 更新加权平均开仓价
                    if abs_old_qty > 0 and old_quantity < 0:
                        # 已有空头,加仓
                        position['entry_price'] = (
                            (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                        )
                    else:
                        # 新开空头
                        position['entry_price'] = trade_price
                        position['first_open_time'] = trade.trade_time

                    position['quantity'] = -new_quantity  # 空头为负数
                    position['total_margin'] += trade_margin

                elif trade.side == 'buy':
                    # 平空仓
                    new_quantity = old_quantity + trade_quantity

                    if new_quantity <= 0:
                        # 部分平仓,保持空头
                        position['quantity'] = new_quantity
                        # 按比例减少保证金
                        if old_quantity < 0:
                            position['total_margin'] *= (abs(new_quantity) / abs(old_quantity))
                    else:
                        # 空头平完并反向开多
                        position['quantity'] = new_quantity
                        position['entry_price'] = trade_price
                        position['total_margin'] = trade_margin
                        position['first_open_time'] = trade.trade_time

        # 保存或更新持仓记录
        result_positions = []

        for symbol, data in positions_data.items():
            quantity = data['quantity']

            # 查找现有持仓
            position = self.db.query(PositionModel).filter(
                PositionModel.account_id == account_id,
                PositionModel.symbol == symbol
            ).first()

            # 持仓为0: 标记为已清仓
            if quantity == 0:
                closed_at_time = data.get('last_trade_time') or datetime.utcnow()
                if position:
                    position.quantity = Decimal('0')
                    position.is_closed = True
                    position.closed_at = closed_at_time
                    position.unrealized_pnl = Decimal('0')
                    position.unrealized_pnl_percent = Decimal('0')
                    position.roe_percent = Decimal('0')
                    if position.first_buy_time:
                        position.holding_days = (closed_at_time - position.first_buy_time).days
                    result_positions.append(position)
                else:
                    # 创建已清仓的持仓记录（保留历史）
                    holding_days = None
                    if data.get('first_open_time'):
                        holding_days = (closed_at_time - data['first_open_time']).days

                    position = PositionModel(
                        account_id=account_id,
                        symbol=symbol,
                        position_type='futures',
                        position_side=None,
                        quantity=Decimal('0'),
                        entry_price=data['entry_price'],
                        leverage=data['leverage'],
                        margin_used=Decimal('0'),
                        first_buy_time=data['first_open_time'],
                        holding_days=holding_days,
                        is_closed=True,
                        closed_at=closed_at_time,
                        unrealized_pnl=Decimal('0'),
                        unrealized_pnl_percent=Decimal('0'),
                        roe_percent=Decimal('0')
                    )
                    self.db.add(position)
                    result_positions.append(position)
                continue

            # 确定持仓方向
            position_side = 'LONG' if quantity > 0 else 'SHORT'

            if position:
                # 更新现有持仓
                position.position_type = 'futures'
                position.position_side = position_side
                position.quantity = quantity
                position.entry_price = data['entry_price']
                position.leverage = data['leverage']
                position.margin_used = data['total_margin']
                position.first_buy_time = data['first_open_time']
                position.is_closed = False  # 重新开仓
                position.closed_at = None
                position.update_holding_days()
            else:
                # 创建新持仓
                position = PositionModel(
                    account_id=account_id,
                    symbol=symbol,
                    position_type='futures',
                    position_side=position_side,
                    quantity=quantity,
                    entry_price=data['entry_price'],
                    leverage=data['leverage'],
                    margin_used=data['total_margin'],
                    first_buy_time=data['first_open_time'],
                    is_closed=False
                )
                position.update_holding_days()
                self.db.add(position)

            result_positions.append(position)

        # 提交所有更改
        self.db.commit()

        return result_positions

    def calculate_positions_for_user(self, user_id: UUID) -> Dict[UUID, List[PositionModel]]:
        """
        计算用户所有账户的持仓

        Args:
            user_id: 用户 ID

        Returns:
            账户 ID -> 持仓列表的字典
        """
        # 获取用户的所有交易账户
        accounts = self.db.query(TradeAccountModel).filter(
            TradeAccountModel.user_id == user_id
        ).all()

        result = {}
        for account in accounts:
            positions = self.calculate_positions_for_account(account.id)
            result[account.id] = positions

        return result

    def recalculate_positions_after_trade(
        self,
        account_id: UUID,
        symbol: str
    ) -> Optional[PositionModel]:
        """
        在添加/删除交易记录后,重新计算指定标的的持仓

        这是一个优化版本,只重算单个标的,而不是整个账户
        支持现货和合约两种模式

        Args:
            account_id: 交易账户 ID
            symbol: 交易标的符号

        Returns:
            更新后的持仓记录,如果持仓为 0 则返回 None
        """
        # 获取账户类型
        account = self.db.query(TradeAccountModel).filter(
            TradeAccountModel.id == account_id
        ).first()

        if not account:
            return None

        # 获取该标的的所有交易记录
        trades = self.db.query(TradeModel).filter(
            TradeModel.account_id == account_id,
            TradeModel.symbol == symbol
        ).order_by(TradeModel.trade_time).all()

        # 根据账户类型选择计算方法
        if account.is_futures_account():
            return self._recalculate_futures_position(account_id, symbol, trades)
        else:
            return self._recalculate_spot_position(account_id, symbol, trades)

    def _recalculate_spot_position(
        self,
        account_id: UUID,
        symbol: str,
        trades: List[TradeModel]
    ) -> Optional[PositionModel]:
        """
        重新计算现货持仓 (保持原有逻辑)

        Args:
            account_id: 账户ID
            symbol: 标的符号
            trades: 交易记录列表

        Returns:
            持仓记录或None
        """
        # 计算持仓
        quantity = Decimal('0')
        total_cost = Decimal('0')
        first_buy_time = None

        for trade in trades:
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_fee = Decimal(str(trade.fee)) if trade.fee else Decimal('0')

            if trade.side == 'buy':
                old_quantity = quantity
                old_total_cost = total_cost

                new_cost = (trade_quantity * trade_price) + trade_fee
                total_cost = old_total_cost + new_cost
                quantity = old_quantity + trade_quantity

                if first_buy_time is None:
                    first_buy_time = trade.trade_time

            elif trade.side == 'sell':
                quantity = quantity - trade_quantity

                if quantity > 0:
                    cost_ratio = (quantity + trade_quantity) / quantity
                    total_cost = total_cost / cost_ratio
                else:
                    total_cost = Decimal('0')
                    first_buy_time = None

        # 查找现有持仓
        position = self.db.query(PositionModel).filter(
            PositionModel.account_id == account_id,
            PositionModel.symbol == symbol
        ).first()

        if quantity <= 0:
            # 持仓为 0,标记为已清仓
            if position:
                last_sell_time = max(
                    (t.trade_time for t in trades if t.side == 'sell'),
                    default=None
                )
                last_trade_time = max(
                    (t.trade_time for t in trades),
                    default=None
                )
                closed_at_time = last_sell_time or last_trade_time or datetime.utcnow()

                position.quantity = Decimal('0')
                position.is_closed = True
                position.closed_at = closed_at_time
                position.unrealized_pnl = Decimal('0')
                position.unrealized_pnl_percent = Decimal('0')
                self.db.commit()
                self.db.refresh(position)
                return position
            return None

        # 计算平均成本
        average_cost = total_cost / quantity if quantity > 0 else Decimal('0')

        if position:
            # 更新现有持仓
            position.position_type = 'spot'
            position.quantity = quantity
            position.average_cost = average_cost
            position.first_buy_time = first_buy_time
            position.is_closed = False  # 重新开仓
            position.closed_at = None
            position.update_holding_days()
        else:
            # 创建新持仓
            position = PositionModel(
                account_id=account_id,
                symbol=symbol,
                position_type='spot',
                quantity=quantity,
                average_cost=average_cost,
                first_buy_time=first_buy_time,
                is_closed=False
            )
            position.update_holding_days()
            self.db.add(position)

        self.db.commit()
        self.db.refresh(position)

        return position

    def _recalculate_futures_position(
        self,
        account_id: UUID,
        symbol: str,
        trades: List[TradeModel]
    ) -> Optional[PositionModel]:
        """
        重新计算合约持仓 (单向持仓模式)

        Args:
            account_id: 账户ID
            symbol: 标的符号
            trades: 交易记录列表

        Returns:
            持仓记录或None
        """
        # 计算持仓 (与_calculate_futures_positions逻辑相同,但只处理单个标的)
        quantity = Decimal('0')
        entry_price = Decimal('0')
        total_margin = Decimal('0')
        leverage = Decimal('1')
        first_open_time = None

        for trade in trades:
            trade_quantity = Decimal(str(trade.quantity))
            trade_price = Decimal(str(trade.price))
            trade_margin = Decimal(str(trade.margin)) if trade.margin else Decimal('0')

            old_quantity = quantity
            old_entry_price = entry_price

            # 获取杠杆
            if trade.leverage:
                leverage = Decimal(str(trade.leverage))

            # 根据position_side和side判断操作类型
            if trade.position_side == 'LONG':
                if trade.side == 'buy':
                    # 开多/加多
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    if abs_old_qty > 0 and old_quantity > 0:
                        entry_price = (
                            (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                        )
                    else:
                        entry_price = trade_price
                        first_open_time = trade.trade_time

                    quantity = new_quantity
                    total_margin += trade_margin

                elif trade.side == 'sell':
                    # 平多
                    new_quantity = old_quantity - trade_quantity

                    if new_quantity >= 0:
                        quantity = new_quantity
                        if old_quantity > 0:
                            total_margin *= (new_quantity / old_quantity)
                    else:
                        quantity = new_quantity
                        entry_price = trade_price
                        total_margin = trade_margin
                        first_open_time = trade.trade_time

            elif trade.position_side == 'SHORT':
                if trade.side == 'sell':
                    # 开空/加空
                    abs_old_qty = abs(old_quantity)
                    new_quantity = abs_old_qty + trade_quantity

                    if abs_old_qty > 0 and old_quantity < 0:
                        entry_price = (
                            (abs_old_qty * old_entry_price + trade_quantity * trade_price) / new_quantity
                        )
                    else:
                        entry_price = trade_price
                        first_open_time = trade.trade_time

                    quantity = -new_quantity
                    total_margin += trade_margin

                elif trade.side == 'buy':
                    # 平空
                    new_quantity = old_quantity + trade_quantity

                    if new_quantity <= 0:
                        quantity = new_quantity
                        if old_quantity < 0:
                            total_margin *= (abs(new_quantity) / abs(old_quantity))
                    else:
                        quantity = new_quantity
                        entry_price = trade_price
                        total_margin = trade_margin
                        first_open_time = trade.trade_time

        # 查找现有持仓
        position = self.db.query(PositionModel).filter(
            PositionModel.account_id == account_id,
            PositionModel.symbol == symbol
        ).first()

        # 持仓为0,标记为已清仓
        if quantity == 0:
            if position:
                position.quantity = Decimal('0')
                position.is_closed = True
                last_trade_time = max((t.trade_time for t in trades), default=None)
                position.closed_at = last_trade_time or datetime.utcnow()
                position.unrealized_pnl = Decimal('0')
                position.unrealized_pnl_percent = Decimal('0')
                position.roe_percent = Decimal('0')
                if position.first_buy_time:
                    position.holding_days = (position.closed_at - position.first_buy_time).days
                self.db.commit()
                self.db.refresh(position)
                return position
            return None

        # 确定持仓方向
        position_side = 'LONG' if quantity > 0 else 'SHORT'

        if position:
            # 更新现有持仓
            position.position_type = 'futures'
            position.position_side = position_side
            position.quantity = quantity
            position.entry_price = entry_price
            position.leverage = leverage
            position.margin_used = total_margin
            position.first_buy_time = first_open_time
            position.is_closed = False  # 重新开仓
            position.closed_at = None
            position.update_holding_days()
        else:
            # 创建新持仓
            position = PositionModel(
                account_id=account_id,
                symbol=symbol,
                position_type='futures',
                position_side=position_side,
                quantity=quantity,
                entry_price=entry_price,
                leverage=leverage,
                margin_used=total_margin,
                first_buy_time=first_open_time,
                is_closed=False
            )
            position.update_holding_days()
            self.db.add(position)

        self.db.commit()
        self.db.refresh(position)

        return position

    def get_position_summary(self, user_id: UUID) -> Dict:
        """
        获取用户持仓汇总信息

        Args:
            user_id: 用户 ID

        Returns:
            汇总信息字典
        """
        # 查询用户的所有持仓
        positions = self.db.query(PositionModel).join(
            TradeAccountModel,
            PositionModel.account_id == TradeAccountModel.id
        ).filter(
            TradeAccountModel.user_id == user_id,
            PositionModel.quantity > 0
        ).all()

        total_positions = len(positions)

        total_cost = 0.0
        total_market_value = 0.0
        total_unrealized_pnl = 0.0

        for position in positions:
            position_cost = float(position.total_cost or 0)
            market_value = float(position.market_value or 0)
            total_cost += position_cost
            total_market_value += market_value

            if position.unrealized_pnl is not None:
                total_unrealized_pnl += float(position.unrealized_pnl)
            elif position.current_price is not None:
                total_unrealized_pnl += market_value - position_cost

        total_unrealized_pnl_percent = (
            (total_unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
        )

        return {
            'total_positions': total_positions,
            'total_cost': total_cost,
            'total_market_value': total_market_value,
            'total_unrealized_pnl': total_unrealized_pnl,
            'total_unrealized_pnl_percent': total_unrealized_pnl_percent,
        }
