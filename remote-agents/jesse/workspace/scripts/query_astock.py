import pymysql, os, json

url = os.environ.get('TRADING_NOTES_DATABASE_URL') or os.environ.get('TRADING_NOTES_DATABASE_URL', '')
if not url:
    # Try user-level env
    import subprocess
    result = subprocess.run(
        ['powershell', '-Command', "[System.Environment]::GetEnvironmentVariable('TRADING_NOTES_DATABASE_URL','User')"],
        capture_output=True, text=True
    )
    url = result.stdout.strip()

if not url:
    print(json.dumps({"error": "TRADING_NOTES_DATABASE_URL not set"}))
    exit(1)

# Parse: mysql+pymysql://user:pass@host:port/database
url = url.replace('mysql+pymysql://', '')
userpass, hostdb = url.split('@', 1)
user, password = userpass.split(':', 1)
hostport, database = hostdb.split('/', 1)
host, port = hostport.split(':', 1)

conn = pymysql.connect(
    host=host, port=int(port), user=user, password=password,
    database=database, charset='utf8mb4'
)
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute("""
    SELECT p.id, p.symbol, p.quantity, p.average_cost, p.current_price,
           p.unrealized_pnl, p.unrealized_pnl_percent, p.entry_price,
           p.holding_days, p.notes,
           a.account_name, a.account_type, a.broker
    FROM positions p
    JOIN trade_accounts a ON p.account_id = a.id
    WHERE p.is_closed = 0 AND a.account_type = 'a_stock'
""")
rows = cur.fetchall()
print(json.dumps(rows, default=str, ensure_ascii=False))
conn.close()
