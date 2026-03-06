from fastapi import APIRouter, Depends, HTTPException, status, Header, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from decimal import Decimal

from ....core.database import get_db
from ....core.security import decode_token
from ....models.trade import Trade as TradeModel
from ....models.trade_account import TradeAccount as TradeAccountModel
from ....schemas.trade import (
    Trade, TradeCreate, TradeUpdate, TradeWithAccount,
    TradeListResponse, TradeStats, TradeBulkCreate, TradeBulkCreateResponse, ActionType,
    TradeReviewRequest, BatchReviewRequest
)
from ....services.trade_service import TradeService
from ....services.trade_review_service import TradeReviewService
from ....services.market_data_service import get_market_data_service

router = APIRouter()


async def enrich_trade_symbol_names(trades: List[TradeModel], db: Session):
    """为交易记录补充标的名称 (按账户市场分别补全)"""
    missing_trades = [trade for trade in trades if not trade.symbol_name]
    if not missing_trades:
        return

    account_ids = list({trade.account_id for trade in missing_trades})
    account_rows = db.query(TradeAccountModel.id, TradeAccountModel.account_type).filter(
        TradeAccountModel.id.in_(account_ids)
    ).all()
    account_type_map = {row[0]: row[1] for row in account_rows}

    missing_a_stock: List[str] = []
    missing_us_stock: List[str] = []

    for trade in missing_trades:
        account_type = (account_type_map.get(trade.account_id) or "").lower()
        if account_type == "a_stock":
            missing_a_stock.append(trade.symbol)
        elif account_type == "us_stock":
            missing_us_stock.append(trade.symbol)

    if not missing_a_stock and not missing_us_stock:
        return

    market_service = get_market_data_service()
    fetched: dict[str, str] = {}
    if missing_a_stock:
        fetched.update(await market_service.fetch_a_stock_names(missing_a_stock))
    if missing_us_stock:
        fetched.update(await market_service.fetch_us_stock_names(missing_us_stock))

    if not fetched:
        return

    for trade in missing_trades:
        if not trade.symbol_name and trade.symbol in fetched:
            trade.symbol_name = fetched[trade.symbol]


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


@router.get("/", response_model=TradeListResponse)
async def get_trades(
    account_id: Optional[UUID] = None,
    account_type: Optional[str] = None,
    broker: Optional[str] = None,
    symbol: Optional[str] = None,
    side: Optional[str] = None,
    sync_source: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取交易记录列表 (支持分页和过滤)"""

    # 基础查询: 只查询当前用户的交易账户下的交易
    query = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id
    )

    # 应用过滤条件
    if account_id:
        query = query.filter(TradeModel.account_id == account_id)

    if account_type:
        query = query.filter(TradeAccountModel.account_type == account_type.lower())

    if broker:
        query = query.filter(func.lower(TradeAccountModel.broker) == broker.lower())

    if symbol:
        query = query.filter(TradeModel.symbol.ilike(f"%{symbol}%"))

    if side:
        query = query.filter(TradeModel.side == side.lower())

    if sync_source:
        query = query.filter(TradeModel.sync_source == sync_source.lower())

    if start_date:
        query = query.filter(TradeModel.trade_time >= start_date)

    if end_date:
        query = query.filter(TradeModel.trade_time <= end_date)

    # 计算总数
    total = query.count()

    # 分页查询 (按交易时间降序)
    trades = query.order_by(desc(TradeModel.trade_time)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    await enrich_trade_symbol_names(trades, db)

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return TradeListResponse(
        trades=trades,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("/", response_model=Trade, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade_data: TradeCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """创建单条交易记录（支持自动判断操作类型）"""

    # 验证交易账户是否属于当前用户
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == trade_data.account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found or does not belong to you"
        )

    # 检查是否重复 (如果有 trade_id_external)
    if trade_data.trade_id_external:
        existing = db.query(TradeModel).filter(
            TradeModel.account_id == trade_data.account_id,
            TradeModel.trade_id_external == trade_data.trade_id_external
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Trade with this external ID already exists"
            )

    # 如果没有指定 action_type，自动推断
    if not trade_data.action_type:
        trade_service = TradeService(db)
        inferred_action_type = trade_service.infer_action_type(
            symbol=trade_data.symbol,
            side=trade_data.side,
            quantity=trade_data.quantity,
            account_id=trade_data.account_id,
            position_side=trade_data.position_side,
            trade_time=trade_data.trade_time
        )

        # 将推断结果设置到 trade_data
        if inferred_action_type:
            trade_data.action_type = inferred_action_type

    # 创建交易记录
    db_trade = TradeModel(**trade_data.model_dump())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)

    return db_trade


@router.get("/{trade_id}", response_model=Trade)
async def get_trade(
    trade_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取单条交易记录详情"""

    trade = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeModel.id == trade_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )

    await enrich_trade_symbol_names([trade], db)
    return trade


