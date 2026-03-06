"""
Discipline Analytics Service - Analyze trading discipline and patterns
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime, timedelta
from collections import Counter

from ..models.position_cycle import PositionCycle as PositionCycleModel
from ..models.trade import Trade as TradeModel


class DisciplineAnalyticsService:
    """Service for analyzing trading discipline and patterns"""

    def __init__(self, db: Session):
        self.db = db

    def analyze_stop_loss_discipline(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Analyze stop loss execution discipline

        Returns:
            - total_cycles: Total number of cycles
            - executed_count: Number of cycles with stop loss executed
            - violated_count: Number of cycles with stop loss violated
            - execution_rate: Percentage of stop loss execution
            - violations: List of worst violations
            - insight: Actionable insight message
        """
        # Get closed cycles with stop loss data
        query = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.user_id == user_id,
            PositionCycleModel.status == 'closed',
            PositionCycleModel.followed_stop_loss.isnot(None)
        )

        if start_date:
            query = query.filter(PositionCycleModel.open_time >= start_date)
        if end_date:
            query = query.filter(PositionCycleModel.close_time <= end_date)

        cycles = query.all()

        if not cycles:
            return {
                "message": "暂无数据",
                "total_cycles": 0,
                "executed_count": 0,
                "violated_count": 0,
                "execution_rate": 0,
                "violations": [],
                "insight": "还没有足够的数据来分析止损纪律"
            }

        total = len(cycles)
        executed = len([c for c in cycles if c.followed_stop_loss is True])
        violated = len([c for c in cycles if c.followed_stop_loss is False])

        # Analyze violations (cases where stop loss was not followed and lost money)
        violations = []
        for cycle in cycles:
            if not cycle.followed_stop_loss and cycle.total_profit_loss:
                loss = float(cycle.total_profit_loss)
                if loss < 0:
                    violations.append({
                        "cycle_id": str(cycle.id),
                        "symbol": cycle.symbol,
                        "loss": loss,
                        "holding_hours": cycle.holding_hours,
                        "emotion": cycle.dominant_emotion,
                        "open_time": cycle.open_time.isoformat() if cycle.open_time else None
                    })

        # Sort by loss (most severe first)
        violations.sort(key=lambda x: x['loss'])

        execution_rate = round(executed / total * 100, 2) if total > 0 else 0

        return {
            "total_cycles": total,
            "executed_count": executed,
            "violated_count": violated,
            "execution_rate": execution_rate,
            "violations": violations[:10],  # Return top 10 worst cases
            "insight": self._generate_stop_loss_insight(executed, violated, violations)
        }

    def _generate_stop_loss_insight(
        self,
        executed: int,
        violated: int,
        violations: List[Dict]
    ) -> str:
        """Generate actionable insight for stop loss discipline"""
        if violated == 0:
            return "✅ 优秀！你严格执行了所有止损计划。"

        total = executed + violated
        rate = executed / total * 100 if total > 0 else 0

        if rate >= 80:
            return f"✅ 良好！止损执行率 {rate:.1f}%，继续保持。"
        elif rate >= 60:
            return f"⚠️ 一般。止损执行率 {rate:.1f}%，建议加强纪律。"
        else:
            # Analyze violations to find patterns
            emotions = [v.get('emotion') for v in violations if v.get('emotion')]
            if emotions:
                emotion_counter = Counter(emotions)
                dominant_emotion = emotion_counter.most_common(1)[0][0]

                emotion_names = {
                    'calm': '冷静',
                    'fearful': '恐惧',
                    'greedy': '贪婪',
                    'fomo': '害怕踏空',
                    'panic': '恐慌',
                    'confident': '自信',
                    'excited': '兴奋',
                    'regretful': '后悔'
                }
                emotion_name = emotion_names.get(dominant_emotion, dominant_emotion)

                return f"❌ 需改进！止损执行率仅 {rate:.1f}%，违规时常伴随'{emotion_name}'情绪。"
            else:
                return f"❌ 需改进！止损执行率仅 {rate:.1f}%，请严格遵守止损纪律。"

    def analyze_emotion_impact(self, user_id: UUID) -> Dict[str, Any]:
        """
        Analyze how emotions impact trading results

        Returns:
            - emotion_stats: Statistics for each emotion
            - insight: Key findings
        """
        cycles = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.user_id == user_id,
            PositionCycleModel.status == 'closed',
            PositionCycleModel.dominant_emotion.isnot(None)
        ).all()

        if not cycles:
            return {
                "message": "暂无情绪数据",
                "emotion_stats": {},
                "insight": "还没有足够的情绪数据来分析"
            }

        emotion_stats = {}
        emotions = ['calm', 'fearful', 'greedy', 'fomo', 'panic', 'confident', 'excited', 'regretful']

        for emotion in emotions:
            emotion_cycles = [c for c in cycles if c.dominant_emotion == emotion]

            if not emotion_cycles:
                continue

            win_count = len([c for c in emotion_cycles if c.total_profit_loss and float(c.total_profit_loss) > 0])
            total_count = len(emotion_cycles)

            avg_roi = 0
            avg_holding_hours = 0
            total_pnl = 0

            if emotion_cycles:
                roi_values = [float(c.roi_percent) for c in emotion_cycles if c.roi_percent]
                avg_roi = round(sum(roi_values) / len(roi_values), 2) if roi_values else 0

                holding_values = [c.holding_hours for c in emotion_cycles if c.holding_hours is not None]
                avg_holding_hours = round(sum(holding_values) / len(holding_values), 1) if holding_values else 0

                pnl_values = [float(c.total_profit_loss) for c in emotion_cycles if c.total_profit_loss]
                total_pnl = round(sum(pnl_values), 2) if pnl_values else 0

            emotion_stats[emotion] = {
                "cycle_count": total_count,
                "win_rate": round(win_count / total_count * 100, 2) if total_count > 0 else 0,
                "avg_roi": avg_roi,
                "avg_holding_hours": avg_holding_hours,
                "total_pnl": total_pnl
            }

        return {
            "emotion_stats": emotion_stats,
            "insight": self._generate_emotion_insight(emotion_stats)
        }

    def _generate_emotion_insight(self, emotion_stats: Dict[str, Any]) -> str:
        """Generate insight from emotion analysis"""
        if not emotion_stats:
            return "暂无足够数据生成建议"

        # Find best and worst emotions by avg_roi
        valid_emotions = {k: v for k, v in emotion_stats.items() if v['cycle_count'] > 0}

        if not valid_emotions:
            return "暂无足够数据生成建议"

        best_emotion = max(valid_emotions.items(), key=lambda x: x[1]['avg_roi'])
        worst_emotion = min(valid_emotions.items(), key=lambda x: x[1]['avg_roi'])

        emotion_names = {
            'calm': '冷静',
            'fearful': '恐惧',
            'greedy': '贪婪',
            'fomo': '害怕踏空',
            'panic': '恐慌',
            'confident': '自信',
            'excited': '兴奋',
            'regretful': '后悔'
        }

        best_name = emotion_names.get(best_emotion[0], best_emotion[0])
        worst_name = emotion_names.get(worst_emotion[0], worst_emotion[0])

        return f"在'{best_name}'状态下，平均收益率为 {best_emotion[1]['avg_roi']:.2f}%；而在'{worst_name}'状态下仅为 {worst_emotion[1]['avg_roi']:.2f}%。建议交易时保持{best_name}心态。"

    def analyze_strategy_effectiveness(self, user_id: UUID) -> Dict[str, Any]:
        """
        Analyze effectiveness of different trading strategies

        Returns:
            - strategy_stats: Statistics for each strategy
            - insight: Key findings
        """
        cycles = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.user_id == user_id,
            PositionCycleModel.status == 'closed',
            PositionCycleModel.primary_strategy.isnot(None)
        ).all()

        if not cycles:
            return {
                "message": "暂无策略数据",
                "strategy_stats": {},
                "insight": "还没有足够的策略数据来分析"
            }

        strategy_stats = {}
        strategies = ['底部反转', '形态突破', '回调低吸', '其他']

        for strategy in strategies:
            strategy_cycles = [c for c in cycles if c.primary_strategy == strategy]

            if not strategy_cycles:
                continue

            win_count = len([c for c in strategy_cycles if c.total_profit_loss and float(c.total_profit_loss) > 0])
            total_count = len(strategy_cycles)

            avg_roi = 0
            avg_holding_hours = 0

            if strategy_cycles:
                roi_values = [float(c.roi_percent) for c in strategy_cycles if c.roi_percent]
                avg_roi = round(sum(roi_values) / len(roi_values), 2) if roi_values else 0

                holding_values = [c.holding_hours for c in strategy_cycles if c.holding_hours is not None]
                avg_holding_hours = round(sum(holding_values) / len(holding_values), 1) if holding_values else 0

            # Find best and worst cases
            best_case = None
            worst_case = None

            if strategy_cycles:
                best_cycle = max(strategy_cycles, key=lambda c: float(c.roi_percent) if c.roi_percent else -999999)
                worst_cycle = min(strategy_cycles, key=lambda c: float(c.roi_percent) if c.roi_percent else 999999)

                if best_cycle.roi_percent:
                    best_case = {
                        "symbol": best_cycle.symbol,
                        "roi": round(float(best_cycle.roi_percent), 2)
                    }

                if worst_cycle.roi_percent:
                    worst_case = {
                        "symbol": worst_cycle.symbol,
                        "roi": round(float(worst_cycle.roi_percent), 2)
                    }

            strategy_stats[strategy] = {
                "cycle_count": total_count,
                "win_rate": round(win_count / total_count * 100, 2) if total_count > 0 else 0,
                "avg_roi": avg_roi,
                "avg_holding_hours": avg_holding_hours,
                "best_case": best_case,
                "worst_case": worst_case
            }

        return {
            "strategy_stats": strategy_stats,
            "insight": self._generate_strategy_insight(strategy_stats)
        }

    def _generate_strategy_insight(self, strategy_stats: Dict[str, Any]) -> str:
        """Generate insight from strategy analysis"""
        if not strategy_stats:
            return "暂无足够数据生成建议"

        valid_strategies = {k: v for k, v in strategy_stats.items() if v['cycle_count'] > 0}

        if not valid_strategies:
            return "暂无足够数据生成建议"

        # Find strategy with highest win rate
        best_win_rate = max(valid_strategies.items(), key=lambda x: x[1]['win_rate'])

        # Find most profitable strategy
        most_profitable = max(valid_strategies.items(), key=lambda x: x[1]['avg_roi'])

        if best_win_rate[0] == most_profitable[0]:
            return f"'{best_win_rate[0]}'策略表现最佳，胜率 {best_win_rate[1]['win_rate']:.2f}%，平均收益 {best_win_rate[1]['avg_roi']:.2f}%。建议重点使用此策略。"
        else:
            return f"'{best_win_rate[0]}'胜率最高({best_win_rate[1]['win_rate']:.2f}%)，但'{most_profitable[0]}'平均收益最高({most_profitable[1]['avg_roi']:.2f}%)。建议根据风险偏好选择。"

    def analyze_holding_time_pattern(self, user_id: UUID) -> Dict[str, Any]:
        """
        Analyze holding time patterns for profitable vs losing trades

        Returns:
            - profitable_trades: Stats for profitable trades
            - loss_trades: Stats for losing trades
            - insight: Key findings
        """
        cycles = self.db.query(PositionCycleModel).filter(
            PositionCycleModel.user_id == user_id,
            PositionCycleModel.status == 'closed',
            PositionCycleModel.holding_hours.isnot(None)
        ).all()

        if not cycles:
            return {
                "message": "暂无数据",
                "profitable_trades": {"count": 0, "avg_holding_hours": 0, "median_holding_hours": 0},
                "loss_trades": {"count": 0, "avg_holding_hours": 0, "median_holding_hours": 0},
                "insight": "还没有足够的数据来分析持仓时间模式"
            }

        # Separate profitable and losing cycles
        profit_cycles = [c for c in cycles if c.total_profit_loss and float(c.total_profit_loss) > 0]
        loss_cycles = [c for c in cycles if c.total_profit_loss and float(c.total_profit_loss) < 0]

        def calculate_stats(cycles_list):
            if not cycles_list:
                return {"count": 0, "avg_holding_hours": 0, "median_holding_hours": 0}

            holding_hours = [c.holding_hours for c in cycles_list if c.holding_hours is not None]

            if not holding_hours:
                return {"count": 0, "avg_holding_hours": 0, "median_holding_hours": 0}

            avg = round(sum(holding_hours) / len(holding_hours), 1)

            # Calculate median
            sorted_hours = sorted(holding_hours)
            n = len(sorted_hours)
            if n % 2 == 0:
                median = round((sorted_hours[n//2 - 1] + sorted_hours[n//2]) / 2, 1)
            else:
                median = round(sorted_hours[n//2], 1)

            return {
                "count": len(cycles_list),
                "avg_holding_hours": avg,
                "median_holding_hours": median
            }

        profit_stats = calculate_stats(profit_cycles)
        loss_stats = calculate_stats(loss_cycles)

        return {
            "profitable_trades": profit_stats,
            "loss_trades": loss_stats,
            "insight": self._generate_holding_time_insight(
                profit_stats['avg_holding_hours'],
                loss_stats['avg_holding_hours']
            )
        }

    def _generate_holding_time_insight(self, profit_avg: float, loss_avg: float) -> str:
        """Generate insight from holding time analysis"""
        if profit_avg == 0 or loss_avg == 0:
            return "暂无足够数据生成建议"

        ratio = profit_avg / loss_avg if loss_avg > 0 else 0

        if ratio < 0.5:
            return f"⚠️ 你倾向于拿不住盈利(平均 {profit_avg:.1f}h)，但拿得住亏损(平均 {loss_avg:.1f}h)。建议：让利润奔跑，及时止损。"
        elif ratio > 2:
            return f"✅ 优秀！你能够持有盈利仓位(平均 {profit_avg:.1f}h)，并及时止损(平均 {loss_avg:.1f}h)。"
        else:
            return f"持仓时间较为均衡，盈利平均 {profit_avg:.1f}h，亏损平均 {loss_avg:.1f}h。"

    def get_dashboard(self, user_id: UUID, time_range: str = "30d") -> Dict[str, Any]:
        """
        Get comprehensive discipline dashboard data

        Args:
            user_id: User ID
            time_range: Time range filter (7d, 30d, 90d, all)

        Returns:
            Combined analytics data for dashboard
        """
        # Calculate date range
        start_date = None
        if time_range == "7d":
            start_date = datetime.utcnow() - timedelta(days=7)
        elif time_range == "30d":
            start_date = datetime.utcnow() - timedelta(days=30)
        elif time_range == "90d":
            start_date = datetime.utcnow() - timedelta(days=90)

        # Get all analytics
        stop_loss = self.analyze_stop_loss_discipline(user_id, start_date=start_date)
        emotion = self.analyze_emotion_impact(user_id)
        strategy = self.analyze_strategy_effectiveness(user_id)
        holding_time = self.analyze_holding_time_pattern(user_id)

        return {
            "time_range": time_range,
            "stop_loss_discipline": stop_loss,
            "emotion_impact": emotion,
            "strategy_effectiveness": strategy,
            "holding_time_pattern": holding_time
        }
