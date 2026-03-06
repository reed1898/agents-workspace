#!/usr/bin/env bash
set -euo pipefail

DATE_STR="$(date +%F)"
OUT_DIR="/Users/rain/.openclaw/workspace/reports/daily"
mkdir -p "$OUT_DIR"

VEILLE_DIR="/Users/rain/.openclaw/workspace/skills/veille/scripts"
MULTI_DIR="/Users/rain/.openclaw/workspace/skills/multi-source-news-digest"

VEILLE_JSON="/tmp/veille-${DATE_STR}.json"
MULTI_TXT="/tmp/multi-${DATE_STR}.txt"
REPORT_MD="${OUT_DIR}/${DATE_STR}.md"

cd "$VEILLE_DIR"
python3 veille.py fetch --hours 24 --filter-seen --filter-topic > "$VEILLE_JSON"

cd "$MULTI_DIR"
python3 skill.py refresh >/dev/null 2>&1 || true
python3 skill.py digest > "$MULTI_TXT" || true

python3 - <<'PY'
import json, os, datetime
from pathlib import Path

date_str = os.popen('date +%F').read().strip()
veille_json = f"/tmp/veille-{date_str}.json"
multi_txt = f"/tmp/multi-{date_str}.txt"
report_md = Path(f"/Users/rain/.openclaw/workspace/reports/daily/{date_str}.md")

articles = []
try:
    with open(veille_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        articles = data.get('articles', [])
except Exception:
    pass

lines = []
lines.append(f"# Daily AI/Web3 Digest - {date_str}")
lines.append("")
lines.append("## Candidate Pool")
lines.append(f"- veille items: {len(articles)}")
if Path(multi_txt).exists():
    size_kb = Path(multi_txt).stat().st_size // 1024
    lines.append(f"- multi-source digest captured: {size_kb} KB")
else:
    lines.append("- multi-source digest captured: 0 KB")
lines.append("")
lines.append("## Must-Read 3")
lines.append("- TBC")
lines.append("- TBC")
lines.append("- TBC")
lines.append("")
lines.append("## AI Opportunities / Risks")
lines.append("- TBC")
lines.append("")
lines.append("## Web3 Opportunities / Risks")
lines.append("- TBC")
lines.append("")
lines.append("## Today Actions (max 3)")
lines.append("- TBC")
lines.append("")
lines.append("## X Drafts")
lines.append("### Short Post")
lines.append("- TBC")
lines.append("### Insight Post")
lines.append("- TBC")
lines.append("")
lines.append("## Top veille items (raw)")
for a in articles[:15]:
    title = a.get('title','').replace('\n',' ').strip()
    url = a.get('url','').strip()
    src = a.get('source','').strip()
    if title:
        lines.append(f"- [{src}] {title} - {url}")

report_md.write_text("\n".join(lines), encoding='utf-8')
print(report_md)
PY

echo "Generated: $REPORT_MD"
echo "Veille JSON: $VEILLE_JSON"
echo "Multi digest: $MULTI_TXT"
