import os, pymysql

c = pymysql.connect(
    host=os.environ['TRADING_NOTES_MYSQL_HOST'],
    port=int(os.environ['TRADING_NOTES_MYSQL_PORT']),
    user=os.environ['TRADING_NOTES_MYSQL_USER'],
    password=os.environ['TRADING_NOTES_MYSQL_PASSWORD'],
    database=os.environ['TRADING_NOTES_MYSQL_DATABASE']
)
cur = c.cursor()
cur.execute("""
    SELECT p.symbol, p.quantity, p.average_cost, p.entry_price, p.current_price,
           p.unrealized_pnl, p.unrealized_pnl_percent, p.holding_days,
           a.account_name, a.broker
    FROM positions p
    JOIN trade_accounts a ON p.account_id = a.id
    WHERE p.is_closed = 0 AND a.account_type = 'a_stock'
    ORDER BY p.symbol
""")
rows = cur.fetchall()
print("SYMBOL|QTY|AVG_COST|ENTRY|CURRENT|PNL|PNL%|DAYS|ACCOUNT|BROKER")
for r in rows:
    print("|".join(str(x) for x in r))
c.close()
