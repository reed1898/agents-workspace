#!/usr/bin/env bash
set -euo pipefail

CFG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
SERVICE="${1:-Wi-Fi}"

if [[ ! -f "$CFG" ]]; then
  echo "config not found: $CFG" >&2
  exit 1
fi

proxy_info="$(/usr/sbin/networksetup -getwebproxy "$SERVICE" 2>/dev/null || true)"
if [[ -z "$proxy_info" ]]; then
  echo "network service not found or no proxy info: $SERVICE" >&2
  exit 1
fi

enabled="$(echo "$proxy_info" | awk -F': ' '/^Enabled:/{print $2}')"
host="$(echo "$proxy_info" | awk -F': ' '/^Server:/{print $2}')"
port="$(echo "$proxy_info" | awk -F': ' '/^Port:/{print $2}')"

if [[ "$enabled" != "Yes" || -z "$host" || -z "$port" || "$port" == "0" ]]; then
  echo "system web proxy disabled or invalid on $SERVICE; skip"
  exit 0
fi

new_proxy="http://${host}:${port}"

read -r old_tg old_dc <<<"$(python3 - <<'PY' "$CFG"
import json,sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    j=json.load(f)
print((j.get('channels',{}).get('telegram',{}).get('proxy') or ''), (j.get('channels',{}).get('discord',{}).get('proxy') or ''))
PY
)"

if [[ "$old_tg" == "$new_proxy" && "$old_dc" == "$new_proxy" ]]; then
  echo "proxy unchanged: $new_proxy"
  exit 0
fi

python3 - <<'PY' "$CFG" "$new_proxy"
import json,sys
p,proxy=sys.argv[1],sys.argv[2]
with open(p,'r',encoding='utf-8') as f:
    j=json.load(f)
channels=j.setdefault('channels',{})
channels.setdefault('telegram',{})['proxy']=proxy
channels.setdefault('discord',{})['proxy']=proxy
with open(p,'w',encoding='utf-8') as f:
    json.dump(j,f,ensure_ascii=False,indent=2)
    f.write('\n')
PY

openclaw gateway restart >/dev/null 2>&1 || true

echo "proxy updated: ${old_tg:-none}/${old_dc:-none} -> $new_proxy; gateway restarted"
