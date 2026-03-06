from fastapi import APIRouter
from .endpoints import auth, trade_accounts, trades, positions, import_trades, klines, position_cycles, analytics, dashboard, closed_positions, ibkr_import, strategy_settings

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(trade_accounts.router, prefix="/trade-accounts", tags=["trade-accounts"])
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(closed_positions.router, prefix="/closed-positions", tags=["closed-positions"])
api_router.include_router(import_trades.router, prefix="/import", tags=["import"])
api_router.include_router(ibkr_import.router, prefix="/ibkr", tags=["ibkr-import"])
api_router.include_router(klines.router, prefix="/market", tags=["market-data"])
api_router.include_router(position_cycles.router, prefix="/position-cycles", tags=["position-cycles"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(strategy_settings.router, prefix="/strategy-settings", tags=["strategy-settings"])

# Placeholder for future routers
# api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
