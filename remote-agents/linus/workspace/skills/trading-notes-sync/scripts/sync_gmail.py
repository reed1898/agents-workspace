#!/usr/bin/env python3
"""
Sync A-share trades from Gmail attachments (GTJA/国泰海通).

Fetches email attachments containing trade records, parses them, and imports.

Usage:
    python scripts/sync_gmail.py [--account-name NAME] [--since-days 7] [--dry-run] [-v]
"""

import argparse
import hashlib
import os
import sys
from datetime import datetime
from typing import List

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

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


def main():
    parser = argparse.ArgumentParser(description="Sync trades from Gmail (GTJA)")
    parser.add_argument("--account-name", help="Sync only this account (exact name match)")
    parser.add_argument("--since-days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Parse only, don't write to DB")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    # Gmail OAuth config
    gmail_client_id = os.environ.get("GOOGLE_GMAIL_CLIENT_ID") or os.environ.get("GOOGLE_CLIENT_ID")
    gmail_client_secret = os.environ.get("GOOGLE_GMAIL_CLIENT_SECRET") or os.environ.get("GOOGLE_CLIENT_SECRET")

    if not gmail_client_id or not gmail_client_secret:
        log.error("❌ GOOGLE_GMAIL_CLIENT_ID and GOOGLE_GMAIL_CLIENT_SECRET not set")
        log.error("   Add them to ~/.openclaw/workspace/.env")
        sys.exit(1)

    try:
        # Find GTJA accounts with Gmail configured
        all_accounts = get_accounts(db, account_name=args.account_name)
        gmail_accounts = [
            a for a in all_accounts
            if a.gmail_refresh_token_encrypted and a.broker == "gtja"
        ]

        if not gmail_accounts:
            if args.account_name:
                log.error(f"No GTJA account with Gmail sync found: '{args.account_name}'")
            else:
                log.error("No GTJA accounts with Gmail OAuth configured")
            sys.exit(1)

        log.info(f"Found {len(gmail_accounts)} GTJA account(s) with Gmail sync")

        total_imported = 0
        total_skipped = 0
        total_failed = 0

        for account in gmail_accounts:
            account_label = f"{account.account_name} ({account.gmail_address or 'unknown'})"
            log.info(f"━━━ Syncing: {account_label} ━━━")

            # Refresh OAuth token
            try:
                refresh_token = decrypt_api_key(account.gmail_refresh_token_encrypted)
                access_token = refresh_access_token(
                    gmail_client_id,
                    gmail_client_secret,
                    refresh_token,
                )
            except (GmailOAuthError, Exception) as e:
                log.error(f"❌ Gmail OAuth failed: {e}")
                log.error("   The refresh token may have expired. Re-authorize via the Web UI.")
                total_failed += 1
                continue

            # Fetch attachments
            try:
                service = GmailApiService(access_token)
                attachments = service.fetch_attachments(
                    sender="SecuritiesDepository@gtht.com",
                    subject_prefix="0391510001668558",
                    since_days=args.since_days,
                )
                log.info(f"Found {len(attachments)} attachment(s) in last {args.since_days} days")
            except Exception as e:
                log.error(f"❌ Gmail API error: {e}")
                total_failed += 1
                continue

            if not attachments:
                log.info("No new attachments found")
                continue

            # Filter to trade-related attachments
            trade_keywords = ("交易明细", "成交明细")
            filtered = [
                att for att in attachments
                if any(kw in att.get("filename", "") for kw in trade_keywords)
            ]
            log.info(f"Filtered to {len(filtered)} trade attachment(s)")

            if not filtered:
                log.info("No trade attachments found")
                continue

            # Parse and import each attachment
            broker_template = account.broker or "gtja"
            for attachment in filtered:
                filename = attachment.get("filename", "unknown")
                content = attachment.get("content", b"")

                # Dedup key
                raw_key = attachment.get("message_id") or filename
                message_key = hashlib.md5(str(raw_key).encode()).hexdigest()
                import_filename = f"gmail:{message_key}:{filename}"
                if len(import_filename) > 255:
                    import_filename = import_filename[:255]

                # Check if already imported
                existing = db.query(ImportHistoryModel).filter(
                    ImportHistoryModel.account_id == account.id,
                    ImportHistoryModel.filename == import_filename,
                    ImportHistoryModel.import_source == "gmail_sync",
                ).first()
                if existing:
                    log.info(f"  ⏭️  Already imported: {filename}")
                    total_skipped += 1
                    continue

                # Parse file
                try:
                    csv_parser = get_parser(broker_template)
                    trades_data = csv_parser.parse_file(filename, content)
                    parse_errors = csv_parser.errors
                except CSVParseError as e:
                    log.error(f"  ❌ Parse error for {filename}: {e}")
                    total_failed += 1
                    continue

                log.info(f"  📄 {filename}: {len(trades_data)} trade(s), {len(parse_errors)} error(s)")

                if args.dry_run:
                    for t in trades_data[:5]:
                        log.info(f"    {t['symbol']} {t['side']} {t['quantity']}@{t['price']} ({t.get('trade_time', '')})")
                    if len(trades_data) > 5:
                        log.info(f"    ... and {len(trades_data) - 5} more")
                    continue

                # Import trades
                success_count = 0
                dup_count = 0
                fail_count = len(parse_errors)

                for trade_data in trades_data:
                    try:
                        ext_id = trade_data.get("trade_id_external")
                        if ext_id:
                            existing_trade = db.query(TradeModel).filter(
                                TradeModel.account_id == account.id,
                                TradeModel.trade_id_external == ext_id,
                            ).first()
                            if existing_trade:
                                dup_count += 1
                                continue

                        trade = TradeModel(
                            account_id=account.id,
                            symbol=trade_data["symbol"],
                            side=trade_data["side"],
                            quantity=trade_data["quantity"],
                            price=trade_data["price"],
                            fee=trade_data.get("fee", 0),
                            trade_time=datetime.fromisoformat(trade_data["trade_time"]),
                            trade_id_external=ext_id,
                            sync_source="import",
                            notes=trade_data.get("notes", ""),
                        )
                        db.add(trade)
                        success_count += 1
                    except Exception as e:
                        fail_count += 1
                        log.warning(f"    ⚠️  Row error: {e}")

                # Update cash balance from parser if available
                if (
                    getattr(csv_parser, "cash_balance", None) is not None
                    and getattr(csv_parser, "IMPORT_CASH_BALANCE", True)
                ):
                    account.cash_balance = csv_parser.cash_balance
                    account.cash_currency = csv_parser.cash_currency

                # Record import history
                import_history = ImportHistoryModel(
                    account_id=account.id,
                    user_id=account.user_id,
                    filename=import_filename,
                    broker_template=broker_template,
                    import_source="gmail_sync",
                    total_rows=len(trades_data) + len(parse_errors),
                    success_count=success_count,
                    failed_count=fail_count,
                    duplicate_count=dup_count,
                    completed_at=datetime.utcnow(),
                )
                db.add(import_history)

                try:
                    db.commit()
                except Exception as e:
                    db.rollback()
                    log.error(f"  ❌ DB commit failed: {e}")
                    total_failed += 1
                    continue

                total_imported += success_count
                total_skipped += dup_count
                total_failed += fail_count

                log.info(f"  ✅ Imported: {success_count}, Duplicates: {dup_count}, Failed: {fail_count}")

            # Recalculate positions after all files for this account
            if not args.dry_run and total_imported > 0:
                try:
                    pos_service = PositionService(db)
                    pos_service.calculate_positions_for_account(account.id)
                    log.info(f"  📊 Positions recalculated")
                except Exception as e:
                    log.warning(f"  ⚠️  Position calculation failed: {e}")

        # Summary
        log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if args.dry_run:
            log.info("[DRY RUN] No changes made")
        else:
            log.info(f"Total imported: {total_imported}")
            log.info(f"Total skipped (duplicates/already imported): {total_skipped}")
            if total_failed:
                log.warning(f"Total failed: {total_failed}")
            else:
                log.info("No errors 🎉")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
