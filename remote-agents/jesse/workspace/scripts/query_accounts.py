#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, pymysql

host = os.environ["TRADING_NOTES_MYSQL_HOST"]
port = int(os.environ["TRADING_NOTES_MYSQL_PORT"])
db = os.environ["TRADING_NOTES_MYSQL_DATABASE"]
user = os.environ["TRADING_NOTES_MYSQL_USER"]
pwd = os.environ["TRADING_NOTES_MYSQL_PASSWORD"]

conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database=db, charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)

cur.execute("DESCRIBE trade_accounts")
print("=== TRADE_ACCOUNTS SCHEMA ===")
for row in cur.fetchall():
    print(f"  {row['Field']}: {row['Type']}")

cur.execute("SELECT * FROM trade_accounts")
print("\n=== ALL TRADE_ACCOUNTS ===")
for a in cur.fetchall():
    for k, v in a.items():
        if hasattr(v, 'as_integer_ratio'):
            a[k] = float(v)
    print(json.dumps(a, ensure_ascii=False, default=str))

cur.close()
conn.close()
