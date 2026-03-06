from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class PositionBase(BaseModel):
    """持仓基础 Schema

    支持现货和合约持仓:
    - 现货: position_type='spot', quantity>0, average_cost有值
    - 合约: position_type='futures', quantity正负表示多空, entry_price有值
    """
    symbol: str = Field(..., min_length=1, max_length=50, description="交易标的符号")
    position_type: str = Field(default='spot', description="持仓类型: spot, futures")
    position_side: Optional[str] = Field(None, description="持仓方向: LONG, SHORT (仅合约)")
    quantity: Decimal = Field(..., description="持仓数量 (合约: 正=多头,负=空头)")
    average_cost: Optional[Decimal] = Field(None, gt=0, description="平均成本价 (现货)")
    entry_price: Optional[Decimal] = Field(None, gt=0, description="开仓均价 (合约)")

    # 合约专用字段
    leverage: Optional[Decimal] = Field(None, gt=0, description="杠杆倍数 (仅合约)")
    margin_used: Optional[Decimal] = Field(None, ge=0, description="占用保证金 (仅合约)")
    liquidation_price: Optional[Decimal] = Field(None, description="强平价 (仅合约)")

    # 通用字段
    current_price: Optional[Decimal] = Field(None, description="当前市场价格")
    unrealized_pnl: Optional[Decimal] = Field(None, description="未实现盈亏(金额)")
    unrealized_pnl_percent: Optional[Decimal] = Field(None, description="未实现盈亏(百分比)")
    roe_percent: Optional[Decimal] = Field(None, description="ROE收益率% (仅合约)")
    first_buy_time: Optional[datetime] = Field(None, description="第一次买入时间")
    notes: Optional[str] = Field(None, max_length=2000, description="持仓备注")

    holding_days: Optional[int] = Field(None, ge=0, description="持仓天数")

    # 持仓状态
    is_closed: bool = Field(default=False, description="是否已清仓")
    closed_at: Optional[datetime] = Field(None, description="清仓时间")

    # 已清仓持仓专用字段
    final_price: Optional[Decimal] = Field(None, description="清仓价格 (最后一笔卖出价)")
    realized_pnl: Optional[Decimal] = Field(None, description="已实现盈亏(金额)")
    realized_pnl_percent: Optional[Decimal] = Field(None, description="已实现盈亏(百分比)")


class PositionCreate(PositionBase):
    """创建持仓记录的 Schema"""
    account_id: UUID = Field(..., description="交易账户 ID")


class PositionUpdate(BaseModel):
    """更新持仓记录的 Schema (允许部分更新)"""
    position_type: Optional[str] = None
    position_side: Optional[str] = None
    quantity: Optional[Decimal] = None
    average_cost: Optional[Decimal] = Field(None, gt=0)
    entry_price: Optional[Decimal] = Field(None, gt=0)
    leverage: Optional[Decimal] = Field(None, gt=0)
    margin_used: Optional[Decimal] = Field(None, ge=0)
    liquidation_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    unrealized_pnl: Optional[Decimal] = None
    unrealized_pnl_percent: Optional[Decimal] = None
    roe_percent: Optional[Decimal] = None
    first_buy_time: Optional[datetime] = None
    notes: Optional[str] = None

    holding_days: Optional[int] = Field(None, ge=0)


class PositionNoteUpdate(BaseModel):
    """更新持仓备注的 Schema"""
    notes: Optional[str] = Field(None, max_length=2000, description="持仓备注")


class Position(PositionBase):
    """持仓响应 Schema"""
    id: UUID
    account_id: UUID
    symbol_name: Optional[str] = Field(None, description="标的名称")
    last_updated: datetime
    average_cost: Optional[Decimal] = Field(None, ge=0, description="平均成本价 (现货)")
    entry_price: Optional[Decimal] = Field(None, ge=0, description="开仓均价 (合约)")

    # 计算属性
    total_cost: Optional[Decimal] = Field(None, description="总成本")
    market_value: Optional[Decimal] = Field(None, description="当前市值")
    is_profitable: Optional[bool] = Field(None, description="是否盈利")

    model_config = {
        "from_attributes": True  # Pydantic v2 的配置方式
    }


class PositionWithAccount(Position):
    """包含账户信息的持仓 Schema"""
    account_name: Optional[str] = Field(None, description="账户名称")
    account_type: Optional[str] = Field(None, description="账户类型")


class PositionListResponse(BaseModel):
    """持仓列表响应 Schema"""
    positions: list[Position]
    total: int = Field(..., description="总记录数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=50, description="每页记录数")
    total_pages: int = Field(..., description="总页数")


class PositionStats(BaseModel):
    """持仓统计信息 Schema"""
    total_positions: int = Field(..., description="持仓标的数量")
    total_cost: Decimal = Field(..., description="总成本")
    total_market_value: Decimal = Field(..., description="总市值")
    total_unrealized_pnl: Decimal = Field(..., description="总未实现盈亏")
    total_unrealized_pnl_percent: Decimal = Field(..., description="总未实现盈亏百分比")
    total_realized_pnl: Decimal = Field(default=Decimal('0'), description="总已实现盈亏")
    profitable_positions: int = Field(..., description="盈利持仓数量")
    losing_positions: int = Field(..., description="亏损持仓数量")
    average_holding_days: Optional[int] = Field(None, description="平均持仓天数")


class PositionPriceUpdate(BaseModel):
    """更新持仓价格的 Schema"""
    symbol: str = Field(..., description="交易标的符号")
    current_price: Decimal = Field(..., gt=0, description="当前市场价格")


class PositionPriceRefreshSelection(BaseModel):
    """按持仓ID刷新价格的 Schema"""
    position_ids: list[UUID] = Field(..., min_length=1, description="持仓ID列表")


class PositionBulkPriceUpdate(BaseModel):
    """批量更新持仓价格的 Schema"""
    prices: list[PositionPriceUpdate] = Field(..., min_length=1, description="价格更新列表")


class PositionSummary(BaseModel):
    """持仓汇总信息 Schema (用于 Dashboard)"""
    symbol: str = Field(..., description="交易标的符号")
    symbol_name: Optional[str] = Field(None, description="标的名称")
    quantity: Decimal = Field(..., description="持仓数量")
    average_cost: Decimal = Field(..., description="平均成本价")
    current_price: Optional[Decimal] = Field(None, description="当前价格")
    market_value: Optional[Decimal] = Field(None, description="市值")
    unrealized_pnl: Optional[Decimal] = Field(None, description="未实现盈亏")
    unrealized_pnl_percent: Optional[Decimal] = Field(None, description="盈亏百分比")
    holding_days: Optional[int] = Field(None, description="持仓天数")
    account_name: Optional[str] = Field(None, description="账户名称")
    account_type: Optional[str] = Field(None, description="账户类型")


class PositionsByAccountType(BaseModel):
    """按账户类型分组的持仓统计 Schema"""
    account_type: str = Field(..., description="账户类型")
    positions_count: int = Field(..., description="持仓数量")
    total_market_value: Decimal = Field(..., description="总市值")
    total_unrealized_pnl: Decimal = Field(..., description="总未实现盈亏")
    unrealized_pnl_percent: Decimal = Field(..., description="盈亏百分比")
    positions: list[PositionSummary] = Field(..., description="持仓列表")
