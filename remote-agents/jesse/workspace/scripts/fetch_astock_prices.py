#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch real-time prices for A-stock positions from eastmoney"""
import json, urllib.request, ssl

# A-stock symbols from the two accounts
# Account 3afb... (国信证券): 002050.SZ, 300065.SZ, 600118.SH, 600877.SH, 601698.SH, 688048.SH, 688102.SH
# Account 7b32... (国泰君安): 000547.SZ, 000592.SZ, 002291.SZ, 002410.SZ, 002606.SZ, 002809.SZ, 300077.SZ, 300136.SZ, 300170.SZ, 300433.SZ, 300442.SZ, 300762.SZ, 600105.SH, 600633.SH, 600763.SH, 603778.SH, 603919.SH, 688568.SH

symbols = [
    "002050", "300065", "600118", "600877", "601698", "688048", "688102",
    "000547", "000592", "002291", "002410", "002606", "002809",
    "300077", "300136", "300170", "300433", "300442", "300762",
    "600105", "600633", "600763", "603778", "603919", "688568"
]

secids = []
for s in symbols:
    if s.startswith("6"):
        secids.append(f"1.{s}")
    else:
        secids.append(f"0.{s}")

# Fetch individually using push2his which works
ctx = ssl.create_default_context()
results = {}
for secid in secids:
    try:
        url = f"https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f170&secid={secid}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            d = json.loads(resp.read().decode('utf-8'))
        if d.get('data'):
            code = d['data']['f57']
            results[code] = {
                'code': code,
                'name': d['data'].get('f58', ''),
                'close': d['data'].get('f43'),      # 收盘价
                'high': d['data'].get('f44'),        # 最高
                'low': d['data'].get('f45'),         # 最低
                'open': d['data'].get('f46'),        # 开盘
                'volume': d['data'].get('f47'),      # 成交量(���)
                'amount': d['data'].get('f48'),      # 成交额
                'change_pct': d['data'].get('f170'), # 涨跌幅%
            }
    except Exception as e:
        sym = secid.split('.')[1]
        print(f"Error fetching {secid}: {e}")

print(json.dumps(results, ensure_ascii=False, indent=2))
