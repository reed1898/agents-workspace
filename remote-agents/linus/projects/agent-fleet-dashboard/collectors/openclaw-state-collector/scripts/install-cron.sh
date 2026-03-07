#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
COLLECTOR_DIR="$ROOT_DIR/collectors/openclaw-state-collector"
LOG_PATH="${OPENCLAW_COLLECTOR_LOG:-$HOME/.openclaw/logs/collector.log}"
mkdir -p "$(dirname "$LOG_PATH")"

CRON_CMD="*/2 * * * * cd $ROOT_DIR && npm run -w collectors/openclaw-state-collector collect >> $LOG_PATH 2>&1"
TMP_FILE="$(mktemp)"

# Keep existing entries, replace collector line if it exists.
(crontab -l 2>/dev/null | grep -v "openclaw-state-collector collect" || true; echo "$CRON_CMD") > "$TMP_FILE"
crontab "$TMP_FILE"
rm -f "$TMP_FILE"

echo "Installed collector cron:"
echo "$CRON_CMD"
