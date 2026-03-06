from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from ....core.database import get_db
from ....core.security import decode_token
from ....services.discipline_analytics_service import DisciplineAnalyticsService

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


@router.get("/stop-loss-discipline")
async def get_stop_loss_discipline(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Analyze stop loss execution discipline

    Query Parameters:
        - start_date: Filter cycles after this date (ISO format)
        - end_date: Filter cycles before this date (ISO format)

    Returns:
        - total_cycles: Total number of cycles analyzed
        - executed_count: Number of cycles with stop loss executed
        - violated_count: Number of cycles with stop loss violated
        - execution_rate: Percentage of stop loss execution
        - violations: List of worst violations (top 10)
        - insight: Actionable insight message
    """
    service = DisciplineAnalyticsService(db)

    try:
        result = service.analyze_stop_loss_discipline(
            user_id=current_user_id,
            start_date=start_date,
            end_date=end_date
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze stop loss discipline: {str(e)}"
        )


@router.get("/emotion-impact")
async def get_emotion_impact(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Analyze how emotions impact trading results

    Returns:
        - emotion_stats: Statistics for each emotion (calm, fearful, greedy, etc.)
        - insight: Key findings and recommendations
    """
    service = DisciplineAnalyticsService(db)

    try:
        result = service.analyze_emotion_impact(user_id=current_user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze emotion impact: {str(e)}"
        )


@router.get("/strategy-effectiveness")
async def get_strategy_effectiveness(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Analyze effectiveness of different trading strategies

    Returns:
        - strategy_stats: Statistics for each strategy (底部反转, 形态突破, 回调低吸, 其他)
        - insight: Key findings and recommendations
    """
    service = DisciplineAnalyticsService(db)

    try:
        result = service.analyze_strategy_effectiveness(user_id=current_user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze strategy effectiveness: {str(e)}"
        )


@router.get("/holding-time-pattern")
async def get_holding_time_pattern(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Analyze holding time patterns for profitable vs losing trades

    Returns:
        - profitable_trades: Stats for profitable trades (count, avg, median)
        - loss_trades: Stats for losing trades (count, avg, median)
        - insight: Key findings and recommendations
    """
    service = DisciplineAnalyticsService(db)

    try:
        result = service.analyze_holding_time_pattern(user_id=current_user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze holding time pattern: {str(e)}"
        )


@router.get("/discipline-dashboard")
async def get_discipline_dashboard(
    time_range: str = Query("30d", regex="^(7d|30d|90d|all)$"),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive discipline analysis dashboard

    Query Parameters:
        - time_range: Time range filter (7d, 30d, 90d, all) - default: 30d

    Returns:
        - time_range: Applied time range
        - stop_loss_discipline: Stop loss analysis data
        - emotion_impact: Emotion analysis data
        - strategy_effectiveness: Strategy analysis data
        - holding_time_pattern: Holding time analysis data
    """
    service = DisciplineAnalyticsService(db)

    try:
        result = service.get_dashboard(
            user_id=current_user_id,
            time_range=time_range
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get discipline dashboard: {str(e)}"
        )
