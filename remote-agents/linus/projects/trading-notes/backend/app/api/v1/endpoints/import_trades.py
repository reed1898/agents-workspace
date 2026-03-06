"""交易记录导入API端点"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional

from ....core.database import get_db
from ....core.security import decode_token, decrypt_api_key, encrypt_api_key
from ....core.config import settings
from ....models.import_history import ImportHistory as ImportHistoryModel
from ....models.trade_account import TradeAccount
from ....models.trade import Trade as TradeModel
from ....schemas.import_history import (
    ImportHistory,
    ImportHistoryList,
    CSVImportResponse,
    GmailSyncResponse,
    GmailSyncFileResult
)
from ....schemas.trade import TradeBase
from ....services.csv_parser_service import get_parser, CSVParseError
from ....services.gmail_sync_service import (
    GmailApiService,
    GmailOAuthError,
    build_gmail_oauth_url,
    exchange_code_for_tokens,
    refresh_access_token,
)
from jose import jwt, JWTError
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
import httpx
import logging
import hashlib


router = APIRouter()
logger = logging.getLogger(__name__)


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


def _build_gmail_oauth_state(user_id: UUID, account_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "account_id": str(account_id),
        "exp": datetime.utcnow() + timedelta(minutes=10),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _decode_gmail_oauth_state(state: str) -> dict:
    try:
        return jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的授权状态: {str(exc)}"
        )


def _get_gmail_oauth_config() -> tuple[str, str, str]:
    client_id = settings.GOOGLE_GMAIL_CLIENT_ID or settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_GMAIL_CLIENT_SECRET or settings.GOOGLE_CLIENT_SECRET
    redirect_uri = settings.GOOGLE_GMAIL_REDIRECT_URI or settings.GOOGLE_REDIRECT_URI

    logger.info(
        "Gmail OAuth config loaded: gmail_client_id_set=%s gmail_client_secret_set=%s gmail_redirect_uri=%s "
        "fallback_client_id_set=%s fallback_client_secret_set=%s fallback_redirect_uri=%s selected_redirect_uri=%s",
        bool(settings.GOOGLE_GMAIL_CLIENT_ID),
        bool(settings.GOOGLE_GMAIL_CLIENT_SECRET),
        bool(settings.GOOGLE_GMAIL_REDIRECT_URI),
        bool(settings.GOOGLE_CLIENT_ID),
        bool(settings.GOOGLE_CLIENT_SECRET),
        bool(settings.GOOGLE_REDIRECT_URI),
        redirect_uri,
    )

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gmail OAuth 未配置"
        )

    return client_id, client_secret, redirect_uri


def _import_trades_from_bytes(
    db: Session,
    account: TradeAccount,
    user_id: UUID,
    filename: str,
    file_content: bytes,
    import_source: str
) -> CSVImportResponse:
    broker_template = account.broker
    if not broker_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户未设置券商类型,请先在账户设置中配置券商信息"
        )

    try:
        parser = get_parser(broker_template)
        trades_data = parser.parse_file(filename, file_content)
        parse_errors = parser.errors
    except CSVParseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件解析失败: {str(e)}"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"不支持的券商类型: {broker_template}。"
                "支持的券商: tonghuashun, gtja, guosen, moomoo, ibkr, generic"
            )
        )

    if (
        getattr(parser, "cash_balance", None) is not None
        and getattr(parser, "IMPORT_CASH_BALANCE", True)
    ):
        account.cash_balance = parser.cash_balance
        account.cash_currency = parser.cash_currency

    import_history = ImportHistoryModel(
        account_id=account.id,
        user_id=user_id,
        filename=filename,
        broker_template=broker_template,
        import_source=import_source,
        total_rows=len(trades_data) + len(parse_errors)
    )
    db.add(import_history)
    db.flush()

    success_count = 0
    failed_count = len(parse_errors)
    duplicate_count = 0

    for trade_data in trades_data:
        try:
            existing = db.query(TradeModel).filter(
                TradeModel.account_id == account.id,
                TradeModel.trade_id_external == trade_data['trade_id_external']
            ).first()

            if existing:
                duplicate_count += 1
                continue

            trade = TradeModel(
                account_id=account.id,
                symbol=trade_data['symbol'],
                side=trade_data['side'],
                quantity=trade_data['quantity'],
                price=trade_data['price'],
                fee=trade_data['fee'],
                trade_time=datetime.fromisoformat(trade_data['trade_time']),
                trade_id_external=trade_data['trade_id_external'],
                sync_source="import",
                notes=trade_data.get('notes', '')
            )
            db.add(trade)
            success_count += 1

        except Exception as e:
            failed_count += 1
            parse_errors.append({
                'row': 'unknown',
                'error': f"数据库插入失败: {str(e)}"
            })

    import_history.success_count = success_count
    import_history.failed_count = failed_count
    import_history.duplicate_count = duplicate_count
    import_history.error_details = {'errors': parse_errors} if parse_errors else None
    import_history.completed_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(import_history)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库提交失败: {str(e)}"
        )

    if success_count > 0:
        try:
            from ....services.position_service import PositionService
            position_service = PositionService(db)
            position_service.calculate_positions_for_account(account.id)
        except Exception:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("持仓计算失败", exc_info=True)

    if success_count == len(trades_data):
        message = f"导入成功! 共导入 {success_count} 条交易记录,持仓已更新"
    elif success_count > 0:
        message = (
            f"部分导入成功: {success_count} 条成功, {failed_count} 条失败, {duplicate_count} 条重复,持仓已更新"
        )
    else:
        message = f"导入失败: {failed_count} 条失败, {duplicate_count} 条重复"

    return CSVImportResponse(
        import_id=import_history.id,
        total_rows=import_history.total_rows,
        success_count=success_count,
        failed_count=failed_count,
        duplicate_count=duplicate_count,
        error_details=parse_errors if parse_errors else None,
        message=message
    )


@router.post("/csv-upload", response_model=CSVImportResponse, status_code=status.HTTP_201_CREATED)
async def upload_csv_import(
    account_id: UUID = Form(..., description="交易账户ID"),
    file: UploadFile = File(..., description="CSV/Excel文件"),
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    CSV/Excel文件导入交易记录

    支持的券商模板:
    - tonghuashun: 同花顺
    - gtja: 国泰君安/国泰海通
    - guosen: 国信证券 (Excel)
    - moomoo: moomoo
    - ibkr: 盈透证券
    - generic: 通用格式

    流程:
    1. 验证账户所有权
    2. 根据账户broker字段自动选择解析模板
    3. 解析CSV文件
    4. 创建导入历史记录
    5. 批量插入交易记录
    6. 更新导入统计
    """
    # 1. 验证账户所有权
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == current_user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="账户不存在或无权访问"
        )

    # 2. 根据账户broker字段自动选择模板
    if not account.broker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户未设置券商类型,请先在账户设置中配置券商信息"
        )

    broker_template = account.broker

    # 验证文件类型
    if not file.filename.lower().endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持CSV或Excel文件"
        )

    # 文件大小限制 (10MB)
    file_content = await file.read()
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="文件大小不能超过10MB"
        )

    # 3. 解析文件
    try:
        parser = get_parser(broker_template)
        trades_data = parser.parse_file(file.filename, file_content)
        parse_errors = parser.errors

    except CSVParseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件解析失败: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"不支持的券商类型: {broker_template}。"
                "支持的券商: tonghuashun, gtja, guosen, moomoo, ibkr, generic"
            )
        )

    # 3. 创建导入历史记录
    # 注意：部分券商的资金流水“余额/剩余资金”字段可能存在口径问题，默认不一定可用于自动更新账户余额。
    if (
        getattr(parser, "cash_balance", None) is not None
        and getattr(parser, "IMPORT_CASH_BALANCE", True)
    ):
        account.cash_balance = parser.cash_balance
        account.cash_currency = parser.cash_currency

    import_history = ImportHistoryModel(
        account_id=account_id,
        user_id=current_user_id,
        filename=file.filename,
        broker_template=broker_template,
        import_source="csv_import",
        total_rows=len(trades_data) + len(parse_errors)
    )
    db.add(import_history)
    db.flush()  # 获取ID但不提交

    # 4. 批量插入交易记录
    success_count = 0
    failed_count = len(parse_errors)
    duplicate_count = 0

    for trade_data in trades_data:
        try:
            # 检查是否重复(基于external_id)
            existing = db.query(TradeModel).filter(
                TradeModel.account_id == account_id,
                TradeModel.trade_id_external == trade_data['trade_id_external']
            ).first()

            if existing:
                duplicate_count += 1
                continue

            # 创建交易记录
            trade = TradeModel(
                account_id=account_id,
                symbol=trade_data['symbol'],
                side=trade_data['side'],
                quantity=trade_data['quantity'],
                price=trade_data['price'],
                fee=trade_data['fee'],
                trade_time=datetime.fromisoformat(trade_data['trade_time']),
                trade_id_external=trade_data['trade_id_external'],
                sync_source="import",
                notes=trade_data.get('notes', '')
            )
            db.add(trade)
            success_count += 1

        except Exception as e:
            failed_count += 1
            parse_errors.append({
                'row': 'unknown',
                'error': f"数据库插入失败: {str(e)}"
            })

    # 5. 更新导入历史统计
    import_history.success_count = success_count
    import_history.failed_count = failed_count
    import_history.duplicate_count = duplicate_count
    import_history.error_details = {'errors': parse_errors} if parse_errors else None
    import_history.completed_at = datetime.utcnow()

    # 提交事务
    try:
        db.commit()
        db.refresh(import_history)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库提交失败: {str(e)}"
        )

    # 6. 导入成功后,计算持仓
    if success_count > 0:
        try:
            from ....services.position_service import PositionService
            position_service = PositionService(db)
            position_service.calculate_positions_for_account(account_id)
        except Exception as e:
            # 持仓计算失败不影响导入成功,只记录日志
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"持仓计算失败: {str(e)}", exc_info=True)

    # 构建响应消息
    if success_count == len(trades_data):
        message = f"导入成功! 共导入 {success_count} 条交易记录,持仓已更新"
    elif success_count > 0:
        message = f"部分导入成功: {success_count} 条成功, {failed_count} 条失败, {duplicate_count} 条重复,持仓已更新"
    else:
        message = f"导入失败: {failed_count} 条失败, {duplicate_count} 条重复"

    return CSVImportResponse(
        import_id=import_history.id,
        total_rows=import_history.total_rows,
        success_count=success_count,
        failed_count=failed_count,
        duplicate_count=duplicate_count,
        error_details=parse_errors if parse_errors else None,
        message=message
    )


