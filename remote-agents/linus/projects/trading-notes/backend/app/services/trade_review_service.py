"""
交易复盘服务 - Phase 4 纪律系统

提供交易补录、未复盘交易查询等功能
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import HTTPException

from ..models.trade import Trade as TradeModel
from ..models.trade_account import TradeAccount as TradeAccountModel
from ..schemas.trade import TradeReviewData


class TradeReviewService:
    """交易复盘服务类"""

    def __init__(self, db: Session):
        self.db = db

    def review_trade(
        self,
        trade_id: UUID,
        user_id: UUID,
        review_data: TradeReviewData
    ) -> TradeModel:
        """
        单笔交易补录

        Args:
            trade_id: 交易ID
            user_id: 用户ID
            review_data: 补录数据

        Returns:
            更新后的交易记录

        Raises:
            HTTPException: 如果交易不存在
        """
        # 查询交易记录
        trade = self.db.query(TradeModel).join(
            TradeAccountModel,
            TradeModel.account_id == TradeAccountModel.id
        ).filter(
            and_(
                TradeModel.id == trade_id,
                TradeAccountModel.user_id == user_id
            )
        ).first()

        if not trade:
            raise HTTPException(status_code=404, detail="交易记录不存在")

        # 更新情绪字段
        if review_data.action_type is not None:
            trade.action_type = review_data.action_type.value
        if review_data.action_reason is not None:
            trade.action_reason = review_data.action_reason
        if review_data.emotion_state is not None:
            trade.emotion_state = review_data.emotion_state.value
        if review_data.emotion_intensity is not None:
            trade.emotion_intensity = review_data.emotion_intensity

        # 更新止损止盈字段
        if review_data.planned_stop_loss is not None:
            trade.planned_stop_loss = review_data.planned_stop_loss
        if review_data.actual_stop_loss is not None:
            trade.actual_stop_loss = review_data.actual_stop_loss
        if review_data.stop_loss_executed is not None:
            trade.stop_loss_executed = review_data.stop_loss_executed
        if review_data.planned_take_profit is not None:
            trade.planned_take_profit = review_data.planned_take_profit
        if review_data.actual_take_profit is not None:
            trade.actual_take_profit = review_data.actual_take_profit

        # 更新策略标签
        if review_data.exit_strategy is not None:
            trade.exit_strategy = review_data.exit_strategy.value
        if review_data.action_strategy is not None:
            trade.action_strategy = review_data.action_strategy

        # 更新备注
        if review_data.notes is not None:
            trade.notes = review_data.notes

        # 标记为已复盘
        trade.reviewed = True
        trade.reviewed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(trade)

        return trade

    def batch_review_trades(
        self,
        user_id: UUID,
        trade_ids: List[UUID],
        common_data: Dict[str, Any]
    ) -> List[TradeModel]:
        """
        批量补录交易(当晚集中补录)

        Args:
            user_id: 用户ID
            trade_ids: 交易ID列表
            common_data: 通用补录数据(应用到所有交易)

        Returns:
            更新后的交易记录列表
        """
        # 查询所有交易
        trades = self.db.query(TradeModel).join(
            TradeAccountModel,
            TradeModel.account_id == TradeAccountModel.id
        ).filter(
            and_(
                TradeModel.id.in_(trade_ids),
                TradeAccountModel.user_id == user_id
            )
        ).all()

        if not trades:
            raise HTTPException(status_code=404, detail="没有找到符合条件的交易记录")

        # 应用通用数据到所有交易
        for trade in trades:
            if common_data.get('action_strategy'):
                trade.action_strategy = common_data['action_strategy']
            if common_data.get('action_type'):
                trade.action_type = common_data['action_type']
            if common_data.get('action_reason'):
                trade.action_reason = common_data['action_reason']
            if common_data.get('emotion_state'):
                trade.emotion_state = common_data['emotion_state']
            if common_data.get('emotion_intensity'):
                trade.emotion_intensity = common_data['emotion_intensity']
            if common_data.get('planned_stop_loss'):
                trade.planned_stop_loss = common_data['planned_stop_loss']
            if common_data.get('planned_take_profit'):
                trade.planned_take_profit = common_data['planned_take_profit']
            if common_data.get('exit_strategy'):
                trade.exit_strategy = common_data['exit_strategy']

            trade.reviewed = True
            trade.reviewed_at = datetime.utcnow()

        self.db.commit()

        # 刷新所有记录
        for trade in trades:
            self.db.refresh(trade)

        return trades

    def get_unreviewed_trades(
        self,
        user_id: UUID,
        days: int = 7,
        account_id: Optional[UUID] = None
    ) -> List[TradeModel]:
        """
        获取未复盘的交易(用于提醒)

        Args:
            user_id: 用户ID
            days: 查询最近N天的交易(默认7天)
            account_id: 可选的账户筛选

        Returns:
            未复盘的交易记录列表
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # 构建查询
        query = self.db.query(TradeModel).join(
            TradeAccountModel,
            TradeModel.account_id == TradeAccountModel.id
        ).filter(
            and_(
                TradeAccountModel.user_id == user_id,
                TradeModel.reviewed == False,
                TradeModel.trade_time >= cutoff_date
            )
        )

        # 如果指定了账户,添加账户筛选
        if account_id:
            query = query.filter(TradeModel.account_id == account_id)

        # 按交易时间倒序排列
        trades = query.order_by(TradeModel.trade_time.desc()).all()

        return trades

    def get_trade_with_user_check(
        self,
        trade_id: UUID,
        user_id: UUID
    ) -> TradeModel:
        """
        获取交易记录并验证用户权限

        Args:
            trade_id: 交易ID
            user_id: 用户ID

        Returns:
            交易记录

        Raises:
            HTTPException: 如果交易不存在或无权访问
        """
        trade = self.db.query(TradeModel).join(
            TradeAccountModel,
            TradeModel.account_id == TradeAccountModel.id
        ).filter(
            and_(
                TradeModel.id == trade_id,
                TradeAccountModel.user_id == user_id
            )
        ).first()

        if not trade:
            raise HTTPException(
                status_code=404,
                detail="交易记录不存在或无权访问"
            )

        return trade
