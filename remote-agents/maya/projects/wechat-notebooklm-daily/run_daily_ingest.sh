#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/rain/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/noding_bb7b/msg/file"
OUTDIR="$HOME/.openclaw/projects/wechat-notebooklm-daily/output"
mkdir -p "$OUTDIR"
DATE_TAG=$(date +%Y-%m-%d)
RUN_LOG="$OUTDIR/run-${DATE_TAG}.log"
exec > >(tee -a "$RUN_LOG") 2>&1

if [[ ! -d "$ROOT" ]]; then echo "[ERROR] ROOT not found: $ROOT"; exit 1; fi

TMP_LIST=$(mktemp)
# Primary: natural day
find "$ROOT" -type f \( -iname '*.pdf' -o -iname '*.PDF' \) -newermt "$DATE_TAG 00:00:00" ! -newermt "$DATE_TAG 23:59:59" | sort > "$TMP_LIST"
CNT=$(wc -l < "$TMP_LIST" | tr -d ' ')
WINDOW="today"
# Fallback for early midnight runs: use last 24h
if [[ "$CNT" -eq 0 ]]; then
  find "$ROOT" -type f \( -iname '*.pdf' -o -iname '*.PDF' \) -mtime -1 | sort > "$TMP_LIST"
  CNT=$(wc -l < "$TMP_LIST" | tr -d ' ')
  WINDOW="last24h"
fi

echo "[INFO] date=$DATE_TAG window=$WINDOW pdf_count=$CNT"
if [[ "$CNT" -eq 0 ]]; then echo "[WARN] no pdf found"; rm -f "$TMP_LIST"; exit 0; fi

TITLE="财联社日报-${DATE_TAG}-${WINDOW}"
SUMMARY_MD="$OUTDIR/summary-${DATE_TAG}-${WINDOW}.md"
CREATE_JSON=$(~/.local/bin/notebooklm create "$TITLE" --json)
NB_ID=$(python3 - <<'PY' "$CREATE_JSON"
import json,sys
j=json.loads(sys.argv[1]); print(j['notebook']['id'])
PY
)
echo "[INFO] notebook=$NB_ID title=$TITLE"

a=0; f=0
while IFS= read -r fp; do
  [ -z "$fp" ] && continue
  name=$(basename "$fp")
  echo "[ADD] $name"
  if ~/.local/bin/notebooklm source add --notebook "$NB_ID" --type file "$fp" >/dev/null 2>&1; then a=$((a+1)); else f=$((f+1)); echo "[FAIL] $name"; fi
done < "$TMP_LIST"
rm -f "$TMP_LIST"

echo "[INFO] added=$a failed=$f"
PROMPT='你是一名买方研究员。请基于今天导入的全部PDF，输出一份结构化A股投资日报：\n1) 今日核心主线（3-6条）\n2) 每条主线的催化剂、受益环节、风险点\n3) 重点公司线索（仅列文档中出现频次高且逻辑清晰的）\n4) 明日观察清单（事件/数据/价格信号）\n5) 明确区分“事实”与“推断”，不要编造未出现的信息。输出中文。'
~/.local/bin/notebooklm ask --notebook "$NB_ID" --new "$PROMPT" > "$SUMMARY_MD" || true

echo "[DONE] notebook_id=$NB_ID"
echo "[DONE] summary=$SUMMARY_MD"