@router.get("/history/{account_id}", response_model=ImportHistoryList)
def get_import_history(
    account_id: UUID,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    获取指定账户的导入历史记录

    Args:
        account_id: 账户ID
        skip: 跳过记录数
        limit: 返回记录数限制

    Returns:
        导入历史列表
    """
    # 验证账户所有权
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == current_user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="账户不存在或无权访问"
        )

    # 查询导入历史
    query = db.query(ImportHistoryModel).filter(
        ImportHistoryModel.account_id == account_id
    ).order_by(ImportHistoryModel.created_at.desc())

    total = query.count()
    imports = query.offset(skip).limit(limit).all()

    return ImportHistoryList(
        imports=imports,
        total=total
    )


@router.get("/gmail/oauth/start")
def start_gmail_oauth(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """发起 Gmail OAuth 授权"""
    logger.info("Start Gmail OAuth: account_id=%s user_id=%s", account_id, current_user_id)

    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == current_user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="账户不存在或无权访问"
        )

    client_id, client_secret, redirect_uri = _get_gmail_oauth_config()

    if account.broker != "gtja":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该账户不支持 Gmail 自动同步"
        )

    try:
        client_id, client_secret, redirect_uri = _get_gmail_oauth_config()
        state = _build_gmail_oauth_state(current_user_id, account_id)
        auth_url = build_gmail_oauth_url(
            client_id,
            redirect_uri,
            state
        )
        return {"auth_url": auth_url}
    except HTTPException:
        logger.exception("Gmail OAuth start failed due to config or validation error")
        raise
    except Exception:
        logger.exception("Gmail OAuth start failed due to unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gmail OAuth 启动失败"
        )


@router.get("/gmail/oauth/callback", response_class=HTMLResponse)
def gmail_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Gmail OAuth 回调"""
    if not code or not state:
        return HTMLResponse("缺少授权参数，请关闭窗口重试。", status_code=400)

    try:
        payload = _decode_gmail_oauth_state(state)
    except HTTPException as exc:
        return HTMLResponse(exc.detail, status_code=exc.status_code)
    user_id = payload.get("sub")
    account_id = payload.get("account_id")

    if not user_id or not account_id:
        return HTMLResponse("授权状态无效，请关闭窗口重试。", status_code=400)

    try:
        user_uuid = UUID(user_id)
        account_uuid = UUID(account_id)
    except ValueError:
        return HTMLResponse("授权状态无效，请关闭窗口重试。", status_code=400)

    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_uuid,
        TradeAccount.user_id == user_uuid
    ).first()

    if not account:
        return HTMLResponse("账户不存在或无权访问。", status_code=404)

    if account.broker != "gtja":
        return HTMLResponse("该账户不支持 Gmail 自动同步。", status_code=400)

    try:
        client_id, client_secret, redirect_uri = _get_gmail_oauth_config()
    except HTTPException as exc:
        return HTMLResponse(exc.detail, status_code=exc.status_code)

    try:
        token_data = exchange_code_for_tokens(
            client_id,
            client_secret,
            redirect_uri,
            code
        )
    except GmailOAuthError as exc:
        return HTMLResponse(f"Gmail 授权失败: {str(exc)}", status_code=400)

    refresh_token = token_data.get("refresh_token")
    access_token = token_data.get("access_token")
    if not refresh_token and not account.gmail_refresh_token_encrypted:
        return HTMLResponse("未获取到刷新令牌，请选择继续授权。", status_code=400)

    email_address = None
    id_token_str = token_data.get("id_token")
    if id_token_str:
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str,
                google_requests.Request(),
                client_id
            )
            email_address = idinfo.get("email")
        except Exception:
            email_address = None

    if not email_address and access_token:
        try:
            resp = httpx.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10.0
            )
            if resp.status_code == 200:
                email_address = resp.json().get("email")
        except Exception:
            email_address = None

    if refresh_token:
        account.gmail_refresh_token_encrypted = encrypt_api_key(refresh_token)
        account.gmail_connected_at = datetime.utcnow()

    if email_address:
        account.gmail_address = email_address

    db.commit()

    return HTMLResponse(
        "<html><body>Gmail 授权成功，可以关闭窗口。"
        "<script>window.close();</script></body></html>"
    )


