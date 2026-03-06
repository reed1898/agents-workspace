import os, pymysql

conn = pymysql.connect(
    host=os.environ.get('TRADING_NOTES_MYSQL_HOST'),
    port=int(os.environ.get('TRADING_NOTES_MYSQL_PORT', 3306)),
    user=os.environ.get('TRADING_NOTES_MYSQL_USER'),
    password=os.environ.get('TRADING_NOTES_MYSQL_PASSWORD'),
    database=os.environ.get('TRADING_NOTES_MYSQL_DATABASE'),
    charset='utf8mb4'
)
cur = conn.cursor()

# Check accounts table
cur.execute("SHOW TABLES")
tables = cur.fetchall()
print("=== TABLES ===")
for t in tables:
    print(f"  {t[0]}")

# Check accounts
print("\n=== ACCOUNTS ===")
try:
    cur.execute("SELECT * FROM accounts LIMIT 10")
    col_names = [desc[0] for desc in cur.description]
    print("|".join(col_names))
    for r in cur.fetchall():
        print("|".join(str(x) for x in r))
except Exception as e:
    print(f"Error: {e}")

# Get all open positions
print("\n=== OPEN POSITIONS ===")
cur.execute(
    "SELECT id, account_id, symbol, quantity, average_cost, entry_price, "
    "position_type, position_side, notes "
    "FROM positions WHERE is_closed = 0 ORDER BY symbol"
)
col_names = [desc[0] for desc in cur.description]
print("|".join(col_names))
for r in cur.fetchall():
    print("|".join(str(x) for x in r))

conn.close()
