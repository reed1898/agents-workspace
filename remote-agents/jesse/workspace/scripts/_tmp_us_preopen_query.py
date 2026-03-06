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
cur.execute("SELECT NOW() as now_ts")
now = cur.fetchone()['now_ts']
cur.execute("""
SELECT ta.account_name, p.symbol, p.quantity, p.average_cost, p.current_price,
       p.unrealized_pnl, p.unrealized_pnl_percent, p.last_updated,
       (p.quantity * p.current_price) AS market_value
FROM positions p
JOIN trade_accounts ta ON ta.id = p.account_id
WHERE IFNULL(p.is_closed,0)=0 AND ta.account_type='us_stock'
ORDER BY market_value DESC
""")
rows = cur.fetchall()
print(json.dumps({'now': str(now), 'rows': rows}, ensure_ascii=False, default=str))
cur.close(); conn.close()
