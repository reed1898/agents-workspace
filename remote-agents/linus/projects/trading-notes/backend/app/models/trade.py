from __future__ import annotations
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Text, UniqueConstraint, Integer, Boolean, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base
from ..utils.symbol_name import extract_symbol_name


class Trade(Base):
    """交易记录模型

    记录所有交易历史，支持从 API 同步、手动输入、文件导入等多种来源

    支持现货交易和合约交易:
    - 现货: position_side, leverage, margin 为 NULL
    - 合约: position_side=LONG/SHORT, leverage和margin有值
    """
    __tablename__ = "trades"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("trade_accounts.id", ondelete="CASCADE"),
        nullable=False
    )

    # 交易标的信息
    symbol = Column(String(50), nullable=False)  # 例如: BTC/USDT, AAPL, 000001.SZ

    # 交易方向和数量
    side = Column(String(10), nullable=False)  # buy, sell
    quantity = Column(DECIMAL(20, 8), nullable=False)  # 交易数量

    # 价格和费用
    price = Column(DECIMAL(20, 8), nullable=False)  # 成交价格
    fee = Column(DECIMAL(20, 8), default=0)  # 手续费
    fee_currency = Column(String(10), nullable=True)  # 手续费币种

    # 合约交易专用字段 (现货交易时为 NULL)
    position_side = Column(String(10), nullable=True)  # LONG, SHORT, BOTH (单向持仓只用LONG/SHORT)
    leverage = Column(DECIMAL(10, 2), nullable=True)  # 杠杆倍数，如 10.00
    margin = Column(DECIMAL(20, 8), nullable=True)  # 占用保证金

    # 交易时间
    trade_time = Column(DateTime, nullable=False)  # 交易发生时间

    # 外部标识和来源
    trade_id_external = Column(String(100), nullable=True)  # 交易所原始交易 ID
    sync_source = Column(String(20), nullable=False)  # api, manual, import

    # 备注
    notes = Column(Text, nullable=True)

    # 交易理由和K线图 (Phase 3 新增字段)
    action_type = Column(String(20), nullable=True, index=True)  # open, add, reduce, close
    action_reason = Column(Text, nullable=True)  # 操作理由
    action_strategy = Column(String(100), nullable=True)  # 操作策略
    chart_image_url = Column(String(500), nullable=True)  # K线图截图URL
    chart_data = Column(JSON, nullable=True)  # K线数据快照

    # 纪律分析字段 (Phase 4 新增字段)
    emotion_state = Column(String(50), nullable=True, index=True)  # 情绪状态
    emotion_intensity = Column(Integer, nullable=True)  # 情绪强度 1-10
    planned_stop_loss = Column(DECIMAL(20, 8), nullable=True)  # 计划止损价
    actual_stop_loss = Column(DECIMAL(20, 8), nullable=True)  # 实际止损价
    stop_loss_executed = Column(Boolean, nullable=True)  # 是否执行止损
    planned_take_profit = Column(DECIMAL(20, 8), nullable=True)  # 计划止盈价
    actual_take_profit = Column(DECIMAL(20, 8), nullable=True)  # 实际止盈价
    entry_strategy = Column(String(50), nullable=True, index=True)  # 入场策略
    exit_strategy = Column(String(50), nullable=True, index=True)  # 出场策略
    reviewed = Column(Boolean, default=False, nullable=False, index=True)  # 是否已复盘
    reviewed_at = Column(DateTime, nullable=True)  # 复盘时间

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 唯一约束: 同一账户的同一外部交易 ID 不能重复（防止重复导入）
    __table_args__ = (
        UniqueConstraint('account_id', 'trade_id_external', name='uix_account_trade_external'),
    )

    # 关系
    # account = relationship("TradeAccount", back_populates="trades")

    def __repr__(self):
        return f"<Trade {self.symbol} {self.side} {self.quantity} @ {self.price} on {self.trade_time}>"

    @property
    def total_amount(self) -> float:
        """计算交易总金额 (不含手续费)"""
        return float(self.price * self.quantity)

    @property
    def total_cost(self) -> float:
        """计算交易总成本 (含手续费)"""
        return float(self.price * self.quantity + self.fee)

    @property
    def symbol_name(self) -> str | None:
        """从备注中提取标的名称(仅部分导入数据)"""
        override = getattr(self, "_symbol_name_override", None)
        if override:
            return override
        return extract_symbol_name(self.notes)

    @symbol_name.setter
    def symbol_name(self, value: str | None):
        self._symbol_name_override = value
