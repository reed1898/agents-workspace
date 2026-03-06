#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch A-stock real-time quotes via Sina Finance API"""
import urllib.request, ssl, re, json

# All A-stock symbols
symbols = [
    "002050", "300065", "600118", "600877", "601698", "688048", "688102",
    "000547", "000592", "002291", "002410", "002606", "002809",
    "300077", "300136", "300170", "300433", "300442", "300762",
    "600105", "600633", "600763", "603778", "603919", "688568"
]

# Convert to sina format: sh600xxx or sz000xxx
sina_codes = []
for s in symbols:
    if s.startswith("6"):
        sina_codes.append(f"sh{s}")
    else:
        sina_codes.append(f"sz{s}")

codes_str = ",".join(sina_codes)
url = f"https://hq.sinajs.cn/list={codes_str}"

ctx = ssl.create_default_context()
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://finance.sina.com.cn'
})

try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        raw = resp.read()
        # Try different encodings
        try:
            text = raw.decode('gbk')
        except:
            text = raw.decode('utf-8', errors='replace')
    
    results = {}
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # Format: var hq_str_sh600118="中国卫星,92.50,...";
        m = re.match(r'var hq_str_(s[hz]\d+)="(.*)";', line)
        if m:
            code_with_prefix = m.group(1)
            code = code_with_prefix[2:]  # Remove sh/sz prefix
            data = m.group(2)
            if not data:
                print(f"No data for {code}")
                continue
            fields = data.split(',')
            # Sina fields: 0=name, 1=open, 2=yesterday_close, 3=current/close, 
            # 4=high, 5=low, 6=bid, 7=ask, 8=volume(shares), 9=amount
            if len(fields) >= 10:
                name = fields[0]
                yesterday_close = float(fields[2]) if fields[2] else 0
                current = float(fields[3]) if fields[3] else 0
                high = float(fields[4]) if fields[4] else 0
                low = float(fields[5]) if fields[5] else 0
                volume = int(float(fields[8])) if fields[8] else 0
                amount = float(fields[9]) if fields[9] else 0
                change_pct = round((current - yesterday_close) / yesterday_close * 100, 2) if yesterday_close else 0
                
                results[code] = {
                    'code': code,
                    'name': name,
                    'close': current,
                    'yesterday_close': yesterday_close,
                    'high': high,
                    'low': low,
                    'change_pct': change_pct,
                    'volume': volume,
                    'amount': amount
                }
                print(f"{code} {name}: {current} ({change_pct:+.2f}%)")
    
    print(f"\n=== JSON ({len(results)} stocks) ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
