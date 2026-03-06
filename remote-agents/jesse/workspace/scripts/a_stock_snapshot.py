import pymysql
from decimal import Decimal

conn = pymysql.connect(
    host='18.224.71.149', port=3308, user='trading', password='zIcyT=hj=C5',
    database='trading_notes', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()
cur.execute('''
SELECT ta.account_name, ta.account_type, p.symbol, p.quantity, p.current_price,
       p.unrealized_pnl, p.unrealized_pnl_percent, p.last_updated
FROM positions p
LEFT JOIN trade_accounts ta ON ta.id = p.account_id
WHERE IFNULL(p.is_closed,0)=0 AND ta.account_type='a_stock'
ORDER BY p.unrealized_pnl DESC
''')
rows = cur.fetchall()
print('COUNT', len(rows))
total = sum(Decimal(str(r.get('unrealized_pnl') or 0)) for r in rows)
print('TOTAL_PNL', total)
print('TOP_WIN')
for r in rows[:5]:
    print(r['symbol'], r['unrealized_pnl'], r['unrealized_pnl_percent'], r['last_updated'])
print('TOP_LOSS')
for r in rows[-5:]:
    print(r['symbol'], r['unrealized_pnl'], r['unrealized_pnl_percent'], r['last_updated'])

cur.close(); conn.close()
