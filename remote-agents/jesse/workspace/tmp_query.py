import pymysql
conn = pymysql.connect(
    host='18.224.71.149', port=3308,
    user='trading', password='zIcyT=hj=C5',
    database='trading_notes', charset='utf8mb4'
)
cur = conn.cursor()

# trade_accounts schema
print("=== TRADE_ACCOUNTS COLUMNS ===")
cur.execute("DESCRIBE trade_accounts")
for c in cur.fetchall():
    print(c[0], c[1])

print("\n=== ALL TRADE_ACCOUNTS ===")
cur.execute("SELECT * FROM trade_accounts")
col_names = [d[0] for d in cur.description]
print("|".join(col_names))
for r in cur.fetchall():
    print("|".join(str(x) for x in r))

# Get open US stock positions
print("\n=== OPEN US STOCK POSITIONS ===")
cur.execute("""
    SELECT p.symbol, p.quantity, p.average_cost, p.current_price,
           p.unrealized_pnl, p.unrealized_pnl_percent, p.entry_price,
           p.holding_days, a.account_type, a.account_name
    FROM positions p
    JOIN trade_accounts a ON p.account_id = a.id
    WHERE p.is_closed = 0 AND a.account_type = 'us_stock'
""")
col_names = [d[0] for d in cur.description]
print("|".join(col_names))
for r in cur.fetchall():
    print("|".join(str(x) for x in r))

conn.close()
