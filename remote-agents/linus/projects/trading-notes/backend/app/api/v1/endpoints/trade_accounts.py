from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ....core.database import get_db
from ....core.security import encrypt_api_key, decode_token
from ....models.trade_account import TradeAccount as TradeAccountModel
from ....models.user import User as UserModel
from ....schemas.trade_account import TradeAccount, TradeAccountCreate, TradeAccountUpdate, TradeAccountWithCredentials, TradeAccountSyncResponse

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


@router.get("/", response_model=List[TradeAccount])
async def get_trade_accounts(
    account_type: Optional[str] = None,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有交易账户"""
    query = db.query(TradeAccountModel).filter(TradeAccountModel.user_id == user_id)

    if account_type:
        query = query.filter(TradeAccountModel.account_type == account_type)

    accounts = query.order_by(TradeAccountModel.created_at.desc()).all()

    # 为每个账户添加 has_api_credentials 字段
    result = []
    for account in accounts:
        account_dict = {
            **account.__dict__,
            "has_api_credentials": bool(account.api_key_encrypted and account.api_secret_encrypted),
            "has_gmail_credentials": bool(account.gmail_refresh_token_encrypted)
        }
        result.append(account_dict)

    return result


@router.post("/", response_model=TradeAccount, status_code=status.HTTP_201_CREATED)
async def create_trade_account(
    account_data: TradeAccountCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """创建新的交易账户"""
    # 验证账户类型
    valid_types = ["us_stock", "a_stock", "hk_stock", "crypto"]
    if account_data.account_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Must be one of: {', '.join(valid_types)}"
        )

    # 加密 API 凭证
    api_key_encrypted = None
    api_secret_encrypted = None

    if account_data.api_key:
        api_key_encrypted = encrypt_api_key(account_data.api_key)

    if account_data.api_secret:
        api_secret_encrypted = encrypt_api_key(account_data.api_secret)


    # 根据 crypto_sub_type 自动生成 extra_config
    extra_config = account_data.extra_config or {}
    if account_data.account_type == "crypto" and account_data.crypto_sub_type:
        if account_data.crypto_sub_type == "binance_spot":
            extra_config = {
                "trade_type": "spot",
                "exchange": "binance",
                "testnet": False
            }
        elif account_data.crypto_sub_type == "binance_futures":
            extra_config = {
                "trade_type": "futures",
                "contract_type": "perpetual",
                "hedge_mode": False,
                "default_leverage": 10,
                "exchange": "binance",
                "testnet": False
            }

    # 创建账户
    db_account = TradeAccountModel(
        user_id=user_id,
        account_name=account_data.account_name,
        account_type=account_data.account_type,
        broker=account_data.broker,
        description=account_data.description,
        tags=account_data.tags or [],
        api_key_encrypted=api_key_encrypted,
        api_secret_encrypted=api_secret_encrypted,
        ibkr_flex_token=account_data.ibkr_flex_token,
        ibkr_flex_query_id=account_data.ibkr_flex_query_id,
        gmail_address=None,
        gmail_refresh_token_encrypted=None,
        gmail_connected_at=None,
        extra_config=extra_config,
        sync_start_date=account_data.sync_start_date
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


@router.get("/{account_id}", response_model=TradeAccountWithCredentials)
async def get_trade_account(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取单个交易账户详情"""
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 返回账户信息，但不返回实际的 API 密钥，只返回是否设置
    account_dict = {
        **account.__dict__,
        "has_api_key": bool(account.api_key_encrypted),
        "has_api_secret": bool(account.api_secret_encrypted),
        "has_gmail_credentials": bool(account.gmail_refresh_token_encrypted)
    }

    return account_dict


@router.put("/{account_id}", response_model=TradeAccount)
async def update_trade_account(
    account_id: UUID,
    account_data: TradeAccountUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新交易账户信息"""
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 更新字段
    update_data = account_data.model_dump(exclude_unset=True)

    # 处理 API 凭证加密
    if "api_key" in update_data and update_data["api_key"]:
        account.api_key_encrypted = encrypt_api_key(update_data.pop("api_key"))

    if "api_secret" in update_data and update_data["api_secret"]:
        account.api_secret_encrypted = encrypt_api_key(update_data.pop("api_secret"))

    # 处理 IBKR Flex 凭证
    if "ibkr_flex_token" in update_data and update_data["ibkr_flex_token"]:
        account.ibkr_flex_token = update_data.pop("ibkr_flex_token")

    if "ibkr_flex_query_id" in update_data and update_data["ibkr_flex_query_id"]:
        account.ibkr_flex_query_id = update_data.pop("ibkr_flex_query_id")

    # 更新其他字段
    for field, value in update_data.items():
        if hasattr(account, field):
            setattr(account, field, value)

    db.commit()
    db.refresh(account)

    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade_account(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除交易账户"""
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    db.delete(account)
    db.commit()

    return None


@router.get("/stats/by-type")
async def get_trade_accounts_stats(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取按市场类型统计的交易账户数量"""
    accounts = db.query(TradeAccountModel).filter(
        TradeAccountModel.user_id == user_id,
        TradeAccountModel.is_active == True
    ).all()

    stats = {
        "us_stock": {"count": 0, "accounts": []},
        "a_stock": {"count": 0, "accounts": []},
        "hk_stock": {"count": 0, "accounts": []},
        "crypto": {"count": 0, "accounts": []}
    }

    for account in accounts:
        if account.account_type in stats:
            stats[account.account_type]["count"] += 1
            stats[account.account_type]["accounts"].append({
                "id": str(account.id),
                "name": account.account_name,
                "last_sync_at": account.last_sync_at
            })

    return stats


@router.post("/{account_id}/sync")
async def sync_trade_account(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """手动同步交易账户数据（异步任务）

    对于支持 API 的交易账户，从交易所/券商 API 拉取最新交易数据
    返回任务 ID，用于后续查询同步状态
    """
    import logging
    from ....tasks.sync_tasks import sync_account_trades

    logger = logging.getLogger(__name__)

    # 验证账户所有权
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 检查账户类型
    if account.account_type != "crypto":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only crypto accounts support automatic sync currently"
        )

    # 检查账户是否配置了 API 凭证
    if not account.api_key_encrypted or not account.api_secret_encrypted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account API credentials not configured"
        )

    # 提交异步任务
    logger.info(f"提交账户 {account_id} 的同步任务")
    task = sync_account_trades.delay(str(account_id))

    return {
        "status": "pending",
        "message": "Sync task submitted",
        "task_id": task.id,
        "account_id": str(account_id)
    }


@router.get("/sync/task/{task_id}")
async def get_sync_task_status(
    task_id: str,
    user_id: UUID = Depends(get_current_user_id)
):
    """查询同步任务状态

    返回任务的当前状态、进度和结果
    """
    from celery.result import AsyncResult
    from ....core.celery_app import celery_app

    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.state,
    }

    if task_result.state == 'PENDING':
        response["message"] = "Task is waiting to be executed"
    elif task_result.state == 'PROGRESS':
        response["message"] = "Task is in progress"
        response["meta"] = task_result.info
    elif task_result.state == 'SUCCESS':
        response["message"] = "Task completed successfully"
        response["result"] = task_result.result
    elif task_result.state == 'FAILURE':
        response["message"] = "Task failed"
        response["error"] = str(task_result.info)
    else:
        response["message"] = f"Task status: {task_result.state}"

    return response


@router.delete("/{account_id}/data", status_code=status.HTTP_200_OK)
async def clear_account_data(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """清除交易账户的所有交易数据

    注意：此操作不可逆，将删除该账户下的所有交易记录、持仓等数据
    """
    from ....services.binance_sync_service import BinanceSyncService

    # 验证账户所有权
    account = db.query(TradeAccountModel).filter(
        TradeAccountModel.id == account_id,
        TradeAccountModel.user_id == user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade account not found"
        )

    # 清除数据
    sync_service = BinanceSyncService(db)
    result = sync_service.clear_account_trades(str(account_id))

    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get('error', 'Failed to clear data')
        )

    return {
        "status": "success",
        "message": f"Successfully cleared {result['deleted_count']} trades, {result['positions_deleted']} positions, {result['closed_positions_deleted']} closed positions",
        "account_id": str(account_id),
        "deleted_count": result['deleted_count'],
        "positions_deleted": result['positions_deleted'],
        "closed_positions_deleted": result['closed_positions_deleted']
    }
