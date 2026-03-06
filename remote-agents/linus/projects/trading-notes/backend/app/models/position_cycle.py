from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Text, Integer, Boolean, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base


class PositionCycle(Base):
    """持仓周期模型

    记录一个完整的持仓周期（从首次建仓到完全清仓），用于分析交易纪律和表现
    """
    __tablename__ = "position_cycles"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    account_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("trade_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    symbol = Column(String(50), nullable=False, index=True)

    # 持仓周期时间
    open_time = Column(DateTime, nullable=False, index=True)  # 首次建仓时间
    close_time = Column(DateTime, nullable=True)  # 完全清仓时间
    status = Column(String(20), default='open', nullable=False, index=True)  # 'open' / 'closed'

    # 关联的所有交易 (存储 UUID 数组)
    trade_ids = Column(JSON, nullable=False, default=list)  # 按时间顺序排列

    # 整体策略
    primary_strategy = Column(String(50), nullable=True)  # 主要策略

    # 整体情绪评估
    dominant_emotion = Column(String(50), nullable=True)  # 主导情绪
    emotion_stability = Column(Integer, nullable=True)  # 情绪稳定性(1-10)

    # 持仓统计
    total_quantity = Column(DECIMAL(20, 8), nullable=True)  # 总买入量
    average_entry_price = Column(DECIMAL(20, 8), nullable=True)  # 平均成本
    average_exit_price = Column(DECIMAL(20, 8), nullable=True)  # 平均卖出价
    total_profit_loss = Column(DECIMAL(20, 2), nullable=True)  # 总盈亏
    roi_percent = Column(DECIMAL(10, 2), nullable=True)  # 收益率

    # 持仓时长
    holding_hours = Column(Integer, nullable=True)  # 持仓小时数

    # 纪律评估
    followed_stop_loss = Column(Boolean, nullable=True)  # 是否执行止损
    followed_take_profit = Column(Boolean, nullable=True)  # 是否执行止盈
    discipline_score = Column(Integer, nullable=True)  # 纪律评分(0-100)

    # 复盘总结
    what_went_well = Column(Text, nullable=True)  # 做得好的地方
    what_to_improve = Column(Text, nullable=True)  # 需要改进的地方
    lessons_learned = Column(Text, nullable=True)  # 经验教训

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    # user = relationship("User", back_populates="position_cycles")
    # account = relationship("TradeAccount", back_populates="position_cycles")

    def __repr__(self):
        return f"<PositionCycle {self.symbol} {self.status} from {self.open_time}>"
