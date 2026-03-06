"""Redis 缓存管理"""
import json
from typing import Optional, Any
import redis
from app.core.config import settings


class RedisClient:
    """Redis 客户端封装"""

    _instance: Optional[redis.Redis] = None

    @classmethod
    def get_instance(cls) -> redis.Redis:
        """获取 Redis 单例实例"""
        if cls._instance is None:
            cls._instance = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return cls._instance

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            client = cls.get_instance()
            value = client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300) -> bool:
        """设置缓存值"""
        try:
            client = cls.get_instance()
            serialized = json.dumps(value)
            client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    @classmethod
    def delete(cls, key: str) -> bool:
        """删除缓存"""
        try:
            client = cls.get_instance()
            client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    @classmethod
    def exists(cls, key: str) -> bool:
        """检查键是否存在"""
        try:
            client = cls.get_instance()
            return bool(client.exists(key))
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False


# 缓存键生成器
class CacheKeys:
    """缓存键命名规范"""

    @staticmethod
    def kline_data(symbol: str, timeframe: str, exchange: str = "binance") -> str:
        """K线数据缓存键"""
        return f"kline:{exchange}:{symbol}:{timeframe}"

    @staticmethod
    def market_price(symbol: str, exchange: str = "binance") -> str:
        """市场价格缓存键"""
        return f"price:{exchange}:{symbol}"

    @staticmethod
    def user_position(account_id: str) -> str:
        """用户持仓缓存键"""
        return f"position:{account_id}"
