import urllib.request
import json

symbols = ["PLTR", "PLUG", "RKLB", "NFLX", "RBLX", "RDW", "TDY", "QQQ",
           "^GSPC", "^DJI", "^IXIC", "^VIX",
           "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]

for sym in symbols:
    try:
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=price"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            p = data["quoteSummary"]["result"][0]["price"]
            name = p.get("shortName", sym)
            price = p.get("regularMarketPrice", {}).get("raw", "N/A")
            change = p.get("regularMarketChangePercent", {}).get("raw", "N/A")
            prev = p.get("regularMarketPreviousClose", {}).get("raw", "N/A")
            print(f"{sym}|{name}|{price}|{change}|{prev}")
    except Exception as e:
        # Fallback: try v8 chart API
        try:
            url2 = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d"
            req2 = urllib.request.Request(url2, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            with urllib.request.urlopen(req2, timeout=10) as resp2:
                data2 = json.loads(resp2.read())
                meta = data2["chart"]["result"][0]["meta"]
                price = meta.get("regularMarketPrice", "N/A")
                prev = meta.get("chartPreviousClose", "N/A")
                if price != "N/A" and prev != "N/A":
                    chg = (price - prev) / prev * 100
                else:
                    chg = "N/A"
                print(f"{sym}|{sym}|{price}|{chg}|{prev}")
        except Exception as e2:
            print(f"{sym}|ERROR|{e2}")
