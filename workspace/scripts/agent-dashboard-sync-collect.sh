#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/Users/rain/.openclaw/remote-agents/linus/projects/agent-fleet-dashboard"
REPORT_ENDPOINT="https://agent-fleet-backend.reed1898.workers.dev"
REPORT_TOKEN="zKHUNXzN0s0pHxMGjLfme5CWidtM8JwlaaeTJF0KkKM"
AGENT_ID="xiaohong"

PORTS_RAW=$(/usr/sbin/lsof -nP -a -c QuickQ -iTCP -sTCP:LISTEN 2>/dev/null \
  | awk '/127\.0\.0\.1:[0-9]+/ {split($9,a,":"); print a[2]}' \
  | sort -n | uniq)

if [ -z "$PORTS_RAW" ]; then
  echo "[agent-dashboard-sync] QuickQ proxy not detected" >&2
  exit 1
fi

HTTP_PORT=$(printf "%s\n" "$PORTS_RAW" | head -n1)

cd "$PROJECT_ROOT"
NODE_USE_ENV_PROXY=1 \
HTTP_PROXY="http://127.0.0.1:${HTTP_PORT}" \
HTTPS_PROXY="http://127.0.0.1:${HTTP_PORT}" \
REPORT_MODE=cloudflare \
REPORT_ENDPOINT="$REPORT_ENDPOINT" \
REPORT_TOKEN="$REPORT_TOKEN" \
AGENT_ID="$AGENT_ID" \
npm run -w collectors/openclaw-state-collector collect
