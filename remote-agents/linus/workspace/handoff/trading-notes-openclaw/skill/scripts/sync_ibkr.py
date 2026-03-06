#!/usr/bin/env python3
"""
Sync IBKR trades via Flex Query API.

Usage:
    python scripts/sync_ibkr.py [--account-name NAME] [--dry-run] [-v]
"""

import argparse
import sys
from datetime import datetime
from uuid import UUID

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

from app.services.ibkr_flex_service import IBKRFlexService
from app.services.trade_import_service import TradeImportService
from app.models.trade_account import TradeAccount


def main():
    parser = argparse.ArgumentParser(description="Sync IBKR trades via Flex Query")
    parser.add_argument("--account-name", help="Sync only this account (exact name match)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch & parse only, don't write to DB")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    try:
        # Find IBKR accounts (us_stock type with ibkr_flex credentials)
        all_accounts = get_accounts(db, account_name=args.account_name)
        ibkr_accounts = [
            a for a in all_accounts
            if a.ibkr_flex_token and a.ibkr_flex_query_id
        ]

        if not ibkr_accounts:
            if args.account_name:
                log.error(f"No active IBKR account found with name '{args.account_name}' and Flex credentials")
            else:
                log.error("No active IBKR accounts with Flex Query credentials found")
            sys.exit(1)

        log.info(f"Found {len(ibkr_accounts)} IBKR account(s) to sync")

        total_imported = 0
        total_skipped = 0
        total_errors_count = 0

        for account in ibkr_accounts:
            account_label = f"{account.account_name} ({account.account_type})"
            log.info(f"━━━ Syncing: {account_label} ━━━")

            if args.dry_run:
                log.info("[DRY RUN] Would fetch IBKR Flex Query statement")
                log.info(f"  Account ID: {account.id}")
                log.info(f"  Query ID: {account.ibkr_flex_query_id}")
                log.info(f"  Last sync: {account.last_sync_at or 'never'}")

                # Still fetch and parse to show what would be imported
                try:
                    flex_service = IBKRFlexService(
                        token=account.ibkr_flex_token,
                        query_id=account.ibkr_flex_query_id
                    )
                    result = flex_service.fetch_trades_and_cash()
                    trades = result.get("trades", [])
                    cash = result.get("cash_balance")
                    log.info(f"  Would import: {len(trades)} trade(s)")
                    if cash is not None:
                        log.info(f"  Cash balance: {cash} {result.get('cash_currency', '')}")
                    for t in trades[:5]:
                        log.info(f"    {t['symbol']} {t['side']} {t['quantity']}@{t['price']} ({t.get('trade_date', 'unknown')})")
                    if len(trades) > 5:
                        log.info(f"    ... and {len(trades) - 5} more")
                except Exception as e:
                    log.error(f"  Fetch failed: {e}")
                continue

            # Step 1: Fetch from IBKR
            try:
                flex_service = IBKRFlexService(
                    token=account.ibkr_flex_token,
                    query_id=account.ibkr_flex_query_id
                )
                log.info("Requesting IBKR Flex statement...")
                flex_result = flex_service.fetch_trades_and_cash()
                trades_data = flex_result.get("trades", [])
                cash_balance = flex_result.get("cash_balance")
                cash_currency = flex_result.get("cash_currency")
                log.info(f"Fetched {len(trades_data)} trade(s) from IBKR")
            except Exception as e:
                log.error(f"❌ IBKR API error: {e}")
                total_errors_count += 1
                continue

            if not trades_data:
                log.info("No new trades found")
                # Still update cash balance if available
                if cash_balance is not None:
                    account.cash_balance = cash_balance
                    account.cash_currency = cash_currency
                    account.last_sync_at = datetime.utcnow()
                    db.commit()
                    log.info(f"Updated cash balance: {cash_balance} {cash_currency or ''}")
                continue

            # Step 2: Normalize and import
            normalized_trades = []
            for t in trades_data:
                normalized_trades.append({
                    "symbol": t["symbol"],
                    "side": t["side"],
                    "quantity": t["quantity"],
                    "price": t["price"],
                    "trade_date": t.get("trade_date") or datetime.utcnow(),
                    "external_trade_id": t.get("external_trade_id"),
                    "fee": t.get("commission", 0.0),
                    "fee_currency": t.get("currency", "USD"),
                    "notes": f"IBKR Flex Import - {t.get('asset_class', 'Unknown')}",
                })

            try:
                import_service = TradeImportService(db)
                import_result = import_service.import_trades(
                    account_id=account.id,
                    trades_data=normalized_trades,
                    sync_source="api",
                )
                imported = import_result["imported_count"]
                skipped = import_result["skipped_count"]
                errors = import_result["error_count"]

                total_imported += imported
                total_skipped += skipped
                total_errors_count += errors

                log.info(f"✅ Imported: {imported}, Skipped (dup): {skipped}, Errors: {errors}")
                if import_result.get("affected_symbols"):
                    log.info(f"   Affected symbols: {', '.join(import_result['affected_symbols'])}")
            except Exception as e:
                log.error(f"❌ Import failed: {e}")
                total_errors_count += 1
                continue

            # Step 3: Update account metadata
            if cash_balance is not None:
                account.cash_balance = cash_balance
                account.cash_currency = cash_currency
            account.last_sync_at = datetime.utcnow()
            db.commit()

        # Summary
        log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if args.dry_run:
            log.info("[DRY RUN] No changes made")
        else:
            log.info(f"Total imported: {total_imported}")
            log.info(f"Total skipped (duplicates): {total_skipped}")
            if total_errors_count:
                log.warning(f"Total errors: {total_errors_count}")
            else:
                log.info("No errors 🎉")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
