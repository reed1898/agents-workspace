"""
交易服务 - 处理交易相关的业务逻辑

包括操作类型自动判断、交易创建等功能
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from uuid import UUID
from decimal import Decimal

from ..models.trade import Trade as TradeModel
from ..models.position import Position as PositionModel
from ..models.trade_account import TradeAccount as TradeAccountModel
from ..schemas.trade import ActionType


class TradeService:
    """交易服务类"""

    def __init__(self, db: Session):
        self.db = db

    def infer_action_type(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        account_id: UUID,
        position_side: Optional[str] = None,
        trade_time = None
    ) -> Optional[ActionType]:
        """
        自动推断操作类型 (建仓/加仓/减仓/清仓)

        根据交易方向和持仓状态自动判断操作类型。
        支持现货和合约两种模式。

        Args:
            symbol: 交易标的符号
            side: 交易方向 (buy/sell)
            quantity: 交易数量
            account_id: 账户ID
            position_side: 持仓方向 (LONG/SHORT，仅合约)
            trade_time: 交易时间 (用于计算截止时间点的持仓)

        Returns:
            ActionType: 操作类型枚举，如果无法判断则返回 None

        现货逻辑:
        - buy + 无持仓 = open (建仓)
        - buy + 有持仓 = add (加仓)
        - sell + 部分卖出 = reduce (减仓)
        - sell + 全部卖出 = close (清仓)

        合约逻辑:
        - position_side=LONG + side=buy + 无持仓 = open (开多)
        - position_side=LONG + side=buy + 有多头 = add (加多)
        - position_side=LONG + side=sell + 部分平仓 = reduce (减多)
        - position_side=LONG + side=sell + 全部平仓 = close (平多)
        - position_side=SHORT + side=sell + 无持仓 = open (开空)
        - position_side=SHORT + side=sell + 有空头 = add (加空)
        - position_side=SHORT + side=buy + 部分平仓 = reduce (减空)
        - position_side=SHORT + side=buy + 全部平仓 = close (平空)
        """

        # 获取账户类型
        account = self.db.query(TradeAccountModel).filter(
            TradeAccountModel.id == account_id
        ).first()

        if not account:
            return None

        # 获取当前持仓状态 (截止到 trade_time 之前的所有交易)
        # 注意: 这里我们要计算的是**交易发生前**的持仓状态
        query = self.db.query(TradeModel).filter(
            TradeModel.account_id == account_id,
            TradeModel.symbol == symbol
        )

        # 如果提供了交易时间，只计算该时间之前的交易
        if trade_time:
            query = query.filter(TradeModel.trade_time < trade_time)

        trades_before = query.order_by(TradeModel.trade_time).all()

        # 现货逻辑
        if not position_side or not account.is_futures_account():
            return self._infer_spot_action_type(
                side=side,
                quantity=quantity,
                trades_before=trades_before
            )

        # 合约逻辑
        else:
            return self._infer_futures_action_type(
                side=side,
                quantity=quantity,
                position_side=position_side,
                trades_before=trades_before
            )

    def _infer_spot_action_type(
        self,
        side: str,
        quantity: Decimal,
        trades_before: list
    ) -> Optional[ActionType]:
        """
        推断现货交易的操作类型

        Args:
            side: 交易方向
            quantity: 交易数量
            trades_before: 该笔交易之前的所有交易记录

        Returns:
            操作类型
        """
        # 计算当前持仓数量
        current_quantity = Decimal('0')

        for trade in trades_before:
            trade_qty = Decimal(str(trade.quantity))
            if trade.side == 'buy':
                current_quantity += trade_qty
            elif trade.side == 'sell':
                current_quantity -= trade_qty

        quantity_decimal = Decimal(str(quantity))

        if side == 'buy':
            # 买入操作
            if current_quantity == 0:
                return ActionType.OPEN  # 建仓
            else:
                return ActionType.ADD  # 加仓

        elif side == 'sell':
            # 卖出操作
            if current_quantity <= 0:
                # 异常情况: 没有持仓却卖出
                return None

            remaining = current_quantity - quantity_decimal

            if remaining <= 0:
                return ActionType.CLOSE  # 清仓
            else:
                return ActionType.REDUCE  # 减仓

        return None

    def _infer_futures_action_type(
        self,
        side: str,
        quantity: Decimal,
        position_side: str,
        trades_before: list
    ) -> Optional[ActionType]:
        """
        推断合约交易的操作类型 (单向持仓模式)

        Args:
            side: 交易方向 (buy/sell)
            quantity: 交易数量
            position_side: 持仓方向 (LONG/SHORT)
            trades_before: 该笔交易之前的所有交易记录

        Returns:
            操作类型
        """
        # 计算当前持仓数量 (正=多头, 负=空头)
        current_quantity = Decimal('0')

        for trade in trades_before:
            trade_qty = Decimal(str(trade.quantity))

            if trade.position_side == 'LONG':
                if trade.side == 'buy':
                    # 开多/加多
                    current_quantity += trade_qty
                elif trade.side == 'sell':
                    # 平多
                    current_quantity -= trade_qty

            elif trade.position_side == 'SHORT':
                if trade.side == 'sell':
                    # 开空/加空
                    current_quantity -= trade_qty
                elif trade.side == 'buy':
                    # 平空
                    current_quantity += trade_qty

        quantity_decimal = Decimal(str(quantity))

        # 判断操作类型
        if position_side == 'LONG':
            if side == 'buy':
                # 开多/加多
                if current_quantity <= 0:
                    return ActionType.OPEN  # 建多仓
                else:
                    return ActionType.ADD  # 加多仓

            elif side == 'sell':
                # 平多
                if current_quantity <= 0:
                    # 异常: 没有多头却平多
                    return None

                remaining = current_quantity - quantity_decimal

                if remaining <= 0:
                    return ActionType.CLOSE  # 平完多仓
                else:
                    return ActionType.REDUCE  # 减多仓

        elif position_side == 'SHORT':
            if side == 'sell':
                # 开空/加空
                if current_quantity >= 0:
                    return ActionType.OPEN  # 建空仓
                else:
                    return ActionType.ADD  # 加空仓

            elif side == 'buy':
                # 平空
                if current_quantity >= 0:
                    # 异常: 没有空头却平空
                    return None

                remaining = current_quantity + quantity_decimal

                if remaining >= 0:
                    return ActionType.CLOSE  # 平完空仓
                else:
                    return ActionType.REDUCE  # 减空仓

        return None
