from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from uuid import UUID

from ....core.database import get_db
from ....core.security import decode_token
from ....schemas.strategy_settings import StrategySettingsResponse, StrategySettingsUpdate
from ....services.strategy_settings_service import StrategySettingsService

router = APIRouter()


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


@router.get("/", response_model=StrategySettingsResponse)
async def get_strategy_settings(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户的操作策略设置"""
    service = StrategySettingsService(db)
    settings = service.get_or_create(user_id)
    return StrategySettingsResponse(
        market_strategies=settings.market_strategies,
        currency_settings=settings.currency_settings
    )


@router.put("/", response_model=StrategySettingsResponse)
async def update_strategy_settings(
    settings_data: StrategySettingsUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新当前用户的操作策略设置"""
    service = StrategySettingsService(db)
    settings = service.update_settings(
        user_id,
        settings_data.market_strategies,
        settings_data.currency_settings.model_dump() if settings_data.currency_settings else None
    )
    return StrategySettingsResponse(
        market_strategies=settings.market_strategies,
        currency_settings=settings.currency_settings
    )
