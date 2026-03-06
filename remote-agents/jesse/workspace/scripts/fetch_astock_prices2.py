#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, urllib.request, ssl, time

# Remaining symbols that failed
symbols_remaining = [
    "000592", "002291", "002410", "002606", "002809",
    "300077", "300136", "300170", "300433", "300442", "300762",
    "600105", "600633", "600763", "603778", "603919", "688568"
]

ctx = ssl.create_default_context()
results = {}

for s in symbols_remaining:
    secid = f"1.{s}" if s.startswith("6") else f"0.{s}"
    try:
        url = f"https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f170&secid={secid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Connection': 'close'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            d = json.loads(resp.read().decode('utf-8'))
        if d.get('data'):
            code = d['data']['f57']
            results[code] = {
                'code': code,
                'name': d['data'].get('f58', ''),
                'close': d['data'].get('f43'),
                'change_pct': d['data'].get('f170'),
            }
            print(f"OK: {code} = {d['data'].get('f43')} ({d['data'].get('f170')}%)")
        time.sleep(0.5)  # Rate limit
    except Exception as e:
        print(f"Error {secid}: {e}")
        time.sleep(1)

print("\n=== RESULTS ===")
print(json.dumps(results, ensure_ascii=False, indent=2))
