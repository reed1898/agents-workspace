from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from decimal import Decimal

from ....core.database import get_db
from ....models.closed_position import ClosedPosition
from ....models.trade_account import TradeAccount
from ....schemas.closed_position import (
    ClosedPositionResponse,
    ClosedPositionListResponse,
    ClosedPositionStats
)

router = APIRouter()


@router.get("/account/{account_id}", response_model=ClosedPositionListResponse)
def get_closed_positions_by_account(
    account_id: UUID,
    symbol: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    获取指定账户的已平仓记录

    Args:
        account_id: 账户ID
        symbol: 可选,按标的筛选
        skip: 跳过记录数
        limit: 返回记录数
    """
    # 验证账户是否存在
    account = db.query(TradeAccount).filter(TradeAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # 构建查询
    query = db.query(ClosedPosition).filter(
        ClosedPosition.account_id == account_id
    )

    if symbol:
        query = query.filter(ClosedPosition.symbol == symbol)

    # 按平仓时间倒序
    query = query.order_by(ClosedPosition.close_time.desc())

    # 获取总数
    total = query.count()

    # 获取分页数据
    positions = query.offset(skip).limit(limit).all()

    # 计算统计数据
    profitable_count = len([p for p in positions if p.realized_pnl > 0])
    losing_count = len([p for p in positions if p.realized_pnl < 0])
    total_realized_pnl = sum((p.realized_pnl for p in positions), Decimal('0'))
    win_rate = (profitable_count / total * 100) if total > 0 else 0.0

    return ClosedPositionListResponse(
        positions=[ClosedPositionResponse.from_orm(p) for p in positions],
        total=total,
        profitable_count=profitable_count,
        losing_count=losing_count,
        total_realized_pnl=total_realized_pnl,
        win_rate=win_rate
    )


@router.get("/account/{account_id}/stats", response_model=ClosedPositionStats)
def get_closed_positions_stats(
    account_id: UUID,
    symbol: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取指定账户的已平仓统计数据

    Args:
        account_id: 账户ID
        symbol: 可选,按标的筛选
    """
    # 验证账户是否存在
    account = db.query(TradeAccount).filter(TradeAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # 构建查询
    query = db.query(ClosedPosition).filter(
        ClosedPosition.account_id == account_id
    )

    if symbol:
        query = query.filter(ClosedPosition.symbol == symbol)

    # 获取所有记录
    positions = query.all()

    if not positions:
        return ClosedPositionStats(
            total_count=0,
            profitable_count=0,
            losing_count=0,
            win_rate=0.0,
            total_realized_pnl=Decimal('0'),
            average_pnl=Decimal('0'),
            average_pnl_percent=Decimal('0'),
            average_holding_days=0.0,
            best_trade=None,
            worst_trade=None
        )

    # 计算统计数据
    total_count = len(positions)
    profitable_count = len([p for p in positions if p.realized_pnl > 0])
    losing_count = len([p for p in positions if p.realized_pnl < 0])
    win_rate = (profitable_count / total_count * 100) if total_count > 0 else 0.0

    total_realized_pnl = sum((p.realized_pnl for p in positions), Decimal('0'))
    average_pnl = total_realized_pnl / total_count if total_count > 0 else Decimal('0')

    total_pnl_percent = sum((p.realized_pnl_percent for p in positions), Decimal('0'))
    average_pnl_percent = total_pnl_percent / total_count if total_count > 0 else Decimal('0')

    holding_days_list = [p.holding_days for p in positions if p.holding_days is not None]
    average_holding_days = sum(holding_days_list) / len(holding_days_list) if holding_days_list else 0.0

    # 找出最好和最差的交易
    best_trade = max(positions, key=lambda p: float(p.realized_pnl))
    worst_trade = min(positions, key=lambda p: float(p.realized_pnl))

    return ClosedPositionStats(
        total_count=total_count,
        profitable_count=profitable_count,
        losing_count=losing_count,
        win_rate=win_rate,
        total_realized_pnl=total_realized_pnl,
        average_pnl=average_pnl,
        average_pnl_percent=average_pnl_percent,
        average_holding_days=average_holding_days,
        best_trade=ClosedPositionResponse.from_orm(best_trade),
        worst_trade=ClosedPositionResponse.from_orm(worst_trade)
    )


@router.get("/{position_id}", response_model=ClosedPositionResponse)
def get_closed_position_by_id(
    position_id: UUID,
    db: Session = Depends(get_db)
):
    """
    获取单条已平仓记录

    Args:
        position_id: 已平仓记录ID
    """
    position = db.query(ClosedPosition).filter(
        ClosedPosition.id == position_id
    ).first()

    if not position:
        raise HTTPException(status_code=404, detail="Closed position not found")

    return ClosedPositionResponse.from_orm(position)
