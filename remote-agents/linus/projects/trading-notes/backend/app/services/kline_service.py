"""K线数据获取服务"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import ccxt
from sqlalchemy.orm import Session
from ..core.redis import RedisClient, CacheKeys


class KlineService:
    """K线数据获取服务"""

    # 时间框架映射
    TIMEFRAME_MAP = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d",
        "1w": "1w"
    }

    @staticmethod
    def get_exchange_instance(exchange_name: str, api_key: Optional[str] = None, secret: Optional[str] = None):
        """获取交易所实例"""
        exchange_class = getattr(ccxt, exchange_name.lower(), None)
        if not exchange_class:
            raise ValueError(f"Unsupported exchange: {exchange_name}")

        config = {
            'enableRateLimit': True,
        }

        if api_key and secret:
            config['apiKey'] = api_key
            config['secret'] = secret

        return exchange_class(config)

    @staticmethod
    async def fetch_klines(
        symbol: str,
        timeframe: str = "1h",
        exchange: str = "binance",
        limit: int = 500,
        since: Optional[datetime] = None,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        获取K线数据 (支持缓存)

        Args:
            symbol: 交易对符号 (如 BTC/USDT)
            timeframe: 时间框架 (1m, 5m, 15m, 1h, 4h, 1d, 1w)
            exchange: 交易所名称 (默认 binance)
            limit: 获取的K线数量 (最大500)
            since: 起始时间 (可选)
            use_cache: 是否使用缓存 (默认 True)

        Returns:
            K线数据列表
        """
        try:
            # 如果没有指定 since，尝试从缓存获取
            if use_cache and not since:
                cache_key = CacheKeys.kline_data(symbol, timeframe, exchange)
                cached_data = RedisClient.get(cache_key)
                if cached_data:
                    return cached_data

            # 获取交易所实例
            exchange_instance = KlineService.get_exchange_instance(exchange)

            # 验证时间框架
            if timeframe not in KlineService.TIMEFRAME_MAP:
                raise ValueError(f"Invalid timeframe: {timeframe}")

            # 获取K线数据
            since_timestamp = int(since.timestamp() * 1000) if since else None
            ohlcv = exchange_instance.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=since_timestamp,
                limit=min(limit, 500)  # 限制最大数量
            )

            # 转换为标准格式
            klines = []
            for candle in ohlcv:
                klines.append({
                    "time": candle[0] / 1000,  # 转换为秒
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5])
                })

            # 缓存结果 (5分钟TTL)
            if use_cache and not since:
                cache_key = CacheKeys.kline_data(symbol, timeframe, exchange)
                RedisClient.set(cache_key, klines, ttl=300)

            return klines

        except Exception as e:
            raise Exception(f"Failed to fetch klines: {str(e)}")

    @staticmethod
    async def get_klines_for_trade(
        symbol: str,
        trade_time: datetime,
        timeframe: str = "1h",
        exchange: str = "binance",
        bars_before: int = 100,
        bars_after: int = 20
    ) -> Dict[str, Any]:
        """
        获取交易时点前后的K线数据

        Args:
            symbol: 交易对符号
            trade_time: 交易时间
            timeframe: 时间框架
            exchange: 交易所名称
            bars_before: 交易前的K线数量
            bars_after: 交易后的K线数量

        Returns:
            包含K线数据和交易标记的字典
        """
        try:
            # 计算需要获取的总数量
            total_limit = bars_before + bars_after

            # 计算时间框架对应的分钟数
            timeframe_minutes = KlineService._timeframe_to_minutes(timeframe)

            # 计算起始时间 (交易时间前 bars_before 个时间周期)
            since = trade_time - timedelta(minutes=timeframe_minutes * bars_before)

            # 获取K线数据
            klines = await KlineService.fetch_klines(
                symbol=symbol,
                timeframe=timeframe,
                exchange=exchange,
                limit=total_limit,
                since=since
            )

            # 找到最接近交易时间的K线索引
            trade_timestamp = trade_time.timestamp()
            trade_index = None
            min_diff = float('inf')

            for i, kline in enumerate(klines):
                diff = abs(kline['time'] - trade_timestamp)
                if diff < min_diff:
                    min_diff = diff
                    trade_index = i

            return {
                "klines": klines,
                "trade_index": trade_index,
                "trade_timestamp": trade_timestamp,
                "symbol": symbol,
                "timeframe": timeframe
            }

        except Exception as e:
            raise Exception(f"Failed to get klines for trade: {str(e)}")

    @staticmethod
    def _timeframe_to_minutes(timeframe: str) -> int:
        """将时间框架转换为分钟数"""
        timeframe_map = {
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "1h": 60,
            "4h": 240,
            "1d": 1440,
            "1w": 10080
        }
        return timeframe_map.get(timeframe, 60)
