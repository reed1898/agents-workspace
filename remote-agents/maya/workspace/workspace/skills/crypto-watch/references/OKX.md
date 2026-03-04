# OKX public candles

Endpoint used:

- `GET https://www.okx.com/api/v5/market/candles?instId=<INST>&bar=15m&limit=300`

Response:
- `code == "0"` means success
- `data` is an array of candles, newest-first
- Candle fields (strings):
  0 ts(ms), 1 open, 2 high, 3 low, 4 close, 5 vol, ...
