#!/usr/bin/env python3
"""
Sync Binance spot & futures trades via API.

Usage:
    python scripts/sync_binance.py [--account-name NAME] [--symbol SYM] [--dry-run] [-v]
"""

import argparse
import sys
from datetime import datetime

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

from app.services.binance_sync_service import BinanceSyncService


def main():
    parser = argparse.ArgumentParser(description="Sync Binance trades")
    parser.add_argument("--account-name", help="Sync only this account (exact name match)")
    parser.add_argument("--symbol", help="Sync only this trading pair, e.g. BTC/USDT")
    parser.add_argument("--dry-run", action="store_true", help="Query only, don't write to DB")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    try:
        # Find Binance accounts (crypto type with binance broker)
        accounts = get_accounts(db, account_name=args.account_name, account_type="crypto")

        # Filter to only accounts that have Binance API keys
        binance_accounts = [
            a for a in accounts
            if a.api_key_encrypted and a.api_secret_encrypted
        ]

        if not binance_accounts:
            if args.account_name:
                log.error(f"No active Binance account found with name '{args.account_name}'")
            else:
                log.error("No active Binance accounts with API credentials found")
            sys.exit(1)

        log.info(f"Found {len(binance_accounts)} Binance account(s) to sync")

        total_synced = 0
        total_errors = []

        for account in binance_accounts:
            account_label = f"{account.account_name} ({account.account_type})"
            is_futures = account.is_futures_account()
            mode = "futures" if is_futures else "spot"
            log.info(f"━━━ Syncing: {account_label} [{mode}] ━━━")

            if args.dry_run:
                log.info("[DRY RUN] Would sync trades from Binance API")
                log.info(f"  Account ID: {account.id}")
                log.info(f"  Last sync: {account.last_sync_at or 'never'}")
                log.info(f"  Sync start date: {account.sync_start_date or 'not set'}")
                if args.symbol:
                    log.info(f"  Symbol filter: {args.symbol}")
                continue

            sync_service = BinanceSyncService(db)
            result = sync_service.sync_trades(
                account_id=str(account.id),
                symbol=args.symbol,
            )

            if result["success"]:
                synced = result.get("synced_count", 0)
                total_synced += synced
                errors = result.get("errors", [])
                total_errors.extend(errors)

                log.info(f"✅ Synced {synced} new trade(s)")
                log.info(f"   Last sync: {result.get('last_sync_at')}")
                if errors:
                    for err in errors:
                        log.warning(f"   ⚠️  {err}")
            else:
                error_msg = result.get("error", "Unknown error")
                total_errors.append(f"{account_label}: {error_msg}")
                log.error(f"❌ Sync failed: {error_msg}")

        # Summary
        log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if args.dry_run:
            log.info("[DRY RUN] No changes made")
        else:
            log.info(f"Total synced: {total_synced} trade(s)")
            if total_errors:
                log.warning(f"Errors: {len(total_errors)}")
                for err in total_errors:
                    log.warning(f"  - {err}")
            else:
                log.info("No errors 🎉")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
