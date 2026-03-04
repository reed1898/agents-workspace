"""
AvatarKit API - SaaS Configuration
生产环境配置管理，所有敏感信息通过环境变量传入
"""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    AvatarKit SaaS 配置类
    所有敏感配置通过环境变量传入，支持 .env 文件
    """
    
    # ==================== 应用配置 ====================
    APP_NAME: str = "AvatarKit API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "production"  # development / staging / production
    
    # ==================== 数据库配置 ====================
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/avatarkit"
    DATABASE_PUBLIC_URL: Optional[str] = None  # Railway 外部连接 URL
    # 数据库连接池配置
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    @property
    def db_url(self) -> str:
        """获取数据库连接URL，优先使用 DATABASE_PUBLIC_URL（Railway）"""
        if self.DATABASE_PUBLIC_URL:
            # Railway 的 URL 需要转换成 asyncpg 格式
            return self.DATABASE_PUBLIC_URL.replace("postgresql://", "postgresql+asyncpg://")
        return self.DATABASE_URL
    
    # ==================== Redis 配置 ====================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    
    # ==================== 安全配置 ====================
    # JWT 密钥（用于用户登录 Token）
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    
    # API Key 加密密钥
    API_KEY_SALT: str = "your-api-key-salt-change-in-production"
    
    # ==================== 外部 API 密钥 ====================
    FAL_KEY: str = ""  # FAL AI 图片生成
    ELEVENLABS_API_KEY: str = ""  # ElevenLabs 语音合成
    
    # ==================== 存储配置 ====================
    # R2 / S3 兼容存储
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "avatarkit"
    R2_ENDPOINT_URL: Optional[str] = None  # 自定义端点（如 MinIO）
    
    # 本地存储路径（开发和回退用）
    LOCAL_STORAGE_PATH: str = "./storage"
    STORAGE_PUBLIC_URL: str = ""  # 存储文件的公开访问 URL 前缀
    
    # ==================== 支付配置 ====================
    # 支付宝
    ALIPAY_APP_ID: str = ""
    ALIPAY_PRIVATE_KEY: str = ""  # 应用私钥
    ALIPAY_PUBLIC_KEY: str = ""   # 支付宝公钥
    ALIPAY_GATEWAY: str = "https://openapi.alipay.com/gateway.do"
    
    # 微信支付
    WECHAT_APP_ID: str = ""
    WECHAT_MCH_ID: str = ""  # 商户号
    WECHAT_API_KEY: str = ""  # API 密钥
    WECHAT_NOTIFY_URL: str = ""  # 支付回调 URL
    
    # ==================== 计费配置 ====================
    # 价格配置（元）
    PRICE_IMAGE: float = 0.2      # 图片生成
    PRICE_VOICE: float = 0.1      # 语音合成
    PRICE_VIDEO: float = 2.0      # 视频生成
    
    # 免费额度
    FREE_TIER_IMAGES: int = 10    # 每月免费图片数量
    
    # ==================== 限流配置 ====================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "100/minute"  # 默认限流
    RATE_LIMIT_GENERATE: str = "10/minute"  # 生成接口限流
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = Settings()


# 计费配置常量
class Pricing:
    """计费常量"""
    IMAGE = settings.PRICE_IMAGE
    VOICE = settings.PRICE_VOICE
    VIDEO = settings.PRICE_VIDEO
    
    @classmethod
    def get_price(cls, service_type: str) -> float:
        """获取服务价格"""
        prices = {
            "image": cls.IMAGE,
            "voice": cls.VOICE,
            "video": cls.VIDEO,
        }
        return prices.get(service_type, 0.0)


# 用户套餐配置
class UserPlans:
    """用户套餐配置"""
    FREE = "free"
    LITE = "lite"
    PRO = "pro"
    
    LIMITS = {
        FREE: {
            "monthly_images": 10,
            "monthly_voice": 5,
            "monthly_video": 0,
            "storage_gb": 1,
        },
        LITE: {
            "monthly_images": 100,
            "monthly_voice": 50,
            "monthly_video": 5,
            "storage_gb": 5,
        },
        PRO: {
            "monthly_images": 1000,
            "monthly_voice": 500,
            "monthly_video": 50,
            "storage_gb": 20,
        },
    }
    
    @classmethod
    def get_limits(cls, plan: str) -> dict:
        """获取套餐限制"""
        return cls.LIMITS.get(plan, cls.LIMITS[cls.FREE])
