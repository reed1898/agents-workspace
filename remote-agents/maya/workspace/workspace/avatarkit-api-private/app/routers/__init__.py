"""
AvatarKit 路由
"""
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.avatar import router as avatar_router
from app.routers.generate import router as generate_router
from app.routers.billing import router as billing_router

__all__ = [
    "auth_router",
    "user_router",
    "avatar_router",
    "generate_router",
    "billing_router",
]
