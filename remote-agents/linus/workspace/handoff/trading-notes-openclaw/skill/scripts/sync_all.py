#!/usr/bin/env python3
"""
Sync all configured trading accounts in one go.

Detects account type and runs appropriate sync:
- Crypto accounts with API keys → Binance sync
- Accounts with IBKR Flex credentials → IBKR sync
- GTJA accounts with Gmail OAuth → Gmail attachment sync

Usage:
    python scripts/sync_all.py [--dry-run] [-v]
"""

import argparse
import os
import sys
from datetime import datetime

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

from app.services.binance_sync_service import BinanceSyncService
from app.services.ibkr_flex_service import IBKRFlexService
from app.services.trade_import_service import TradeImportService
from app.services.gmail_sync_service import (
    GmailApiService,
    GmailOAuthError,
    refresh_access_token,
)
from app.services.csv_parser_service import get_parser, CSVParseError
from app.core.security import decrypt_api_key
from app.models.trade import Trade as TradeModel
from app.models.import_history import ImportHistory as ImportHistoryModel
from app.services.position_service import PositionService

import hashlib


def sync_binance_account(db, account, dry_run, log):
    """Sync a single Binance account."""
    mode = "futures" if account.is_futures_account() else "spot"
    log.info(f"  Type: Binance {mode}")

    if dry_run:
        log.info(f"  [DRY RUN] Would sync via Binance API")
        log.info(f"  Last sync: {account.last_sync_at or 'never'}")
        return 0, 0

    sync_service = BinanceSyncService(db)
    result = sync_service.sync_trades(account_id=str(account.id))

    if result["success"]:
        synced = result.get("synced_count", 0)
        errors = result.get("errors", [])
        for err in errors:
            log.warning(f"  ⚠️  {err}")
        return synced, len(errors)
    else:
        log.error(f"  ❌ {result.get('error', 'Unknown error')}")
        return 0, 1


def sync_ibkr_account(db, account, dry_run, log):
    """Sync a single IBKR account."""
    log.info(f"  Type: IBKR Flex Query (ID: {account.ibkr_flex_query_id})")

    try:
        flex_service = IBKRFlexService(
            token=account.ibkr_flex_token,
            query_id=account.ibkr_flex_query_id,
        )

        if dry_run:
            log.info(f"  [DRY RUN] Would fetch IBKR Flex statement")
            result = flex_service.fetch_trades_and_cash()
            trades = result.get("trades", [])
            log.info(f"  Found {len(trades)} trade(s)")
            return 0, 0

        log.info("  Fetching IBKR statement...")
        flex_result = flex_service.fetch_trades_and_cash()
        trades_data = flex_result.get("trades", [])
        cash_balance = flex_result.get("cash_balance")
        cash_currency = flex_result.get("cash_currency")

        if not trades_data:
            log.info("  No new trades")
            if cash_balance is not None:
                account.cash_balance = cash_balance
                account.cash_currency = cash_currency
                account.last_sync_at = datetime.utcnow()
                db.commit()
            return 0, 0

        # Normalize and import
        normalized = [{
            "symbol": t["symbol"],
            "side": t["side"],
            "quantity": t["quantity"],
            "price": t["price"],
            "trade_date": t.get("trade_date") or datetime.utcnow(),
            "external_trade_id": t.get("external_trade_id"),
            "fee": t.get("commission", 0.0),
            "fee_currency": t.get("currency", "USD"),
            "notes": f"IBKR Flex Import - {t.get('asset_class', 'Unknown')}",
        } for t in trades_data]

        import_service = TradeImportService(db)
        result = import_service.import_trades(
            account_id=account.id,
            trades_data=normalized,
            sync_source="api",
        )

        if cash_balance is not None:
            account.cash_balance = cash_balance
            account.cash_currency = cash_currency
        account.last_sync_at = datetime.utcnow()
        db.commit()

        imported = result["imported_count"]
        log.info(f"  Imported: {imported}, Skipped: {result['skipped_count']}")
        return imported, result["error_count"]

    except Exception as e:
        log.error(f"  ❌ IBKR error: {e}")
        return 0, 1


