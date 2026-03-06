#!/usr/bin/env python3
"""Test HK and A stock price fetching"""

import yfinance as yf
import akshare as ak

def test_hk_stock_formats():
    """Test different HK stock symbol formats"""
    print("\n=== Testing HK Stock Formats ===")

    # Test different formats for Tencent (腾讯)
    symbols = [
        "0700.HK",      # Without leading zeros
        "00700.HK",     # With leading zeros
        "700.HK",       # Minimal format
    ]

    for symbol in symbols:
        print(f"\nTrying {symbol}...")
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                print(f"✓ SUCCESS: {symbol} = ${price:.2f}")
                return symbol  # Return working format
            else:
                print(f"✗ FAILED: {symbol} - No data")
        except Exception as e:
            print(f"✗ ERROR: {symbol} - {e}")

    return None

def test_a_stock():
    """Test A stock using akshare"""
    print("\n=== Testing A Stock (AKShare) ===")

    try:
        # Get real-time quotes for A shares
        print("Fetching A-stock data from AKShare...")
        df = ak.stock_zh_a_spot_em()

        # Show first few rows
        print(f"\nTotal stocks: {len(df)}")
        print("\nFirst 5 stocks:")
        print(df.head()[['代码', '名称', '最新价', '涨跌幅']])

        # Try specific stock (平安银行 000001)
        stock_code = "000001"
        stock_data = df[df["代码"] == stock_code]

        if not stock_data.empty:
            price = stock_data.iloc[0]["最新价"]
            name = stock_data.iloc[0]["名称"]
            print(f"\n✓ SUCCESS: {stock_code} ({name}) = ¥{price}")
            return True
        else:
            print(f"\n✗ FAILED: Stock {stock_code} not found")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test HK stocks
    working_format = test_hk_stock_formats()
    if working_format:
        print(f"\n✓ HK Stock working format: {working_format}")
    else:
        print("\n✗ No working HK stock format found")

    # Test A stocks
    a_stock_works = test_a_stock()
    if a_stock_works:
        print("\n✓ A Stock (AKShare) is working")
    else:
        print("\n✗ A Stock (AKShare) is NOT working")
