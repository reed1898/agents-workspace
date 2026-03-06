import pymysql
from decimal import Decimal

conn = pymysql.connect(
    host='18.224.71.149', port=3308, user='trading', password='zIcyT=hj=C5',
    database='trading_notes', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

# open positions
cur.execute("""
SELECT 
  p.account_id,
  ta.account_name,
  ta.account_type,
  p.symbol,
  p.position_type,
  p.position_side,
  p.quantity,
  p.current_price,
  p.unrealized_pnl,
  p.unrealized_pnl_percent,
  p.roe_percent,
  p.last_updated
FROM positions p
LEFT JOIN trade_accounts ta ON ta.id = p.account_id
WHERE IFNULL(p.is_closed,0)=0
ORDER BY p.unrealized_pnl DESC
""")
rows = cur.fetchall()

print('OPEN_POSITIONS', len(rows))

# normalize key case helper

def g(r, k):
    if k in r: return r[k]
    ku = k.upper()
    if ku in r: return r[ku]
    kl = k.lower()
    if kl in r: return r[kl]
    for kk,v in r.items():
        if kk.lower()==k.lower():
            return v
    return None

# totals
sum_pnl = Decimal('0')
count_profit = 0
count_loss = 0
by_type = {}

for r in rows:
    upnl = g(r,'unrealized_pnl') or Decimal('0')
    if upnl is None: upnl=Decimal('0')
    if not isinstance(upnl, Decimal):
        upnl = Decimal(str(upnl))
    sum_pnl += upnl
    if upnl > 0: count_profit += 1
    elif upnl < 0: count_loss += 1
    t = (g(r,'position_type') or 'unknown')
    by_type[t] = by_type.get(t, 0) + 1

print('TOTAL_UNREALIZED_PNL', str(sum_pnl))
print('PROFIT_COUNT', count_profit)
print('LOSS_COUNT', count_loss)
print('BY_TYPE', by_type)

# top winners/losers
sorted_rows = sorted(rows, key=lambda r: Decimal(str(g(r,'unrealized_pnl') or 0)), reverse=True)
print('TOP_WINNERS')
for r in sorted_rows[:5]:
    print({
        'account': g(r,'account_name'),
        'symbol': g(r,'symbol'),
        'type': g(r,'position_type'),
        'side': g(r,'position_side'),
        'unrealized_pnl': str(g(r,'unrealized_pnl')),
        'pnl_pct': str(g(r,'unrealized_pnl_percent')),
        'roe_pct': str(g(r,'roe_percent')),
    })

print('TOP_LOSERS')
for r in sorted_rows[-5:]:
    print({
        'account': g(r,'account_name'),
        'symbol': g(r,'symbol'),
        'type': g(r,'position_type'),
        'side': g(r,'position_side'),
        'unrealized_pnl': str(g(r,'unrealized_pnl')),
        'pnl_pct': str(g(r,'unrealized_pnl_percent')),
        'roe_pct': str(g(r,'roe_percent')),
    })

# account summary
cur.execute("""
SELECT
  ta.account_name,
  ta.account_type,
  COUNT(*) AS open_positions,
  SUM(IFNULL(p.unrealized_pnl,0)) AS total_unrealized_pnl
FROM positions p
LEFT JOIN trade_accounts ta ON ta.id = p.account_id
WHERE IFNULL(p.is_closed,0)=0
GROUP BY ta.account_name, ta.account_type
ORDER BY total_unrealized_pnl DESC
""")
print('BY_ACCOUNT')
for r in cur.fetchall():
    print({k.lower(): (str(v) if isinstance(v, Decimal) else v) for k,v in r.items()})

cur.close(); conn.close()
