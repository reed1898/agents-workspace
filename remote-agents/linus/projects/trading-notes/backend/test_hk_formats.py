#!/usr/bin/env python3
"""Test different HK stock symbol formats"""

import yfinance as yf

def test_symbol(symbol):
    """Test a single symbol"""
    print(f"\n{'='*60}")
    print(f"Testing: {symbol}")
    print(f"{'='*60}")

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")

        if hist.empty:
            print(f"❌ FAILED: No data returned")
            return False
        else:
            price = hist['Close'].iloc[-1]
            print(f"✅ SUCCESS: Price = ${price:.2f}")
            print(f"Full data:\n{hist}")
            return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    # 测试腾讯控股 (0700) 的不同格式
    print("\n" + "="*60)
    print("Testing Tencent (腾讯控股) - Stock Code: 0700")
    print("="*60)

    formats = [
        "0700.HK",      # 4位,1个前导零
        "00700.HK",     # 5位,2个前导零
        "700.HK",       # 3位,无前导零
        "0700.hk",      # 小写
        "00700.hk",     # 小写
    ]

    results = {}
    for fmt in formats:
        results[fmt] = test_symbol(fmt)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for fmt, success in results.items():
        status = "✅ Works" if success else "❌ Failed"
        print(f"{fmt:15} {status}")

    # 找出工作的格式
    working = [fmt for fmt, success in results.items() if success]
    if working:
        print(f"\n✅ Working format(s): {', '.join(working)}")
    else:
        print("\n❌ No working format found!")
