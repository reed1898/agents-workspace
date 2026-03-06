from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Integer, Uuid
from datetime import datetime
import uuid
from ..core.database import Base


class ClosedPosition(Base):
    """已平仓记录模型

    记录每次完全或部分平仓的历史,用于盈亏统计和分析。
    当持仓全部或部分卖出时,创建一条记录。

    支持现货和合约:
    - 现货: 记录买入成本和卖出价格,计算盈亏
    - 合约: 记录开仓价和平仓价,计算盈亏

    关键字段:
    - open_time: 本次持仓周期的首次买入时间
    - close_time: 平仓时间
    - realized_pnl: 已实现盈亏金额
    - realized_pnl_percent: 已实现盈亏百分比
    """
    __tablename__ = "closed_positions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("trade_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # 添加索引以提高查询性能
    )

    # 标的信息
    symbol = Column(String(50), nullable=False, index=True)  # 例如: BTC/USDT, AAPL

    # 持仓类型和方向
    position_type = Column(String(20), default='spot', nullable=False)  # spot, futures
    position_side = Column(String(10), nullable=True)  # 合约: LONG/SHORT; 现货: NULL

    # 平仓数量和价格
    quantity = Column(DECIMAL(20, 8), nullable=False)  # 本次平仓的数量
    entry_price = Column(DECIMAL(20, 8), nullable=False)  # 开仓均价(成本价)
    exit_price = Column(DECIMAL(20, 8), nullable=False)  # 平仓价格(卖出价)

    # 合约专用字段
    leverage = Column(DECIMAL(10, 2), nullable=True)  # 杠杆倍数
    margin_used = Column(DECIMAL(20, 8), nullable=True)  # 本次平仓占用的保证金

    # 盈亏信息
    realized_pnl = Column(DECIMAL(20, 8), nullable=False)  # 已实现盈亏(金额)
    realized_pnl_percent = Column(DECIMAL(10, 4), nullable=False)  # 已实现盈亏(百分比)
    roe_percent = Column(DECIMAL(10, 4), nullable=True)  # 合约: ROE收益率(基于保证金)

    # 时间信息
    open_time = Column(DateTime, nullable=False)  # 本次持仓周期的首次买入时间
    close_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)  # 平仓时间
    holding_days = Column(Integer, nullable=True)  # 持仓天数

    # 手续费
    total_fees = Column(DECIMAL(20, 8), nullable=True, default=0)  # 本次平仓相关的总手续费

    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ClosedPosition {self.symbol} qty={self.quantity} pnl={self.realized_pnl}>"

    @property
    def is_profitable(self) -> bool:
        """判断是否盈利"""
        return float(self.realized_pnl) > 0

    @property
    def total_cost(self) -> float:
        """计算总成本"""
        return float(abs(self.quantity) * self.entry_price)

    @property
    def total_proceeds(self) -> float:
        """计算总收入"""
        return float(abs(self.quantity) * self.exit_price)
