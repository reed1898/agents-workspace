"""
Redis 缓存和限流管理
"""
import json
from typing import Optional, Any

import redis.asyncio as redis

from app.config import settings


class RedisManager:
    """Redis 连接管理器"""
    
    _instance = None
    _redis: Optional[redis.Redis] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        """建立 Redis 连接"""
        if self._redis is None:
            kwargs = {"decode_responses": True}
            if settings.REDIS_PASSWORD:
                kwargs["password"] = settings.REDIS_PASSWORD
            self._redis = await redis.from_url(settings.REDIS_URL, **kwargs)
        return self._redis
    
    async def disconnect(self):
        """关闭 Redis 连接"""
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    @property
    def client(self) -> redis.Redis:
        """获取 Redis 客户端"""
        if self._redis is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._redis


# 全局 Redis 管理器实例
redis_manager = RedisManager()


# ==================== API Key 缓存 ====================

async def cache_api_key_user(api_key: str, user_id: str, ttl: int = 3600):
    """
    缓存 API Key 到用户的映射
    
    Args:
        api_key: API Key
        user_id: 用户 ID
        ttl: 缓存时间（秒）
    """
    r = redis_manager.client
    key = f"apikey:{api_key}"
    await r.setex(key, ttl, user_id)


async def get_cached_user_id_by_api_key(api_key: str) -> Optional[str]:
    """
    从缓存获取 API Key 对应的用户 ID
    
    Args:
        api_key: API Key
        
    Returns:
        用户 ID 或 None
    """
    r = redis_manager.client
    key = f"apikey:{api_key}"
    return await r.get(key)


async def invalidate_api_key_cache(api_key: str):
    """使 API Key 缓存失效"""
    r = redis_manager.client
    key = f"apikey:{api_key}"
    await r.delete(key)


# ==================== 限流管理 ====================

async def check_rate_limit(key: str, limit: int, window: int) -> tuple[bool, int]:
    """
    检查限流
    
    Args:
        key: 限流键（如："rate:apikey:xxx"）
        limit: 限制次数
        window: 时间窗口（秒）
        
    Returns:
        (是否允许, 剩余次数)
    """
    r = redis_manager.client
    
    # 使用 Redis 计数器实现滑动窗口限流
    current = await r.get(key)
    if current is None:
        # 第一次请求
        await r.setex(key, window, 1)
        return True, limit - 1
    
    current_count = int(current)
    if current_count >= limit:
        # 超过限制
        ttl = await r.ttl(key)
        return False, 0
    
    # 增加计数
    await r.incr(key)
    return True, limit - current_count - 1


async def get_rate_limit_status(key: str, limit: int, window: int) -> dict:
    """
    获取限流状态
    
    Returns:
        {
            "limit": 限制次数,
            "remaining": 剩余次数,
            "reset": 重置时间戳,
            "window": 时间窗口
        }
    """
    r = redis_manager.client
    current = await r.get(key)
    ttl = await r.ttl(key)
    
    if current is None:
        remaining = limit
        reset_at = 0
    else:
        remaining = max(0, limit - int(current))
        reset_at = ttl if ttl > 0 else window
    
    return {
        "limit": limit,
        "remaining": remaining,
        "reset": reset_at,
        "window": window
    }


# ==================== 用户配额缓存 ====================

async def cache_user_quota(user_id: str, quota: dict, ttl: int = 300):
    """
    缓存用户配额信息
    
    Args:
        user_id: 用户 ID
        quota: 配额信息字典
        ttl: 缓存时间（秒）
    """
    r = redis_manager.client
    key = f"quota:{user_id}"
    await r.setex(key, ttl, json.dumps(quota))


async def get_cached_user_quota(user_id: str) -> Optional[dict]:
    """获取缓存的用户配额"""
    r = redis_manager.client
    key = f"quota:{user_id}"
    data = await r.get(key)
    if data:
        return json.loads(data)
    return None


async def invalidate_user_quota_cache(user_id: str):
    """使用户配额缓存失效"""
    r = redis_manager.client
    key = f"quota:{user_id}"
    await r.delete(key)


# ==================== 健康检查 ====================

async def check_redis_connection() -> bool:
    """检查 Redis 连接状态"""
    try:
        r = redis_manager.client
        await r.ping()
        return True
    except Exception:
        return False
