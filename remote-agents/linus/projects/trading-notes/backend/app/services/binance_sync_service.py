"""币安交易同步服务

直接调用币安 REST API 同步交易记录
"""
import os
import time
import hmac
import hashlib
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple, Set
from urllib.parse import urlencode

import requests
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.trade_account import TradeAccount
from ..models.trade import Trade
from ..core.security import decrypt_api_key
from .position_service import PositionService

SPOT_BASE_URL = "https://api.binance.com"
FUTURES_BASE_URL = "https://fapi.binance.com"
DEFAULT_FALLBACK_DAYS = 7


class BinanceSyncService:
    """币安交易同步服务"""

    def __init__(self, db: Session):
        self.db = db

    def _get_api_credentials(self, account: TradeAccount) -> Tuple[str, str]:
        """获取并解密 API 凭证"""
        if not account.api_key_encrypted or not account.api_secret_encrypted:
            raise ValueError(f"账户 {account.account_name} 未配置 API 凭证")

        api_key = decrypt_api_key(account.api_key_encrypted)
        api_secret = decrypt_api_key(account.api_secret_encrypted)
        return api_key, api_secret

    def _get_proxies(self) -> Optional[Dict[str, str]]:
        """从环境变量读取代理配置"""
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")

        proxies: Dict[str, str] = {}
        if http_proxy:
            proxies["http"] = http_proxy
        if https_proxy:
            proxies["https"] = https_proxy

        return proxies or None

    def _sign_params(self, params: Dict[str, Any], api_secret: str) -> str:
        query = urlencode(params, doseq=True)
        signature = hmac.new(api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{query}&signature={signature}"

    def _request(
        self,
        method: str,
        base_url: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
    ) -> Any:
        params = params or {}
        headers: Dict[str, str] = {}

        if signed:
            if not api_key or not api_secret:
                raise ValueError("缺少 API 凭证，无法签名请求")
            params["timestamp"] = int(time.time() * 1000)
            params.setdefault("recvWindow", 10000)
            query = self._sign_params(params, api_secret)
            headers["X-MBX-APIKEY"] = api_key
        else:
            query = urlencode(params, doseq=True)

        url = f"{base_url}{path}"
        if query:
            url = f"{url}?{query}"

        response = requests.request(
            method.upper(),
            url,
            headers=headers,
            timeout=15,
            proxies=self._get_proxies(),
        )

        try:
            data = response.json()
        except ValueError:
            data = response.text

        if not response.ok:
            raise ValueError(f"Binance API error {response.status_code}: {data}")

        return data

    def _get_exchange_metadata(
        self, is_futures: bool
    ) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, Set[str]]]:
        """获取交易对映射"""
        base_url = FUTURES_BASE_URL if is_futures else SPOT_BASE_URL
        path = "/fapi/v1/exchangeInfo" if is_futures else "/api/v3/exchangeInfo"
        info = self._request("GET", base_url, path)

        symbol_id_to_symbol: Dict[str, str] = {}
        symbol_symbol_to_id: Dict[str, str] = {}
        base_asset_to_symbols: Dict[str, Set[str]] = {}

        for item in info.get("symbols", []):
            if item.get("status") not in ("TRADING", "PRE_TRADING"):
                continue
            symbol_id = item.get("symbol")
            base_asset = item.get("baseAsset")
            quote_asset = item.get("quoteAsset")
            if not symbol_id or not base_asset or not quote_asset:
                continue
            display = f"{base_asset}/{quote_asset}"
            symbol_id_to_symbol[symbol_id] = display
            symbol_symbol_to_id[display.upper()] = symbol_id
            base_asset_to_symbols.setdefault(base_asset, set()).add(symbol_id)

        return symbol_id_to_symbol, symbol_symbol_to_id, base_asset_to_symbols

    def _resolve_symbol(
        self,
        raw_symbol: str,
        symbol_id_to_symbol: Dict[str, str],
        symbol_symbol_to_id: Dict[str, str],
    ) -> Optional[Tuple[str, str]]:
        normalized = raw_symbol.strip().upper()
        if not normalized:
            return None
        if "/" in normalized:
            symbol_id = symbol_symbol_to_id.get(normalized)
            if not symbol_id:
                return None
            return symbol_id, symbol_id_to_symbol.get(symbol_id, normalized)
        symbol_id = normalized
        return symbol_id, symbol_id_to_symbol.get(symbol_id, normalized)

    def _get_spot_symbols_from_balance(
        self,
        api_key: str,
        api_secret: str,
        base_asset_to_symbols: Dict[str, Set[str]],
    ) -> Set[str]:
        data = self._request(
            "GET",
            SPOT_BASE_URL,
            "/api/v3/account",
            signed=True,
            api_key=api_key,
            api_secret=api_secret,
        )

        symbols: Set[str] = set()
        for balance in data.get("balances", []):
            asset = balance.get("asset")
            if not asset:
                continue
            free = Decimal(str(balance.get("free", "0")))
            locked = Decimal(str(balance.get("locked", "0")))
            if free + locked <= 0:
                continue
            for symbol_id in base_asset_to_symbols.get(asset, set()):
                symbols.add(symbol_id)

        return symbols

    def _get_futures_symbols_from_positions(
        self,
        api_key: str,
        api_secret: str,
    ) -> Set[str]:
        data = self._request(
            "GET",
            FUTURES_BASE_URL,
            "/fapi/v2/account",
            signed=True,
            api_key=api_key,
            api_secret=api_secret,
        )

        symbols: Set[str] = set()
        for position in data.get("positions", []):
            symbol_id = position.get("symbol")
            if not symbol_id:
                continue
            position_amt = Decimal(str(position.get("positionAmt", "0")))
            if position_amt != 0:
                symbols.add(symbol_id)

        return symbols

    def _get_futures_symbols_from_income(
        self,
        api_key: str,
        api_secret: str,
        since_ms: Optional[int],
    ) -> Set[str]:
        now_ms = int(time.time() * 1000)
        if since_ms is None:
            since_ms = now_ms - DEFAULT_FALLBACK_DAYS * 24 * 60 * 60 * 1000

        symbols: Set[str] = set()
        fetch_since = since_ms

        for _ in range(20):
            params: Dict[str, Any] = {
                "startTime": int(fetch_since),
                "endTime": int(now_ms),
                "limit": 1000,
            }

            batch = self._request(
                "GET",
                FUTURES_BASE_URL,
                "/fapi/v1/income",
                params=params,
                signed=True,
                api_key=api_key,
                api_secret=api_secret,
            )

            if not batch:
                break

            for item in batch:
                symbol_id = item.get("symbol")
                if symbol_id:
                    symbols.add(symbol_id)

            if len(batch) < params["limit"]:
                break

            last_time = batch[-1].get("time")
            if last_time is None or last_time <= fetch_since:
                break

            fetch_since = last_time + 1

        return symbols

    def _fetch_my_trades(
        self,
        symbol_id: str,
        since_ms: Optional[int],
        limit: int,
        is_futures: bool,
        api_key: str,
        api_secret: str,
    ) -> List[Dict[str, Any]]:
        base_url = FUTURES_BASE_URL if is_futures else SPOT_BASE_URL
        path = "/fapi/v1/userTrades" if is_futures else "/api/v3/myTrades"

        trades: List[Dict[str, Any]] = []
        fetch_since = since_ms

        for _ in range(10):
            params: Dict[str, Any] = {
                "symbol": symbol_id,
                "limit": limit,
            }
            if fetch_since is not None:
                params["startTime"] = int(fetch_since)

            batch = self._request(
                "GET",
                base_url,
                path,
                params=params,
                signed=True,
                api_key=api_key,
                api_secret=api_secret,
            )

            if not batch:
                break

            trades.extend(batch)

            if len(batch) < limit:
                break

            last_time = batch[-1].get("time")
            if last_time is None or (fetch_since is not None and last_time <= fetch_since):
                break

            fetch_since = last_time + 1

        return trades

    def _create_trade_from_binance(
        self,
        account: TradeAccount,
        trade_data: Dict[str, Any],
        symbol_display: str,
        is_futures: bool,
    ) -> Trade:
        trade_time = datetime.fromtimestamp(trade_data["time"] / 1000)
        quantity = Decimal(str(trade_data.get("qty") or trade_data.get("executedQty") or "0"))
        price = Decimal(str(trade_data.get("price") or "0"))
        fee = Decimal(str(trade_data.get("commission") or "0"))
        fee_currency = trade_data.get("commissionAsset")

        if is_futures:
            side = str(trade_data.get("side", "")).lower()
        else:
            side = "buy" if trade_data.get("isBuyer") else "sell"

        trade = Trade(
            account_id=account.id,
            symbol=symbol_display,
            side=side,
            quantity=quantity,
            price=price,
            fee=fee,
            fee_currency=fee_currency,
            trade_time=trade_time,
            trade_id_external=str(trade_data.get("id")),
            sync_source="api",
            notes=None,
        )

        if is_futures:
            trade.position_side = trade_data.get("positionSide", "BOTH")
            trade.leverage = Decimal(str(account.get_leverage()))
            if trade.leverage and trade.leverage != 0:
                trade.margin = (quantity * price) / trade.leverage

        return trade

    def sync_trades(
        self,
        account_id: str,
        symbol: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 1000,
    ) -> Dict[str, Any]:
        """同步交易记录"""
        account = self.db.query(TradeAccount).filter(TradeAccount.id == account_id).first()
        if not account:
            return {
                "success": False,
                "error": f"账户不存在: {account_id}",
            }

        try:
            api_key, api_secret = self._get_api_credentials(account)
            is_futures = account.is_futures_account()

            symbol_id_to_symbol, symbol_symbol_to_id, base_asset_to_symbols = self._get_exchange_metadata(is_futures)

            # 确定同步起始时间（增量同步）
            sync_since = since
            if sync_since is None:
                if account.last_sync_at:
                    sync_since = account.last_sync_at
                elif account.sync_start_date:
                    sync_since = account.sync_start_date

            since_ms = int(sync_since.timestamp() * 1000) if sync_since else None

            synced_count = 0
            errors: List[str] = []

            symbols_to_sync: List[Tuple[str, str]] = []
            if symbol:
                resolved = self._resolve_symbol(symbol, symbol_id_to_symbol, symbol_symbol_to_id)
                if not resolved:
                    return {
                        "success": False,
                        "error": f"未知交易对: {symbol}",
                        "account_id": str(account_id),
                    }
                symbols_to_sync.append(resolved)
            else:
                manual_symbols = []
                if account.extra_config:
                    manual_symbols = account.extra_config.get("sync_symbols") or account.extra_config.get("symbols") or []

                if isinstance(manual_symbols, str):
                    manual_symbols = [item.strip() for item in manual_symbols.split(",") if item.strip()]

                for raw_symbol in manual_symbols:
                    resolved = self._resolve_symbol(raw_symbol, symbol_id_to_symbol, symbol_symbol_to_id)
                    if resolved:
                        symbols_to_sync.append(resolved)
                    else:
                        errors.append(f"未知交易对: {raw_symbol}")

                if not symbols_to_sync:
                    if is_futures:
                        symbol_ids = self._get_futures_symbols_from_positions(api_key, api_secret)
                        if not symbol_ids:
                            symbol_ids = self._get_futures_symbols_from_income(api_key, api_secret, since_ms)
                    else:
                        symbol_ids = self._get_spot_symbols_from_balance(api_key, api_secret, base_asset_to_symbols)

                    for symbol_id in symbol_ids:
                        display = symbol_id_to_symbol.get(symbol_id, symbol_id)
                        symbols_to_sync.append((symbol_id, display))

                if not symbols_to_sync:
                    return {
                        "success": False,
                        "error": "未找到可同步的交易对。可在账户 extra_config 设置 sync_symbols，例如: [\"BTC/USDT\", \"ETH/USDT\"]。",
                        "account_id": str(account_id),
                    }

            for symbol_id, symbol_display in symbols_to_sync:
                try:
                    result = self._sync_symbol_trades(
                        account,
                        api_key,
                        api_secret,
                        symbol_id,
                        symbol_display,
                        since_ms,
                        limit,
                        is_futures,
                    )
                    synced_count += result["synced_count"]
                    errors.extend(result["errors"])
                except Exception as exc:
                    errors.append(f"同步 {symbol_display} 失败: {str(exc)}")
                    continue

            account.last_sync_at = datetime.utcnow()
            self.db.commit()

            if synced_count > 0:
                try:
                    position_service = PositionService(self.db)
                    position_service.calculate_positions_for_account(account.id)
                except Exception as exc:
                    errors.append(f"持仓计算失败: {str(exc)}")

            return {
                "success": True,
                "synced_count": synced_count,
                "errors": errors,
                "account_id": str(account_id),
                "last_sync_at": account.last_sync_at,
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "account_id": str(account_id),
            }

    def _sync_symbol_trades(
        self,
        account: TradeAccount,
        api_key: str,
        api_secret: str,
        symbol_id: str,
        symbol_display: str,
        since_ms: Optional[int],
        limit: int,
        is_futures: bool,
    ) -> Dict[str, Any]:
        """同步单个交易对的交易记录"""
        synced_count = 0
        errors: List[str] = []

        try:
            trades = self._fetch_my_trades(symbol_id, since_ms, limit, is_futures, api_key, api_secret)

            for trade_data in trades:
                try:
                    external_id = str(trade_data.get("id"))
                    if not external_id:
                        continue

                    existing_trade = self.db.query(Trade).filter(
                        and_(
                            Trade.account_id == account.id,
                            Trade.trade_id_external == external_id,
                        )
                    ).first()

                    if existing_trade:
                        continue

                    trade_time = datetime.fromtimestamp(trade_data["time"] / 1000)
                    if account.sync_start_date and trade_time < account.sync_start_date:
                        continue

                    new_trade = self._create_trade_from_binance(account, trade_data, symbol_display, is_futures)
                    self.db.add(new_trade)
                    synced_count += 1

                except Exception as exc:
                    errors.append(f"处理交易 {trade_data.get('id')} 失败: {str(exc)}")
                    continue

            if synced_count > 0:
                self.db.commit()

        except Exception as exc:
            errors.append(f"获取 {symbol_display} 交易记录失败: {str(exc)}")

        return {
            "synced_count": synced_count,
            "errors": errors,
        }

    def clear_account_trades(self, account_id: str) -> Dict[str, Any]:
        """清除账户的所有交易数据"""
        from ..models.position import Position
        from ..models.closed_position import ClosedPosition

        try:
            account = self.db.query(TradeAccount).filter(TradeAccount.id == account_id).first()
            if not account:
                return {
                    "success": False,
                    "error": f"账户不存在: {account_id}",
                }

            trades_deleted = self.db.query(Trade).filter(Trade.account_id == account_id).delete()
            positions_deleted = self.db.query(Position).filter(Position.account_id == account_id).delete()
            closed_positions_deleted = self.db.query(ClosedPosition).filter(ClosedPosition.account_id == account_id).delete()

            account.last_sync_at = None

            self.db.commit()

            return {
                "success": True,
                "deleted_count": trades_deleted,
                "positions_deleted": positions_deleted,
                "closed_positions_deleted": closed_positions_deleted,
                "account_id": str(account_id),
            }

        except Exception as exc:
            self.db.rollback()
            return {
                "success": False,
                "error": str(exc),
                "account_id": str(account_id),
            }
