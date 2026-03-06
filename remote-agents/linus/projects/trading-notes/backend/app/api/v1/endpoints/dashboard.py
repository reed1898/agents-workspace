"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from ....core.database import get_db
from ....core.security import decode_token
from ....services.dashboard_service import DashboardService
from ....services.market_data_service import get_market_data_service
from ....schemas.dashboard import DashboardSummary

router = APIRouter()
logger = logging.getLogger(__name__)


def get_current_user_id(authorization: str = Header(...)) -> UUID:
    """Get current user ID from JWT Token"""
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


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get complete dashboard summary

    Returns:
        DashboardSummary with:
        - Overview metrics (total market value, P&L, etc.)
        - Positions summary (by market type)
        - Recent 10 trades
        - Pending review position cycles
        - Discipline score
        - Quick stats
    """
    logger.info(f"Dashboard summary requested for user {user_id}")

    try:
        dashboard_service = DashboardService(db)
        summary = dashboard_service.get_dashboard_summary(user_id)

        missing_symbols = [
            trade.symbol for trade in summary.recent_trades if not trade.symbol_name
        ]
        if missing_symbols:
            market_service = get_market_data_service()
            fetched = await market_service.fetch_a_stock_names(missing_symbols)
            for trade in summary.recent_trades:
                if not trade.symbol_name and trade.symbol in fetched:
                    trade.symbol_name = fetched[trade.symbol]
        return summary
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting dashboard summary: {str(e)}"
        )
