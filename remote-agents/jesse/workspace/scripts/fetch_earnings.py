"""Fetch earnings/announcement schedule from cninfo for all positions"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# A-share annual report deadline: April 30
# Q1 report deadline: April 30  
# Semi-annual report: August 31
# Q3 report: October 31
# 2025 annual report disclosure period: Jan-Apr 2026

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

# Try to get earnings calendar from Tencent QQ finance
for code, name in stocks.items():
    prefix = "sh" if code.startswith("6") else "sz"
    # Try ifind / tushare style query
    url = f"https://basic.10jqka.com.cn/{code}/company.html"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://basic.10jqka.com.cn/"
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('gbk', errors='replace')
            # Look for 预约披露日 or similar
            import re
            # Find disclosure date patterns
            matches = re.findall(r'(预约|预计|年报|季报|半年报)[^<]{0,50}(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
            if matches:
                print(f"{code} {name}: {matches[:3]}")
            else:
                # Try to find any date patterns near 'report' or '财报'
                matches2 = re.findall(r'(财报|报告|业绩)[^<]{0,30}(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
                if matches2:
                    print(f"{code} {name}: {matches2[:3]}")
                else:
                    print(f"{code} {name}: 未找到财报日期")
    except Exception as e:
        print(f"{code} {name}: ERROR {e}")

print("\n=== 注意 ===")
print("2025年年报披露截止日: 2026年4月30日")
print("当前距4月30日还有55天")
print("具体各公司预约披露日需查询交易所公告")
