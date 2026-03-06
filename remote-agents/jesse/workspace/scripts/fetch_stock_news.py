"""Fetch individual stock news from East Money for all positions"""
import urllib.request
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

stocks = {
    "002050": "三花智控", "300065": "海兰信", "600118": "中国卫星",
    "600877": "电科芯片", "601698": "中国卫通", "688048": "长光华芯",
    "688102": "斯瑞新材", "000547": "航天发展", "000592": "平潭发展",
    "002291": "遥望科技", "002410": "广联达", "002606": "大连电瓷",
    "002809": "红墙股份", "300077": "国民技术", "300136": "信维通信",
    "300170": "汉得信息", "300433": "蓝思科技", "300442": "润泽科技",
    "300762": "上海瀚讯", "600105": "永鼎股份", "600633": "浙数文化",
    "600763": "通策医疗", "603778": "国晟科技", "603919": "金徽酒",
    "688568": "中科星图"
}

# Map code to secid format for eastmoney
def get_secid(code):
    if code.startswith("6"):
        return f"1.{code}"
    else:
        return f"0.{code}"

# Fetch announcements from cninfo
for code, name in stocks.items():
    secid = get_secid(code)
    # Try east money news API
    url = f"https://np-listapi.eastmoney.com/comm/wap/getListInfo?cb=&client=wap&type=1&mession=&fc={code}&pageSize=3&pageIndex=1&param=&ShareholderCode=&Token="
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://wap.eastmoney.com/"
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"\n=== {code} {name} ===")
            if data.get("data") and data["data"].get("list"):
                for item in data["data"]["list"][:3]:
                    title = item.get("Art_Title", item.get("title", ""))
                    date = item.get("Art_ShowTime", item.get("showtime", ""))
                    print(f"  [{date}] {title}")
            else:
                print(f"  No news data")
    except Exception as e:
        print(f"\n=== {code} {name} === ERROR: {e}")
    time.sleep(0.3)
