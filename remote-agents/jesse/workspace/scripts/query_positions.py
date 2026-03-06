#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, pymysql, urllib.request

host = os.environ["TRADING_NOTES_MYSQL_HOST"]
port = int(os.environ["TRADING_NOTES_MYSQL_PORT"])
db = os.environ["TRADING_NOTES_MYSQL_DATABASE"]
user = os.environ["TRADING_NOTES_MYSQL_USER"]
pwd = os.environ["TRADING_NOTES_MYSQL_PASSWORD"]

conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database=db, charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)

# List all tables
cur.execute("SHOW TABLES")
print("=== TABLES ===")
for row in cur.fetchall():
    print(list(row.values())[0])

# Check if there's an account_type column in positions
cur.execute("SHOW COLUMNS FROM positions LIKE 'account_type'")
has_account_type = cur.fetchone()
print(f"\nHas account_type in positions: {has_account_type is not None}")

# Get distinct account_ids for reference
cur.execute("SELECT DISTINCT account_id FROM positions WHERE is_closed=0")
print("\n=== DISTINCT ACCOUNT_IDS (open) ===")
for row in cur.fetchall():
    print(row['account_id'])

# Get all open positions - positions table has no account_type directly
# Let's check what we have
cur.execute("""
    SELECT id, symbol, quantity, average_cost, entry_price,
           current_price, unrealized_pnl, unrealized_pnl_percent,
           position_type, position_side, notes, holding_days,
           account_id
    FROM positions
    WHERE is_closed = 0
    ORDER BY account_id, symbol
""")
positions = cur.fetchall()
print(f"\n=== ALL OPEN POSITIONS ({len(positions)}) ===")
for p in positions:
    for k, v in p.items():
        if hasattr(v, 'as_integer_ratio'):
            p[k] = float(v)
    print(json.dumps(p, ensure_ascii=False, default=str))

cur.close()
conn.close()
