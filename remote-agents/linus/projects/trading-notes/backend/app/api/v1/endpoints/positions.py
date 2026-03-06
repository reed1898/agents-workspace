from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, case
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import logging

from ....core.database import get_db
from ....core.security import decode_token
from ....models.position import Position as PositionModel
from ....models.trade import Trade as TradeModel
from ....models.trade_account import TradeAccount as TradeAccountModel
from ....schemas.position import (
    Position, PositionCreate, PositionUpdate, PositionWithAccount,
    PositionListResponse, PositionStats, PositionPriceUpdate,
    PositionBulkPriceUpdate, PositionSummary, PositionsByAccountType,
    PositionNoteUpdate, PositionPriceRefreshSelection
)
from ....utils.symbol_name import extract_symbol_name
from ....services.market_data_service import get_market_data_service

router = APIRouter()
logger = logging.getLogger(__name__)


def get_current_user_id(authorization: str = Header(...)) -> UUID:
    """从 JWT Token 获取当前用户 ID"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return UUID(user_id)


def build_symbol_name_map(
    db: Session,
    user_id: UUID,
    symbols: List[str],
    account_id: Optional[UUID] = None
) -> dict[str, str]:
    """从交易备注中解析标的名称映射"""
    if not symbols:
        return {}

    query = db.query(TradeModel.symbol, TradeModel.notes).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        TradeModel.symbol.in_(symbols)
    )

    if account_id:
        query = query.filter(TradeModel.account_id == account_id)

    query = query.order_by(desc(TradeModel.trade_time))

    symbol_name_map: dict[str, str] = {}
    for symbol_value, notes in query:
        if symbol_value in symbol_name_map:
            continue
        name = extract_symbol_name(notes)
        if name:
            symbol_name_map[symbol_value] = name

    return symbol_name_map


async def enrich_symbol_name_map(symbols: List[str], symbol_name_map: dict[str, str]) -> dict[str, str]:
    """使用行情接口补全标的名称(A股)"""
    missing_symbols = [symbol for symbol in symbols if symbol not in symbol_name_map]
    if not missing_symbols:
        return symbol_name_map

    try:
        market_service = get_market_data_service()
        fetched = await market_service.fetch_a_stock_names(missing_symbols)
        if fetched:
            symbol_name_map.update(fetched)
    except Exception as exc:
        logger.warning("Failed to enrich A-stock names: %s", exc, exc_info=True)

    return symbol_name_map


@router.get("/", response_model=PositionListResponse)
async def get_positions(
    account_id: Optional[UUID] = None,
    account_type: Optional[str] = Query(None, description="筛选账户类型"),
    symbol: Optional[str] = None,
    is_closed: Optional[bool] = Query(None, description="筛选持仓状态: None=全部, False=持仓中, True=已清仓"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取持仓列表 (支持分页和过滤)

    参数:
    - account_id: 筛选特定账户
    - account_type: 筛选账户类型
    - symbol: 筛选标的符号 (支持模糊搜索)
    - is_closed: 筛选持仓状态 (None=全部, False=持仓中, True=已清仓)
    - page: 页码
    - page_size: 每页大小
    """

    # 基础查询: 只查询当前用户的交易账户下的持仓
    query = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id
    )

    # 应用过滤条件
    if account_id:
        query = query.filter(PositionModel.account_id == account_id)

    if account_type:
        query = query.filter(TradeAccountModel.account_type == account_type)

    if symbol:
        query = query.filter(PositionModel.symbol.ilike(f"%{symbol}%"))

    if is_closed is not None:
        query = query.filter(PositionModel.is_closed == is_closed)
        is_closed_filter = is_closed
    else:
        # 默认只显示持仓中的记录
        query = query.filter(PositionModel.is_closed == False)
        is_closed_filter = False

    # 计算总数
    total = query.count()

    # 分页查询 (持仓按市值降序, 已清仓按清仓时间倒序)
    if is_closed_filter:
        # MySQL 不支持 NULLS LAST，使用 CASE 兼容处理
        closed_at_nulls_last = case(
            (PositionModel.closed_at.is_(None), 1),
            else_=0
        )
        positions = query.order_by(
            closed_at_nulls_last,
            desc(PositionModel.closed_at),
            desc(PositionModel.last_updated)
        ).offset((page - 1) * page_size).limit(page_size).all()
    else:
        positions = query.order_by(
            desc(PositionModel.quantity * PositionModel.current_price)
        ).offset((page - 1) * page_size).limit(page_size).all()

    symbol_name_map = build_symbol_name_map(
        db,
        user_id,
        [position.symbol for position in positions],
        account_id
    )
    symbol_name_map = await enrich_symbol_name_map(
        [position.symbol for position in positions],
        symbol_name_map
    )
    for position in positions:
        position.symbol_name = symbol_name_map.get(position.symbol)

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return PositionListResponse(
        positions=positions,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{position_id}", response_model=Position)
async def get_position(
    position_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取单个持仓详情"""

    position = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        PositionModel.id == position_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    symbol_name_map = build_symbol_name_map(
        db,
        user_id,
        [position.symbol],
        position.account_id
    )
    symbol_name_map = await enrich_symbol_name_map([position.symbol], symbol_name_map)
    position.symbol_name = symbol_name_map.get(position.symbol)

    return position


@router.get("/stats/summary", response_model=PositionStats)
async def get_position_stats(
    account_id: Optional[UUID] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取持仓统计信息"""

    # 基础查询: 只统计持仓中的记录
    query = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.is_closed == False
    )

    # 应用过滤
    if account_id:
        query = query.filter(PositionModel.account_id == account_id)

    positions = query.all()

    # 计算统计数据
    total_positions = len(positions)

    total_cost = 0.0
    total_market_value = 0.0
    total_unrealized_pnl = 0.0

    for position in positions:
        position_cost = float(position.total_cost or 0)
        market_value = float(position.market_value or 0)
        total_cost += position_cost
        total_market_value += market_value

        if position.unrealized_pnl is not None:
            total_unrealized_pnl += float(position.unrealized_pnl)
        elif position.current_price is not None:
            total_unrealized_pnl += market_value - position_cost

    total_unrealized_pnl_percent = (
        (total_unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
    )

    profitable_positions = sum(
        1 for p in positions
        if p.unrealized_pnl and float(p.unrealized_pnl) > 0
    )

    losing_positions = sum(
        1 for p in positions
        if p.unrealized_pnl and float(p.unrealized_pnl) < 0
    )

    # 计算平均持仓天数
    holding_days_list = [p.holding_days for p in positions if p.holding_days]
    average_holding_days = (
        sum(holding_days_list) // len(holding_days_list)
        if holding_days_list else None
    )

    # 计算已实现盈亏 (从已清仓的持仓中获取)
    closed_positions_query = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.is_closed == True
    )

    if account_id:
        closed_positions_query = closed_positions_query.filter(PositionModel.account_id == account_id)

    closed_positions = closed_positions_query.all()

    total_realized_pnl = sum(
        float(p.realized_pnl) if p.realized_pnl else 0
        for p in closed_positions
    )

    return PositionStats(
        total_positions=total_positions,
        total_cost=Decimal(str(total_cost)),
        total_market_value=Decimal(str(total_market_value)),
        total_unrealized_pnl=Decimal(str(total_unrealized_pnl)),
        total_unrealized_pnl_percent=Decimal(str(total_unrealized_pnl_percent)),
        total_realized_pnl=Decimal(str(total_realized_pnl)),
        profitable_positions=profitable_positions,
        losing_positions=losing_positions,
        average_holding_days=average_holding_days
    )


@router.patch("/{position_id}/notes", response_model=Position)
async def update_position_notes(
    position_id: UUID,
    payload: PositionNoteUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新持仓备注"""
    position = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        PositionModel.id == position_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    notes_value = payload.notes.strip() if payload.notes else None
    position.notes = notes_value

    db.commit()
    db.refresh(position)

    symbol_name_map = build_symbol_name_map(
        db,
        user_id,
        [position.symbol],
        position.account_id
    )
    symbol_name_map = await enrich_symbol_name_map([position.symbol], symbol_name_map)
    position.symbol_name = symbol_name_map.get(position.symbol)

    return position


@router.post("/update-price", response_model=Position)
async def update_position_price(
    price_update: PositionPriceUpdate,
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新单个持仓的价格"""

    # 验证账户
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 查找持仓
    position = db.query(PositionModel).filter(
        PositionModel.account_id == account_id,
        PositionModel.symbol == price_update.symbol
    ).first()

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    # 更新价格和盈亏
    position.update_price_and_pnl(float(price_update.current_price))
    position.update_holding_days()

    db.commit()
    db.refresh(position)

    return position


@router.post("/update-prices-bulk")
async def bulk_update_prices(
    bulk_update: PositionBulkPriceUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """批量更新持仓价格"""

    updated_count = 0
    failed_count = 0

    for price_update in bulk_update.prices:
        try:
            # 查找所有账户下的该标的持仓
            positions = db.query(PositionModel).join(
                TradeAccountModel,
                PositionModel.account_id == TradeAccountModel.id
            ).filter(
                TradeAccountModel.user_id == user_id,
                PositionModel.symbol == price_update.symbol
            ).all()

            for position in positions:
                position.update_price_and_pnl(float(price_update.current_price))
                position.update_holding_days()
                updated_count += 1

        except Exception:
            failed_count += 1
            continue

    db.commit()

    return {
        "updated_count": updated_count,
        "failed_count": failed_count
    }


@router.get("/summary/by-account", response_model=List[PositionSummary])
async def get_positions_summary(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取所有持仓汇总 (用于 Dashboard)"""

    positions = db.query(
        PositionModel,
        TradeAccountModel.account_name,
        TradeAccountModel.account_type
    ).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.is_closed == False
    ).order_by(
        desc(PositionModel.quantity * PositionModel.current_price)
    ).all()

    symbol_name_map = build_symbol_name_map(
        db,
        user_id,
        [position.symbol for position, _, _ in positions]
    )
    symbol_name_map = await enrich_symbol_name_map(
        [position.symbol for position, _, _ in positions],
        symbol_name_map
    )

    summaries = []
    for position, account_name, account_type in positions:
        # 合约使用 entry_price,现货使用 average_cost
        if position.position_type == 'futures':
            cost_price = position.entry_price or Decimal('0')
        else:
            cost_price = position.average_cost or Decimal('0')

        summary = PositionSummary(
            symbol=position.symbol,
            symbol_name=symbol_name_map.get(position.symbol),
            quantity=position.quantity,
            average_cost=cost_price,
            current_price=position.current_price or Decimal('0'),
            market_value=Decimal(str(position.market_value)) if position.market_value else Decimal('0'),
            unrealized_pnl=position.unrealized_pnl or Decimal('0'),
            unrealized_pnl_percent=position.unrealized_pnl_percent or Decimal('0'),
            holding_days=position.holding_days or 0,
            account_name=account_name,
            account_type=account_type
        )
        summaries.append(summary)

    return summaries


@router.get("/summary/by-type", response_model=List[PositionsByAccountType])
async def get_positions_by_account_type(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """按账户类型分组的持仓统计"""

    # 查询所有持仓及账户信息 (只统计持仓中的)
    positions_data = db.query(
        PositionModel,
        TradeAccountModel.account_name,
        TradeAccountModel.account_type
    ).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.is_closed == False
    ).all()

    symbol_name_map = build_symbol_name_map(
        db,
        user_id,
        [position.symbol for position, _, _ in positions_data]
    )
    symbol_name_map = await enrich_symbol_name_map(
        [position.symbol for position, _, _ in positions_data],
        symbol_name_map
    )

    # 按账户类型分组
    grouped = {}
    for position, account_name, account_type in positions_data:
        if account_type not in grouped:
            grouped[account_type] = []

        # 合约使用 entry_price,现货使用 average_cost
        if position.position_type == 'futures':
            cost_price = position.entry_price or Decimal('0')
        else:
            cost_price = position.average_cost or Decimal('0')

        summary = PositionSummary(
            symbol=position.symbol,
            symbol_name=symbol_name_map.get(position.symbol),
            quantity=position.quantity,
            average_cost=cost_price,
            current_price=position.current_price or Decimal('0'),
            market_value=Decimal(str(position.market_value)) if position.market_value else Decimal('0'),
            unrealized_pnl=position.unrealized_pnl or Decimal('0'),
            unrealized_pnl_percent=position.unrealized_pnl_percent or Decimal('0'),
            holding_days=position.holding_days or 0,
            account_name=account_name,
            account_type=account_type
        )
        grouped[account_type].append(summary)

    # 计算每个类型的统计
    result = []
    for account_type, positions in grouped.items():
        total_market_value = sum(
            float(p.market_value or 0) for p in positions
        )
        # 处理现货和合约的成本计算
        total_cost = sum(
            float(abs(p.quantity) * p.average_cost) if p.average_cost else 0
            for p in positions
        )
        total_unrealized_pnl = sum(
            float(p.unrealized_pnl or 0) for p in positions
        )
        unrealized_pnl_percent = (
            (total_unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
        )

        result.append(PositionsByAccountType(
            account_type=account_type,
            positions_count=len(positions),
            total_market_value=Decimal(str(total_market_value)),
            total_unrealized_pnl=Decimal(str(total_unrealized_pnl)),
            unrealized_pnl_percent=Decimal(str(unrealized_pnl_percent)),
            positions=positions
        ))

    return result


@router.get("/symbol/{symbol}", response_model=Position)
async def get_position_by_symbol(
    symbol: str,
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """根据标的和账户ID获取持仓详情"""

    # 验证账户权限
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 查询持仓
    position = db.query(PositionModel).filter(
        PositionModel.account_id == account_id,
        PositionModel.symbol == symbol
    ).first()

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    symbol_name_map = build_symbol_name_map(db, user_id, [position.symbol], account_id)
    symbol_name_map = await enrich_symbol_name_map([position.symbol], symbol_name_map)
    position.symbol_name = symbol_name_map.get(position.symbol)

    return position


@router.post("/refresh-prices/selection")
async def refresh_selected_positions_prices(
    payload: PositionPriceRefreshSelection,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """刷新指定持仓列表的实时价格"""
    if not payload.position_ids:
        return {
            "updated_count": 0,
            "failed_count": 0,
            "total_positions": 0,
            "message": "No positions to update"
        }

    positions_rows = db.query(PositionModel, TradeAccountModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.id.in_(payload.position_ids)
    ).all()

    if not positions_rows:
        return {
            "updated_count": 0,
            "failed_count": len(payload.position_ids),
            "total_positions": 0,
            "message": "No positions found"
        }

    missing_count = max(len(payload.position_ids) - len(positions_rows), 0)

    market_service = get_market_data_service()
    updated_count = 0
    failed_count = missing_count

    for position, account in positions_rows:
        try:
            position.account = account
            current_price = await market_service.get_current_price(
                position.symbol,
                account.account_type,
                force_refresh=True
            )
            if current_price is None:
                failed_count += 1
                continue
            if position.is_closed:
                position.current_price = Decimal(str(current_price))
                position.last_updated = datetime.utcnow()
            else:
                position.update_price_and_pnl(float(current_price))
                position.update_holding_days()
            updated_count += 1
        except Exception:
            failed_count += 1
            continue

    db.commit()

    return {
        "updated_count": updated_count,
        "failed_count": failed_count,
        "total_positions": len(positions_rows),
        "message": "价格刷新完成"
    }


@router.post("/refresh-prices")
async def refresh_all_positions_prices(
    account_id: Optional[UUID] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """刷新持仓的实时价格（使用MarketDataService）

    Args:
        account_id: 可选，指定账户ID，如果为空则刷新用户所有账户的持仓

    Returns:
        {
            "updated_count": 更新成功的数量,
            "failed_count": 更新失败的数量,
            "message": 结果消息
        }
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== Refresh prices called for user_id={user_id}, account_id={account_id} ===")

    # 查询用户的持仓（需要预加载 account 关系） - 只刷新持仓中的
    query = db.query(PositionModel).join(
        TradeAccountModel,
        PositionModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        PositionModel.is_closed == False
    )

    if account_id:
        query = query.filter(PositionModel.account_id == account_id)

    total_positions = query.count()
    logger.info(f"Found {total_positions} positions to update")

    if total_positions == 0:
        logger.info("No positions found, returning early")
        return {
            "updated_count": 0,
            "failed_count": 0,
            "message": "No positions to update"
        }

    from ....tasks.sync_tasks import refresh_position_prices

    task = refresh_position_prices.delay(str(user_id), str(account_id) if account_id else None)

    return {
        "status": "queued",
        "task_id": task.id,
        "updated_count": 0,
        "failed_count": 0,
        "total_positions": total_positions,
        "message": "价格刷新任务已提交"
    }


@router.get("/refresh-prices/task/{task_id}")
async def get_refresh_prices_task_status(
    task_id: str,
    user_id: UUID = Depends(get_current_user_id)
):
    """查询刷新价格任务状态"""
    from celery.result import AsyncResult
    from ....core.celery_app import celery_app

    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.state,
    }

    if task_result.state == 'PENDING':
        response["message"] = "Task is waiting to be executed"
    elif task_result.state == 'PROGRESS':
        response["message"] = "Task is in progress"
        response["meta"] = task_result.info
    elif task_result.state == 'SUCCESS':
        response["message"] = "Task completed successfully"
        response["result"] = task_result.result
    elif task_result.state == 'FAILURE':
        response["message"] = "Task failed"
        response["error"] = str(task_result.info)
    else:
        response["message"] = f"Task status: {task_result.state}"

    return response
