#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="${HOME}/.openclaw/workspace"
INSIGHTS_FILE="${WORKSPACE_DIR}/trading/insights.md"
RULES_FILE="${WORKSPACE_DIR}/trading/rules.md"

mkdir -p "${WORKSPACE_DIR}/trading"

now_utc() { date -u "+%Y-%m-%d %H:%M:%S UTC"; }
iso_utc() { date -u "+%Y-%m-%dT%H:%M:%SZ"; }

die() { echo "Error: $*" >&2; exit 1; }

usage() {
  cat <<'EOF'
trade-log - store trading insights to git-synced workspace

Usage:
  trade-log add "text" [--tags "t1,t2"] [--style "A,B"] [--type insight|summary|rule|mistake|review] [--one "一句话"] [--symbol "BTC"] [--tf "15m"]
  trade-log recent [n]
  trade-log search "query" [--limit n]
  trade-log since "<ISO-UTC>"          # e.g. 2026-02-01T00:00:00Z
  trade-log week                       # last 7 days (UTC)
  trade-log digest-week [--out path]   # write weekly digest markdown
  trade-log stats

Notes:
  - Writes to ~/.openclaw/workspace/trading/insights.md
EOF
}

cmd_add() {
  local text="${1:-}"; shift || true
  [ -n "${text}" ] || die "missing text"

  local tags=""
  local style=""
  local type="insight"
  local symbol=""
  local tf=""
  local one=""

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --tags) tags="$2"; shift 2;;
      --style) style="$2"; shift 2;;
      --type) type="$2"; shift 2;;
      --symbol) symbol="$2"; shift 2;;
      --tf) tf="$2"; shift 2;;
      --one) one="$2"; shift 2;;
      -h|--help) usage; exit 0;;
      *) die "unknown arg: $1";;
    esac
  done

  local ts_human; ts_human=$(now_utc)
  local ts_iso; ts_iso=$(iso_utc)

  {
    echo "## ${type} — ${ts_human}"
    echo
    echo "- ts: ${ts_iso}"
    [ -n "${type}" ] && echo "- type: ${type}"
    [ -n "${style}" ] && echo "- style: ${style}"
    [ -n "${tags}" ] && echo "- tags: ${tags}"
    [ -n "${symbol}" ] && echo "- symbol: ${symbol}"
    [ -n "${tf}" ] && echo "- tf: ${tf}"
    [ -n "${one}" ] && echo "- one: ${one}"
    echo
    echo "### raw"
    echo
    echo "${text}"
    echo
    echo "---"
    echo
  } >> "${INSIGHTS_FILE}"

  echo "OK: appended to ${INSIGHTS_FILE}"
}

cmd_recent() {
  local n="${1:-20}"
  # Print last N entries (each entry is separated by '---')
  awk -v n="$n" '
    BEGIN{RS="---"; ORS="---\n"}
    {buf[NR]=$0}
    END{
      start=NR-n+1; if(start<1) start=1;
      for(i=start;i<=NR;i++) print buf[i];
    }
  ' "${INSIGHTS_FILE}" | sed '/^$/N;/^\n$/D'
}

cmd_search() {
  local q="${1:-}"; shift || true
  [ -n "$q" ] || die "missing query"
  local limit=20
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --limit) limit="$2"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done
  # crude: show matching lines + some context
  if command -v rg >/dev/null 2>&1; then
    rg -n --context 3 "$q" "${INSIGHTS_FILE}" | head -n "$((limit*15))"
  else
    grep -n -C 3 -- "$q" "${INSIGHTS_FILE}" | head -n "$((limit*15))" || true
  fi
}

cmd_since() {
  local since_iso="${1:-}"
  [ -n "$since_iso" ] || die "missing since ISO timestamp, e.g. 2026-02-01T00:00:00Z"
  python3 - <<PY
import re,sys,datetime
from pathlib import Path

p=Path(r"${INSIGHTS_FILE}")
text=p.read_text(encoding='utf-8') if p.exists() else ''

since_str=r"${since_iso}"
try:
  since=datetime.datetime.fromisoformat(since_str.replace('Z','+00:00'))
except Exception as e:
  print(f"Error: invalid ISO time: {since_str}", file=sys.stderr)
  sys.exit(2)

# split by entry header lines
lines=text.splitlines()
entries=[]
cur=[]
for line in lines:
  if line.startswith('## ') and cur:
    entries.append(cur); cur=[line]
  else:
    cur.append(line)
if cur:
  entries.append(cur)

out=[]
for ent in entries:
  block='\n'.join(ent).strip('\n')
  m=re.search(r"^\- ts: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$", block, re.M)
  if not m:
    continue
  ts=datetime.datetime.fromisoformat(m.group(1).replace('Z','+00:00'))
  if ts>=since:
    out.append(block+'\n\n---\n')

print('\n'.join(out).strip())
PY
}

cmd_week() {
  # last 7 days from now (UTC)
  local since
  since=$(python3 - <<'PY'
import datetime
now=datetime.datetime.now(datetime.timezone.utc)
since=now-datetime.timedelta(days=7)
print(since.isoformat().replace('+00:00','Z'))
PY
)
  cmd_since "$since"
}

cmd_digest_week() {
  local out_path="${WORKSPACE_DIR}/trading/weekly-digest.md"
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --out) out_path="$2"; shift 2;;
      *) die "unknown arg: $1";;
    esac
  done

  local week_text
  week_text=$(cmd_week || true)

  {
    echo "# Weekly Trading Digest (raw extract)"
    echo
    echo "- generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "- range: last 7 days (UTC)"
    echo
    echo "## Entries"
    echo
    if [ -n "${week_text}" ]; then
      echo "${week_text}"
    else
      echo "(no entries in last 7 days)"
    fi
  } > "$out_path"

  echo "OK: wrote ${out_path}"
}

cmd_stats() {
  echo "Insights file: ${INSIGHTS_FILE}"
  [ -f "${INSIGHTS_FILE}" ] || die "insights file missing"
  local count
  count=$(grep -c '^## ' "${INSIGHTS_FILE}" || true)
  echo "Entries: ${count}"
  echo "Top tags (rough):"
  if command -v rg >/dev/null 2>&1; then
    rg -n '^\- tags: ' "${INSIGHTS_FILE}" \
      | sed 's/.*- tags: //' \
      | tr ',' '\n' \
      | sed 's/^ *//;s/ *$//' \
      | grep -v '^$' \
      | sort | uniq -c | sort -nr | head -n 15
  else
    grep -n '^\- tags: ' "${INSIGHTS_FILE}" \
      | sed 's/.*- tags: //' \
      | tr ',' '\n' \
      | sed 's/^ *//;s/ *$//' \
      | grep -v '^$' \
      | sort | uniq -c | sort -nr | head -n 15
  fi
}

case "${1:-}" in
  add) shift; cmd_add "$@";;
  recent) shift; cmd_recent "$@";;
  search) shift; cmd_search "$@";;
  since) shift; cmd_since "$@";;
  week) shift; cmd_week "$@";;
  digest-week) shift; cmd_digest_week "$@";;
  stats) shift; cmd_stats;;
  -h|--help|help|"") usage;;
  *) die "unknown command: $1";;
esac
