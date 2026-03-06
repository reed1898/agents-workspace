"""
IBKR Flex API 导入端点
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
from celery.result import AsyncResult
from uuid import UUID

from ....core.database import get_db
from ....core.security import decode_token
from ....core.celery_app import celery_app
from ....models.trade_account import TradeAccount
from ....tasks.sync_tasks import import_ibkr_trades

router = APIRouter()


def get_current_user_id(authorization: str = Header(...)) -> UUID:
    """从 JWT Token 获取当前用户 ID"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return UUID(payload["sub"])


class IBKRImportRequest(BaseModel):
    """IBKR 导入请求"""
    token: str
    query_id: str
    save_credentials: bool = False  # 是否保存凭证到账户


class IBKRImportResponse(BaseModel):
    """IBKR 导入响应"""
    task_id: str
    message: str
    account_id: str


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str
    status: str  # PENDING, PROGRESS, SUCCESS, FAILURE
    progress: int  # 0-100
    result: Dict[str, Any] | None = None
    error: str | None = None


@router.post("/{account_id}/import", response_model=IBKRImportResponse)
async def import_ibkr_account_trades(
    account_id: UUID,
    request: IBKRImportRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    使用 IBKR Flex API 导入交易数据（异步）

    Args:
        account_id: 交易账户 ID
        request: 包含 token 和 query_id 的请求
        db: 数据库会话

    Returns:
        包含任务 ID 的响应
    """
    # 验证账户存在且属于当前用户
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == user_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # 如果需要保存凭证
    if request.save_credentials:
        account.ibkr_flex_token = request.token
        account.ibkr_flex_query_id = request.query_id
        db.commit()

    # 启动异步任务
    try:
        task = import_ibkr_trades.delay(
            account_id=str(account_id),
            token=request.token,
            query_id=request.query_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to start background task. Please ensure the task worker is running. Error: {str(e)}"
        )

    return IBKRImportResponse(
        task_id=task.id,
        message="IBKR import task started",
        account_id=str(account_id)
    )


@router.post("/{account_id}/import-with-saved-credentials", response_model=IBKRImportResponse)
async def import_ibkr_with_saved_credentials(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    使用账户已保存的 IBKR Flex 凭证导入交易数据

    Args:
        account_id: 交易账户 ID
        db: 数据库会话

    Returns:
        包含任务 ID 的响应
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"=== IBKR Import Request ===")
    logger.info(f"Account ID: {account_id}")

    # 获取账户（验证属于当前用户）
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == user_id
    ).first()
    if not account:
        logger.error(f"Account not found: {account_id}")
        raise HTTPException(status_code=404, detail="Account not found")

    logger.info(f"Account found: {account.account_name}")
    logger.info(f"IBKR Flex Token: {account.ibkr_flex_token}")
    logger.info(f"IBKR Flex Query ID: {account.ibkr_flex_query_id}")

    # 验证凭证
    if not account.ibkr_flex_token or not account.ibkr_flex_query_id:
        logger.error("IBKR Flex credentials not configured")
        raise HTTPException(
            status_code=400,
            detail="IBKR Flex credentials not configured for this account"
        )

    # 启动异步任务
    logger.info("Starting async task...")
    try:
        task = import_ibkr_trades.delay(
            account_id=str(account_id),
            token=account.ibkr_flex_token,
            query_id=account.ibkr_flex_query_id
        )
        logger.info(f"Task started with ID: {task.id}")
    except Exception as e:
        logger.error(f"Failed to start Celery task: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Failed to start background task. Please ensure the task worker is running. Error: {str(e)}"
        )

    return IBKRImportResponse(
        task_id=task.id,
        message="IBKR import task started with saved credentials",
        account_id=str(account_id)
    )


@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_import_task_status(
    task_id: str,
    user_id: UUID = Depends(get_current_user_id)
):
    """
    获取导入任务状态

    Args:
        task_id: Celery 任务 ID

    Returns:
        任务状态信息
    """
    task_result = AsyncResult(task_id, app=celery_app)

    # 获取任务状态
    status = task_result.state
    progress = 0
    result = None
    error = None

    if status == 'PENDING':
        progress = 0
    elif status == 'PROGRESS':
        # 从任务 meta 中获取进度
        info = task_result.info or {}
        progress = info.get('progress', 0)
    elif status == 'SUCCESS':
        progress = 100
        result = task_result.result
    elif status == 'FAILURE':
        progress = 0
        error = str(task_result.info)

    return TaskStatusResponse(
        task_id=task_id,
        status=status,
        progress=progress,
        result=result,
        error=error
    )


@router.delete("/{account_id}/credentials")
async def delete_ibkr_credentials(
    account_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    删除账户的 IBKR Flex 凭证

    Args:
        account_id: 交易账户 ID
        db: 数据库会话

    Returns:
        成功消息
    """
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == user_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.ibkr_flex_token = None
    account.ibkr_flex_query_id = None
    db.commit()

    return {"message": "IBKR Flex credentials deleted successfully"}
