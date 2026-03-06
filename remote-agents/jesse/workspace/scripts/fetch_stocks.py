"""Fetch latest A-stock prices and info from Tencent finance API"""
import urllib.request
import json
import re

# All 25 positions
symbols = [
    "002050", "300065", "600118", "600877", "601698",
    "688048", "688102", "000547", "000592", "002291",
    "002410", "002606", "002809", "300077", "300136",
    "300170", "300433", "300442", "300762", "600105",
    "600633", "600763", "603778", "603919", "688568"
]

# Convert to Tencent format: sh=60xxxx/68xxxx, sz=00xxxx/30xxxx/002xxx
tencent_codes = []
for s in symbols:
    if s.startswith("6"):
        tencent_codes.append(f"sh{s}")
    else:
        tencent_codes.append(f"sz{s}")

url = f"https://qt.gtimg.cn/q={','.join(tencent_codes)}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode('gbk')
        # Parse each line: v_shXXXXXX="1~name~code~price~...";
        for line in raw.strip().split('\n'):
            line = line.strip()
            if not line or '="' not in line:
                continue
            m = re.search(r'v_(\w+)="(.+)"', line)
            if m:
                code = m.group(1)
                fields = m.group(2).split('~')
                if len(fields) > 5:
                    name = fields[1]
                    current = fields[3]
                    prev_close = fields[4]
                    pct_change = fields[32] if len(fields) > 32 else "?"
                    high = fields[33] if len(fields) > 33 else "?"
                    low = fields[34] if len(fields) > 34 else "?"
                    volume = fields[6] if len(fields) > 6 else "?"  # in hands (手)
                    turnover = fields[37] if len(fields) > 37 else "?"  # in yuan
                    print(f"{code}: {name} | 昨收:{prev_close} | 现价:{current} | 涨跌:{pct_change}% | 最高:{high} | 最低:{low} | 成交量:{volume}手 | 成交额:{turnover}")
except Exception as e:
    print(f"ERROR: {e}")
