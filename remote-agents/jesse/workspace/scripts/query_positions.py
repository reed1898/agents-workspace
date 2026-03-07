import os, pymysql

conn = pymysql.connect(
    host=os.environ['TRADING_NOTES_MYSQL_HOST'],
    port=int(os.environ['TRADING_NOTES_MYSQL_PORT']),
    user=os.environ['TRADING_NOTES_MYSQL_USER'],
    password=os.environ['TRADING_NOTES_MYSQL_PASSWORD'],
    database=os.environ['TRADING_NOTES_MYSQL_DATABASE'],
    charset='utf8mb4'
)
cur = conn.cursor()
sql = (
    "SELECT p.symbol, p.quantity, p.average_cost, p.current_price, "
    "p.unrealized_pnl, p.unrealized_pnl_percent, p.entry_price, "
    "p.holding_days, a.account_name, a.broker "
    "FROM positions p "
    "JOIN trade_accounts a ON p.account_id = a.id "
    "WHERE p.is_closed = 0 AND a.account_type = 'us_stock' "
    "ORDER BY a.broker, p.symbol"
)
cur.execute(sql)
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
for r in rows:
    print(dict(zip(cols, r)))
conn.close()
