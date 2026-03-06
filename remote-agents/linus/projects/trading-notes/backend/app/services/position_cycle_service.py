"""
Position Cycle Service - Auto-detect and analyze trading cycles
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from collections import Counter

from ..models.position_cycle import PositionCycle as PositionCycleModel
from ..models.trade import Trade as TradeModel
from ..schemas.position_cycle import PositionCycleReview


class PositionCycleService:
    """Position Cycle Service for managing trading cycles"""

    def __init__(self, db: Session):
        self.db = db

    def auto_detect_position_cycles(
        self,
        account_id: UUID,
        symbol: str,
        user_id: UUID
    ) -> List[PositionCycleModel]:
        """
        Auto-detect position cycles for a given symbol

        Logic:
        1. Get all trades sorted by time
        2. Track position changes
        3. When position = 0, cycle complete
        4. Support both spot and futures (position_side)

        Args:
            account_id: Trading account ID
            symbol: Trading symbol
            user_id: User ID

        Returns:
            List of detected position cycles
        """
        # Get all trades sorted by time
        trades = self.db.query(TradeModel).filter(
            TradeModel.account_id == account_id,
            TradeModel.symbol == symbol,
            TradeModel.user_id == user_id
        ).order_by(TradeModel.trade_time).all()

        if not trades:
            return []

        # Check if this is futures trading (has position_side)
        is_futures = any(t.position_side for t in trades)

        if is_futures:
            return self._detect_futures_cycles(trades, account_id, symbol, user_id)
        else:
            return self._detect_spot_cycles(trades, account_id, symbol, user_id)

    def _detect_spot_cycles(
        self,
        trades: List[TradeModel],
        account_id: UUID,
        symbol: str,
        user_id: UUID
    ) -> List[PositionCycleModel]:
        """Detect cycles for spot trading"""
        cycles = []
        current_cycle_trades = []
        position_quantity = Decimal(0)

        for trade in trades:
            current_cycle_trades.append(trade.id)

            # Calculate position change
            if trade.side == 'buy':
                position_quantity += Decimal(str(trade.quantity))
            elif trade.side == 'sell':
                position_quantity -= Decimal(str(trade.quantity))

            # Position closed = cycle complete
            if abs(position_quantity) < Decimal('0.00000001') and current_cycle_trades:
                cycle = self._create_position_cycle(
                    account_id=account_id,
                    symbol=symbol,
                    user_id=user_id,
                    trade_ids=current_cycle_trades,
                    status='closed'
                )
                if cycle:
                    cycles.append(cycle)
                current_cycle_trades = []
                position_quantity = Decimal(0)

        # If there's an open position, create an open cycle
        if current_cycle_trades and abs(position_quantity) > Decimal('0.00000001'):
            cycle = self._create_position_cycle(
                account_id=account_id,
                symbol=symbol,
                user_id=user_id,
                trade_ids=current_cycle_trades,
                status='open'
            )
            if cycle:
                cycles.append(cycle)

        return cycles

    def _detect_futures_cycles(
        self,
        trades: List[TradeModel],
        account_id: UUID,
        symbol: str,
        user_id: UUID
    ) -> List[PositionCycleModel]:
        """Detect cycles for futures trading (separate long/short)"""
        cycles = []

        # Separate long and short trades
        long_trades = [t for t in trades if t.position_side == 'long']
        short_trades = [t for t in trades if t.position_side == 'short']

        # Detect cycles for long positions
        if long_trades:
            long_cycles = self._detect_spot_cycles(long_trades, account_id, symbol, user_id)
            cycles.extend(long_cycles)

        # Detect cycles for short positions
        if short_trades:
            short_cycles = self._detect_spot_cycles(short_trades, account_id, symbol, user_id)
            cycles.extend(short_cycles)

        return cycles

    def _create_position_cycle(
        self,
        account_id: UUID,
        symbol: str,
        user_id: UUID,
        trade_ids: List[UUID],
        status: str
    ) -> Optional[PositionCycleModel]:
        """Create a position cycle record"""
        if not trade_ids:
            return None

        trades = self.db.query(TradeModel).filter(
            TradeModel.id.in_(trade_ids)
        ).order_by(TradeModel.trade_time).all()

        if not trades:
            return None

        # Check if cycle already exists
        existing = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.account_id == account_id,
            PositionCycleModel.symbol == symbol,
            PositionCycleModel.open_time == trades[0].trade_time
        ).first()

        if existing:
            return existing

        cycle = PositionCycleModel(
            user_id=user_id,
            account_id=account_id,
            symbol=symbol,
            trade_ids=[str(tid) for tid in trade_ids],
            open_time=trades[0].trade_time,
            close_time=trades[-1].trade_time if status == 'closed' else None,
            status=status
        )

        self.db.add(cycle)
        self.db.commit()
        self.db.refresh(cycle)

        # Calculate metrics
        self.calculate_cycle_metrics(cycle.id)

        return cycle

    def calculate_cycle_metrics(self, cycle_id: UUID) -> PositionCycleModel:
        """Calculate all metrics for a position cycle"""
        cycle = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.id == cycle_id
        ).first()

        if not cycle:
            raise ValueError(f"Cycle {cycle_id} not found")

        trades = self.db.query(TradeModel).filter(
            TradeModel.id.in_([UUID(tid) for tid in cycle.trade_ids])
        ).order_by(TradeModel.trade_time).all()

        if not trades:
            return cycle

        # Separate buy and sell trades
        buy_trades = [t for t in trades if t.side == 'buy']
        sell_trades = [t for t in trades if t.side == 'sell']

        # Calculate total quantity
        total_buy_qty = sum(Decimal(str(t.quantity)) for t in buy_trades)
        total_sell_qty = sum(Decimal(str(t.quantity)) for t in sell_trades)
        cycle.total_quantity = str(max(total_buy_qty, total_sell_qty))

        # Calculate average entry price
        if buy_trades:
            total_buy_cost = sum(
                Decimal(str(t.quantity)) * Decimal(str(t.price)) for t in buy_trades
            )
            total_buy_quantity = sum(Decimal(str(t.quantity)) for t in buy_trades)
            if total_buy_quantity > 0:
                cycle.average_entry_price = str(total_buy_cost / total_buy_quantity)

        # Calculate average exit price
        if sell_trades:
            total_sell_revenue = sum(
                Decimal(str(t.quantity)) * Decimal(str(t.price)) for t in sell_trades
            )
            total_sell_quantity = sum(Decimal(str(t.quantity)) for t in sell_trades)
            if total_sell_quantity > 0:
                cycle.average_exit_price = str(total_sell_revenue / total_sell_quantity)

        # Calculate profit/loss for closed cycles
        if cycle.status == 'closed' and buy_trades and sell_trades:
            total_cost = sum(
                Decimal(str(t.quantity)) * Decimal(str(t.price)) + Decimal(str(t.fee or 0))
                for t in buy_trades
            )
            total_revenue = sum(
                Decimal(str(t.quantity)) * Decimal(str(t.price)) - Decimal(str(t.fee or 0))
                for t in sell_trades
            )
            profit_loss = total_revenue - total_cost
            cycle.total_profit_loss = str(profit_loss)

            if total_cost > 0:
                roi = (profit_loss / total_cost) * Decimal('100')
                cycle.roi_percent = str(roi)

        # Calculate holding time
        if cycle.close_time:
            holding_seconds = (cycle.close_time - cycle.open_time).total_seconds()
            cycle.holding_hours = int(holding_seconds / 3600)

        # Check discipline execution
        cycle.followed_stop_loss = self._check_stop_loss_execution(trades)
        cycle.followed_take_profit = self._check_take_profit_execution(trades)

        # Calculate discipline score
        cycle.discipline_score = self._calculate_discipline_score(cycle)

        # Analyze dominant emotion
        emotions = [t.emotion_state for t in trades if t.emotion_state]
        if emotions:
            emotion_counter = Counter(emotions)
            cycle.dominant_emotion = emotion_counter.most_common(1)[0][0]

            # Emotion stability (fewer unique emotions = more stable)
            unique_emotions = len(set(emotions))
            cycle.emotion_stability = max(1, 10 - unique_emotions)

        # Infer primary strategy (based on action_strategy)
        strategies = [t.action_strategy for t in trades if t.action_strategy]
        if strategies:
            strategy_counter = Counter(strategies)
            cycle.primary_strategy = strategy_counter.most_common(1)[0][0][:50]

        self.db.commit()
        self.db.refresh(cycle)

        return cycle

    def _check_stop_loss_execution(self, trades: List[TradeModel]) -> Optional[bool]:
        """Check if stop loss was executed"""
        trades_with_stop_loss = [t for t in trades if t.planned_stop_loss]

        if not trades_with_stop_loss:
            return None  # No stop loss set, cannot determine

        # Check if any trade has stop_loss_executed flag
        executed = any(t.stop_loss_executed for t in trades_with_stop_loss)

        return executed

    def _check_take_profit_execution(self, trades: List[TradeModel]) -> Optional[bool]:
        """Check if take profit was executed"""
        trades_with_take_profit = [t for t in trades if t.planned_take_profit]

        if not trades_with_take_profit:
            return None

        # Check if actual take profit >= planned take profit
        for trade in trades_with_take_profit:
            if (trade.actual_take_profit and
                Decimal(str(trade.actual_take_profit)) >= Decimal(str(trade.planned_take_profit))):
                return True

        return False

    def _calculate_discipline_score(self, cycle: PositionCycleModel) -> int:
        """
        Calculate discipline score (0-100)

        Scoring:
        - Base: 50
        - Stop loss execution: +20/-20
        - Take profit execution: +15
        - Emotion stability: +15
        """
        score = 50  # Base score

        # Stop loss execution (+20 / -20)
        if cycle.followed_stop_loss is True:
            score += 20
        elif cycle.followed_stop_loss is False:
            score -= 20

        # Take profit execution (+15)
        if cycle.followed_take_profit is True:
            score += 15

        # Emotion stability (+15)
        if cycle.emotion_stability:
            score += int(cycle.emotion_stability * 1.5)

        # Keep within 0-100 range
        return max(0, min(100, score))

    def list_cycles(
        self,
        user_id: UUID,
        account_id: Optional[UUID] = None,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[PositionCycleModel], int]:
        """List position cycles with filtering and pagination"""
        query = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.user_id == user_id
        )

        if account_id:
            query = query.filter(PositionCycleModel.account_id == account_id)

        if symbol:
            query = query.filter(PositionCycleModel.symbol == symbol)

        if status:
            query = query.filter(PositionCycleModel.status == status)

        total = query.count()

        cycles = query.order_by(
            desc(PositionCycleModel.open_time)
        ).offset((page - 1) * page_size).limit(page_size).all()

        return cycles, total

    def get_cycle(self, cycle_id: UUID, user_id: UUID) -> Optional[PositionCycleModel]:
        """Get a specific cycle"""
        return self.db.query(PositionCycleModel).filter(
            PositionCycleModel.id == cycle_id,
            PositionCycleModel.user_id == user_id
        ).first()

    def review_cycle(
        self,
        cycle_id: UUID,
        user_id: UUID,
        review_data: PositionCycleReview
    ) -> PositionCycleModel:
        """Add review notes to a cycle"""
        cycle = self.get_cycle(cycle_id, user_id)

        if not cycle:
            raise ValueError(f"Cycle {cycle_id} not found")

        if review_data.what_went_well is not None:
            cycle.what_went_well = review_data.what_went_well

        if review_data.what_to_improve is not None:
            cycle.what_to_improve = review_data.what_to_improve

        if review_data.lessons_learned is not None:
            cycle.lessons_learned = review_data.lessons_learned

        self.db.commit()
        self.db.refresh(cycle)

        return cycle

    def delete_cycle(self, cycle_id: UUID, user_id: UUID) -> bool:
        """Delete a position cycle"""
        cycle = self.get_cycle(cycle_id, user_id)

        if not cycle:
            return False

        self.db.delete(cycle)
        self.db.commit()

        return True
