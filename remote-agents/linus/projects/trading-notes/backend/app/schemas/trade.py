from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from enum import Enum


class ActionType(str, Enum):
    """操作类型枚举"""
    OPEN = "open"  # 建仓(首次买入)
    ADD = "add"  # 加仓(持仓中增加)
    REDUCE = "reduce"  # 减仓(部分卖出)
    CLOSE = "close"  # 清仓(全部卖出/平仓)


class EmotionState(str, Enum):
    """情绪状态枚举"""
    CALM = "calm"  # 冷静
    CONFIDENT = "confident"  # 自信
    FEARFUL = "fearful"  # 恐惧
    GREEDY = "greedy"  # 贪婪
    FOMO = "fomo"  # 害怕踏空
    PANIC = "panic"  # 恐慌
    EXCITED = "excited"  # 兴奋
    REGRETFUL = "regretful"  # 后悔


class EntryStrategy(str, Enum):
    """入场策略枚举"""
    BOTTOM_REVERSAL = "底部反转"
    PATTERN_BREAKOUT = "形态突破"
    PULLBACK_ENTRY = "回调低吸"
    OTHER = "其他"


class ExitStrategy(str, Enum):
    """出场策略枚举"""
    TAKE_PROFIT = "止盈离场"
    STOP_LOSS = "止损离场"
    PATTERN_BREAK = "形态破坏"
    EXPECTATION_CHANGE = "预期改变"
    OTHER = "其他"


class TradeBase(BaseModel):
    """交易记录基础 Schema

    支持现货和合约交易:
    - 现货: position_side, leverage, margin 为 None
    - 合约: position_side 必填, leverage 和 margin 有值
    """
    symbol: str = Field(..., min_length=1, max_length=50, description="交易标的符号")
    side: str = Field(..., description="交易方向: buy 或 sell")
    quantity: Decimal = Field(..., gt=0, description="交易数量")
    price: Decimal = Field(..., gt=0, description="成交价格")
    fee: Decimal = Field(default=Decimal("0"), ge=0, description="手续费")
    fee_currency: Optional[str] = Field(None, max_length=10, description="手续费币种")
    trade_time: datetime = Field(..., description="交易时间")
    trade_id_external: Optional[str] = Field(None, max_length=100, description="交易所原始交易ID")
    notes: Optional[str] = Field(None, description="备注")

    # 合约交易专用字段
    position_side: Optional[str] = Field(None, max_length=10, description="持仓方向: LONG, SHORT (仅合约)")
    leverage: Optional[Decimal] = Field(None, gt=0, description="杠杆倍数 (仅合约)")
    margin: Optional[Decimal] = Field(None, ge=0, description="占用保证金 (仅合约)")

    # 交易理由和K线图字段
    action_type: Optional[ActionType] = Field(None, description="操作类型: open, add, reduce, close")
    action_reason: Optional[str] = Field(None, description="操作理由")
    action_strategy: Optional[str] = Field(None, max_length=100, description="操作策略")
    chart_image_url: Optional[str] = Field(None, max_length=500, description="K线图截图URL")
    chart_data: Optional[Dict[str, Any]] = Field(None, description="K线数据快照")

    @field_validator('side')
    @classmethod
    def validate_side(cls, v: str) -> str:
        """验证交易方向"""
        if v.lower() not in ['buy', 'sell']:
            raise ValueError('side must be "buy" or "sell"')
        return v.lower()

    @field_validator('position_side')
    @classmethod
    def validate_position_side(cls, v: Optional[str]) -> Optional[str]:
        """验证持仓方向"""
        if v is not None and v.upper() not in ['LONG', 'SHORT', 'BOTH']:
            raise ValueError('position_side must be "LONG", "SHORT", or "BOTH"')
        return v.upper() if v else None


class TradeCreate(TradeBase):
    """创建交易记录的 Schema"""
    account_id: UUID = Field(..., description="交易账户 ID")
    sync_source: str = Field(default="manual", description="数据来源: api, manual, import")

    @field_validator('sync_source')
    @classmethod
    def validate_sync_source(cls, v: str) -> str:
        """验证数据来源"""
        valid_sources = ['api', 'manual', 'import']
        if v.lower() not in valid_sources:
            raise ValueError(f'sync_source must be one of: {", ".join(valid_sources)}')
        return v.lower()


class TradeUpdate(BaseModel):
    """更新交易记录的 Schema (允许部分更新)"""
    symbol: Optional[str] = Field(None, min_length=1, max_length=50)
    side: Optional[str] = None
    quantity: Optional[Decimal] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)
    fee: Optional[Decimal] = Field(None, ge=0)
    fee_currency: Optional[str] = Field(None, max_length=10)
    trade_time: Optional[datetime] = None
    notes: Optional[str] = None

    # 合约字段
    position_side: Optional[str] = None
    leverage: Optional[Decimal] = Field(None, gt=0)
    margin: Optional[Decimal] = Field(None, ge=0)

    # 交易理由和K线图字段
    action_type: Optional[ActionType] = None
    action_reason: Optional[str] = None
    action_strategy: Optional[str] = Field(None, max_length=100)
    chart_image_url: Optional[str] = Field(None, max_length=500)

    @field_validator('side')
    @classmethod
    def validate_side(cls, v: Optional[str]) -> Optional[str]:
        """验证交易方向"""
        if v is not None and v.lower() not in ['buy', 'sell']:
            raise ValueError('side must be "buy" or "sell"')
        return v.lower() if v else None

    @field_validator('position_side')
    @classmethod
    def validate_position_side(cls, v: Optional[str]) -> Optional[str]:
        """验证持仓方向"""
        if v is not None and v.upper() not in ['LONG', 'SHORT', 'BOTH']:
            raise ValueError('position_side must be "LONG", "SHORT", or "BOTH"')
        return v.upper() if v else None


