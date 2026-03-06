"""Dashboard service for aggregating data"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Tuple, Optional
from uuid import UUID
import logging

from ..models.position import Position
from ..models.trade import Trade
from ..models.trade_account import TradeAccount
from ..models.position_cycle import PositionCycle
from ..services.strategy_settings_service import StrategySettingsService
from ..schemas.dashboard import (
    DashboardSummary,
    OverviewMetrics,
    PositionsSummaryMetrics,
    RecentTrade,
    PendingReview,
    QuickStats
)

logger = logging.getLogger(__name__)
USD_BASED_ACCOUNT_TYPES = {"us_stock", "crypto"}


class DashboardService:
    """Service for dashboard data aggregation"""

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_summary(self, user_id: UUID) -> DashboardSummary:
        """Get complete dashboard summary for a user

        Args:
            user_id: User UUID

        Returns:
            DashboardSummary with all dashboard data
        """
        logger.info(f"Getting dashboard summary for user {user_id}")

        usd_cny_rate = self._get_usd_cny_rate(user_id)

        # Get all data in parallel queries
        overview = self._get_overview_metrics(user_id, usd_cny_rate)
        positions_summary = self._get_positions_summary(user_id, usd_cny_rate)
        recent_trades = self._get_recent_trades(user_id, limit=10)
        pending_reviews = self._get_pending_reviews(user_id, limit=5)
        quick_stats = self._get_quick_stats(user_id)
        discipline_score = self._get_discipline_score(user_id)

        return DashboardSummary(
            overview=overview,
            positions_summary=positions_summary,
            recent_trades=recent_trades,
            pending_reviews=pending_reviews,
            discipline_score=discipline_score,
            quick_stats=quick_stats
        )

    def _get_overview_metrics(self, user_id: UUID, usd_cny_rate: Decimal) -> OverviewMetrics:
        """Calculate overview metrics"""
        total_cash_balance = self._get_total_cash_balance(user_id, usd_cny_rate)

        # Query all positions for the user
        positions = self.db.query(
            Position,
            TradeAccount.account_type
        ).join(
            TradeAccount,
            Position.account_id == TradeAccount.id
        ).filter(
            TradeAccount.user_id == user_id,
            Position.is_closed == False,
            Position.quantity != 0
        ).all()

        total_cost = Decimal('0')
        total_market_value = Decimal('0')
        total_pnl = Decimal('0')

        for position, account_type in positions:
            fx_rate = usd_cny_rate if account_type in USD_BASED_ACCOUNT_TYPES else Decimal('1')
            position_cost = Decimal(str(position.total_cost or 0)) * fx_rate
            market_value = Decimal(str(position.market_value or 0)) * fx_rate
            total_cost += position_cost
            total_market_value += market_value

            if position.unrealized_pnl is not None:
                total_pnl += Decimal(str(position.unrealized_pnl)) * fx_rate
            elif position.current_price is not None:
                total_pnl += market_value - position_cost
        total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else Decimal('0')

        # TODO: Implement today_pnl calculation (requires historical price data)
        today_pnl = None
        today_pnl_percent = None

        return OverviewMetrics(
            total_market_value=total_market_value,
            total_cash_balance=total_cash_balance,
            total_assets=total_market_value + total_cash_balance,
            total_cost=total_cost,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            today_pnl=today_pnl,
            today_pnl_percent=today_pnl_percent
        )

    def _get_total_cash_balance(self, user_id: UUID, usd_cny_rate: Decimal) -> Decimal:
        accounts = self.db.query(
            TradeAccount.account_type,
            TradeAccount.cash_balance,
            TradeAccount.cash_currency,
        ).filter(
            TradeAccount.user_id == user_id
        ).all()

        total_cash_balance = Decimal("0")
        for account_type, cash_balance, cash_currency in accounts:
            if cash_balance is None:
                continue

            currency = (cash_currency or "").upper()
            is_usd_based = currency in {"USD", "USDT", "USDC"} or account_type in USD_BASED_ACCOUNT_TYPES
            fx_rate = usd_cny_rate if is_usd_based else Decimal("1")
            total_cash_balance += Decimal(str(cash_balance)) * fx_rate

        return total_cash_balance

    def _get_positions_summary(self, user_id: UUID, usd_cny_rate: Decimal) -> PositionsSummaryMetrics:
        """Get positions summary by market"""
        positions_data = self.db.query(
            Position,
            TradeAccount.account_type
        ).join(
            TradeAccount,
            Position.account_id == TradeAccount.id
        ).filter(
            TradeAccount.user_id == user_id,
            Position.is_closed == False,
            Position.quantity != 0
        ).all()

        total_positions = len(positions_data)
        profitable_count = 0
        losing_count = 0
        by_market: Dict[str, Dict[str, Decimal]] = {}

        for position, account_type in positions_data:
            # Count profitable/losing
            if position.unrealized_pnl:
                if float(position.unrealized_pnl) > 0:
                    profitable_count += 1
                elif float(position.unrealized_pnl) < 0:
                    losing_count += 1

            # Aggregate by market
            if account_type not in by_market:
                by_market[account_type] = {
                    'value': Decimal('0'),
                    'pnl': Decimal('0'),
                    'count': 0
                }

            fx_rate = usd_cny_rate if account_type in USD_BASED_ACCOUNT_TYPES else Decimal('1')
            market_value = Decimal(str(position.market_value)) if position.market_value else Decimal('0')
            unrealized_pnl = position.unrealized_pnl or Decimal('0')

            by_market[account_type]['value'] += market_value * fx_rate
            by_market[account_type]['pnl'] += unrealized_pnl * fx_rate
            by_market[account_type]['count'] += 1

        return PositionsSummaryMetrics(
            total_positions=total_positions,
            profitable_count=profitable_count,
            losing_count=losing_count,
            by_market=by_market
        )

    def _get_usd_cny_rate(self, user_id: UUID) -> Decimal:
        service = StrategySettingsService(self.db)
        settings = service.get_or_create(user_id)
        raw_rate = None
        if isinstance(settings.currency_settings, dict):
            raw_rate = settings.currency_settings.get("usd_cny_rate")
        try:
            numeric_rate = Decimal(str(raw_rate))
            if numeric_rate > 0:
                return numeric_rate
        except Exception:
            pass
        return Decimal('1')

    def _get_recent_trades(self, user_id: UUID, limit: int = 10) -> List[RecentTrade]:
        """Get recent trades"""
        trades = self.db.query(
            Trade,
            TradeAccount.account_name,
            TradeAccount.account_type,
        ).join(
            TradeAccount,
            Trade.account_id == TradeAccount.id
        ).filter(
            TradeAccount.user_id == user_id
        ).order_by(
            desc(Trade.trade_time)
        ).limit(limit).all()

        recent_trades = []
        for trade, account_name, account_type in trades:
            recent_trades.append(RecentTrade(
                id=str(trade.id),
                symbol=trade.symbol,
                symbol_name=trade.symbol_name,
                side=trade.side,
                quantity=trade.quantity,
                price=trade.price,
                trade_time=trade.trade_time,
                account_name=account_name,
                account_type=account_type,
            ))

        return recent_trades

    def _get_pending_reviews(self, user_id: UUID, limit: int = 5) -> List[PendingReview]:
        """Get pending review position cycles (closed but not reviewed)"""
        try:
            cycles = self.db.query(
                PositionCycle,
                TradeAccount.account_name
            ).join(
                TradeAccount,
                PositionCycle.account_id == TradeAccount.id
            ).filter(
                PositionCycle.user_id == user_id,
                PositionCycle.status == 'closed',
                PositionCycle.close_time.isnot(None),
                # Not reviewed (missing review fields)
                and_(
                    PositionCycle.what_went_well.is_(None),
                    PositionCycle.what_to_improve.is_(None),
                    PositionCycle.lessons_learned.is_(None)
                )
            ).order_by(
                desc(PositionCycle.close_time)
            ).limit(limit).all()

            pending_reviews = []
            for cycle, account_name in cycles:
                days_since_close = 0
                if cycle.close_time:
                    delta = datetime.utcnow() - cycle.close_time
                    days_since_close = delta.days

                pending_reviews.append(PendingReview(
                    id=str(cycle.id),
                    symbol=cycle.symbol,
                    account_name=account_name,
                    close_time=cycle.close_time,
                    total_profit_loss=cycle.total_profit_loss,
                    roi_percent=cycle.roi_percent,
                    holding_hours=cycle.holding_hours,
                    days_since_close=days_since_close
                ))

            return pending_reviews
        except Exception:
            # Position cycles table may not exist yet (Phase 4 feature)
            return []

    def _get_quick_stats(self, user_id: UUID) -> QuickStats:
        """Get quick statistics"""
        # Count open position cycles
        try:
            open_cycles = self.db.query(func.count(PositionCycle.id)).filter(
                PositionCycle.user_id == user_id,
                PositionCycle.status == 'open'
            ).scalar() or 0
        except Exception:
            # Position cycles table may not exist yet (Phase 4 feature)
            open_cycles = 0

        # Count trades this month
        first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        trades_this_month = self.db.query(func.count(Trade.id)).join(
            TradeAccount,
            Trade.account_id == TradeAccount.id
        ).filter(
            TradeAccount.user_id == user_id,
            Trade.trade_time >= first_day_of_month
        ).scalar() or 0

        # Calculate win rate this month
        try:
            closed_cycles_this_month = self.db.query(PositionCycle).filter(
                PositionCycle.user_id == user_id,
                PositionCycle.status == 'closed',
                PositionCycle.close_time >= first_day_of_month
            ).all()

            win_rate_this_month = None
            if closed_cycles_this_month:
                winning_trades = sum(
                    1 for cycle in closed_cycles_this_month
                    if cycle.total_profit_loss and float(cycle.total_profit_loss) > 0
                )
                win_rate_this_month = Decimal(str(winning_trades / len(closed_cycles_this_month) * 100))
        except Exception:
            # Position cycles table may not exist yet (Phase 4 feature)
            win_rate_this_month = None

        return QuickStats(
            open_position_cycles=open_cycles,
            trades_this_month=trades_this_month,
            win_rate_this_month=win_rate_this_month
        )

    def _get_discipline_score(self, user_id: UUID) -> Optional[Decimal]:
        """Calculate overall discipline score"""
        try:
            # Get closed position cycles with discipline scores
            cycles_with_scores = self.db.query(PositionCycle.discipline_score).filter(
                PositionCycle.user_id == user_id,
                PositionCycle.status == 'closed',
                PositionCycle.discipline_score.isnot(None)
            ).all()

            if not cycles_with_scores:
                return None

            scores = [score[0] for score in cycles_with_scores]
            avg_score = sum(scores) / len(scores)

            return Decimal(str(avg_score))
        except Exception:
            # Position cycles table may not exist yet (Phase 4 feature)
            return None
