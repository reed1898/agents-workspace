"""
用户路由 - 用户信息、余额、使用记录
"""
import uuid
from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.database import get_db
from app.models.user import User
from app.models.usage import UsageLog, MonthlyUsage
from app.schemas import (
    UserProfile,
    UserBalance,
    UserPlanLimits,
    UsageRecord,
    UsageHistoryResponse,
    MonthlyStats,
)
from app.middleware import verify_api_key, get_user_quota_info
from app.config import settings, UserPlans

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(verify_api_key)
):
    """
    获取用户资料
    
    返回当前登录用户的基本信息
    """
    return UserProfile.model_validate(current_user)


@router.get("/balance", response_model=UserBalance)
async def get_balance(
    current_user: User = User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    查询账户余额和配额
    
    返回：
    - 当前余额
    - 免费额度使用情况
    - 月度使用统计
    """
    quota = await get_user_quota_info(current_user)
    limits = UserPlans.get_limits(current_user.plan)
    
    return UserBalance(
        balance=current_user.balance,
        free_credits_remaining=quota["free_credits_remaining"],
        free_credits_total=settings.FREE_TIER_IMAGES,
        monthly_images_used=current_user.monthly_images_used,
        monthly_images_limit=limits["monthly_images"],
        monthly_voice_used=current_user.monthly_voice_used,
        monthly_voice_limit=limits["monthly_voice"],
    )


@router.get("/plan", response_model=UserPlanLimits)
async def get_plan_limits(
    current_user: User = Depends(verify_api_key)
):
    """
    获取当前套餐限制
    """
    limits = UserPlans.get_limits(current_user.plan)
    return UserPlanLimits(
        plan=current_user.plan,
        limits=limits
    )


@router.get("/usage", response_model=UsageHistoryResponse)
async def get_usage_history(
    service_type: Optional[str] = Query(None, description="Filter by service type: image/voice/video"),
    start_date: Optional[datetime] = Query(None, description="Filter from date"),
    end_date: Optional[datetime] = Query(None, description="Filter to date"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    查询使用记录
    
    支持按服务类型和时间范围筛选
    """
    # 构建查询条件
    query = select(UsageLog).where(UsageLog.user_id == current_user.id)
    
    if service_type:
        query = query.where(UsageLog.service_type == service_type)
    
    if start_date:
        query = query.where(UsageLog.created_at >= start_date)
    
    if end_date:
        query = query.where(UsageLog.created_at <= end_date)
    
    # 统计总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页查询
    query = query.order_by(UsageLog.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    pages = (total + page_size - 1) // page_size
    
    return UsageHistoryResponse(
        items=[UsageRecord.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/usage/stats", response_model=list[MonthlyStats])
async def get_usage_stats(
    months: int = Query(6, ge=1, le=12, description="Number of months to return"),
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取月度使用统计
    
    返回最近 N 个月的聚合统计数据
    """
    # 查询月度统计
    query = select(MonthlyUsage).where(
        MonthlyUsage.user_id == current_user.id
    ).order_by(
        MonthlyUsage.year.desc(),
        MonthlyUsage.month.desc()
    ).limit(months)
    
    result = await db.execute(query)
    stats = result.scalars().all()
    
    return [
        MonthlyStats(
            year=s.year,
            month=s.month,
            image_count=s.image_count,
            voice_count=s.voice_count,
            video_count=s.video_count,
            total_cost=s.total_cost,
        )
        for s in stats
    ]


@router.get("/usage/summary")
async def get_usage_summary(
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取使用汇总（用于仪表盘）
    """
    # 今日使用
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    today_query = select(func.count(), func.sum(UsageLog.cost)).where(
        and_(
            UsageLog.user_id == current_user.id,
            UsageLog.created_at >= today,
            UsageLog.status == "success"
        )
    )
    today_result = await db.execute(today_query)
    today_count, today_cost = today_result.fetchone()
    
    # 本月使用
    month_start = today.replace(day=1)
    month_query = select(func.count(), func.sum(UsageLog.cost)).where(
        and_(
            UsageLog.user_id == current_user.id,
            UsageLog.created_at >= month_start,
            UsageLog.status == "success"
        )
    )
    month_result = await db.execute(month_query)
    month_count, month_cost = month_result.fetchone()
    
    # 总计使用
    total_query = select(func.count(), func.sum(UsageLog.cost)).where(
        and_(
            UsageLog.user_id == current_user.id,
            UsageLog.status == "success"
        )
    )
    total_result = await db.execute(total_query)
    total_count, total_cost = total_result.fetchone()
    
    return {
        "today": {
            "requests": today_count or 0,
            "cost": float(today_cost or 0),
        },
        "this_month": {
            "requests": month_count or 0,
            "cost": float(month_cost or 0),
        },
        "total": {
            "requests": total_count or 0,
            "cost": float(total_cost or 0),
        }
    }
