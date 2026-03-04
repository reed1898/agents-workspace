"""
计费中间件
调用前检查余额，调用后扣费
"""
import json
import uuid
from decimal import Decimal
from typing import Optional, Callable
from functools import wraps

from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Pricing
from app.models.user import User
from app.models.usage import UsageLog
from app.redis_cache import get_cached_user_quota, cache_user_quota, invalidate_user_quota_cache


class BillingError(HTTPException):
    """计费错误"""
    def __init__(self, detail: str = "Billing error"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )


class InsufficientBalanceError(HTTPException):
    """余额不足错误"""
    def __init__(self, balance: Decimal, required: Decimal):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient balance. Current: ¥{balance}, Required: ¥{required}",
        )


async def check_user_balance(
    user: User,
    service_type: str,
    db: AsyncSession
) -> tuple[bool, Decimal, bool]:
    """
    检查用户是否有足够余额或免费额度
    
    Args:
        user: 用户对象
        service_type: 服务类型（image/voice/video）
        db: 数据库会话
        
    Returns:
        (是否允许, 实际费用, 是否使用免费额度)
    """
    price = Decimal(str(Pricing.get_price(service_type)))
    
    # 检查是否有免费额度
    if service_type == "image" and user.has_free_credits:
        return True, Decimal("0.00"), True
    
    # 检查余额
    if user.can_afford(price):
        return True, price, False
    
    return False, price, False


async def deduct_usage(
    user: User,
    service_type: str,
    cost: Decimal,
    used_free_credit: bool,
    db: AsyncSession,
    avatar_id: Optional[uuid.UUID] = None,
    request_id: Optional[str] = None,
    request_params: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status_code: str = "success",
    error_message: Optional[str] = None
) -> UsageLog:
    """
    扣除用户使用费用并记录
    
    Args:
        user: 用户对象
        service_type: 服务类型
        cost: 费用
        used_free_credit: 是否使用免费额度
        db: 数据库会话
        avatar_id: 形象 ID
        request_id: 请求 ID
        request_params: 请求参数
        ip_address: IP 地址
        user_agent: User Agent
        status_code: 状态（success/failed/refunded）
        error_message: 错误信息
        
    Returns:
        使用记录对象
    """
    balance_before = user.balance
    
    # 更新用户数据
    if used_free_credit:
        user.free_credits_used += 1
    else:
        success = user.deduct_balance(cost)
        if not success:
            raise BillingError("Failed to deduct balance")
    
    # 更新月度使用统计
    if service_type == "image":
        user.monthly_images_used += 1
    elif service_type == "voice":
        user.monthly_voice_used += 1
    elif service_type == "video":
        user.monthly_video_used += 1
    
    # 刷新缓存
    await invalidate_user_quota_cache(str(user.id))
    
    # 创建使用记录
    usage_log = UsageLog(
        user_id=user.id,
        avatar_id=avatar_id,
        service_type=service_type,
        api_endpoint="",  # 由调用方填充
        cost=cost,
        credits_used=1 if used_free_credit else 0,
        balance_before=balance_before,
        balance_after=user.balance,
        status=status_code,
        error_message=error_message,
        request_id=request_id,
        request_params=json.dumps(request_params) if request_params else None,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    db.add(usage_log)
    await db.flush()
    
    return usage_log


async def get_user_quota_info(user: User) -> dict:
    """
    获取用户配额信息
    优先从缓存获取
    """
    # 尝试从缓存获取
    cached = await get_cached_user_quota(str(user.id))
    if cached:
        return cached
    
    from app.config import settings, UserPlans
    
    # 计算配额
    limits = UserPlans.get_limits(user.plan)
    
    quota = {
        "plan": user.plan,
        "balance": float(user.balance),
        "free_credits_used": user.free_credits_used,
        "free_credits_total": settings.FREE_TIER_IMAGES,
        "free_credits_remaining": user.free_credits_remaining,
        "monthly_images_used": user.monthly_images_used,
        "monthly_images_limit": limits["monthly_images"],
        "monthly_voice_used": user.monthly_voice_used,
        "monthly_voice_limit": limits["monthly_voice"],
        "monthly_video_used": user.monthly_video_used,
        "monthly_video_limit": limits["monthly_video"],
    }
    
    # 缓存配额信息
    await cache_user_quota(str(user.id), quota)
    
    return quota


def require_billing(service_type: str):
    """
    计费装饰器
    自动检查余额和扣费
    
    用法:
        @router.post("/generate")
        @require_billing("image")
        async def generate(request: Request, ...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 提取请求和数据库会话
            request: Optional[Request] = None
            db: Optional[AsyncSession] = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                elif isinstance(arg, AsyncSession):
                    db = arg
            
            request = request or kwargs.get("request")
            db = db or kwargs.get("db")
            
            if not request or not db:
                raise BillingError("Missing request or db session")
            
            # 获取用户
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # 检查余额
            allowed, cost, use_free = await check_user_balance(user, service_type, db)
            if not allowed:
                raise InsufficientBalanceError(user.balance, cost)
            
            # 记录扣费前的信息
            balance_before = user.balance
            
            try:
                # 执行原函数
                result = await func(*args, **kwargs)
                
                # 扣费（成功时）
                await deduct_usage(
                    user=user,
                    service_type=service_type,
                    cost=cost,
                    used_free_credit=use_free,
                    db=db,
                    request_id=getattr(request.state, "request_id", None),
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("User-Agent"),
                )
                
                return result
                
            except Exception as e:
                # 失败时不扣费，但记录失败
                await deduct_usage(
                    user=user,
                    service_type=service_type,
                    cost=Decimal("0.00"),
                    used_free_credit=False,
                    db=db,
                    request_id=getattr(request.state, "request_id", None),
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("User-Agent"),
                    status_code="failed",
                    error_message=str(e),
                )
                raise
        
        return wrapper
    return decorator