@router.post("/gmail-sync", response_model=GmailSyncResponse)
def gmail_sync_import(
    account_id: UUID,
    since_days: int = 7,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """从 Gmail 拉取国泰海通邮件附件并导入交易记录"""
    account = db.query(TradeAccount).filter(
        TradeAccount.id == account_id,
        TradeAccount.user_id == current_user_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="账户不存在或无权访问"
        )

    if account.broker != "gtja":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该账户不支持 Gmail 自动同步"
        )

    if not account.gmail_refresh_token_encrypted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先完成 Gmail 授权绑定"
        )

    client_id, client_secret, _ = _get_gmail_oauth_config()
    refresh_token = decrypt_api_key(account.gmail_refresh_token_encrypted)
    try:
        access_token = refresh_access_token(
            client_id,
            client_secret,
            refresh_token
        )
        service = GmailApiService(access_token)
        attachments = service.fetch_attachments(
            sender="SecuritiesDepository@gtht.com",
            subject_prefix="0391510001668558",
            since_days=since_days
        )
    except GmailOAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gmail 同步失败: {str(exc)}"
        )

    if not attachments:
        return GmailSyncResponse(
            files_imported=0,
            files_skipped=0,
            files_failed=0,
            total_success_count=0,
            total_failed_count=0,
            total_duplicate_count=0,
            message="未找到可导入的邮件附件",
            details=[]
        )

    trade_keywords = ("交易明细", "成交明细")
    filtered_attachments = [
        attachment for attachment in attachments
        if any(keyword in attachment.get("filename", "") for keyword in trade_keywords)
    ]

    if not filtered_attachments:
        return GmailSyncResponse(
            files_imported=0,
            files_skipped=len(attachments),
            files_failed=0,
            total_success_count=0,
            total_failed_count=0,
            total_duplicate_count=0,
            message="未找到交易明细附件",
            details=[]
        )

    files_imported = 0
    files_skipped = len(attachments) - len(filtered_attachments)
    files_failed = 0
    total_success = 0
    total_failed = 0
    total_duplicate = 0
    details: List[GmailSyncFileResult] = []

    for attachment in filtered_attachments:
        raw_key = (
            attachment.get("message_key")
            or attachment.get("message_id")
            or attachment.get("filename")
            or "unknown"
        )
        message_key = hashlib.md5(str(raw_key).encode()).hexdigest()
        import_filename = f"gmail:{message_key}:{attachment['filename']}"
        if len(import_filename) > 255:
            import_filename = import_filename[:255]

        existing = db.query(ImportHistoryModel).filter(
            ImportHistoryModel.account_id == account_id,
            ImportHistoryModel.filename == import_filename,
            ImportHistoryModel.import_source == "gmail_sync"
        ).first()
        if existing:
            files_skipped += 1
            continue

        try:
            result = _import_trades_from_bytes(
                db=db,
                account=account,
                user_id=current_user_id,
                filename=import_filename,
                file_content=attachment["content"],
                import_source="gmail_sync"
            )
            files_imported += 1
            total_success += result.success_count
            total_failed += result.failed_count
            total_duplicate += result.duplicate_count
            details.append(GmailSyncFileResult(
                filename=attachment["filename"],
                import_id=result.import_id,
                success_count=result.success_count,
                failed_count=result.failed_count,
                duplicate_count=result.duplicate_count,
                message=result.message
            ))
        except HTTPException as e:
            files_failed += 1
            db.rollback()
            details.append(GmailSyncFileResult(
                filename=attachment["filename"],
                import_id=None,
                success_count=0,
                failed_count=0,
                duplicate_count=0,
                message=str(e.detail)
            ))

    account.last_sync_at = datetime.utcnow()
    db.commit()

    message = (
        f"导入 {files_imported} 个附件,跳过 {files_skipped} 个,失败 {files_failed} 个,"
        f"新增 {total_success} 条交易记录"
    )

    return GmailSyncResponse(
        files_imported=files_imported,
        files_skipped=files_skipped,
        files_failed=files_failed,
        total_success_count=total_success,
        total_failed_count=total_failed,
        total_duplicate_count=total_duplicate,
        message=message,
        details=details
    )


@router.get("/templates", response_model=List[dict])
def get_supported_templates():
    """
    获取支持的券商模板列表

    Returns:
        券商模板列表
    """
    from ....services.csv_parser_service import BROKER_TEMPLATES

    templates = []
    for key, template_class in BROKER_TEMPLATES.items():
        templates.append({
            'value': key,
            'label': {
                'tonghuashun': '同花顺',
                'gtja': '国泰君安',
                'guosen': '国信证券',
                'moomoo': 'moomoo',
                'ibkr': '盈透证券',
                'generic': '通用格式'
            }.get(key, key),
            'description': template_class.__doc__ or ''
        })

    return templates
