"""Fetch latest A-stock prices - fix encoding"""
import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

symbols = [
    "002050", "300065", "600118", "600877", "601698",
    "688048", "688102", "000547", "000592", "002291",
    "002410", "002606", "002809", "300077", "300136",
    "300170", "300433", "300442", "300762", "600105",
    "600633", "600763", "603778", "603919", "688568"
]

tencent_codes = []
for s in symbols:
    if s.startswith("6"):
        tencent_codes.append(f"sh{s}")
    else:
        tencent_codes.append(f"sz{s}")

url = f"https://qt.gtimg.cn/q={','.join(tencent_codes)}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    raw = resp.read().decode('gbk')
    results = []
    for line in raw.strip().split('\n'):
        line = line.strip()
        if not line or '="' not in line:
            continue
        m = re.search(r'v_(\w+)="(.+)"', line)
        if m:
            code = m.group(1)
            f = m.group(2).split('~')
            if len(f) > 45:
                results.append({
                    "code": code,
                    "name": f[1],
                    "current": f[3],
                    "prev_close": f[4],
                    "open": f[5],
                    "volume_hands": f[6],
                    "pct_change": f[32],
                    "high": f[33],
                    "low": f[34],
                    "turnover_wan": f[37],
                    "pe": f[39],
                    "pb": f[46] if len(f) > 46 else "",
                    "total_mv": f[45] if len(f) > 45 else "",
                })
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
