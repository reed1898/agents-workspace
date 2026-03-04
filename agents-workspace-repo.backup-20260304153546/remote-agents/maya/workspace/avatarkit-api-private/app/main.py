"""
AvatarKit API - SaaS 版本入口
FastAPI 应用主文件
"""
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db, close_db, check_db_connection
from app.redis_cache import redis_manager, check_redis_connection
from app.routers import (
    auth_router,
    user_router,
    avatar_router,
    generate_router,
    billing_router,
)
from app.schemas import HealthCheck, ErrorResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    - 启动时初始化数据库和 Redis
    - 关闭时清理资源
    """
    # 启动
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 连接 Redis
    try:
        await redis_manager.connect()
        print("✅ Redis connected")
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e}")
    
    # 初始化数据库（开发环境自动创建表，生产环境使用 Alembic）
    if settings.ENV == "development":
        await init_db()
        print("✅ Database initialized")
    
    yield
    
    # 关闭
    print("🛑 Shutting down...")
    await close_db()
    await redis_manager.disconnect()
    print("✅ Cleanup complete")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    AvatarKit API - 多用户 Avatar 生成 SaaS 服务
    
    ## 认证方式
    所有 API 端点（除了注册/登录）需要 API Key 认证：
    - Header: `X-API-Key: your_api_key`
    - 或 Header: `Authorization: Bearer your_api_key`
    
    ## 功能
    - 🎨 图片生成：基于 Flux 模型生成 Avatar 图片
    - 🎤 语音合成：基于 ElevenLabs 的语音生成
    - 📹 视频生成：即将上线
    
    ## 计费
    - 图片生成：¥0.2/张（新用户每月 10 张免费）
    - 语音合成：¥0.1/次
    - 视频生成：¥2/个
    """,
    lifespan=lifespan,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 异常处理 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    # 生成请求追踪 ID
    request_id = str(uuid.uuid4())[:8]
    
    # 记录错误（生产环境应接入日志系统）
    print(f"[Error {request_id}] {request.method} {request.url}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "code": f"ERR_{request_id}",
            "message": str(exc) if settings.DEBUG else "Please contact support"
        }
    )


# ==================== 路由 ====================

# 认证路由
app.include_router(auth_router, prefix="/v1")

# 用户路由
app.include_router(user_router, prefix="/v1/user")

# 形象管理路由
app.include_router(avatar_router, prefix="/v1")

# 生成路由
app.include_router(generate_router, prefix="/v1")

# 计费路由
app.include_router(billing_router, prefix="/v1")


# ==================== 基础端点 ====================

@app.get("/", include_in_schema=False)
async def root():
    """根路径重定向到文档"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else None,
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    健康检查端点
    
    返回服务状态和各组件健康状况
    """
    services = {
        "database": await check_db_connection(),
        "redis": await check_redis_connection(),
    }
    
    all_healthy = all(services.values())
    
    return HealthCheck(
        status="healthy" if all_healthy else "degraded",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        services=services
    )


@app.get("/v1/pricing")
async def get_pricing():
    """
    获取服务定价信息
    """
    from app.config import Pricing, settings
    
    return {
        "currency": "CNY",
        "services": {
            "image": {
                "price": Pricing.IMAGE,
                "unit": "per_image",
                "description": "基于 Flux 模型生成图片"
            },
            "voice": {
                "price": Pricing.VOICE,
                "unit": "per_request",
                "description": "基于 ElevenLabs 语音合成"
            },
            "video": {
                "price": Pricing.VIDEO,
                "unit": "per_video",
                "description": "即将上线"
            }
        },
        "free_tier": {
            "monthly_images": settings.FREE_TIER_IMAGES,
            "description": "新用户每月免费额度"
        }
    }


# 导入 datetime 用于健康检查
from datetime import datetime


# ==================== 主入口 ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
