"""
AvatarKit 中间件
"""
from app.middleware.auth import (
    verify_api_key,
    verify_api_key_optional,
    get_current_user_id,
    AuthenticationError,
    RateLimitMiddleware,
)
from app.middleware.billing import (
    require_billing,
    check_user_balance,
    deduct_usage,
    get_user_quota_info,
    BillingError,
    InsufficientBalanceError,
)

__all__ = [
    # 认证
    "verify_api_key",
    "verify_api_key_optional",
    "get_current_user_id",
    "AuthenticationError",
    "RateLimitMiddleware",
    # 计费
    "require_billing",
    "check_user_balance",
    "deduct_usage",
    "get_user_quota_info",
    "BillingError",
    "InsufficientBalanceError",
]
