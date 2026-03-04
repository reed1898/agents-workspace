"""
订单模型 - 充值和支付
"""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, DateTime, Numeric, Integer, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Order(Base):
    """
    充值订单表
    记录用户的充值订单和支付状态
    """
    __tablename__ = "orders"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 订单号（对外显示）
    order_no = Column(String(64), unique=True, nullable=False, index=True)
    
    # 关联用户
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 支付信息
    payment_method = Column(String(20), nullable=False)  # alipay / wechat
    payment_status = Column(String(20), default="pending", nullable=False)  # pending / paid / failed / refunded
    
    # 金额
    amount = Column(Numeric(10, 2), nullable=False)  # 支付金额（元）
    credits = Column(Integer, nullable=False)  # 获得积分（如有）
    
    # 第三方支付信息
    third_party_order_id = Column(String(128), nullable=True, index=True)  # 支付宝/微信订单号
    third_party_response = Column(Text, nullable=True)  # 支付回调原始数据
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)  # 订单过期时间
    
    # 元数据
    description = Column(String(255), default="Account recharge", nullable=True)
    client_ip = Column(String(45), nullable=True)
    
    # 退款信息
    refund_amount = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=True)
    refund_reason = Column(Text, nullable=True)
    refunded_at = Column(DateTime, nullable=True)
    
    # 索引
    __table_args__ = (
        Index('ix_orders_user_status', 'user_id', 'payment_status'),
        Index('ix_orders_created', 'created_at'),
    )
    
    @property
    def is_paid(self) -> bool:
        """检查订单是否已支付"""
        return self.payment_status == "paid"
    
    @property
    def is_expired(self) -> bool:
        """检查订单是否已过期"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_no={self.order_no}, status={self.payment_status})>"


class Transaction(Base):
    """
    交易流水表
    记录账户余额变动的详细流水
    """
    __tablename__ = "transactions"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 关联
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    usage_log_id = Column(UUID(as_uuid=True), ForeignKey("usage_logs.id", ondelete="SET NULL"), nullable=True)
    
    # 交易信息
    transaction_type = Column(String(20), nullable=False)  # recharge / deduction / refund / bonus
    
    # 金额（正数表示入账，负数表示出账）
    amount = Column(Numeric(10, 2), nullable=False)
    
    # 余额快照
    balance_before = Column(Numeric(10, 2), nullable=False)
    balance_after = Column(Numeric(10, 2), nullable=False)
    
    # 描述
    description = Column(String(255), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 索引
    __table_args__ = (
        Index('ix_transactions_user_created', 'user_id', 'created_at'),
        Index('ix_transactions_type', 'transaction_type'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"


class PricingPackage(Base):
    """
    充值套餐表
    配置可选的充值套餐（如：充100送10）
    """
    __tablename__ = "pricing_packages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 套餐信息
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # 金额配置
    amount = Column(Numeric(10, 2), nullable=False)  # 支付金额
    credits = Column(Integer, nullable=False)  # 获得积分/额度
    bonus_credits = Column(Integer, default=0, nullable=False)  # 赠送额度
    
    # 状态
    is_active = Column(True, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<PricingPackage(name={self.name}, amount={self.amount})>"
