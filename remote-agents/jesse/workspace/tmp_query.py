import os, pymysql, json

host = os.environ.get('TRADING_NOTES_MYSQL_HOST')
port = int(os.environ.get('TRADING_NOTES_MYSQL_PORT', '3306'))
db = os.environ.get('TRADING_NOTES_MYSQL_DATABASE')
user = os.environ.get('TRADING_NOTES_MYSQL_USER')
pwd = os.environ.get('TRADING_NOTES_MYSQL_PASSWORD')

conn = pymysql.connect(host=host, port=port, database=db, user=user, password=pwd, charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)

print("=== TRADE_ACCOUNTS SCHEMA ===")
cur.execute("DESCRIBE trade_accounts")
for c in cur.fetchall():
    print(c)

print("\n=== ALL TRADE_ACCOUNTS ===")
cur.execute("SELECT * FROM trade_accounts")
for r in cur.fetchall():
    print(r)

print("\n=== US STOCK OPEN POSITIONS ===")
cur.execute("""
    SELECT p.symbol, p.quantity, p.average_cost, p.entry_price, p.current_price, 
           p.unrealized_pnl, p.unrealized_pnl_percent, p.position_side, p.notes,
           a.account_name, a.account_type
    FROM positions p 
    JOIN trade_accounts a ON p.account_id = a.id 
    WHERE p.is_closed = 0 AND a.account_type = 'us_stock'
    ORDER BY a.account_name, p.symbol
""")
rows = cur.fetchall()
for r in rows:
    for k, v in r.items():
        if hasattr(v, '__float__'):
            r[k] = float(v)
print(json.dumps(rows, indent=2, ensure_ascii=False, default=str))

conn.close()
