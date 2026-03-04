"""
Pydantic Schemas - 数据验证和序列化
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Literal

from pydantic import BaseModel, Field, EmailStr, ConfigDict


# ==================== 通用响应 ====================

class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str
    code: Optional[str] = None


class PaginatedResponse(BaseModel):
    """分页响应基类"""
    total: int
    page: int = 1
    page_size: int = 20
    pages: int


# ==================== 认证相关 ====================

class UserRegisterRequest(BaseModel):
    """用户注册请求"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)


class UserLoginRequest(BaseModel):
    """用户登录请求"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """登录 Token 响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    api_key: str  # 用户的 API Key
    api_secret: str  # 用户的 API Secret（仅注册/刷新时返回）


class RefreshKeyResponse(BaseModel):
    """刷新 API Key 响应"""
    api_key: str
    api_secret: str
    message: str = "API Key refreshed successfully"


# ==================== 用户信息 ====================

class UserProfile(BaseModel):
    """用户资料"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    email: str
    full_name: Optional[str]
    company: Optional[str]
    plan: str
    is_verified: bool
    created_at: datetime


class UserBalance(BaseModel):
    """用户余额"""
    balance: Decimal = Field(..., decimal_places=2)
    currency: str = "CNY"
    free_credits_remaining: int
    free_credits_total: int
    monthly_images_used: int
    monthly_images_limit: int
    monthly_voice_used: int
    monthly_voice_limit: int


class UserPlanLimits(BaseModel):
    """用户套餐限制"""
    plan: str
    limits: dict


# ==================== 使用记录 ====================

class UsageRecord(BaseModel):
    """使用记录"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    service_type: str
    cost: Decimal
    status: str
    created_at: datetime


class UsageHistoryResponse(PaginatedResponse):
    """使用记录列表"""
    items: List[UsageRecord]


class MonthlyStats(BaseModel):
    """月度统计"""
    year: int
    month: int
    image_count: int
    voice_count: int
    video_count: int
    total_cost: Decimal


# ==================== 形象管理 ====================

class AvatarCreate(BaseModel):
    """创建形象请求"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    style: Optional[str] = Field(None, max_length=50)
    style_prompt: Optional[str] = None
    voice_id: Optional[str] = Field(None, max_length=100)


class AvatarUpdate(BaseModel):
    """更新形象请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    style: Optional[str] = Field(None, max_length=50)
    style_prompt: Optional[str] = None
    voice_id: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class AvatarResponse(BaseModel):
    """形象响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    description: Optional[str]
    reference_image_url: Optional[str]
    style: Optional[str]
    voice_id: Optional[str]
    is_active: bool
    total_generations: int
    created_at: datetime
    updated_at: datetime


class AvatarListResponse(PaginatedResponse):
    """形象列表响应"""
    items: List[AvatarResponse]


# ==================== 生成请求 ====================

class GenerateImageRequest(BaseModel):
    """生成图片请求"""
    prompt: str = Field(..., min_length=1, max_length=2000)
    style: Optional[str] = Field(None, max_length=50)
    negative_prompt: Optional[str] = None
    width: Optional[int] = Field(None, ge=512, le=2048)
    height: Optional[int] = Field(None, ge=512, le=2048)


class GenerateImageResponse(BaseModel):
    """生成图片响应"""
    generation_id: uuid.UUID
    image_url: str
    cost: Decimal
    used_free_credit: bool


class GenerateVoiceRequest(BaseModel):
    """生成语音请求"""
    text: str = Field(..., min_length=1, max_length=5000)
    emotion: Optional[str] = Field(None, max_length=50)
    voice_id: Optional[str] = None  # 覆盖 avatar 的默认 voice_id


class GenerateVoiceResponse(BaseModel):
    """生成语音响应"""
    generation_id: uuid.UUID
    audio_url: str
    duration_seconds: float
    cost: Decimal
    used_free_credit: bool


# ==================== 订单和支付 ====================

class CreateOrderRequest(BaseModel):
    """创建订单请求"""
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    payment_method: Literal["alipay", "wechat"]
    description: Optional[str] = None


class OrderResponse(BaseModel):
    """订单响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    order_no: str
    amount: Decimal
    payment_method: str
    payment_status: str
    created_at: datetime
    expires_at: datetime
    checkout_url: Optional[str] = None  # 支付跳转 URL


class OrderListResponse(PaginatedResponse):
    """订单列表响应"""
    items: List[OrderResponse]


class PricingPackageResponse(BaseModel):
    """充值套餐响应"""
    id: uuid.UUID
    name: str
    description: Optional[str]
    amount: Decimal
    credits: int
    bonus_credits: int


# ==================== 健康检查 ====================

class HealthCheck(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    timestamp: datetime
    services: dict
