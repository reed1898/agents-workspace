---
name: crypto-watch
description: Assistive crypto market watch (BTC/ETH/BNB/SOL etc). Periodically checks price moves and alerts on anomalies (crash/spike/bounce) via Telegram using OpenClaw cron. Use when user asks to "辅助盯盘/盯着币价".
---

# Crypto Watch (anomaly alerts)

This is a lightweight "watch the market for me" workflow.

## Data (separated)

- Watchlist config (user data): `~/.openclaw/workspace/crypto-watch/watchlist.json`
- Template: `skills/crypto-watch/assets/watchlist.template.json`
- Runtime state (machine-local): `/tmp/openclaw/crypto-watch-state.json`

## Default behavior

- Poll every N minutes (from watchlist)
- For each symbol, fetch at least 300x 15m candles (Binance public klines API by default; OKX fallback)
- Compute 15m and 1h % move, plus basic structure context (range, simple swing structure, volume)
- Focus on price action (Dow/Wyckoff style) rather than MA-based signals
- When an alert triggers, also generate a wide 15m K-line chart image (saved under /tmp) and send it to Telegram
- Alert types:
  - Intrabar Shock (unfinished candle): catches violent 15m swings that may fade before close
  - Crash: strong negative move (pct and/or z-score)
  - Spike: strong positive move (pct and/or z-score)
  - Bounce: after crash, price rebounds from the crash low within a window
  - Breakout/Breakdown: close breaks recent range (default last 50 bars) with volume confirmation
- Cooldown: avoid spamming repeated alerts

## Operator rules

- If no alert: respond with `NO_REPLY`.
- If alert: send a concise Telegram message summarizing the trigger.

## Admin tasks

- Start/stop is done by creating/removing the cron job.
- Update symbols/thresholds by editing `crypto-watch/watchlist.json`.
