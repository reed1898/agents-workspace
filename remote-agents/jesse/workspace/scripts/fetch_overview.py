import urllib.request
import json
import time

symbols = ['PLTR', 'RKLB', 'NFLX', 'RBLX', 'RDW', 'TDY']

for sym in symbols:
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=calendarEvents,defaultKeyStatistics,financialData"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        result = data.get('quoteSummary', {}).get('result', [{}])[0]
        cal = result.get('calendarEvents', {})
        earnings = cal.get('earnings', {})
        earnings_date = earnings.get('earningsDate', [])
        ex_div = cal.get('exDividendDate', {})
        stats = result.get('defaultKeyStatistics', {})
        fin = result.get('financialData', {})
        print(f"{sym}: earningsDate={[e.get('fmt') for e in earnings_date]}, "
              f"beta={stats.get('beta', {}).get('raw', 'N/A')}, "
              f"52wHigh={stats.get('fiftyTwoWeekHigh', {}).get('raw', 'N/A')}, "
              f"52wLow={stats.get('fiftyTwoWeekLow', {}).get('raw', 'N/A')}, "
              f"targetMeanPrice={fin.get('targetMeanPrice', {}).get('raw', 'N/A')}")
    except Exception as e:
        print(f"{sym}: ERROR {e}")
    time.sleep(0.5)
