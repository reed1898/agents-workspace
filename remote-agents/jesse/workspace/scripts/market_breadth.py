#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get market advance/decline counts"""
import urllib.request, json, ssl

ctx = ssl.create_default_context()

# Fetch page by page to count advance/decline
# Use eastmoney API with f3 field (change_pct) - get all at once if possible 
# or sample to estimate

# Strategy: get total, then get the middle page to find the crossover point
# total = 5193

# Actually, let's try to use the f104/f105/f106 fields from market index
# f104 = advance count, f105 = decline count, f106 = flat count
try:
    url = "https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f44,f45,f46,f47,f48,f57,f58,f104,f105,f106,f170&secid=1.000001"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        d = json.loads(resp.read().decode('utf-8'))
    print("Shanghai index data:")
    print(json.dumps(d.get('data', {}), ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")

# Alternative: try the datacenter API for market breadth
try:
    url2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1&pageNumber=1&reportName=RPT_MARKET_UPDOWN_ANALYSIS&columns=ALL"
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=15, context=ctx) as resp2:
        d2 = json.loads(resp2.read().decode('utf-8'))
    print("\nMarket breadth data:")
    print(json.dumps(d2, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Breadth error: {e}")

# Try the cls.cn API for market breadth
try:
    url3 = "https://x-quote.cls.cn/v2/quote/a/market/current?app=CailianpressWeb&os=web&sv=8.4.6"
    req3 = urllib.request.Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req3, timeout=15, context=ctx) as resp3:
        d3 = json.loads(resp3.read().decode('utf-8'))
    print("\nCLS market data:")
    print(json.dumps(d3, ensure_ascii=False, indent=2)[:3000])
except Exception as e:
    print(f"CLS error: {e}")
