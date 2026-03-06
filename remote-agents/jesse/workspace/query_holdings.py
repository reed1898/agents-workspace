import pymysql

conn = pymysql.connect(
    host='18.224.71.149',
    port=3308,
    user='trading',
    password='zIcyT=hj=C5',
    database='trading_notes'
)
cur = conn.cursor()

cur.execute(
    "SELECT p.symbol, p.quantity, p.average_cost, p.current_price, "
    "p.unrealized_pnl, p.unrealized_pnl_percent, p.position_side, "
    "p.first_buy_time, p.holding_days, p.last_updated, p.notes, "
    "a.account_name "
    "FROM positions p JOIN trade_accounts a ON p.account_id = a.id "
    "WHERE a.account_type = 'us_stock' AND p.is_closed = 0 ORDER BY p.symbol"
)
cols = [desc[0] for desc in cur.description]
print("||".join(cols))
print("---")
for row in cur.fetchall():
    print("||".join(str(x) if x is not None else "" for x in row))

cur.close()
conn.close()
