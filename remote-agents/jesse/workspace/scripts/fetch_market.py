import urllib.request
import json

# Use East Money API for global market overview
urls = {
    # US indices
    "us_markets": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.DJIA,100.NDX,100.SPX&fields=f2,f3,f4,f12,f14",
    # HK indices
    "hk_markets": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.HSI,100.HSTECH&fields=f2,f3,f4,f12,f14",
    # EUR indices
    "eu_markets": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.FTSE,100.GDAXI,100.FCHI&fields=f2,f3,f4,f12,f14",
    # Commodities & FX
    "commodities": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.UDI,113.USDCNH,142.GC2506,142.CL2504&fields=f2,f3,f4,f12,f14",
    # A50 futures  
    "a50": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.CHA50CFD&fields=f2,f3,f4,f12,f14",
    # BTC
    "btc": "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.BTCUSD&fields=f2,f3,f4,f12,f14",
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.eastmoney.com/"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"=== {name} ===")
            if data.get("data") and data["data"].get("diff"):
                for item in data["data"]["diff"]:
                    print(f"  {item.get('f14','?')} ({item.get('f12','?')}): {item.get('f2','?')}  涨跌幅: {item.get('f3','?')}%  涨跌额: {item.get('f4','?')}")
            else:
                print(f"  No data: {json.dumps(data, ensure_ascii=False)[:200]}")
    except Exception as e:
        print(f"=== {name} === ERROR: {e}")

# 10Y US Treasury
try:
    url_bond = "https://push2.eastmoney.com/api/qt/stock/get?secid=100.TNX&fields=f43,f44,f45,f46,f47,f170"
    req = urllib.request.Request(url_bond, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.eastmoney.com/"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print(f"=== 10Y UST ===")
        print(f"  {json.dumps(data.get('data',{}), ensure_ascii=False)[:300]}")
except Exception as e:
    print(f"=== 10Y UST === ERROR: {e}")

# KWEB (China tech ETF) as proxy for 中概
try:
    url_kweb = "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=100.KWEB&fields=f2,f3,f4,f12,f14"
    req = urllib.request.Request(url_kweb, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.eastmoney.com/"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print(f"=== KWEB ===")
        if data.get("data") and data["data"].get("diff"):
            for item in data["data"]["diff"]:
                print(f"  {item.get('f14','?')} ({item.get('f12','?')}): {item.get('f2','?')}  涨跌幅: {item.get('f3','?')}%")
        else:
            print(f"  No data")
except Exception as e:
    print(f"=== KWEB === ERROR: {e}")
