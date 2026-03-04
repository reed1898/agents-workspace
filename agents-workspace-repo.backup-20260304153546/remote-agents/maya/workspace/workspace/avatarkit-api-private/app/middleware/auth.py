"""
API Key 认证中间件
"""
import uuid
from typing import Optional

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.redis_cache import get_cached_user_id_by_api_key, cache_api_key_user

# 用于文档的 Bearer Token 安全方案
security = HTTPBearer(auto_error=False)


class AuthenticationError(HTTPException):
    """认证错误"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


async def extract_api_key(request: Request) -> Optional[str]:
    """
    从请求中提取 API Key
    支持以下方式：
    1. Header: X-API-Key
    2. Header: Authorization: Bearer xxx
    3. Query: ?api_key=xxx
    """
    # 1. 尝试从 X-API-Key header 获取
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return api_key
    
    # 2. 尝试从 Authorization header 获取
    auth_header = request.headers.get("Authorization")
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
    
    # 3. 尝试从 query 参数获取（不推荐用于生产环境）
    api_key = request.query_params.get("api_key")
    if api_key:
        return api_key
    
    return None


async def get_user_by_api_key(api_key: str, db: AsyncSession) -> Optional[User]:
    """
    通过 API Key 获取用户
    先查缓存，再查数据库
    """
    if not api_key:
        return None
    
    # 1. 检查缓存
    cached_user_id = await get_cached_user_id_by_api_key(api_key)
    if cached_user_id:
        # 从数据库获取完整用户信息
        result = await db.execute(
            select(User).where(User.id == uuid.UUID(cached_user_id))
        )
        user = result.scalar_one_or_none()
        if user and user.is_active:
            return user
    
    # 2. 查询数据库
    result = await db.execute(
        select(User).where(User.api_key == api_key)
    )
    user = result.scalar_one_or_none()
    
    if user and user.is_active:
        # 缓存用户 ID
        await cache_api_key_user(api_key, str(user.id))
        return user
    
    return None


async def verify_api_key(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    验证 API Key 并返回用户
    
    用法:
        @router.get("/protected")
        async def protected_endpoint(current_user: User = Depends(verify_api_key)):
            return {"user_id": current_user.id}
    """
    api_key = await extract_api_key(request)
    
    if not api_key:
        raise AuthenticationError("Missing API Key. Provide it via X-API-Key header or Authorization: Bearer token")
    
    user = await get_user_by_api_key(api_key, db)
    
    if not user:
        raise AuthenticationError("Invalid API Key")
    
    if not user.is_active:
        raise AuthenticationError("Account is deactivated")
    
    # 将用户信息存入请求状态，供后续使用
    request.state.user = user
    request.state.user_id = user.id
    
    return user


async def verify_api_key_optional(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    可选的 API Key 验证
    如果没有提供 API Key，返回 None
    """
    try:
        return await verify_api_key(request, db)
    except AuthenticationError:
        return None


async def get_current_user_id(request: Request) -> uuid.UUID:
    """
    从请求状态获取当前用户 ID
    需要先使用 verify_api_key
    """
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise AuthenticationError("User not authenticated")
    return user_id


class RateLimitMiddleware:
    """
    限流中间件
    基于 Redis 的滑动窗口限流
    """
    
    def __init__(self, default_limit: int = 100, default_window: int = 60):
        self.default_limit = default_limit
        self.default_window = default_window
    
    async def __call__(self, request: Request, call_next):
        from app.redis_cache import check_rate_limit
        from app.config import settings
        
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # 获取限流键
        client_ip = request.client.host if request.client else "unknown"
        
        # 尝试获取用户 ID
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            rate_key = f"rate:user:{user_id}"
        else:
            rate_key = f"rate:ip:{client_ip}"
        
        # 根据路径调整限流策略
        path = request.url.path
        if "/generate" in path:
            limit, window = 10, 60  # 生成接口更严格
        else:
            limit, window = self.default_limit, self.default_window
        
        # 检查限流
        allowed, remaining = await check_rate_limit(rate_key, limit, window)
        
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(window)}
            )
        
        # 执行请求
        response = await call_next(request)
        
        # 添加限流响应头
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
