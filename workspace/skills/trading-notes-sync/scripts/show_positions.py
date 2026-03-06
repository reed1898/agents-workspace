#!/usr/bin/env python3
"""
Show current portfolio positions across all accounts.

Usage:
    python scripts/show_positions.py [--account-name NAME] [--include-closed] [--summary] [-v]
"""

import argparse
import sys
from decimal import Decimal

# ── Setup ────────────────────────────────────────────────────────────────────
from _common import get_db, get_accounts, setup_logging

from app.models.position import Position
from app.models.trade_account import TradeAccount
from app.models.trade import Trade


def format_pnl(value, percent=None):
    """Format PnL with color indicator."""
    if value is None:
        return "—"
    val = float(value)
    sign = "+" if val >= 0 else ""
    pct_str = ""
    if percent is not None:
        pct_val = float(percent)
        pct_str = f" ({sign}{pct_val:.2f}%)"
    emoji = "🟢" if val >= 0 else "🔴"
    return f"{emoji} {sign}{val:,.2f}{pct_str}"


def format_quantity(qty, position_type="spot"):
    """Format quantity with direction for futures."""
    val = float(qty)
    if position_type == "futures":
        if val > 0:
            return f"{val:,.4f} LONG"
        elif val < 0:
            return f"{abs(val):,.4f} SHORT"
    return f"{val:,.4f}"


def main():
    parser = argparse.ArgumentParser(description="Show portfolio positions")
    parser.add_argument("--account-name", help="Filter by account name")
    parser.add_argument("--include-closed", action="store_true", help="Include closed positions")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    log = setup_logging(args.verbose)
    db = get_db()

    try:
        # Build query
        query = db.query(Position, TradeAccount).join(
            TradeAccount, Position.account_id == TradeAccount.id
        ).filter(TradeAccount.is_active == True)

        if args.account_name:
            query = query.filter(TradeAccount.account_name == args.account_name)

        if not args.include_closed:
            query = query.filter(Position.is_closed == False)

        results = query.order_by(TradeAccount.account_name, Position.symbol).all()

        if not results:
            log.info("No positions found")
            if not args.include_closed:
                log.info("(Use --include-closed to see closed positions)")
            sys.exit(0)

        # Group by account
        accounts_positions = {}
        for position, account in results:
            key = (str(account.id), account.account_name, account.account_type)
            if key not in accounts_positions:
                accounts_positions[key] = {
                    "account": account,
                    "positions": [],
                }
            accounts_positions[key]["positions"].append(position)

        # Summary stats
        total_open = 0
        total_closed = 0
        total_cost = Decimal("0")
        total_unrealized = Decimal("0")
        total_realized = Decimal("0")

        for key, data in accounts_positions.items():
            account = data["account"]
            positions = data["positions"]
            account_label = f"{account.account_name} ({account.account_type})"

            open_positions = [p for p in positions if not p.is_closed]
            closed_positions = [p for p in positions if p.is_closed]
            total_open += len(open_positions)
            total_closed += len(closed_positions)

            if not args.summary:
                print(f"\n{'━' * 60}")
                print(f"📁 {account_label}")
                if account.cash_balance:
                    print(f"   💰 Cash: {float(account.cash_balance):,.2f} {account.cash_currency or ''}")
                if account.last_sync_at:
                    print(f"   🔄 Last sync: {account.last_sync_at.strftime('%Y-%m-%d %H:%M')}")
                print(f"{'─' * 60}")

            # Open positions
            if open_positions and not args.summary:
                print(f"\n  📈 Open Positions ({len(open_positions)})")
                print(f"  {'Symbol':<16s} {'Qty':>12s} {'Cost':>10s} {'Current':>10s} {'PnL':>20s} {'Days':>5s}")
                print(f"  {'─' * 75}")

            for p in open_positions:
                cost_price = p.average_cost if p.position_type == "spot" else p.entry_price
                cost_val = float(abs(p.quantity) * (cost_price or 0))
                total_cost += Decimal(str(cost_val))

                if p.unrealized_pnl is not None:
                    total_unrealized += Decimal(str(p.unrealized_pnl))

                if not args.summary:
                    current_str = f"{float(p.current_price):,.4f}" if p.current_price else "—"
                    cost_str = f"{float(cost_price):,.4f}" if cost_price else "—"
                    pnl_str = format_pnl(p.unrealized_pnl, p.unrealized_pnl_percent)
                    qty_str = format_quantity(p.quantity, p.position_type)
                    days_str = str(p.holding_days) if p.holding_days is not None else "—"

                    print(f"  {p.symbol:<16s} {qty_str:>12s} {cost_str:>10s} {current_str:>10s} {pnl_str:>20s} {days_str:>5s}")

                    if args.verbose and p.position_type == "futures":
                        leverage_str = f"{float(p.leverage)}x" if p.leverage else "—"
                        margin_str = f"{float(p.margin_used):,.2f}" if p.margin_used else "—"
                        roe_str = f"{float(p.roe_percent):.2f}%" if p.roe_percent else "—"
                        print(f"  {'':16s} Leverage: {leverage_str}  Margin: {margin_str}  ROE: {roe_str}")

            # Closed positions
            if closed_positions and args.include_closed and not args.summary:
                print(f"\n  📉 Closed Positions ({len(closed_positions)})")
                print(f"  {'Symbol':<16s} {'Qty':>12s} {'Realized PnL':>20s} {'Closed':>12s}")
                print(f"  {'─' * 62}")

            for p in closed_positions:
                if p.realized_pnl is not None:
                    total_realized += Decimal(str(p.realized_pnl))

                if args.include_closed and not args.summary:
                    pnl_str = format_pnl(p.realized_pnl, p.realized_pnl_percent)
                    closed_str = p.closed_at.strftime("%Y-%m-%d") if p.closed_at else "—"
                    qty_str = f"{float(p.quantity):,.4f}" if p.quantity else "—"
                    print(f"  {p.symbol:<16s} {qty_str:>12s} {pnl_str:>20s} {closed_str:>12s}")

        # Summary
        print(f"\n{'━' * 60}")
        print(f"📊 Portfolio Summary")
        print(f"{'─' * 60}")
        print(f"  Open positions:   {total_open}")
        if args.include_closed:
            print(f"  Closed positions: {total_closed}")
        print(f"  Total cost:       {float(total_cost):>14,.2f}")
        if total_unrealized != 0:
            pct = (total_unrealized / total_cost * 100) if total_cost > 0 else 0
            print(f"  Unrealized PnL:   {format_pnl(total_unrealized, pct)}")
        if total_realized != 0 and args.include_closed:
            print(f"  Realized PnL:     {format_pnl(total_realized)}")
        print(f"{'━' * 60}")

    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=args.verbose)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
