"""
认证路由 - 注册、登录、API Key 管理
"""
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.user import User, APIKeyHistory, generate_api_key, hash_api_secret
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshKeyResponse,
    ErrorResponse,
)
from app.redis_cache import invalidate_api_key_cache

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def hash_password(password: str) -> str:
    """哈希密码"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: uuid.UUID, expires_delta: timedelta = None) -> str:
    """创建 JWT Token"""
    if expires_delta is None:
        expires_delta = timedelta(hours=settings.JWT_EXPIRE_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """通过邮箱获取用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered"},
    }
)
async def register(request: Request, data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    
    - 创建新用户账户
    - 生成 API Key 和 Secret
    - 返回登录 Token
    """
    # 检查邮箱是否已注册
    existing = await get_user_by_email(data.email, db)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 生成 API 凭证
    api_key = generate_api_key()
    api_secret = secrets.token_urlsafe(32)
    api_secret_hash = hash_api_secret(api_secret, settings.API_KEY_SALT)
    
    # 创建用户
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        api_key=api_key,
        api_secret_hash=api_secret_hash,
        full_name=data.full_name,
    )
    
    db.add(user)
    await db.flush()
    
    # 记录 API Key 创建
    history = APIKeyHistory(
        user_id=user.id,
        action="created",
        api_key_prefix=api_key[:12],
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )
    db.add(history)
    
    # 创建 Token
    access_token = create_access_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRE_HOURS * 3600,
        api_key=api_key,
        api_secret=api_secret,  # 仅在注册时返回一次
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    }
)
async def login(request: Request, data: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录
    
    - 验证邮箱和密码
    - 更新最后登录时间
    - 返回登录 Token
    """
    # 查找用户
    user = await get_user_by_email(data.email, db)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    
    # 创建 Token
    access_token = create_access_token(user.id)
    
    # 注意：登录时不返回 API Secret
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRE_HOURS * 3600,
        api_key=user.api_key,
        api_secret="***",  # 登录不返回 secret
    )


@router.post(
    "/refresh-key",
    response_model=RefreshKeyResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication required"},
    }
)
async def refresh_api_key(
    request: Request,
    credentials: HTTPBearer = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    刷新 API Key
    
    - 需要 Bearer Token 认证
    - 生成新的 API Key 和 Secret
    - 旧 API Key 立即失效
    """
    # 验证 JWT Token
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = uuid.UUID(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # 获取用户
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # 使旧 API Key 缓存失效
    await invalidate_api_key_cache(user.api_key)
    
    # 生成新的 API 凭证
    old_key_prefix = user.api_key[:12]
    user.api_key = generate_api_key()
    new_secret = secrets.token_urlsafe(32)
    user.api_secret_hash = hash_api_secret(new_secret, settings.API_KEY_SALT)
    
    # 记录刷新历史
    history = APIKeyHistory(
        user_id=user.id,
        action="rotated",
        api_key_prefix=old_key_prefix,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )
    db.add(history)
    
    return RefreshKeyResponse(
        api_key=user.api_key,
        api_secret=new_secret,
    )
