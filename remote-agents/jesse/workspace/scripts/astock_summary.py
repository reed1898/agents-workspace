#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股盘后总结 - 查询持仓 + 获取实时价格"""
import os, json, sys, urllib.request

import pymysql

# --- 1. Query positions from DB ---
host = os.environ.get("TRADING_NOTES_MYSQL_HOST")
port = int(os.environ.get("TRADING_NOTES_MYSQL_PORT", "3306"))
db = os.environ.get("TRADING_NOTES_MYSQL_DATABASE")
user = os.environ.get("TRADING_NOTES_MYSQL_USER")
pwd = os.environ.get("TRADING_NOTES_MYSQL_PASSWORD")

conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database=db, charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)

cur.execute("""
    SELECT id, symbol, name, account, direction, quantity, avg_cost, account_type, notes
    FROM positions
    WHERE is_closed=0 AND account_type='a_stock'
    ORDER BY account, symbol
""")
positions = cur.fetchall()

# Also check if there are any other open A-stock-like positions
cur.execute("""
    SELECT DISTINCT account_type FROM positions WHERE is_closed=0
""")
all_types = [r['account_type'] for r in cur.fetchall()]

cur.close()
conn.close()

print(f"=== POSITIONS ({len(positions)}) ===")
for p in positions:
    # Convert Decimal to float for JSON serialization
    qty = float(p['quantity']) if p['quantity'] else 0
    cost = float(p['avg_cost']) if p['avg_cost'] else 0
    print(json.dumps({
        'id': p['id'],
        'symbol': p['symbol'],
        'name': p['name'],
        'account': p['account'],
        'direction': p['direction'],
        'quantity': qty,
        'avg_cost': cost,
        'notes': p.get('notes', '')
    }, ensure_ascii=False))

print(f"\n=== ALL OPEN ACCOUNT TYPES ===")
print(json.dumps(all_types, ensure_ascii=False))

# --- 2. Get real-time prices for each position ---
if positions:
    symbols = []
    for p in positions:
        sym = p['symbol']
        # Determine market: 6xx = Shanghai (1.), 0xx/3xx = Shenzhen (0.)
        if sym.startswith('6'):
            secid = f"1.{sym}"
        else:
            secid = f"0.{sym}"
        symbols.append(secid)
    
    secids_str = ",".join(symbols)
    url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f5,f6,f12,f14,f15,f16,f17,f18&secids={secids_str}"
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.eastmoney.com'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        print(f"\n=== REALTIME PRICES ===")
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                print(json.dumps(item, ensure_ascii=False))
        else:
            print("No price data returned")
            print(json.dumps(data, ensure_ascii=False))
    except Exception as e:
        print(f"Price fetch error: {e}")
        # Fallback: try individual requests
        print("\n=== FALLBACK INDIVIDUAL PRICES ===")
        for secid in symbols:
            try:
                url2 = f"https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f44,f45,f46,f57,f58,f170&secid={secid}"
                req2 = urllib.request.Request(url2)
                with urllib.request.urlopen(req2, timeout=10) as resp2:
                    d2 = json.loads(resp2.read().decode('utf-8'))
                if d2.get('data'):
                    print(json.dumps(d2['data'], ensure_ascii=False))
            except Exception as e2:
                print(f"Error for {secid}: {e2}")

# --- 3. Get market breadth (advance/decline counts) ---
print(f"\n=== MARKET BREADTH ===")
# Get stocks with positive change
try:
    # We'll sample the full list and count
    url_all = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1&po=1&np=1&fltt=2&fields=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fid=f3"
    req_all = urllib.request.Request(url_all, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.eastmoney.com'})
    with urllib.request.urlopen(req_all, timeout=10) as resp:
        d = json.loads(resp.read().decode('utf-8'))
    total = d['data']['total']
    print(f"Total: {total}")
    
    # Get a larger sample to estimate advance/decline
    # Actually, let's try the datacenter API for market stats
    url_stats = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1&pageNumber=1&reportName=RPT_MARKET_UPDOWN_ANALYSIS&columns=ALL"
    req_stats = urllib.request.Request(url_stats, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_stats, timeout=10) as resp:
        stats = json.loads(resp.read().decode('utf-8'))
    print(json.dumps(stats, ensure_ascii=False))
except Exception as e:
    print(f"Breadth error: {e}")

# --- 4. Get total market turnover ---
print(f"\n=== MARKET VOLUME ===")
try:
    # SH total
    url_sh = "https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f46,f47,f48,f57,f58,f170&secid=1.000001"
    req_sh = urllib.request.Request(url_sh)
    with urllib.request.urlopen(req_sh, timeout=10) as resp:
        sh = json.loads(resp.read().decode('utf-8'))
    print(f"SH: {json.dumps(sh['data'], ensure_ascii=False)}")
    
    url_sz = "https://push2his.eastmoney.com/api/qt/stock/get?fltt=2&fields=f43,f46,f47,f48,f57,f58,f170&secid=0.399001"
    req_sz = urllib.request.Request(url_sz)
    with urllib.request.urlopen(req_sz, timeout=10) as resp:
        sz = json.loads(resp.read().decode('utf-8'))
    print(f"SZ: {json.dumps(sz['data'], ensure_ascii=False)}")
except Exception as e:
    print(f"Volume error: {e}")
