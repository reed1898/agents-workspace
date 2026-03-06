---
name: trading-notes-sync
description: Sync trading positions across multiple markets (Binance, IBKR, A-shares, HK stocks) for the trading-notes project. Use when Reed asks to sync trades, update positions, import trading records, or check portfolio status. Supports automatic API sync (Binance, IBKR Flex), Gmail attachment import (GTJA), and manual CSV/Excel import (Moomoo, Guosen).
---

# trading-notes-sync

CLI scripts to sync trading data across multiple exchanges/brokers, bypassing the Web UI.

## First-Time Setup

The scripts reuse the trading-notes backend code and need its Python dependencies. Run once:

```bash
cd ~/.openclaw/workspace/skills/trading-notes-sync
bash scripts/setup.sh
```

This creates a `.venv` and installs dependencies from the project's `requirements.txt`.

## Prerequisites

Environment variables (read from `~/.openclaw/workspace/.env`):

| Variable | Description |
|---|---|
| `TRADING_NOTES_DATABASE_URL` | PostgreSQL connection string for trading-notes DB |
| `TRADING_NOTES_ENCRYPTION_KEY` | Fernet key for decrypting stored API credentials |
| `GOOGLE_GMAIL_CLIENT_ID` | Google OAuth client ID (Gmail sync only) |
| `GOOGLE_GMAIL_CLIENT_SECRET` | Google OAuth client secret (Gmail sync only) |

All API keys/tokens are stored **encrypted in the database** (`trade_accounts` table) — no secrets in this skill.

## Scripts

All scripts are in `scripts/` relative to this SKILL.md. Run them with:

```bash
cd ~/.openclaw/workspace/skills/trading-notes-sync
.venv/bin/python scripts/<script>.py [options]
# Or: source .venv/bin/activate && python scripts/<script>.py [options]
```

### sync_binance.py — Binance Spot & Futures

```bash
# Sync all Binance accounts
python scripts/sync_binance.py

# Sync a specific account
python scripts/sync_binance.py --account-name "币安合约"

# Sync a specific symbol
python scripts/sync_binance.py --account-name "币安现货" --symbol BTC/USDT

# Dry run (query only, no DB writes)
python scripts/sync_binance.py --dry-run
```

### sync_ibkr.py — IBKR Flex Query (US Stocks)

```bash
# Sync all IBKR accounts
python scripts/sync_ibkr.py

# Sync specific account
python scripts/sync_ibkr.py --account-name "IBKR"

# Dry run
python scripts/sync_ibkr.py --dry-run
```

### sync_gmail.py — Gmail Attachment Import (A-shares, GTJA/国泰海通)

```bash
# Sync from Gmail (last 7 days)
python scripts/sync_gmail.py

# Specify days to look back
python scripts/sync_gmail.py --since-days 30

# Sync specific account
python scripts/sync_gmail.py --account-name "国泰海通"

# Dry run
python scripts/sync_gmail.py --dry-run
```

### import_csv.py — Manual CSV/Excel Import

```bash
# Import CSV with auto-detected broker template
python scripts/import_csv.py --file ~/Downloads/trades.csv --account-name "国信"

# Specify broker explicitly
python scripts/import_csv.py --file ~/Downloads/trades.xlsx --account-name "国信" --broker guosen

# Import moomoo trades
python scripts/import_csv.py --file ~/Downloads/moomoo.csv --account-name "Moomoo" --broker moomoo

# Dry run (parse only, show what would be imported)
python scripts/import_csv.py --file ~/Downloads/trades.csv --account-name "国信" --broker guosen --dry-run
```

Supported brokers: `tonghuashun`, `gtja`, `guosen`, `moomoo`, `ibkr`, `generic`

### sync_all.py — Sync All Configured Accounts

```bash
# Sync everything that has credentials
python scripts/sync_all.py

# Dry run
python scripts/sync_all.py --dry-run
```

Automatically detects account types and runs the appropriate sync:
- Binance accounts → API sync
- IBKR accounts → Flex Query sync
- GTJA accounts with Gmail → Gmail attachment sync

### show_positions.py — View Current Positions

```bash
# Show all open positions
python scripts/show_positions.py

# Show positions for specific account
python scripts/show_positions.py --account-name "币安现货"

# Include closed positions
python scripts/show_positions.py --include-closed

# Show summary only
python scripts/show_positions.py --summary
```

## How It Works

These scripts **reuse the existing trading-notes service layer** (`~/.openclaw/projects/trading-notes/backend/app/services/`). They add the project backend to `sys.path` and directly import:

- `BinanceSyncService` — Binance REST API sync
- `IBKRFlexService` — IBKR Flex Web Service
- `GmailApiService` — Gmail OAuth + attachment fetch
- `CSVParserService` — Multi-broker CSV/Excel parsing
- `TradeImportService` — Unified trade import with dedup
- `PositionService` — Position calculation from trades

No sync logic is duplicated — all business logic comes from the project.
