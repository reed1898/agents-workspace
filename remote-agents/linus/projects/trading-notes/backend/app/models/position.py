from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Integer, UniqueConstraint, Boolean, Text, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base


class Position(Base):
    """持仓模型

    记录当前持仓状态，由交易记录计算得出

    支持现货和合约持仓:
    - 现货: position_type='spot', quantity > 0, average_cost 有效
    - 合约单向持仓: position_type='futures', quantity 正数=多头/负数=空头, entry_price 有效

    持仓状态:
    - is_closed=False: 当前持仓 (quantity != 0)
    - is_closed=True: 已清仓持仓 (quantity = 0, 保留历史记录)
    """
    __tablename__ = "positions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("trade_accounts.id", ondelete="CASCADE"),
        nullable=False
    )

    # 标的信息
    symbol = Column(String(50), nullable=False)  # 例如: BTC/USDT, AAPL, 000001.SZ

    # 持仓类型和方向
    position_type = Column(String(20), default='spot', nullable=False)  # spot, futures
    position_side = Column(String(10), nullable=True)  # 合约: LONG/SHORT; 现货: NULL

    # 持仓数量和成本
    quantity = Column(DECIMAL(20, 8), nullable=False)  # 现货: >0; 合约单向: 正=多/负=空
    average_cost = Column(DECIMAL(20, 8), nullable=True)  # 现货使用: 平均成本价
    entry_price = Column(DECIMAL(20, 8), nullable=True)  # 合约使用: 开仓均价

    # 合约专用字段
    leverage = Column(DECIMAL(10, 2), nullable=True)  # 杠杆倍数
    margin_used = Column(DECIMAL(20, 8), nullable=True)  # 占用保证金
    liquidation_price = Column(DECIMAL(20, 8), nullable=True)  # 强平价

    # 当前价格和盈亏
    current_price = Column(DECIMAL(20, 8), nullable=True)  # 当前市场价格
    unrealized_pnl = Column(DECIMAL(20, 8), nullable=True)  # 未实现盈亏 (金额)
    unrealized_pnl_percent = Column(DECIMAL(10, 4), nullable=True)  # 未实现盈亏 (百分比)
    roe_percent = Column(DECIMAL(10, 4), nullable=True)  # 合约: ROE收益率 (基于保证金)

    notes = Column(Text, nullable=True)  # 持仓备注

    # 持仓时间信息
    first_buy_time = Column(DateTime, nullable=True)  # 本次持仓周期的第一次买入时间
    holding_days = Column(Integer, nullable=True)  # 持仓天数

    # 已清仓标记和清仓信息
    is_closed = Column(Boolean, default=False, nullable=False)  # 是否已清仓
    closed_at = Column(DateTime, nullable=True)  # 清仓时间
    final_price = Column(DECIMAL(20, 8), nullable=True)  # 清仓时的最终价格 (最后一笔卖出价)
    realized_pnl = Column(DECIMAL(20, 8), nullable=True)  # 已实现盈亏 (金额)
    realized_pnl_percent = Column(DECIMAL(10, 4), nullable=True)  # 已实现盈亏 (百分比)

    # 更新时间
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 唯一约束: 同一账户的同一标的只能有一条持仓记录
    # 注意: 对于单向持仓模式的合约,一个标的只会有一条记录(多或空通过quantity正负区分)
    # 如果未来支持双向持仓,需要修改此约束包含 position_side
    __table_args__ = (
        UniqueConstraint('account_id', 'symbol', name='uix_account_symbol'),
    )

    # 关系
    # account = relationship("TradeAccount", back_populates="positions")

    def __repr__(self):
        return f"<Position {self.symbol} qty={self.quantity} cost={self.average_cost}>"

    @property
    def total_cost(self) -> float:
        """计算总成本"""
        # 合约使用 entry_price，现货使用 average_cost
        if self.position_type == 'futures':
            cost_price = self.entry_price or 0
        else:
            cost_price = self.average_cost or 0
        return float(abs(self.quantity) * cost_price)

    @property
    def market_value(self) -> float:
        """计算当前市值"""
        if self.current_price is None:
            if self.position_type == 'futures':
                cost_price = self.entry_price
            else:
                cost_price = self.average_cost
            if cost_price is None:
                return 0.0
            return float(self.quantity * cost_price)
        return float(self.quantity * self.current_price)

    @property
    def is_profitable(self) -> bool:
        """判断是否盈利"""
        if self.unrealized_pnl is None:
            return False
        return float(self.unrealized_pnl) > 0

    def update_price_and_pnl(self, current_price: float):
        """更新当前价格并重新计算盈亏

        Args:
            current_price: 当前市场价格
        """
        from decimal import Decimal

        # 将价格转换为 Decimal
        current_price_decimal = Decimal(str(current_price))
        self.current_price = current_price_decimal

        if self.position_type == 'spot':
            # 现货盈亏计算
            cost_value = self.quantity * self.average_cost
            market_value = self.quantity * current_price_decimal

            # 计算盈亏金额
            self.unrealized_pnl = market_value - cost_value

            # 计算盈亏百分比
            if cost_value > 0:
                self.unrealized_pnl_percent = (self.unrealized_pnl / cost_value) * 100
            else:
                self.unrealized_pnl_percent = Decimal('0')

        elif self.position_type == 'futures':
            # 合约盈亏计算
            if self.entry_price is None or self.entry_price == 0:
                self.unrealized_pnl = Decimal('0')
                self.unrealized_pnl_percent = Decimal('0')
                self.roe_percent = Decimal('0')
                return

            abs_quantity = abs(self.quantity)

            if self.quantity > 0:
                # 多头盈亏: (当前价 - 开仓价) * 数量
                self.unrealized_pnl = (current_price_decimal - self.entry_price) * abs_quantity
            elif self.quantity < 0:
                # 空头盈亏: (开仓价 - 当前价) * 数量
                self.unrealized_pnl = (self.entry_price - current_price_decimal) * abs_quantity
            else:
                # 持仓为0
                self.unrealized_pnl = Decimal('0')
                self.unrealized_pnl_percent = Decimal('0')
                self.roe_percent = Decimal('0')
                return

            # 计算盈亏百分比 (基于开仓价值)
            entry_value = abs_quantity * self.entry_price
            if entry_value > 0:
                self.unrealized_pnl_percent = (self.unrealized_pnl / entry_value) * 100
            else:
                self.unrealized_pnl_percent = Decimal('0')

            # 计算 ROE (基于保证金)
            if self.margin_used and self.margin_used > 0:
                self.roe_percent = (self.unrealized_pnl / self.margin_used) * 100
            else:
                self.roe_percent = Decimal('0')

        self.last_updated = datetime.utcnow()

    def update_holding_days(self):
        """更新持仓天数"""
        if self.first_buy_time:
            delta = datetime.utcnow() - self.first_buy_time
            self.holding_days = delta.days
