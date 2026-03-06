from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class TradeAccountBase(BaseModel):
    """交易账户基础 Schema"""
    account_name: str
    account_type: str  # us_stock, a_stock, hk_stock, crypto
    broker: Optional[str] = None  # 券商/交易所: moomoo, interactive_brokers, binance, okx, etc.
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class TradeAccountCreate(TradeAccountBase):
    """创建交易账户 Schema"""
    crypto_sub_type: Optional[str] = None  # binance_spot, binance_futures
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    ibkr_flex_token: Optional[str] = None
    ibkr_flex_query_id: Optional[str] = None
    extra_config: Optional[Dict[str, Any]] = None
    sync_start_date: Optional[datetime] = None


class TradeAccountUpdate(BaseModel):
    """更新交易账户 Schema"""
    account_name: Optional[str] = None
    broker: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    ibkr_flex_token: Optional[str] = None
    ibkr_flex_query_id: Optional[str] = None
    is_active: Optional[bool] = None
    cash_balance: Optional[Decimal] = None
    cash_currency: Optional[str] = None
    extra_config: Optional[Dict[str, Any]] = None
    sync_start_date: Optional[datetime] = None


class TradeAccountInDB(TradeAccountBase):
    """数据库中的交易账户 Schema"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    is_active: bool
    last_sync_at: Optional[datetime] = None
    sync_start_date: Optional[datetime] = None
    ibkr_flex_token: Optional[str] = None
    ibkr_flex_query_id: Optional[str] = None
    gmail_address: Optional[str] = None
    gmail_connected_at: Optional[datetime] = None
    cash_balance: Optional[Decimal] = None
    cash_currency: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    extra_config: Optional[Dict[str, Any]] = None


class TradeAccount(TradeAccountInDB):
    """交易账户响应 Schema (不包含敏感信息)"""
    has_api_credentials: bool = False
    has_gmail_credentials: bool = False


class TradeAccountWithCredentials(TradeAccountInDB):
    """包含凭证的交易账户 Schema (仅用于管理)"""
    has_api_key: bool = False
    has_api_secret: bool = False
    has_gmail_credentials: bool = False


class TradeAccountSyncResponse(BaseModel):
    """交易账户同步响应 Schema"""
    status: str
    message: str
    account_id: str
    last_sync_at: Optional[datetime]
    synced_trades: int
