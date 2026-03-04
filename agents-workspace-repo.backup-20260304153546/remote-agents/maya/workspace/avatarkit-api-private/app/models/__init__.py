"""
AvatarKit 数据库模型
"""
from app.database import Base

# 导入所有模型以便 Alembic 迁移使用
from app.models.user import User, APIKeyHistory
from app.models.avatar import Avatar, AvatarGeneration, VoiceGeneration
from app.models.usage import UsageLog, MonthlyUsage
from app.models.order import Order, Transaction, PricingPackage

__all__ = [
    "Base",
    "User",
    "APIKeyHistory",
    "Avatar",
    "AvatarGeneration",
    "VoiceGeneration",
    "UsageLog",
    "MonthlyUsage",
    "Order",
    "Transaction",
    "PricingPackage",
]