def sync_gmail_account(db, account, dry_run, log):
    """Sync a single GTJA account via Gmail."""
    log.info(f"  Type: Gmail sync ({account.gmail_address or 'unknown'})")

    gmail_client_id = os.environ.get("GOOGLE_GMAIL_CLIENT_ID") or os.environ.get("GOOGLE_CLIENT_ID")
    gmail_client_secret = os.environ.get("GOOGLE_GMAIL_CLIENT_SECRET") or os.environ.get("GOOGLE_CLIENT_SECRET")

    if not gmail_client_id or not gmail_client_secret:
        log.warning("  ⚠️  Gmail OAuth not configured, skipping")
        return 0, 0

    try:
        refresh_token = decrypt_api_key(account.gmail_refresh_token_encrypted)
        access_token = refresh_access_token(gmail_client_id, gmail_client_secret, refresh_token)
    except Exception as e:
        log.error(f"  ❌ Gmail OAuth failed: {e}")
        return 0, 1

    try:
        service = GmailApiService(access_token)
        attachments = service.fetch_attachments(
            sender="SecuritiesDepository@gtht.com",
            subject_prefix="0391510001668558",
            since_days=7,
        )
    except Exception as e:
        log.error(f"  ❌ Gmail API error: {e}")
        return 0, 1

    if not attachments:
        log.info("  No new attachments")
        return 0, 0

    # Filter trade attachments
    trade_keywords = ("交易明细", "成交明细")
    filtered = [
        att for att in attachments
        if any(kw in att.get("filename", "") for kw in trade_keywords)
    ]

    if not filtered:
        log.info("  No trade attachments found")
        return 0, 0

    total_imported = 0
    total_errors = 0
    broker_template = account.broker or "gtja"

    for attachment in filtered:
        filename = attachment.get("filename", "unknown")
        content = attachment.get("content", b"")

        raw_key = attachment.get("message_id") or filename
        message_key = hashlib.md5(str(raw_key).encode()).hexdigest()
        import_filename = f"gmail:{message_key}:{filename}"
        if len(import_filename) > 255:
            import_filename = import_filename[:255]

        existing = db.query(ImportHistoryModel).filter(
            ImportHistoryModel.account_id == account.id,
            ImportHistoryModel.filename == import_filename,
            ImportHistoryModel.import_source == "gmail_sync",
        ).first()
        if existing:
            continue

        if dry_run:
            try:
                p = get_parser(broker_template)
                trades = p.parse_file(filename, content)
                log.info(f"  [DRY RUN] {filename}: {len(trades)} trades")
            except Exception as e:
                log.warning(f"  [DRY RUN] {filename}: parse error: {e}")
            continue

        try:
            csv_parser = get_parser(broker_template)
            trades_data = csv_parser.parse_file(filename, content)
        except CSVParseError as e:
            log.error(f"  ❌ Parse error ({filename}): {e}")
            total_errors += 1
            continue

        success = 0
        dups = 0
        for td in trades_data:
            try:
                ext_id = td.get("trade_id_external")
                if ext_id:
                    ex = db.query(TradeModel).filter(
                        TradeModel.account_id == account.id,
                        TradeModel.trade_id_external == ext_id,
                    ).first()
                    if ex:
                        dups += 1
                        continue
                trade = TradeModel(
                    account_id=account.id,
                    symbol=td["symbol"],
                    side=td["side"],
                    quantity=td["quantity"],
                    price=td["price"],
                    fee=td.get("fee", 0),
                    trade_time=datetime.fromisoformat(td["trade_time"]),
                    trade_id_external=ext_id,
                    sync_source="import",
                    notes=td.get("notes", ""),
                )
                db.add(trade)
                success += 1
            except Exception as e:
                total_errors += 1

        if getattr(csv_parser, "cash_balance", None) is not None and getattr(csv_parser, "IMPORT_CASH_BALANCE", True):
            account.cash_balance = csv_parser.cash_balance
            account.cash_currency = csv_parser.cash_currency

        import_history = ImportHistoryModel(
            account_id=account.id,
            user_id=account.user_id,
            filename=import_filename,
            broker_template=broker_template,
            import_source="gmail_sync",
            total_rows=len(trades_data),
            success_count=success,
            failed_count=0,
            duplicate_count=dups,
            completed_at=datetime.utcnow(),
        )
        db.add(import_history)

        try:
            db.commit()
        except Exception as e:
            db.rollback()
            log.error(f"  ❌ Commit failed: {e}")
            total_errors += 1
            continue

        total_imported += success
        if success > 0:
            log.info(f"  {filename}: +{success} trades")

    # Recalculate positions
    if not dry_run and total_imported > 0:
        try:
            pos_service = PositionService(db)
            pos_service.calculate_positions_for_account(account.id)
        except Exception as e:
            log.warning(f"  ⚠️  Position calc failed: {e}")

    return total_imported, total_errors


def main():
    parser = argparse.ArgumentParser(description="Sync all configured trading accounts")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to DB")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    try:
        all_accounts = get_accounts(db)
        if not all_accounts:
            log.error("No active accounts found")
            sys.exit(1)

        log.info(f"Found {len(all_accounts)} active account(s)")

        grand_total_synced = 0
        grand_total_errors = 0
        synced_accounts = 0

        for account in all_accounts:
            label = f"{account.account_name} ({account.account_type})"
            log.info(f"\n━━━ {label} ━━━")

            synced = 0
            errors = 0

            # Determine sync method
            if account.account_type == "crypto" and account.api_key_encrypted and account.api_secret_encrypted:
                synced, errors = sync_binance_account(db, account, args.dry_run, log)
            elif account.ibkr_flex_token and account.ibkr_flex_query_id:
                synced, errors = sync_ibkr_account(db, account, args.dry_run, log)
            elif account.gmail_refresh_token_encrypted and account.broker == "gtja":
                synced, errors = sync_gmail_account(db, account, args.dry_run, log)
            else:
                log.info("  ⏭️  No sync method configured (no API keys / Flex / Gmail)")
                continue

            if synced > 0 or errors > 0:
                synced_accounts += 1
            grand_total_synced += synced
            grand_total_errors += errors

            if synced > 0:
                log.info(f"  ✅ +{synced} trade(s)")
            elif errors == 0:
                log.info(f"  ✅ Up to date")

        # Summary
        log.info("\n" + "━" * 40)
        if args.dry_run:
            log.info("[DRY RUN] No changes made")
        else:
            log.info(f"Accounts synced: {synced_accounts}/{len(all_accounts)}")
            log.info(f"Total new trades: {grand_total_synced}")
            if grand_total_errors:
                log.warning(f"Total errors: {grand_total_errors}")
            else:
                log.info("All clean 🎉")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