class Trade(TradeBase):
    """交易记录响应 Schema"""
    id: UUID
    account_id: UUID
    symbol_name: Optional[str] = Field(None, description="标的名称")
    sync_source: str
    created_at: datetime
    updated_at: datetime

    # Phase 4: 纪律分析字段
    emotion_state: Optional[str] = None
    emotion_intensity: Optional[int] = None
    planned_stop_loss: Optional[Decimal] = None
    actual_stop_loss: Optional[Decimal] = None
    stop_loss_executed: Optional[bool] = None
    planned_take_profit: Optional[Decimal] = None
    actual_take_profit: Optional[Decimal] = None
    entry_strategy: Optional[str] = None
    exit_strategy: Optional[str] = None
    action_strategy: Optional[str] = None
    reviewed: bool = False
    reviewed_at: Optional[datetime] = None

    # 计算属性
    total_amount: Optional[Decimal] = Field(None, description="交易总金额 (不含手续费)")
    total_cost: Optional[Decimal] = Field(None, description="交易总成本 (含手续费)")

    model_config = {
        "from_attributes": True  # Pydantic v2 的配置方式
    }

    @field_validator('position_side')
    @classmethod
    def validate_position_side(cls, v: Optional[str]) -> Optional[str]:
        """验证持仓方向 - 允许 LONG, SHORT, BOTH, 以及 None (现货)"""
        if v is not None and v.upper() not in ['LONG', 'SHORT', 'BOTH']:
            raise ValueError('position_side must be "LONG", "SHORT", or "BOTH"')
        return v.upper() if v else None


class TradeWithAccount(Trade):
    """包含账户信息的交易记录 Schema"""
    account_name: Optional[str] = Field(None, description="账户名称")
    account_type: Optional[str] = Field(None, description="账户类型")


class TradeListResponse(BaseModel):
    """交易记录列表响应 Schema"""
    trades: list[Trade]
    total: int = Field(..., description="总记录数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=50, description="每页记录数")
    total_pages: int = Field(..., description="总页数")


class TradeStats(BaseModel):
    """交易统计信息 Schema"""
    total_trades: int = Field(..., description="总交易次数")
    buy_count: int = Field(..., description="买入次数")
    sell_count: int = Field(..., description="卖出次数")
    total_volume: Decimal = Field(..., description="总交易量 (按金额)")
    total_fees: Decimal = Field(..., description="总手续费")
    unique_symbols: int = Field(..., description="交易标的数量")
    first_trade_date: Optional[datetime] = Field(None, description="第一笔交易日期")
    last_trade_date: Optional[datetime] = Field(None, description="最后一笔交易日期")


class TradeBulkCreate(BaseModel):
    """批量创建交易记录的 Schema"""
    account_id: UUID = Field(..., description="交易账户 ID")
    trades: list[TradeBase] = Field(..., min_length=1, description="交易记录列表")
    sync_source: str = Field(default="import", description="数据来源")
    skip_duplicates: bool = Field(default=True, description="是否跳过重复记录")

    @field_validator('sync_source')
    @classmethod
    def validate_sync_source(cls, v: str) -> str:
        """验证数据来源"""
        valid_sources = ['api', 'manual', 'import']
        if v.lower() not in valid_sources:
            raise ValueError(f'sync_source must be one of: {", ".join(valid_sources)}')
        return v.lower()


class TradeBulkCreateResponse(BaseModel):
    """批量创建交易记录的响应 Schema"""
    success_count: int = Field(..., description="成功创建的记录数")
    failed_count: int = Field(..., description="失败的记录数")
    duplicate_count: int = Field(..., description="重复跳过的记录数")
    created_trades: list[Trade] = Field(..., description="成功创建的交易记录")


# ============ Phase 4: Trade Review Schemas ============

class TradeReviewData(BaseModel):
    """交易补录数据 Schema"""
    action_type: Optional[ActionType] = Field(None, description="操作类型")
    action_reason: Optional[str] = Field(None, description="操作理由")
    emotion_state: Optional[EmotionState] = Field(None, description="情绪状态")
    emotion_intensity: Optional[int] = Field(None, ge=1, le=10, description="情绪强度 1-10")
    planned_stop_loss: Optional[Decimal] = Field(None, gt=0, description="计划止损价")
    actual_stop_loss: Optional[Decimal] = Field(None, gt=0, description="实际止损价")
    stop_loss_executed: Optional[bool] = Field(None, description="是否执行止损")
    planned_take_profit: Optional[Decimal] = Field(None, gt=0, description="计划止盈价")
    actual_take_profit: Optional[Decimal] = Field(None, gt=0, description="实际止盈价")
    entry_strategy: Optional[EntryStrategy] = Field(None, description="入场策略")
    exit_strategy: Optional[ExitStrategy] = Field(None, description="出场策略")
    action_strategy: Optional[str] = Field(None, max_length=100, description="操作策略")
    notes: Optional[str] = Field(None, description="补充备注")


class TradeReviewRequest(TradeReviewData):
    """单笔交易补录请求"""
    pass


class BatchReviewRequest(BaseModel):
    """批量交易补录请求"""
    trade_ids: list[UUID] = Field(..., min_length=1, description="要补录的交易ID列表")
    common_data: Dict[str, Any] = Field(..., description="通用补录数据(应用到所有交易)")


class UnreviewedTradesQuery(BaseModel):
    """查询未复盘交易参数"""
    days: int = Field(default=7, ge=1, le=90, description="查询最近N天的未复盘交易")
    account_id: Optional[UUID] = Field(None, description="筛选特定账户")
