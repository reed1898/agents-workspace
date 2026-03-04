"""
使用记录模型 - 计费和审计
"""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, DateTime, Numeric, Integer, Text, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class UsageLog(Base):
    """
    使用记录表
    记录每次 API 调用的计费信息，用于审计和报表
    """
    __tablename__ = "usage_logs"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 关联
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.id", ondelete="SET NULL"), nullable=True)
    
    # 调用信息
    service_type = Column(String(20), nullable=False)  # image / voice / video / storage
    api_endpoint = Column(String(255), nullable=False)  # 调用的 API 端点
    
    # 计费信息
    cost = Column(Numeric(10, 2), nullable=False)  # 实际扣费金额
    credits_used = Column(Integer, default=0, nullable=False)  # 使用的免费额度
    balance_before = Column(Numeric(10, 2), nullable=False)  # 扣费前余额
    balance_after = Column(Numeric(10, 2), nullable=False)  # 扣费后余额
    
    # 状态
    status = Column(String(20), default="success", nullable=False)  # success / failed / refunded
    error_code = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # 请求详情（用于审计）
    request_id = Column(String(100), nullable=True, index=True)  # 请求追踪 ID
    request_params = Column(Text, nullable=True)  # 请求参数摘要（JSON）
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 索引
    __table_args__ = (
        Index('ix_usage_user_type_created', 'user_id', 'service_type', 'created_at'),
        Index('ix_usage_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<UsageLog(id={self.id}, user_id={self.user_id}, type={self.service_type}, cost={self.cost})>"


class MonthlyUsage(Base):
    """
    月度使用统计表
    按月聚合的使用统计，便于快速查询和报表
    """
    __tablename__ = "monthly_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 关联
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 统计周期
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    
    # 使用量统计
    image_count = Column(Integer, default=0, nullable=False)
    voice_count = Column(Integer, default=0, nullable=False)
    video_count = Column(Integer, default=0, nullable=False)
    
    # 计费统计
    total_cost = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    free_credits_used = Column(Integer, default=0, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 唯一约束
    __table_args__ = (
        Index('ix_monthly_usage_user_year_month', 'user_id', 'year', 'month', unique=True),
    )
    
    def __repr__(self):
        return f"<MonthlyUsage(user_id={self.user_id}, {self.year}-{self.month}, cost={self.total_cost})>"