@router.put("/{trade_id}", response_model=Trade)
async def update_trade(
    trade_id: UUID,
    trade_data: TradeUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新交易记录"""

    trade = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeModel.id == trade_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )

    # 更新字段
    update_data = trade_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(trade, field):
            setattr(trade, field, value)

    db.commit()
    db.refresh(trade)

    return trade


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(
    trade_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除交易记录

    删除trade后会自动重新计算该账户的positions和closed_positions
    """

    trade = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeModel.id == trade_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )

    # 保存account_id,用于后续重新计算持仓
    account_id = trade.account_id

    # 删除交易记录
    db.delete(trade)
    db.commit()

    # 重新计算该账户的持仓(会自动重新生成closed_positions)
    from ....services.position_service import PositionService
    position_service = PositionService(db)
    position_service.calculate_positions_for_account(account_id)

    return None


@router.get("/stats/summary", response_model=TradeStats)
async def get_trade_stats(
    account_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取交易统计信息"""

    # 基础查询
    query = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id
    )

    # 应用过滤
    if account_id:
        query = query.filter(TradeModel.account_id == account_id)

    if start_date:
        query = query.filter(TradeModel.trade_time >= start_date)

    if end_date:
        query = query.filter(TradeModel.trade_time <= end_date)

    trades = query.all()

    # 计算统计数据
    total_trades = len(trades)
    buy_count = sum(1 for t in trades if t.side == 'buy')
    sell_count = sum(1 for t in trades if t.side == 'sell')

    total_volume = sum(float(t.price * t.quantity) for t in trades)
    total_fees = sum(float(t.fee) for t in trades if t.fee)

    unique_symbols = len(set(t.symbol for t in trades))

    first_trade_date = min((t.trade_time for t in trades), default=None)
    last_trade_date = max((t.trade_time for t in trades), default=None)

    return TradeStats(
        total_trades=total_trades,
        buy_count=buy_count,
        sell_count=sell_count,
        total_volume=Decimal(str(total_volume)),
        total_fees=Decimal(str(total_fees)),
        unique_symbols=unique_symbols,
        first_trade_date=first_trade_date,
        last_trade_date=last_trade_date
    )


@router.post("/bulk", response_model=TradeBulkCreateResponse)
async def bulk_create_trades(
    bulk_data: TradeBulkCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """批量创建交易记录 (用于导入)"""

    # 验证账户
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == bulk_data.account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    success_count = 0
    failed_count = 0
    duplicate_count = 0
    created_trades = []

    for trade_data in bulk_data.trades:
        try:
            # 检查重复
            if trade_data.trade_id_external:
                existing = db.query(TradeModel).filter(
                    TradeModel.account_id == bulk_data.account_id,
                    TradeModel.trade_id_external == trade_data.trade_id_external
                ).first()

                if existing:
                    if bulk_data.skip_duplicates:
                        duplicate_count += 1
                        continue
                    else:
                        failed_count += 1
                        continue

            # 创建交易
            db_trade = TradeModel(
                account_id=bulk_data.account_id,
                sync_source=bulk_data.sync_source,
                **trade_data.model_dump()
            )
            db.add(db_trade)
            db.flush()  # 刷新以获取 ID，但不提交
            db.refresh(db_trade)
            created_trades.append(db_trade)
            success_count += 1

        except Exception as e:
            failed_count += 1
            continue

    # 提交所有成功的交易
    db.commit()

    return TradeBulkCreateResponse(
        success_count=success_count,
        failed_count=failed_count,
        duplicate_count=duplicate_count,
        created_trades=created_trades
    )


@router.put("/{trade_id}/rationale", response_model=Trade)
async def update_trade_rationale(
    trade_id: UUID,
    action_type: Optional[ActionType] = None,
    action_reason: Optional[str] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """单独更新交易理由和操作类型"""

    trade = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeModel.id == trade_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )

    # 更新字段
    if action_type is not None:
        trade.action_type = action_type.value if isinstance(action_type, ActionType) else action_type

    if action_reason is not None:
        trade.action_reason = action_reason

    db.commit()
    db.refresh(trade)

    return trade


@router.post("/{trade_id}/upload-chart")
async def upload_chart_image(
    trade_id: UUID,
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """上传K线图截图"""

    from ....utils.file_upload import save_upload_file, delete_upload_file

    # 验证交易记录是否属于当前用户
    trade = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeModel.id == trade_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )

    # 删除旧的图片文件(如果存在)
    if trade.chart_image_url:
        delete_upload_file(trade.chart_image_url)

    # 保存新文件
    file_path = await save_upload_file(file, "charts")

    # 更新交易记录
    trade.chart_image_url = file_path
    db.commit()
    db.refresh(trade)

    return {
        "chart_url": file_path,
        "message": "Chart image uploaded successfully"
    }


@router.get("/by-symbol/{symbol}", response_model=List[Trade])
async def get_trades_by_symbol(
    symbol: str,
    account_id: Optional[UUID] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """按标的查询所有交易（用于展示操作历史）"""

    # 基础查询
    query = db.query(TradeModel).join(
        TradeAccountModel,
        TradeModel.account_id == TradeAccountModel.id
    ).filter(
        TradeAccountModel.user_id == user_id,
        TradeModel.symbol == symbol
    )

    # 如果指定了账户，进一步过滤
    if account_id:
        query = query.filter(TradeModel.account_id == account_id)

    # 按时间正序排列(从旧到新，用于时间线展示)
    trades = query.order_by(TradeModel.trade_time).all()

    await enrich_trade_symbol_names(trades, db)
    return trades


# ============ Phase 4: Trade Review Endpoints ============

@router.put("/{trade_id}/review", response_model=Trade)
async def review_trade(
    trade_id: UUID,
    review_data: TradeReviewRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    单笔交易补录

    用于事后补充交易的情绪、止损止盈、策略等信息
    """
    review_service = TradeReviewService(db)

    try:
        trade = review_service.review_trade(trade_id, user_id, review_data)
        return trade
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to review trade: {str(e)}"
        )


@router.post("/batch-review", response_model=List[Trade])
async def batch_review_trades(
    request: BatchReviewRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    批量补录交易

    用于当晚集中补录多笔交易的通用信息
    """
    review_service = TradeReviewService(db)

    try:
        trades = review_service.batch_review_trades(
            user_id,
            request.trade_ids,
            request.common_data
        )
        return trades
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to batch review trades: {str(e)}"
        )


@router.get("/unreviewed", response_model=List[Trade])
async def get_unreviewed_trades(
    days: int = Query(7, ge=1, le=90, description="查询最近N天的未复盘交易"),
    account_id: Optional[UUID] = Query(None, description="筛选特定账户"),
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取未复盘的交易

    返回指定天数内尚未补录的交易记录，用于提醒用户
    """
    review_service = TradeReviewService(db)

    try:
        trades = review_service.get_unreviewed_trades(user_id, days, account_id)
        return trades
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch unreviewed trades: {str(e)}"
        )
