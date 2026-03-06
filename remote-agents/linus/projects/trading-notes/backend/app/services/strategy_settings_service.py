from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.user_strategy_settings import UserStrategySettings
from ..schemas.strategy_settings import MarketStrategyConfig


DEFAULT_MARKET_STRATEGIES: Dict[str, Dict[str, list[str]]] = {
    "a_stock": {"open": [], "add": [], "reduce": [], "close": []},
    "us_stock": {"open": [], "add": [], "reduce": [], "close": []},
    "hk_stock": {"open": [], "add": [], "reduce": [], "close": []},
    "crypto": {"open": [], "add": [], "reduce": [], "close": []},
}
DEFAULT_CURRENCY_SETTINGS: Dict[str, float] = {
    "usd_cny_rate": 7.2
}


def _merge_with_defaults(market_strategies: Dict[str, Any]) -> Dict[str, Dict[str, list[str]]]:
    merged = {key: {**value} for key, value in DEFAULT_MARKET_STRATEGIES.items()}
    for market, config in (market_strategies or {}).items():
        if market not in merged:
            merged[market] = {"open": [], "add": [], "reduce": [], "close": []}
        if hasattr(config, "model_dump"):
            config = config.model_dump()
        if isinstance(config, dict):
            for action in ["open", "add", "reduce", "close"]:
                if action in config:
                    merged[market][action] = config.get(action) or []
    return merged


def _normalize_currency_settings(settings: Optional[Dict[str, Any]]) -> Dict[str, float]:
    rate = DEFAULT_CURRENCY_SETTINGS["usd_cny_rate"]
    if isinstance(settings, dict):
        raw_rate = settings.get("usd_cny_rate")
        try:
            numeric_rate = float(raw_rate)
            if numeric_rate > 0:
                rate = numeric_rate
        except (TypeError, ValueError):
            pass
    return {"usd_cny_rate": rate}


class StrategySettingsService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, user_id: UUID) -> UserStrategySettings:
        settings = self.db.query(UserStrategySettings).filter(
            UserStrategySettings.user_id == user_id
        ).first()

        if settings:
            settings.market_strategies = _merge_with_defaults(settings.market_strategies)
            settings.currency_settings = _normalize_currency_settings(settings.currency_settings)
            self.db.commit()
            self.db.refresh(settings)
            return settings

        settings = UserStrategySettings(
            user_id=user_id,
            market_strategies=_merge_with_defaults({}),
            currency_settings=_normalize_currency_settings(None)
        )
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def update_settings(
        self,
        user_id: UUID,
        market_strategies: Optional[Dict[str, MarketStrategyConfig]] = None,
        currency_settings: Optional[Dict[str, Any]] = None
    ) -> UserStrategySettings:
        settings = self.db.query(UserStrategySettings).filter(
            UserStrategySettings.user_id == user_id
        ).first()

        normalized_market = _merge_with_defaults(market_strategies or (settings.market_strategies if settings else {}))
        normalized_currency = _normalize_currency_settings(
            currency_settings if currency_settings is not None else (settings.currency_settings if settings else None)
        )

        if settings:
            settings.market_strategies = normalized_market
            settings.currency_settings = normalized_currency
        else:
            settings = UserStrategySettings(
                user_id=user_id,
                market_strategies=normalized_market,
                currency_settings=normalized_currency
            )
            self.db.add(settings)

        self.db.commit()
        self.db.refresh(settings)
        return settings
