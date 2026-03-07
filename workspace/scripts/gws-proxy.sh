#!/bin/bash
# gws wrapper: auto-detect QuickQ proxy + token refresh
# QuickQ 端口可能变化，每次自动检测

# 自动检测 QuickQ HTTP 代理端口
QUICKQ_PORT=$(/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | grep -Ei 'quickqser|quickq' | grep -E '127.0.0.1|localhost' | head -1 | sed -E 's/.*(127.0.0.1|localhost):([0-9]+).*/\2/')

if [ -z "$QUICKQ_PORT" ]; then
  echo "⚠️  QuickQ not running, trying without proxy..." >&2
else
  export https_proxy="http://127.0.0.1:$QUICKQ_PORT"
  export http_proxy="http://127.0.0.1:$QUICKQ_PORT"
fi

CREDS_FILE="$HOME/Library/Application Support/gws/credentials.json"
CLIENT_FILE="$HOME/Library/Application Support/gws/client_secret.json"

# Auto refresh token
if [ -f "$CREDS_FILE" ] && [ -f "$CLIENT_FILE" ]; then
  REFRESH_TOKEN=$(python3 -c "import json; print(json.load(open('$CREDS_FILE'))['refresh_token'])" 2>/dev/null)
  CLIENT_ID=$(python3 -c "import json; print(json.load(open('$CLIENT_FILE'))['installed']['client_id'])" 2>/dev/null)
  CLIENT_SECRET=$(python3 -c "import json; print(json.load(open('$CLIENT_FILE'))['installed']['client_secret'])" 2>/dev/null)
  
  if [ -n "$REFRESH_TOKEN" ] && [ -n "$CLIENT_ID" ]; then
    PROXY_FLAG=""
    [ -n "$QUICKQ_PORT" ] && PROXY_FLAG="-x http://127.0.0.1:$QUICKQ_PORT"
    
    NEW_TOKEN=$(curl -s $PROXY_FLAG --connect-timeout 10 -X POST https://oauth2.googleapis.com/token \
      -d "refresh_token=$REFRESH_TOKEN" \
      -d "client_id=$CLIENT_ID" \
      -d "client_secret=$CLIENT_SECRET" \
      -d "grant_type=refresh_token" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
    
    if [ -n "$NEW_TOKEN" ]; then
      export GOOGLE_WORKSPACE_CLI_TOKEN="$NEW_TOKEN"
    fi
  fi
fi

exec gws "$@"
