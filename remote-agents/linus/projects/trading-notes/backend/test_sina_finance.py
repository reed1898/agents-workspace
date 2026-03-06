#!/usr/bin/env python3
"""Test Sina Finance API for A-stock prices"""

import httpx
import re

def test_sina_finance(stock_code):
    """
    测试新浪财经API获取A股价格

    新浪财经API格式:
    http://hq.sinajs.cn/list=sh600519  (上交所)
    http://hq.sinajs.cn/list=sz000001  (深交所)

    返回格式: var hq_str_sh600519="贵州茅台,2789.00,2782.00,2795.00,..."
    """
    try:
        # 判断交易所 (6开头是上交所, 0/3开头是深交所)
        if stock_code.startswith('6'):
            prefix = 'sh'
        elif stock_code.startswith('0') or stock_code.startswith('3'):
            prefix = 'sz'
        else:
            print(f"Unknown stock code format: {stock_code}")
            return None

        symbol = f"{prefix}{stock_code}"
        url = f"http://hq.sinajs.cn/list={symbol}"

        print(f"\nTesting {stock_code} ({symbol})...")
        print(f"URL: {url}")

        # 添加请求头避免403错误
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://finance.sina.com.cn'
        }
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析返回数据
        content = response.text
        print(f"Response: {content[:200]}...")

        # 提取股票数据
        # 格式: var hq_str_sh600519="股票名称,今日开盘价,昨收盘,当前价格,..."
        match = re.search(r'"([^"]+)"', content)
        if not match:
            print("Failed to parse response")
            return None

        data = match.group(1).split(',')
        if len(data) < 4:
            print("Insufficient data fields")
            return None

        name = data[0]
        current_price = float(data[3])

        print(f"✓ SUCCESS: {name} ({stock_code}) = ¥{current_price}")
        return current_price

    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 测试几个常见A股
    test_stocks = [
        "000001",  # 平安银行 (深交所)
        "600519",  # 贵州茅台 (上交所)
        "000858",  # 五粮液 (深交所)
    ]

    for stock in test_stocks:
        test_sina_finance(stock)
