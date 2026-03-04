"""
计费路由 - 充值订单和支付
"""
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.order import Order, Transaction, PricingPackage
from app.schemas import (
    CreateOrderRequest,
    OrderResponse,
    OrderListResponse,
    PricingPackageResponse,
)
from app.middleware import verify_api_key

router = APIRouter(prefix="/orders", tags=["Billing"])


def generate_order_no() -> str:
    """生成唯一订单号"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = uuid.uuid4().hex[:8].upper()
    return f"AK{timestamp}{random_suffix}"


@router.get("/packages", response_model=list[PricingPackageResponse])
async def get_pricing_packages(
    db: AsyncSession = Depends(get_db)
):
    """
    获取充值套餐列表
    """
    result = await db.execute(
        select(PricingPackage)
        .where(PricingPackage.is_active == True)
        .order_by(PricingPackage.sort_order)
    )
    packages = result.scalars().all()
    
    return [
        PricingPackageResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            amount=p.amount,
            credits=p.credits,
            bonus_credits=p.bonus_credits,
        )
        for p in packages
    ]


@router.post("/create", response_model=OrderResponse)
async def create_order(
    request: Request,
    data: CreateOrderRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    创建充值订单
    
    - 支持支付宝和微信支付
    - 返回支付跳转 URL
    """
    # 验证金额
    if data.amount < Decimal("0.01"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be at least ¥0.01"
        )
    
    # 创建订单
    order = Order(
        order_no=generate_order_no(),
        user_id=current_user.id,
        payment_method=data.payment_method,
        amount=data.amount,
        credits=int(data.amount * 10),  # 示例：1元 = 10积分
        description=data.description or "Account recharge",
        client_ip=request.client.host if request.client else None,
        expires_at=datetime.utcnow() + timedelta(hours=2),  # 2小时过期
    )
    
    db.add(order)
    await db.flush()
    
    # 创建支付（根据支付方式）
    checkout_url = None
    
    if data.payment_method == "alipay":
        # TODO: 调用支付宝 SDK 创建支付
        # checkout_url = await create_alipay_order(order)
        pass
    elif data.payment_method == "wechat":
        # TODO: 调用微信支付 SDK 创建支付
        # checkout_url = await create_wechat_order(order)
        pass
    
    return OrderResponse(
        id=order.id,
        order_no=order.order_no,
        amount=order.amount,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        created_at=order.created_at,
        expires_at=order.expires_at,
        checkout_url=checkout_url,
    )


@router.get("", response_model=OrderListResponse)
async def list_orders(
    status: str = Query(None, description="Filter by status: pending/paid/failed"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取订单列表
    """
    query = select(Order).where(Order.user_id == current_user.id)
    
    if status:
        query = query.where(Order.payment_status == status)
    
    # 统计总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页
    query = query.order_by(Order.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    pages = (total + page_size - 1) // page_size
    
    return OrderListResponse(
        items=[
            OrderResponse(
                id=item.id,
                order_no=item.order_no,
                amount=item.amount,
                payment_method=item.payment_method,
                payment_status=item.payment_status,
                created_at=item.created_at,
                expires_at=item.expires_at,
            )
            for item in items
        ],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/{order_no}", response_model=OrderResponse)
async def get_order(
    order_no: str,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取订单详情
    """
    result = await db.execute(
        select(Order).where(
            Order.order_no == order_no,
            Order.user_id == current_user.id
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponse(
        id=order.id,
        order_no=order.order_no,
        amount=order.amount,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        created_at=order.created_at,
        expires_at=order.expires_at,
    )


# ==================== Webhook 回调 ====================

@router.post("/webhook/alipay")
async def alipay_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    支付宝支付回调
    
    处理支付宝异步通知
    """
    # 获取表单数据
    form_data = await request.form()
    data = dict(form_data)
    
    # TODO: 验证支付宝签名
    # TODO: 处理支付结果
    
    return {"code": "SUCCESS", "message": "OK"}


@router.post("/webhook/wechat")
async def wechat_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    微信支付回调
    
    处理微信支付异步通知
    """
    # 获取 XML 数据
    xml_data = await request.body()
    
    # TODO: 解析 XML
    # TODO: 验证签名
    # TODO: 处理支付结果
    
    # 返回微信要求的响应格式
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
