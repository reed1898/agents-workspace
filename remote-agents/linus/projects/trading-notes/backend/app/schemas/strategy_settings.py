from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Dict, List, Optional


class MarketStrategyConfig(BaseModel):
    open: List[str] = Field(default_factory=list, description="建仓策略列表")
    add: List[str] = Field(default_factory=list, description="加仓策略列表")
    reduce: List[str] = Field(default_factory=list, description="减仓策略列表")
    close: List[str] = Field(default_factory=list, description="清仓策略列表")

    @field_validator("open", "add", "reduce", "close", mode="before")
    @classmethod
    def normalize_strategy_list(cls, value: List[str]) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            return []
        cleaned: List[str] = []
        for item in value:
            if item is None:
                continue
            text = str(item).strip()
            if text and text not in cleaned:
                cleaned.append(text)
        return cleaned


class CurrencySettings(BaseModel):
    usd_cny_rate: float = Field(7.2, gt=0, description="美元兑人民币汇率")

    @field_validator("usd_cny_rate", mode="before")
    @classmethod
    def normalize_usd_cny_rate(cls, value: float) -> float:
        if value is None:
            return 7.2
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return 7.2
        return numeric if numeric > 0 else 7.2


class StrategySettingsBase(BaseModel):
    market_strategies: Dict[str, MarketStrategyConfig] = Field(
        default_factory=dict,
        description="按市场分类的操作策略"
    )
    currency_settings: CurrencySettings = Field(
        default_factory=CurrencySettings,
        description="货币相关配置"
    )


class StrategySettingsUpdate(BaseModel):
    market_strategies: Optional[Dict[str, MarketStrategyConfig]] = Field(
        default=None,
        description="按市场分类的操作策略"
    )
    currency_settings: Optional[CurrencySettings] = Field(
        default=None,
        description="货币相关配置"
    )


class StrategySettingsResponse(StrategySettingsBase):
    model_config = ConfigDict(from_attributes=True)
