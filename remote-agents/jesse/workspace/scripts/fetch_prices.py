import urllib.request
import json
import time

symbols = ['PLTR', 'RKLB', 'NFLX', 'RBLX', 'RDW', 'TDY']

for sym in symbols:
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        result = data['chart']['result'][0]
        meta = result['meta']
        closes = result['indicators']['quote'][0]['close']
        print(f"{sym}: price={meta.get('regularMarketPrice')}, prevClose={meta.get('chartPreviousClose')}, closes={closes[-3:]}")
    except Exception as e:
        print(f"{sym}: ERROR {e}")
    time.sleep(1)
