#!/usr/bin/env python3
"""
Import trades from a CSV/Excel file.

Usage:
    python scripts/import_csv.py --file PATH --account-name NAME [--broker BROKER] [--dry-run] [-v]

Supported brokers: tonghuashun, gtja, guosen, moomoo, ibkr, generic
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

from app.services.csv_parser_service import get_parser, CSVParseError, BROKER_TEMPLATES
from app.models.trade import Trade as TradeModel
from app.models.import_history import ImportHistory as ImportHistoryModel
from app.services.position_service import PositionService


def main():
    parser = argparse.ArgumentParser(description="Import trades from CSV/Excel file")
    parser.add_argument("--file", "-f", required=True, help="Path to CSV/Excel file")
    parser.add_argument("--account-name", "-a", required=True, help="Target account name")
    parser.add_argument(
        "--broker", "-b",
        help=f"Broker template (default: from account config). Options: {', '.join(BROKER_TEMPLATES.keys())}",
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse and show, don't import")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    try:
        # Validate file
        file_path = Path(args.file).expanduser().resolve()
        if not file_path.exists():
            log.error(f"❌ File not found: {file_path}")
            sys.exit(1)

        ext = file_path.suffix.lower()
        if ext not in (".csv", ".xls", ".xlsx"):
            log.error(f"❌ Unsupported file type: {ext}. Use .csv, .xls, or .xlsx")
            sys.exit(1)

        # Find account
        accounts = get_accounts(db, account_name=args.account_name)
        if not accounts:
            log.error(f"❌ No active account found with name '{args.account_name}'")
            sys.exit(1)
        account = accounts[0]

        # Determine broker template
        broker = args.broker or account.broker
        if not broker:
            log.error("❌ No broker template specified. Use --broker or set broker on the account.")
            log.error(f"   Available: {', '.join(BROKER_TEMPLATES.keys())}")
            sys.exit(1)

        if broker not in BROKER_TEMPLATES:
            log.error(f"❌ Unknown broker: {broker}")
            log.error(f"   Available: {', '.join(BROKER_TEMPLATES.keys())}")
            sys.exit(1)

        log.info(f"Account: {account.account_name} ({account.account_type})")
        log.info(f"Broker template: {broker}")
        log.info(f"File: {file_path}")

        # Read and parse file
        file_content = file_path.read_bytes()
        filename = file_path.name

        try:
            csv_parser = get_parser(broker)
            trades_data = csv_parser.parse_file(filename, file_content)
            parse_errors = csv_parser.errors
        except CSVParseError as e:
            log.error(f"❌ Parse error: {e}")
            sys.exit(1)

        log.info(f"Parsed {len(trades_data)} trade(s), {len(parse_errors)} parse error(s)")

        if parse_errors:
            for err in parse_errors[:10]:
                log.warning(f"  ⚠️  Row {err.get('row', '?')}: {err.get('error', 'unknown')}")
            if len(parse_errors) > 10:
                log.warning(f"  ... and {len(parse_errors) - 10} more errors")

        if not trades_data:
            log.warning("No trades parsed from file")
            sys.exit(0)

        # Show preview
        log.info("── Preview (first 10) ──")
        for t in trades_data[:10]:
            log.info(
                f"  {t['symbol']:>12s} {t['side']:>4s} "
                f"{t['quantity']:>10.2f} @ {t['price']:>10.4f}  "
                f"fee={t.get('fee', 0):.2f}  {t.get('trade_time', '')}"
            )
        if len(trades_data) > 10:
            log.info(f"  ... and {len(trades_data) - 10} more")

        if args.dry_run:
            log.info("\n[DRY RUN] No changes made")
            sys.exit(0)

        # Import trades
        success_count = 0
        dup_count = 0
        fail_count = len(parse_errors)

        for trade_data in trades_data:
            try:
                ext_id = trade_data.get("trade_id_external")
                if ext_id:
                    existing = db.query(TradeModel).filter(
                        TradeModel.account_id == account.id,
                        TradeModel.trade_id_external == ext_id,
                    ).first()
                    if existing:
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
                log.warning(f"  ⚠️  Import error: {e}")

        # Update cash balance if available from parser
        if (
            getattr(csv_parser, "cash_balance", None) is not None
            and getattr(csv_parser, "IMPORT_CASH_BALANCE", True)
        ):
            account.cash_balance = csv_parser.cash_balance
            account.cash_currency = csv_parser.cash_currency
            log.info(f"Updated cash balance: {csv_parser.cash_balance} {csv_parser.cash_currency or ''}")

        # Record import history
        import_history = ImportHistoryModel(
            account_id=account.id,
            user_id=account.user_id,
            filename=filename,
            broker_template=broker,
            import_source="cli_import",
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
            log.error(f"❌ DB commit failed: {e}")
            sys.exit(1)

        log.info(f"\n✅ Imported: {success_count}, Duplicates: {dup_count}, Failed: {fail_count}")

        # Recalculate positions
        if success_count > 0:
            try:
                pos_service = PositionService(db)
                pos_service.calculate_positions_for_account(account.id)
                log.info("📊 Positions recalculated")
            except Exception as e:
                log.warning(f"⚠️  Position calculation failed: {e}")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
