"""
用户模型 - 核心认证和计费
"""
import uuid
import secrets
import hashlib
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, DateTime, Numeric, Integer, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from app.database import Base


def generate_api_key() -> str:
    """生成安全的 API Key"""
    return f"ak_{secrets.token_urlsafe(32)}"


def hash_api_secret(secret: str, salt: str) -> str:
    """哈希 API Secret"""
    return hashlib.sha256(f"{secret}{salt}".encode()).hexdigest()


class User(Base):
    """
    用户表
    存储用户基本信息、API 认证凭证和账户余额
    """
    __tablename__ = "users"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 基本信息
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # bcrypt 哈希
    
    # API 认证
    api_key = Column(String(100), unique=True, nullable=False, index=True)
    api_secret_hash = Column(String(255), nullable=False)  # 存储哈希值
    
    # 账户信息
    balance = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)  # 余额（元）
    free_credits_used = Column(Integer, default=0, nullable=False)  # 本月已用免费额度
    
    # 套餐信息
    plan = Column(String(20), default="free", nullable=False)  # free/lite/pro
    plan_expires_at = Column(DateTime, nullable=True)  # 套餐过期时间
    
    # 用户状态
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)  # 邮箱验证状态
    
    # 配额限制（每月重置）
    monthly_images_used = Column(Integer, default=0, nullable=False)
    monthly_voice_used = Column(Integer, default=0, nullable=False)
    monthly_video_used = Column(Integer, default=0, nullable=False)
    quota_reset_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 元数据
    full_name = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # 复合索引
    __table_args__ = (
        Index('ix_users_plan_active', 'plan', 'is_active'),
    )
    
    @validates('email')
    def validate_email(self, key, email):
        """验证邮箱格式"""
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        return email.lower().strip()
    
    @validates('plan')
    def validate_plan(self, key, plan):
        """验证套餐类型"""
        allowed = ['free', 'lite', 'pro']
        if plan not in allowed:
            raise ValueError(f"Plan must be one of {allowed}")
        return plan
    
    @property
    def has_free_credits(self) -> bool:
        """检查是否还有免费额度"""
        from app.config import settings
        return self.free_credits_used < settings.FREE_TIER_IMAGES
    
    @property
    def free_credits_remaining(self) -> int:
        """剩余免费额度"""
        from app.config import settings
        remaining = settings.FREE_TIER_IMAGES - self.free_credits_used
        return max(0, remaining)
    
    def can_afford(self, amount: Decimal) -> bool:
        """检查余额是否足够"""
        return self.balance >= amount
    
    def deduct_balance(self, amount: Decimal) -> bool:
        """
        扣除余额
        返回是否成功扣除（余额不足返回 False）
        """
        if not self.can_afford(amount):
            return False
        self.balance -= amount
        return True
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, plan={self.plan})>"


class APIKeyHistory(Base):
    """
    API Key 历史记录
    用于审计和安全追踪
    """
    __tablename__ = "api_key_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action = Column(String(20), nullable=False)  # created / rotated / revoked
    api_key_prefix = Column(String(20), nullable=False)  # 存储前缀用于识别
    ip_address = Column(String(45), nullable=True)  # IPv6 支持
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index('ix_api_key_history_user_created', 'user_id', 'created_at'),
    )
