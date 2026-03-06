"""
Celery 任务：交易账户同步
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID
import asyncio

from ..core.celery_app import celery_app
from ..core.config import settings
from ..services.binance_sync_service import BinanceSyncService
from ..services.ibkr_flex_service import IBKRFlexService
from ..services.trade_import_service import TradeImportService
from ..models.trade_account import TradeAccount
from ..models.import_history import ImportHistory
from ..models.position import Position as PositionModel
from ..services.market_data_service import MarketDataService

logger = logging.getLogger(__name__)

# 创建数据库会话工厂
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True, name="refresh_position_prices")
def refresh_position_prices(self, user_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
    """
    异步刷新持仓价格的 Celery 任务

    Args:
        user_id: 用户 ID
        account_id: 可选账户 ID
    """
    db = SessionLocal()
    try:
        logger.info(f"开始异步刷新持仓价格，任务 ID: {self.request.id}")

        self.update_state(state='PROGRESS', meta={'status': 'fetching', 'progress': 10})

        user_uuid = UUID(user_id)
        account_uuid = UUID(account_id) if account_id else None

        query = db.query(PositionModel).join(
            TradeAccount,
            PositionModel.account_id == TradeAccount.id
        ).filter(
            TradeAccount.user_id == user_uuid,
            PositionModel.is_closed == False
        )

        if account_uuid:
            query = query.filter(PositionModel.account_id == account_uuid)

        positions = query.all()
        total_positions = len(positions)
        if total_positions == 0:
            return {
                'status': 'success',
                'updated_count': 0,
                'failed_count': 0,
                'total_positions': 0,
                'completed_at': datetime.utcnow().isoformat()
            }

        for position in positions:
            if not hasattr(position, 'account') or position.account is None:
                position.account = db.query(TradeAccount).filter(
                    TradeAccount.id == position.account_id
                ).first()

        self.update_state(state='PROGRESS', meta={'status': 'updating', 'progress': 30})

        async def _run_update() -> int:
            service = MarketDataService()
            try:
                return await service.update_position_prices(positions, db)
            finally:
                await service.close()

        updated_count = asyncio.run(_run_update())
        failed_count = total_positions - updated_count

        return {
            'status': 'success',
            'updated_count': updated_count,
            'failed_count': failed_count,
            'total_positions': total_positions,
            'completed_at': datetime.utcnow().isoformat()
        }

    except Exception as exc:
        logger.error(f"刷新持仓价格失败: {str(exc)}", exc_info=True)
        return {
            'status': 'failed',
            'error': str(exc),
            'completed_at': datetime.utcnow().isoformat()
        }
    finally:
        db.close()


@celery_app.task(bind=True, name="sync_account_trades")
def sync_account_trades(self, account_id: str) -> Dict[str, Any]:
    """
    同步交易账户数据的 Celery 任务

    Args:
        self: Celery task instance
        account_id: 交易账户 ID

    Returns:
        包含同步结果的字典
    """
    db = SessionLocal()
    try:
        logger.info(f"开始异步同步账户 {account_id} 的交易数据，任务 ID: {self.request.id}")

        # 更新任务状态为进行中
        self.update_state(state='PROGRESS', meta={'status': 'syncing', 'progress': 0})

        sync_service = BinanceSyncService(db)
        result = sync_service.sync_trades(account_id)

        logger.info(f"账户 {account_id} 同步完成: {result}")

        if result['success']:
            return {
                'status': 'success',
                'account_id': account_id,
                'synced_count': result.get('synced_count', 0),
                'last_sync_at': result.get('last_sync_at'),
                'completed_at': datetime.utcnow().isoformat()
            }
        else:
            return {
                'status': 'failed',
                'account_id': account_id,
                'error': result.get('error', 'Unknown error'),
                'completed_at': datetime.utcnow().isoformat()
            }

    except Exception as e:
        logger.error(f"同步账户 {account_id} 时发生异常: {str(e)}", exc_info=True)
        return {
            'status': 'failed',
            'account_id': account_id,
            'error': str(e),
            'completed_at': datetime.utcnow().isoformat()
        }
    finally:
        db.close()


@celery_app.task(bind=True, name="import_ibkr_trades")
def import_ibkr_trades(self, account_id: str, token: str, query_id: str) -> Dict[str, Any]:
    """
    异步导入 IBKR 交易数据的 Celery 任务

    Args:
        self: Celery task instance
        account_id: 交易账户 ID
        token: IBKR Flex Query token
        query_id: IBKR Flex Query ID

    Returns:
        包含导入结果的字典
    """
    db = SessionLocal()
    try:
        try:
            account_uuid = account_id if isinstance(account_id, UUID) else UUID(account_id)
        except (TypeError, ValueError):
            logger.error(f"无效的账户 ID: {account_id}")
            return {
                'status': 'failed',
                'account_id': str(account_id),
                'error': 'Invalid account_id',
                'completed_at': datetime.utcnow().isoformat()
            }

        account_id_str = str(account_uuid)

        logger.info(f"开始异步导入 IBKR 账户 {account_id_str} 的交易数据，任务 ID: {self.request.id}")

        # 更新任务状态为进行中
        self.update_state(state='PROGRESS', meta={'status': 'fetching', 'progress': 10})

        # 获取账户信息
        account = db.query(TradeAccount).filter(TradeAccount.id == account_uuid).first()
        if not account:
            return {
                'status': 'failed',
                'account_id': account_id_str,
                'error': 'Account not found',
                'completed_at': datetime.utcnow().isoformat()
            }

        # Step 1: 使用 Flex API 获取数据
        self.update_state(state='PROGRESS', meta={'status': 'requesting_statement', 'progress': 20})
        flex_service = IBKRFlexService(token, query_id)

        try:
            flex_result = flex_service.fetch_trades_and_cash()
            trades_data = flex_result.get("trades", [])
            cash_balance = flex_result.get("cash_balance")
            cash_currency = flex_result.get("cash_currency")
        except Exception as e:
            logger.error(f"Failed to fetch IBKR trades: {str(e)}")
            return {
                'status': 'failed',
                'account_id': account_id,
                'error': f'IBKR API error: {str(e)}',
                'completed_at': datetime.utcnow().isoformat()
            }

        self.update_state(state='PROGRESS', meta={'status': 'parsing', 'progress': 50})

        # Step 2: 使用统一的交易导入服务（自动处理去重、存储和持仓计算）
        trade_import_service = TradeImportService(db)

        # 标准化交易数据格式
        normalized_trades = []
        for trade_data in trades_data:
            normalized_trade = {
                'symbol': trade_data['symbol'],
                'side': trade_data['side'],
                'quantity': trade_data['quantity'],
                'price': trade_data['price'],
                'trade_date': trade_data.get('trade_date') or datetime.utcnow(),
                'external_trade_id': trade_data.get('external_trade_id'),
                'fee': trade_data.get('commission', 0.0),
                'fee_currency': trade_data.get('currency', 'USD'),
                'position_side': trade_data.get('position_side'),
                'leverage': trade_data.get('leverage'),
                'margin': trade_data.get('margin'),
                'notes': f"IBKR Flex Import - Asset: {trade_data.get('asset_class', 'Unknown')}"
            }
            normalized_trades.append(normalized_trade)

        self.update_state(state='PROGRESS', meta={'status': 'saving', 'progress': 80})

        # 批量导入交易并自动计算持仓
        try:
            import_result = trade_import_service.import_trades(
                account_id=account_uuid,
                trades_data=normalized_trades,
                sync_source='api'
            )
            imported_count = import_result['imported_count']
            skipped_count = import_result['skipped_count']
            error_count = import_result['error_count']
        except Exception as e:
            logger.error(f"Trade import service failed: {str(e)}", exc_info=True)
            return {
                'status': 'failed',
                'account_id': account_id_str,
                'error': f'Trade import failed: {str(e)}',
                'completed_at': datetime.utcnow().isoformat()
            }

        # Step 3: 记录导入历史
        import_history = ImportHistory(
            account_id=account_uuid,
            user_id=account.user_id,
            filename=f'ibkr_flex_query_{query_id}',
            broker_template='ibkr_flex',
            import_source='ibkr_flex_api',
            total_rows=len(trades_data),
            success_count=imported_count,
            failed_count=error_count,
            duplicate_count=skipped_count,
            error_details={
                'query_id': query_id,
                'task_id': self.request.id
            } if error_count > 0 else None,
            completed_at=datetime.utcnow()
        )
        db.add(import_history)

        # 更新账户余额和同步时间
        if cash_balance is not None:
            account.cash_balance = cash_balance
            account.cash_currency = cash_currency
        account.last_sync_at = datetime.utcnow()

        db.commit()

        self.update_state(state='PROGRESS', meta={'status': 'completed', 'progress': 100})

        logger.info(f"IBKR 导入完成 - 账户: {account_id_str}, 导入: {imported_count}, 跳过: {skipped_count}, 错误: {error_count}")

        return {
            'status': 'success',
            'account_id': account_id_str,
            'imported_count': imported_count,
            'skipped_count': skipped_count,
            'error_count': error_count,
            'completed_at': datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"导入 IBKR 账户 {account_id} 时发生异常: {str(e)}", exc_info=True)
        db.rollback()
        return {
            'status': 'failed',
            'account_id': str(account_id),
            'error': str(e),
            'completed_at': datetime.utcnow().isoformat()
        }
    finally:
        db.close()
