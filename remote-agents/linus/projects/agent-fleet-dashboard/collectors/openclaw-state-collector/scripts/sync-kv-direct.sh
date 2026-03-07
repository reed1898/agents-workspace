#!/usr/bin/env bash
set -euo pipefail

# Cron may have a minimal PATH; pin common bin paths.
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
WRANGLER_BIN="${WRANGLER_BIN:-/usr/local/bin/wrangler}"

# Direct KV sync fallback when /ingest endpoint is unreachable from local shell.
NAMESPACE_ID="${FLEET_KV_NAMESPACE_ID:-f78f3c3252f249a8b95b9d2271990849}"
AGENT_ID="${AGENT_ID:-linus}"
AGENT_NAME="${AGENT_NAME:-Linus}"
AGENT_ROLE="${AGENT_ROLE:-Builder}"
AGENT_DESC="${AGENT_DESC:-Main build copilot}"
INTERVAL_SEC="${INTERVAL_SEC:-60}"
HOST_NAME="${HOST_NAME:-$(hostname)}"
MODEL_NAME="${MODEL_NAME:-gpt-5.3-codex}"
CHANNEL_NAME="${CHANNEL_NAME:-telegram}"

NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

STATUS_RAW="ok"
if command -v openclaw >/dev/null 2>&1; then
  STATUS_RAW="$(openclaw status 2>/dev/null | head -n 1 | tr -d '\n' || true)"
  STATUS_RAW="${STATUS_RAW:-ok}"
fi

HEARTBEAT_JSON=$(cat <<JSON
{"agent_id":"${AGENT_ID}","last_seen":"${NOW}","interval_sec":${INTERVAL_SEC},"status":"ok"}
JSON
)

CRON_JSON=$(cat <<JSON
{"agent_id":"${AGENT_ID}","jobs":[{"name":"collector","schedule":"* * * * *","consecutive_failures":0,"last_run_at":"${NOW}","last_status":"ok"}]}
JSON
)

RUNTIME_JSON=$(cat <<JSON
{"agent_id":"${AGENT_ID}","runtime":{"host":"${HOST_NAME}","model":"${MODEL_NAME}","channel":"${CHANNEL_NAME}","last_openclaw_status_raw":"${STATUS_RAW}"}}
JSON
)

"${WRANGLER_BIN}" kv key put --namespace-id="${NAMESPACE_ID}" --remote "fleet:heartbeat:${AGENT_ID}" "${HEARTBEAT_JSON}" >/dev/null
"${WRANGLER_BIN}" kv key put --namespace-id="${NAMESPACE_ID}" --remote "fleet:cron:${AGENT_ID}" "${CRON_JSON}" >/dev/null
"${WRANGLER_BIN}" kv key put --namespace-id="${NAMESPACE_ID}" --remote "fleet:runtime:${AGENT_ID}" "${RUNTIME_JSON}" >/dev/null
"${WRANGLER_BIN}" kv key put --namespace-id="${NAMESPACE_ID}" --remote "fleet:updated_at" "${NOW}" >/dev/null

echo "${NOW} synced ${AGENT_ID} to KV ${NAMESPACE_ID}"
