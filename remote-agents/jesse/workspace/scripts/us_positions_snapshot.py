import pymysql, json

conn = pymysql.connect(
    host='18.224.71.149',
    port=3308,
    user='trading',
    password='zIcyT=hj=C5',
    database='trading_notes',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)
cur = conn.cursor()
cur.execute("""
SELECT ta.account_name, p.symbol, p.quantity, p.average_cost, p.current_price,
       p.unrealized_pnl, p.unrealized_pnl_percent, p.last_updated
FROM positions p
JOIN trade_accounts ta ON ta.id = p.account_id
WHERE IFNULL(p.is_closed,0)=0 AND ta.account_type='us_stock'
ORDER BY p.unrealized_pnl DESC
""")
rows = cur.fetchall()
print(json.dumps(rows, ensure_ascii=False, default=str))
cur.close(); conn.close()
