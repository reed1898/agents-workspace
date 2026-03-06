from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional


class ClosedPositionBase(BaseModel):
    """已平仓记录基础Schema"""
    symbol: str
    position_type: str  # spot, futures
    position_side: Optional[str] = None  # LONG, SHORT, None
    quantity: Decimal
    entry_price: Decimal
    exit_price: Decimal
    leverage: Optional[Decimal] = None
    margin_used: Optional[Decimal] = None
    realized_pnl: Decimal
    realized_pnl_percent: Decimal
    roe_percent: Optional[Decimal] = None
    open_time: datetime
    close_time: datetime
    holding_days: Optional[int] = None
    total_fees: Decimal = Decimal('0')


class ClosedPositionCreate(ClosedPositionBase):
    """创建已平仓记录Schema"""
    account_id: UUID


class ClosedPositionResponse(ClosedPositionBase):
    """已平仓记录响应Schema"""
    id: UUID
    account_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ClosedPositionListResponse(BaseModel):
    """已平仓记录列表响应"""
    positions: list[ClosedPositionResponse]
    total: int
    profitable_count: int
    losing_count: int
    total_realized_pnl: Decimal
    win_rate: float  # 胜率


class ClosedPositionStats(BaseModel):
    """已平仓统计"""
    total_count: int
    profitable_count: int
    losing_count: int
    win_rate: float
    total_realized_pnl: Decimal
    average_pnl: Decimal
    average_pnl_percent: Decimal
    average_holding_days: float
    best_trade: Optional[ClosedPositionResponse] = None
    worst_trade: Optional[ClosedPositionResponse] = None
