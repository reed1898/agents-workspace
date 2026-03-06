"""Dashboard schemas for API responses"""
from pydantic import BaseModel
from decimal import Decimal
from typing import List, Dict, Optional
from datetime import datetime


class OverviewMetrics(BaseModel):
    """Dashboard overview metrics"""
    total_market_value: Decimal
    total_cash_balance: Decimal
    total_assets: Decimal
    total_cost: Decimal
    total_pnl: Decimal
    total_pnl_percent: Decimal
    today_pnl: Optional[Decimal] = None  # 今日盈亏（需要历史价格）
    today_pnl_percent: Optional[Decimal] = None


class PositionsSummaryMetrics(BaseModel):
    """Positions summary metrics"""
    total_positions: int
    profitable_count: int
    losing_count: int
    by_market: Dict[str, Dict[str, Decimal]]  # {market_type: {value, pnl, count}}


class RecentTrade(BaseModel):
    """Recent trade information"""
    id: str
    symbol: str
    symbol_name: Optional[str] = None
    side: str
    quantity: Decimal
    price: Decimal
    trade_time: datetime
    account_name: str
    account_type: str

    class Config:
        from_attributes = True


class PendingReview(BaseModel):
    """Pending review position cycle"""
    id: str
    symbol: str
    account_name: str
    close_time: datetime
    total_profit_loss: Optional[Decimal]
    roi_percent: Optional[Decimal]
    holding_hours: Optional[int]
    days_since_close: int

    class Config:
        from_attributes = True


class QuickStats(BaseModel):
    """Quick statistics"""
    open_position_cycles: int
    trades_this_month: int
    win_rate_this_month: Optional[Decimal] = None


class DashboardSummary(BaseModel):
    """Complete dashboard summary response"""
    overview: OverviewMetrics
    positions_summary: PositionsSummaryMetrics
    recent_trades: List[RecentTrade]
    pending_reviews: List[PendingReview]
    discipline_score: Optional[Decimal] = None
    quick_stats: QuickStats
