"""行情数据服务

支持获取多个市场的实时价格数据：
- 加密货币 (crypto): 通过 CoinGecko API
- 美股 (us_stock): 通过 Yahoo Finance
- A股 (a_stock): 通过 AKShare
- 港股 (hk_stock): 通过 Yahoo Finance
"""

import asyncio
import logging
import re
import time
from typing import Optional, Dict, List, Tuple
from decimal import Decimal
from datetime import datetime

import httpx
import yfinance as yf
import akshare as ak

from app.core.redis import RedisClient, CacheKeys
from app.models.position import Position

logger = logging.getLogger(__name__)

# 配置
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
BINANCE_SPOT_API_URL = "https://api.binance.com"
BINANCE_FUTURES_API_URL = "https://fapi.binance.com"
BINANCE_DELIVERY_API_URL = "https://dapi.binance.com"
CACHE_TTL = 2  # 实时价格缓存（秒）
A_STOCK_NAME_TTL = 86400  # 1天缓存
US_STOCK_NAME_TTL = 86400  # 1天缓存


class MarketDataService:
    """市场数据服务类"""

    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        # Yahoo Finance 限流保护
        self._yahoo_last_request = 0.0
        self._yahoo_min_interval = 0.35
        self._yahoo_rate_limit_until = 0.0
        self._yahoo_rate_limit_lock = asyncio.Lock()
        # CoinGecko 交易对映射 (币安交易对 -> CoinGecko ID)
        self.crypto_symbol_map = {
            "BTC": "bitcoin",
            "BTCUSDT": "bitcoin",
            "ETH": "ethereum",
            "ETHUSDT": "ethereum",
            "BNB": "binancecoin",
            "BNBUSDT": "binancecoin",
            "SOL": "solana",
            "SOLUSDT": "solana",
            "ADA": "cardano",
            "ADAUSDT": "cardano",
            "XRP": "ripple",
            "XRPUSDT": "ripple",
            "DOT": "polkadot",
            "DOTUSDT": "polkadot",
            "DOGE": "dogecoin",
            "DOGEUSDT": "dogecoin",
            "MATIC": "matic-network",
            "MATICUSDT": "matic-network",
            "AVAX": "avalanche-2",
            "AVAXUSDT": "avalanche-2",
            "LINK": "chainlink",
            "LINKUSDT": "chainlink",
            "UNI": "uniswap",
            "UNIUSDT": "uniswap",
            "LTC": "litecoin",
            "LTCUSDT": "litecoin",
            "BCH": "bitcoin-cash",
            "BCHUSDT": "bitcoin-cash",
            "ATOM": "cosmos",
            "ATOMUSDT": "cosmos",
            "ETC": "ethereum-classic",
            "ETCUSDT": "ethereum-classic",
            "XLM": "stellar",
            "XLMUSDT": "stellar",
            "ALGO": "algorand",
            "ALGOUSDT": "algorand",
            "VET": "vechain",
            "VETUSDT": "vechain",
            "FIL": "filecoin",
            "FILUSDT": "filecoin",
            "TRX": "tron",
            "TRXUSDT": "tron",
            "XMR": "monero",
            "XMRUSDT": "monero",
            "EOS": "eos",
            "EOSUSDT": "eos",
            "AAVE": "aave",
            "AAVEUSDT": "aave",
            "GRT": "the-graph",
            "GRTUSDT": "the-graph",
            "THETA": "theta-token",
            "THETAUSDT": "theta-token",
            "AXS": "axie-infinity",
            "AXSUSDT": "axie-infinity",
            "SAND": "the-sandbox",
            "SANDUSDT": "the-sandbox",
            "MANA": "decentraland",
            "MANAUSDT": "decentraland",
            "APE": "apecoin",
            "APEUSDT": "apecoin",
        }

    async def close(self):
        """关闭HTTP客户端"""
        await self.http_client.aclose()

    def _normalize_crypto_symbol(self, symbol: str) -> Optional[str]:
        """标准化加密货币交易对

        将币安交易对 (如 BTCUSDT) 转换为 CoinGecko ID (如 bitcoin)
        """
        symbol = str(symbol or "").strip().upper()

        # 移除常见的报价货币后缀
        for suffix in ["USDT", "USDC", "BUSD", "USD"]:
            if symbol.endswith(suffix):
                base = symbol[:-len(suffix)]
                if base in self.crypto_symbol_map:
                    return self.crypto_symbol_map[base]

        # 直接匹配
        if symbol in self.crypto_symbol_map:
            return self.crypto_symbol_map[symbol]

        # 如果包含 / 分隔符 (如 BTC/USDT)
        if "/" in symbol:
            base = symbol.split("/")[0]
            if base in self.crypto_symbol_map:
                return self.crypto_symbol_map[base]

        logger.warning(f"Unknown crypto symbol: {symbol}")
        return None

    def _normalize_binance_symbol(self, symbol: str) -> str:
        """标准化为 Binance 交易对 ID

        支持:
        - BTCUSDT
        - BTC/USDT
        - BTC-USDT
        - btc/usdt
        - 去除空格
        """
        clean_symbol = str(symbol or "").strip().upper()
        clean_symbol = re.sub(r"\s+", "", clean_symbol)

        if "/" in clean_symbol:
            base, quote = clean_symbol.split("/", 1)
            return f"{base}{quote}"
        if "-" in clean_symbol:
            parts = clean_symbol.split("-", 1)
            if len(parts) == 2 and parts[0] and parts[1]:
                return f"{parts[0]}{parts[1]}"
        return clean_symbol

    def _yahoo_is_rate_limited(self) -> bool:
        return time.time() < self._yahoo_rate_limit_until

    async def _yahoo_throttle(self) -> bool:
        """Yahoo Finance 请求节流; 返回 False 表示当前处于限流窗口内."""
        async with self._yahoo_rate_limit_lock:
            if self._yahoo_is_rate_limited():
                return False
            now = time.time()
            wait = self._yahoo_min_interval - (now - self._yahoo_last_request)
            if wait > 0:
                await asyncio.sleep(wait)
            self._yahoo_last_request = time.time()
            return True

    def _yahoo_mark_rate_limited(self, seconds: int = 30) -> None:
        self._yahoo_rate_limit_until = max(self._yahoo_rate_limit_until, time.time() + seconds)

    async def _fetch_binance_price(self, symbol_id: str, base_url: str, path: str) -> Optional[float]:
        try:
            response = await self.http_client.get(
                f"{base_url}{path}",
                params={"symbol": symbol_id},
            )
            if response.status_code != 200:
                return None
            data = response.json()
            price_str = data.get("price")
            if not price_str:
                return None
            return float(price_str)
        except Exception:
            return None

    async def fetch_crypto_price(self, symbol: str) -> Optional[float]:
        """获取加密货币价格 (通过 CoinGecko)

        Args:
            symbol: 交易对符号，如 BTCUSDT, ETH, BTC/USDT

        Returns:
            价格 (USD)，失败返回 None
        """
        try:
            # 1) 优先尝试 Binance 公共行情（覆盖更多交易对）
            # 仅对 USD 稳定币计价对使用，避免 BTC/ETH 这类非 USD 计价导致单位不一致
            stable_quotes = ("USD", "USDT", "USDC", "BUSD")
            raw = str(symbol or "").strip().upper()
            raw_no_space = re.sub(r"\s+", "", raw)
            main_symbol = raw_no_space.split("_", 1)[0]

            quote: Optional[str] = None
            if "/" in raw_no_space:
                parts = raw_no_space.split("/", 1)
                quote = parts[1] if len(parts) == 2 else None
            elif "-" in raw_no_space:
                parts = raw_no_space.split("-", 1)
                quote = parts[1] if len(parts) == 2 else None
            else:
                for suffix in stable_quotes:
                    if main_symbol.endswith(suffix) and len(main_symbol) > len(suffix):
                        quote = suffix
                        break

            if quote in stable_quotes:
                binance_symbol_id = self._normalize_binance_symbol(symbol)
                for base_url, path in [
                    (BINANCE_SPOT_API_URL, "/api/v3/ticker/price"),
                    (BINANCE_FUTURES_API_URL, "/fapi/v1/ticker/price"),
                    (BINANCE_DELIVERY_API_URL, "/dapi/v1/ticker/price"),
                ]:
                    price = await self._fetch_binance_price(binance_symbol_id, base_url, path)
                    if price is not None and price > 0:
                        logger.info(f"Fetched crypto price for {symbol} via Binance: ${price}")
                        return price

            # 2) 回退到 CoinGecko（适配仅有币种符号的情况，如 BTC）
            coingecko_id = self._normalize_crypto_symbol(symbol)
            if not coingecko_id:
                return None

            url = f"{COINGECKO_API_URL}/simple/price"
            params = {"ids": coingecko_id, "vs_currencies": "usd"}
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if coingecko_id in data and "usd" in data[coingecko_id]:
                price = data[coingecko_id]["usd"]
                logger.info(f"Fetched crypto price for {symbol}: ${price}")
                return float(price)
            else:
                logger.warning(f"No price data for {symbol} from CoinGecko")
                return None

        except Exception as e:
            logger.error(f"Error fetching crypto price for {symbol}: {e}")
            return None

    
    def _is_hk_symbol(self, symbol: str) -> bool:
        clean_symbol = str(symbol or "").strip().upper()
        if clean_symbol.endswith(".HK"):
            return True
        base = clean_symbol.split(".")[0]
        return base.isdigit() and len(base) == 5

    async def fetch_stock_price(self, symbol: str, market_type: str) -> Optional[float]:
        """获取股票价格 (通过 Yahoo Finance 或 AKShare)

        Args:
            symbol: 股票代码
            market_type: 市场类型 (us_stock, a_stock, hk_stock)

        Returns:
            价格，失败返回 None
        """
        if market_type == "a_stock":
            if self._is_hk_symbol(symbol):
                logger.info(f"Symbol {symbol} detected as HK, using hk_stock pricing")
                return await self._fetch_yfinance_price(symbol, "hk_stock")
            return await self._fetch_a_stock_price(symbol)
        else:
            # 美股和港股使用 yfinance
            price = await self._fetch_yfinance_price(symbol, market_type)
            if price is not None:
                return price
            # 备用数据源（Stooq）
            return await self._fetch_stooq_price(symbol, market_type)

    async def _fetch_yfinance_price(self, symbol: str, market_type: str) -> Optional[float]:
        """通过 Yahoo Finance 获取股票价格

        Args:
            symbol: 股票代码
            market_type: us_stock 或 hk_stock

        Returns:
            价格，失败返回 None
        """
        try:
            if self._yahoo_is_rate_limited():
                logger.warning("Yahoo Finance rate limited; skipping fetch for %s", symbol)
                return None

            can_fetch = await self._yahoo_throttle()
            if not can_fetch:
                logger.warning("Yahoo Finance rate limited; skipping fetch for %s", symbol)
                return None

            # 港股需要添加 .HK 后缀，并标准化为4位数字
            if market_type == "hk_stock":
                if not symbol.endswith(".HK") and not symbol.endswith(".hk"):
                    # 标准化为4位数字并添加 .HK 后缀
                    # 例如: 00700 -> 0700.HK, 700 -> 0700.HK, 09988 -> 9988.HK
                    if symbol.isdigit():
                        # 先移除前导零,再补齐到4位 (港股标准格式)
                        clean_symbol = str(int(symbol)).zfill(4)
                        symbol = f"{clean_symbol}.HK"
                    else:
                        symbol = f"{symbol}.HK"
                else:
                    # 已经有 .HK 后缀，标准化为4位数字
                    base = symbol.replace(".HK", "").replace(".hk", "")
                    if base.isdigit():
                        clean_symbol = str(int(base)).zfill(4)
                        symbol = f"{clean_symbol}.HK"

            logger.info(f"Fetching price for {symbol} using yfinance")

            ticker = yf.Ticker(symbol)

            # 1) 优先尝试 fast_info (通常更接近实时)
            price = None
            try:
                fast_info = getattr(ticker, "fast_info", None)
                if fast_info:
                    def read_fast_info(key: str):
                        if isinstance(fast_info, dict):
                            return fast_info.get(key)
                        return getattr(fast_info, key, None)

                    for key in ("last_price", "lastPrice", "regular_market_price", "regularMarketPrice"):
                        value = read_fast_info(key)
                        if value is not None:
                            price = value
                            break
            except Exception as exc:
                logger.debug(f"fast_info unavailable for {symbol}: {exc}")

            if price is not None and price > 0:
                logger.info(f"Fetched {market_type} price for {symbol} via fast_info: ${price}")
                return float(price)

            # 2) 使用 1m 级别的历史数据获取最新分钟价
            hist = ticker.history(period="1d", interval="1m")
            if not hist.empty:
                close_series = hist['Close'].dropna()
                if not close_series.empty:
                    price = close_series.iloc[-1]
                    if price and price > 0:
                        logger.info(f"Fetched {market_type} price for {symbol} via 1m history: ${price}")
                        return float(price)

            # 3) 回退到日线收盘价
            hist = ticker.history(period="1d")
            if hist.empty:
                logger.warning(f"No historical data returned for {symbol}")
                return None

            close_series = hist['Close'].dropna()
            if close_series.empty:
                logger.warning(f"No valid close data for {symbol} from Yahoo Finance")
                return None

            price = close_series.iloc[-1]
            if price and price > 0:
                logger.info(f"Fetched {market_type} price for {symbol} via daily close: ${price}")
                return float(price)
            logger.warning(f"No valid price data for {symbol} from Yahoo Finance")
            return None

        except Exception as e:
            message = str(e)
            if "Too Many Requests" in message or "rate limit" in message.lower():
                self._yahoo_mark_rate_limited()
                logger.warning(f"Yahoo Finance rate limited for {symbol}: {message}")
                return None
            logger.error(f"Error fetching {market_type} price for {symbol}: {e}")
            return None

    def _normalize_stooq_symbol(self, symbol: str, market_type: str) -> Optional[str]:
        clean_symbol = str(symbol or "").strip().lower()
        if not clean_symbol:
            return None
        if market_type == "us_stock":
            if clean_symbol.endswith(".us"):
                return clean_symbol
            return f"{clean_symbol}.us"
        if market_type == "hk_stock":
            if clean_symbol.endswith(".hk"):
                return clean_symbol
            return f"{clean_symbol}.hk"
        return None

    async def _fetch_stooq_price(self, symbol: str, market_type: str) -> Optional[float]:
        """通过 Stooq 获取股票价格（备用）"""
        stooq_symbol = self._normalize_stooq_symbol(symbol, market_type)
        if not stooq_symbol:
            return None
        try:
            response = await self.http_client.get(
                "https://stooq.com/q/l/",
                params={"s": stooq_symbol, "f": "sd2t2ohlcv", "h": "e", "e": "csv"},
            )
            if response.status_code != 200:
                return None
            lines = response.text.strip().splitlines()
            if len(lines) < 2:
                return None
            data = lines[1].split(",")
            if len(data) < 8:
                return None
            close_value = data[6]
            if not close_value or close_value.lower() in ("na", "n/a", "nan"):
                return None
            price = float(close_value)
            if price > 0:
                logger.info(f"Fetched {market_type} price for {symbol} via Stooq: {price}")
                return price
            return None
        except Exception as e:
            logger.warning(f"Stooq price fetch failed for {symbol}: {e}")
            return None

    async def _fetch_a_stock_price_sina(self, symbol: str) -> Optional[float]:
        """通过新浪财经获取 A 股实时价格

        Args:
            symbol: A股代码，如 000001 (不带后缀) 或 000001.SZ

        Returns:
            价格，失败返回 None
        """
        try:
            # 移除 .SZ 或 .SH 后缀
            clean_symbol = symbol.split(".")[0]

            # 判断交易所 (6开头是上交所, 0/3开头是深交所)
            if clean_symbol.startswith('6'):
                prefix = 'sh'
            elif clean_symbol.startswith('0') or clean_symbol.startswith('3'):
                prefix = 'sz'
            else:
                logger.warning(f"Unknown A-stock code format: {symbol}")
                return None

            sina_symbol = f"{prefix}{clean_symbol}"
            url = f"http://hq.sinajs.cn/list={sina_symbol}"

            logger.info(f"Fetching A-stock price from Sina for {symbol} ({sina_symbol})")

            # 添加请求头避免403错误
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': 'http://finance.sina.com.cn'
            }

            response = await self.http_client.get(url, headers=headers)
            response.raise_for_status()

            # 解析返回数据
            # 格式: var hq_str_sh600519="贵州茅台,1435.100,1435.000,1429.000,..."
            content = response.text
            match = re.search(r'"([^"]+)"', content)
            if not match:
                logger.warning(f"Failed to parse Sina response for {symbol}")
                return None

            data = match.group(1).split(',')
            if len(data) < 4:
                logger.warning(f"Insufficient data fields from Sina for {symbol}")
                return None

            name = data[0]
            current_price = float(data[3])

            if current_price > 0:
                logger.info(f"Fetched A-stock price from Sina: {name} ({symbol}) = ¥{current_price}")
                return current_price
            else:
                logger.warning(f"Invalid price for {symbol} from Sina: {current_price}")
                return None

        except Exception as e:
            logger.error(f"Error fetching A-stock price from Sina for {symbol}: {e}")
            return None

    def _normalize_a_stock_symbol(self, symbol: str) -> Optional[Tuple[str, str]]:
        """标准化 A 股代码，返回 (canonical, sina_symbol)"""
        clean_symbol = symbol.strip().upper()
        if clean_symbol.endswith(".SH") or clean_symbol.endswith(".SZ"):
            code = clean_symbol.split(".")[0]
        else:
            code = clean_symbol

        if not code.isdigit() or len(code) != 6:
            return None

        if code.startswith("6"):
            suffix = "SH"
            prefix = "sh"
        elif code.startswith("0") or code.startswith("3"):
            suffix = "SZ"
            prefix = "sz"
        else:
            return None

        canonical = f"{code}.{suffix}"
        sina_symbol = f"{prefix}{code}"
        return canonical, sina_symbol

    async def _fetch_a_stock_names_sina(self, sina_symbols: List[str]) -> Dict[str, str]:
        """通过新浪财经批量获取 A 股名称"""
        if not sina_symbols:
            return {}

        results: Dict[str, str] = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://finance.sina.com.cn'
        }

        chunk_size = 50
        for i in range(0, len(sina_symbols), chunk_size):
            chunk = sina_symbols[i:i + chunk_size]
            url = f"http://hq.sinajs.cn/list={','.join(chunk)}"
            try:
                response = await self.http_client.get(url, headers=headers)
                response.raise_for_status()
                content = response.text
                for match in re.finditer(r'var hq_str_(\w+)="([^"]*)"', content):
                    sina_symbol = match.group(1)
                    payload = match.group(2)
                    if not payload:
                        continue
                    parts = payload.split(',')
                    name = parts[0].strip() if parts else ''
                    if name:
                        results[sina_symbol] = name
            except Exception as e:
                logger.warning(f"Failed to fetch A-stock names from Sina: {e}")
                continue

        return results

    def _fetch_a_stock_names_akshare(self, symbols: List[str]) -> Dict[str, str]:
        """通过 AKShare 获取 A 股名称 (备用)"""
        if not symbols:
            return {}

        try:
            df = ak.stock_zh_a_spot_em()
            if df.empty:
                return {}
            code_to_name = dict(zip(df["代码"], df["名称"]))
        except Exception as e:
            logger.warning(f"Failed to fetch A-stock names from AKShare: {e}")
            return {}

        results: Dict[str, str] = {}
        for symbol in symbols:
            code = symbol.split(".")[0]
            name = code_to_name.get(code)
            if name:
                results[symbol] = name

        return results

    async def fetch_a_stock_names(self, symbols: List[str]) -> Dict[str, str]:
        """获取 A 股名称 (新浪优先,AKShare备用,带缓存)"""
        if not symbols:
            return {}

        symbol_meta: Dict[str, Dict[str, List[str] | str]] = {}
        for raw_symbol in symbols:
            normalized = self._normalize_a_stock_symbol(raw_symbol)
            if not normalized:
                continue
            canonical, sina_symbol = normalized
            entry = symbol_meta.setdefault(canonical, {"sina": sina_symbol, "originals": []})
            entry["originals"].append(raw_symbol)

        if not symbol_meta:
            return {}

        result: Dict[str, str] = {}
        missing_sina: Dict[str, str] = {}
        resolved_canonicals = set()
        for canonical, data in symbol_meta.items():
            cache_key = f"stock_name:a_stock:{canonical}"
            cached = RedisClient.get(cache_key)
            if cached:
                for raw_symbol in data["originals"]:
                    result[raw_symbol] = cached
                resolved_canonicals.add(canonical)
            else:
                missing_sina[data["sina"]] = canonical

        fetched = await self._fetch_a_stock_names_sina(list(missing_sina.keys()))
        for sina_symbol, name in fetched.items():
            canonical = missing_sina.get(sina_symbol)
            if not canonical:
                continue
            cache_key = f"stock_name:a_stock:{canonical}"
            RedisClient.set(cache_key, name, ttl=A_STOCK_NAME_TTL)
            for raw_symbol in symbol_meta[canonical]["originals"]:
                result[raw_symbol] = name
            resolved_canonicals.add(canonical)

        unresolved = [c for c in symbol_meta.keys() if c not in resolved_canonicals]
        if unresolved:
            fallback_names = self._fetch_a_stock_names_akshare(unresolved)
            for canonical, name in fallback_names.items():
                cache_key = f"stock_name:a_stock:{canonical}"
                RedisClient.set(cache_key, name, ttl=A_STOCK_NAME_TTL)
                for raw_symbol in symbol_meta[canonical]["originals"]:
                    result[raw_symbol] = name

        return result

    def _normalize_us_stock_symbol(self, symbol: str) -> Optional[str]:
        """标准化美股代码 (用于缓存key)"""
        clean_symbol = symbol.strip().upper()
        if not clean_symbol:
            return None
        return clean_symbol

    def _fetch_yfinance_stock_name_sync(self, symbol: str) -> Optional[str]:
        """通过 Yahoo Finance 获取股票名称 (同步,用于线程)"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info or {}
            for key in ("shortName", "longName", "displayName", "name"):
                name = info.get(key)
                if name:
                    return str(name).strip()
            return None
        except Exception as e:
            logger.warning(f"Error fetching stock name for {symbol} from Yahoo Finance: {e}")
            return None

    async def fetch_us_stock_names(self, symbols: List[str]) -> Dict[str, str]:
        """获取美股名称 (Yahoo Finance,带缓存)"""
        if not symbols:
            return {}

        symbol_meta: Dict[str, List[str]] = {}
        for raw_symbol in symbols:
            canonical = self._normalize_us_stock_symbol(raw_symbol)
            if not canonical:
                continue
            symbol_meta.setdefault(canonical, []).append(raw_symbol)

        if not symbol_meta:
            return {}

        result: Dict[str, str] = {}
        missing: List[str] = []
        for canonical, originals in symbol_meta.items():
            cache_key = f"stock_name:us_stock:{canonical}"
            cached = RedisClient.get(cache_key)
            if cached:
                for raw_symbol in originals:
                    result[raw_symbol] = cached
            else:
                missing.append(canonical)

        if not missing:
            return result

        semaphore = asyncio.Semaphore(5)

        async def fetch_one(canonical_symbol: str) -> tuple[str, Optional[str]]:
            async with semaphore:
                name = await asyncio.to_thread(self._fetch_yfinance_stock_name_sync, canonical_symbol)
                return canonical_symbol, name

        fetched_pairs = await asyncio.gather(*(fetch_one(symbol) for symbol in missing))
        for canonical, name in fetched_pairs:
            if not name:
                continue
            cache_key = f"stock_name:us_stock:{canonical}"
            RedisClient.set(cache_key, name, ttl=US_STOCK_NAME_TTL)
            for raw_symbol in symbol_meta.get(canonical, []):
                result[raw_symbol] = name

        return result

    async def _fetch_a_stock_price_akshare(self, symbol: str) -> Optional[float]:
        """通过 AKShare 获取 A 股实时价格 (备用)

        Args:
            symbol: A股代码，如 000001 (不带后缀) 或 000001.SZ

        Returns:
            价格，失败返回 None
        """
        try:
            # 移除 .SZ 或 .SH 后缀
            clean_symbol = symbol.split(".")[0]

            logger.info(f"Fetching A-stock price from AKShare for {symbol} (code: {clean_symbol})")

            # 使用 AKShare 获取实时行情
            df = ak.stock_zh_a_spot_em()

            # 查找对应股票
            stock_data = df[df["代码"] == clean_symbol]

            if not stock_data.empty:
                price = stock_data.iloc[0]["最新价"]
                if price and float(price) > 0:
                    logger.info(f"Fetched A-stock price from AKShare for {symbol}: ¥{price}")
                    return float(price)

            logger.warning(f"No price data for A-stock {symbol} from AKShare")
            return None

        except Exception as e:
            logger.error(f"Error fetching A-stock price from AKShare for {symbol}: {e}")
            return None

    async def _fetch_a_stock_price(self, symbol: str) -> Optional[float]:
        """获取 A 股实时价格 (使用多数据源,优先级: 新浪 > AKShare)

        Args:
            symbol: A股代码，如 000001 (不带后缀) 或 000001.SZ

        Returns:
            价格，失败返回 None
        """
        # 1. 优先尝试新浪财经 (更稳定)
        price = await self._fetch_a_stock_price_sina(symbol)
        if price is not None:
            return price

        logger.info(f"Sina Finance failed for {symbol}, trying AKShare as backup...")

        # 2. 新浪失败,尝试 AKShare 作为备用
        price = await self._fetch_a_stock_price_akshare(symbol)
        if price is not None:
            return price

        logger.error(f"All A-stock data sources failed for {symbol}")
        return None

    async def get_current_price(
        self,
        symbol: str,
        market_type: str,
        force_refresh: bool = False
    ) -> Optional[float]:
        """获取当前市场价格（带缓存）

        Args:
            symbol: 交易对/股票代码
            market_type: 市场类型 (crypto, us_stock, a_stock, hk_stock)
            force_refresh: 是否强制绕过缓存

        Returns:
            价格，失败返回 None
        """
        # 生成缓存键
        cache_key = f"market_price:{market_type}:{symbol}"

        # 尝试从缓存获取
        cached_price = RedisClient.get(cache_key)
        if cached_price is not None and not force_refresh:
            logger.debug(f"Cache hit for {symbol} ({market_type}): {cached_price}")
            return float(cached_price)

        # 缓存未命中，从数据源获取
        price = None
        if market_type == "crypto":
            price = await self.fetch_crypto_price(symbol)
        elif market_type in ["us_stock", "a_stock", "hk_stock"]:
            price = await self.fetch_stock_price(symbol, market_type)
        else:
            logger.error(f"Unsupported market type: {market_type}")
            return None

        # 保存到缓存
        if price is not None:
            RedisClient.set(cache_key, price, ttl=CACHE_TTL)
            return price

        if cached_price is not None:
            logger.warning(f"Using cached price for {symbol} ({market_type}) after fetch failure")
            return float(cached_price)

        return None

    async def batch_fetch_prices(
        self,
        positions: List[Position]
    ) -> Dict[str, float]:
        """批量获取持仓的当前价格

        Args:
            positions: 持仓列表

        Returns:
            {position_id: price} 字典
        """
        tasks = []
        position_map = {}

        # 创建异步任务
        for position in positions:
            # 从 account 获取 market_type (需要预先加载关系)
            # 这里假设调用方已经加载了 account 关系
            if hasattr(position, 'account') and position.account:
                market_type = position.account.account_type
            else:
                # 如果没有加载关系，尝试从 position 推断
                # 这是一个 fallback，实际应该避免
                logger.warning(f"Position {position.id} missing account relationship")
                continue

            task = self.get_current_price(position.symbol, market_type)
            tasks.append(task)
            position_map[position.id] = len(tasks) - 1  # 记录任务索引

        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 构造结果字典
        prices = {}
        for position_id, task_idx in position_map.items():
            result = results[task_idx]
            if isinstance(result, Exception):
                logger.error(f"Error fetching price for position {position_id}: {result}")
            elif result is not None:
                prices[str(position_id)] = result

        return prices

    async def update_position_prices(
        self,
        positions: List[Position],
        db
    ) -> int:
        """更新持仓的实时价格和盈亏

        Args:
            positions: 持仓列表
            db: 数据库 session

        Returns:
            成功更新的数量
        """
        logger.info(f"Starting price update for {len(positions)} positions")
        updated_count = 0

        for position in positions:
            try:
                # 从 account 获取 market_type
                if hasattr(position, 'account') and position.account:
                    market_type = position.account.account_type
                    logger.info(f"Processing {position.symbol} (type: {market_type})")
                else:
                    logger.warning(f"Position {position.id} missing account, skipping")
                    continue

                # 获取当前价格
                logger.info(f"Fetching price for {position.symbol} from {market_type}")
                current_price = await self.get_current_price(
                    position.symbol,
                    market_type
                )

                if current_price is None:
                    logger.warning(f"Failed to fetch price for {position.symbol}")
                    continue

                logger.info(f"Got price {current_price} for {position.symbol}")

                # 更新价格和盈亏
                position.current_price = Decimal(str(current_price))

                # 计算未实现盈亏
                if position.position_type == 'futures':
                    # 合约持仓
                    entry_price = position.entry_price or Decimal(0)
                    quantity = position.quantity
                    # 盈亏 = (当前价 - 开仓价) * 数量
                    unrealized_pnl = (position.current_price - entry_price) * abs(quantity)
                    # 对于空头，盈亏要取反
                    if quantity < 0:
                        unrealized_pnl = -unrealized_pnl
                    position.unrealized_pnl = unrealized_pnl

                    # ROE (基于保证金)
                    if position.margin_used and position.margin_used > 0:
                        position.roe_percent = (unrealized_pnl / position.margin_used) * 100
                else:
                    # 现货持仓
                    average_cost = position.average_cost or Decimal(0)
                    quantity = position.quantity
                    # 市值
                    market_value = position.current_price * abs(quantity)
                    # 成本
                    total_cost = average_cost * abs(quantity)
                    # 盈亏
                    position.unrealized_pnl = market_value - total_cost

                    # 盈亏百分比
                    if average_cost > 0:
                        position.unrealized_pnl_percent = \
                            ((position.current_price - average_cost) / average_cost) * 100

                position.last_updated = datetime.utcnow()
                updated_count += 1

            except Exception as e:
                logger.error(f"Error updating position {position.id}: {e}")
                continue

        # 提交数据库更改
        try:
            db.commit()
            logger.info(f"Successfully updated {updated_count} positions")
        except Exception as e:
            logger.error(f"Error committing position updates: {e}")
            db.rollback()
            return 0

        return updated_count


# 单例实例
_market_data_service: Optional[MarketDataService] = None


def get_market_data_service() -> MarketDataService:
    """获取市场数据服务单例"""
    global _market_data_service
    if _market_data_service is None:
        _market_data_service = MarketDataService()
    return _market_data_service
