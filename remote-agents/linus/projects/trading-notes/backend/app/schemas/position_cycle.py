from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class PositionCycleBase(BaseModel):
    """持仓周期基础 Schema"""
    symbol: str = Field(..., description="交易标的")
    primary_strategy: Optional[str] = Field(None, description="主要策略")
    what_went_well: Optional[str] = Field(None, description="做得好的地方")
    what_to_improve: Optional[str] = Field(None, description="需要改进的地方")
    lessons_learned: Optional[str] = Field(None, description="经验教训")


class PositionCycle(PositionCycleBase):
    """持仓周期响应 Schema"""
    id: UUID
    user_id: UUID
    account_id: UUID

    # 周期时间
    open_time: datetime
    close_time: Optional[datetime]
    status: str  # 'open' or 'closed'

    # 关联交易
    trade_ids: List[UUID]

    # 情绪评估
    dominant_emotion: Optional[str]
    emotion_stability: Optional[int]

    # 持仓统计
    total_quantity: Optional[Decimal]
    average_entry_price: Optional[Decimal]
    average_exit_price: Optional[Decimal]
    total_profit_loss: Optional[Decimal]
    roi_percent: Optional[Decimal]

    # 持仓时长
    holding_hours: Optional[int]

    # 纪律评估
    followed_stop_loss: Optional[bool]
    followed_take_profit: Optional[bool]
    discipline_score: Optional[int]

    # 时间戳
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class PositionCycleDetail(PositionCycle):
    """持仓周期详情(包含交易列表)"""
    trades: Optional[List] = Field(None, description="关联的交易记录列表")


class PositionCycleReview(BaseModel):
    """持仓周期复盘请求"""
    what_went_well: Optional[str] = Field(None, description="做得好的地方")
    what_to_improve: Optional[str] = Field(None, description="需要改进的地方")
    lessons_learned: Optional[str] = Field(None, description="经验教训")


class AutoDetectRequest(BaseModel):
    """自动识别持仓周期请求"""
    account_id: UUID = Field(..., description="交易账户ID")
    symbol: str = Field(..., description="交易标的")


class PositionCycleListResponse(BaseModel):
    """持仓周期列表响应"""
    cycles: List[PositionCycle]
    total: int = Field(..., description="总记录数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=20, description="每页记录数")
    total_pages: int = Field(..., description="总页数")
