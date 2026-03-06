import urllib.request, json
url = "https://query1.finance.yahoo.com/v8/finance/chart/PLUG?interval=1m&range=1d"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read())
    meta = data["chart"]["result"][0]["meta"]
    price = meta.get("regularMarketPrice", "N/A")
    prev = meta.get("chartPreviousClose", "N/A")
    if price != "N/A" and prev != "N/A":
        chg = (price - prev) / prev * 100
    else:
        chg = "N/A"
    print(f"current: ${price}")
    print(f"prev_close: ${prev}")
    print(f"change: {chg:.2f}%")
    # day low/high from indicators
    quotes = data["chart"]["result"][0].get("indicators",{}).get("quote",[{}])[0]
    lows = [x for x in quotes.get("low",[]) if x is not None]
    highs = [x for x in quotes.get("high",[]) if x is not None]
    if lows: print(f"day_low: ${min(lows):.3f}")
    if highs: print(f"day_high: ${max(highs):.3f}")
