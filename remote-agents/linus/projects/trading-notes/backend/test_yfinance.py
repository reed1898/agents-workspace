#!/usr/bin/env python3
"""Test yfinance price fetching"""

import yfinance as yf

def test_stock_price(symbol):
    print(f"\n=== Testing {symbol} ===")
    try:
        ticker = yf.Ticker(symbol)

        # Try history method
        print(f"Fetching history for {symbol}...")
        hist = ticker.history(period="1d")

        if hist.empty:
            print(f"ERROR: No historical data returned for {symbol}")
        else:
            price = hist['Close'].iloc[-1]
            print(f"SUCCESS: Latest price for {symbol}: ${price:.2f}")
            print(f"Full history data:")
            print(hist)

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # Test US stocks
    test_stock_price("AAPL")
    test_stock_price("TSLA")

    # Test HK stocks
    test_stock_price("00700.HK")
    test_stock_price("09988.HK")
    test_stock_price("01810.HK")
