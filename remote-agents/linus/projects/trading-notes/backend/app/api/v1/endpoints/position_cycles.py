from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from math import ceil

from ....core.database import get_db
from ....core.security import decode_token
from ....models.position_cycle import PositionCycle as PositionCycleModel
from ....models.trade import Trade as TradeModel
from ....schemas.position_cycle import (
    PositionCycle, PositionCycleDetail, PositionCycleReview,
    AutoDetectRequest, PositionCycleListResponse
)
from ....schemas.trade import Trade as TradeSchema
from ....services.position_cycle_service import PositionCycleService

router = APIRouter()


def get_current_user_id(authorization: str = Header(...)) -> UUID:
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


@router.get("/", response_model=PositionCycleListResponse)
async def list_position_cycles(
    account_id: Optional[UUID] = None,
    symbol: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)
    cycles, total = service.list_cycles(
        user_id=current_user_id,
        account_id=account_id,
        symbol=symbol,
        status=status,
        page=page,
        page_size=page_size
    )

    total_pages = ceil(total / page_size) if page_size > 0 else 0

    return PositionCycleListResponse(
        cycles=[PositionCycle.model_validate(c) for c in cycles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{cycle_id}", response_model=PositionCycleDetail)
async def get_position_cycle(
    cycle_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)
    cycle = service.get_cycle(cycle_id, current_user_id)

    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position cycle not found"
        )

    trades = db.query(TradeModel).filter(
        TradeModel.id.in_(cycle.trade_ids)
    ).order_by(TradeModel.trade_time).all()

    cycle_dict = PositionCycle.model_validate(cycle).model_dump()
    cycle_dict['trades'] = [TradeSchema.model_validate(t) for t in trades]

    return PositionCycleDetail(**cycle_dict)


@router.post("/auto-detect", response_model=List[PositionCycle])
async def auto_detect_cycles(
    request: AutoDetectRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)

    try:
        cycles = service.auto_detect_position_cycles(
            account_id=request.account_id,
            symbol=request.symbol,
            user_id=current_user_id
        )

        return [PositionCycle.model_validate(c) for c in cycles]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect position cycles: {str(e)}"
        )


@router.post("/{cycle_id}/review", response_model=PositionCycle)
async def review_position_cycle(
    cycle_id: UUID,
    review_data: PositionCycleReview,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)

    try:
        cycle = service.review_cycle(cycle_id, current_user_id, review_data)
        return PositionCycle.model_validate(cycle)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to review cycle: {str(e)}"
        )


@router.delete("/{cycle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position_cycle(
    cycle_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)

    success = service.delete_cycle(cycle_id, current_user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position cycle not found"
        )

    return None


@router.post("/{cycle_id}/recalculate", response_model=PositionCycle)
async def recalculate_cycle_metrics(
    cycle_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = PositionCycleService(db)

    cycle = service.get_cycle(cycle_id, current_user_id)
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position cycle not found"
        )

    try:
        updated_cycle = service.calculate_cycle_metrics(cycle_id)
        return PositionCycle.model_validate(updated_cycle)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to recalculate metrics: {str(e)}"
        )
