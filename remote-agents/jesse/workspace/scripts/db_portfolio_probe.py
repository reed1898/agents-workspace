import pymysql, json

conn = pymysql.connect(
    host='18.224.71.149',
    port=3308,
    user='trading',
    password='zIcyT=hj=C5',
    database='trading_notes',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=10,
    read_timeout=20,
    write_timeout=20,
)
cur = conn.cursor()

cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY table_name
""")
rows = cur.fetchall()
all_tables = [list(r.values())[0] for r in rows]

keywords = ['position', 'holding', 'portfolio', 'asset', 'balance', 'account', 'crypto', 'stock', 'equity']
candidates = [t for t in all_tables if any(k in t.lower() for k in keywords)]
if not candidates:
    candidates = all_tables

print('TABLES', json.dumps(candidates, ensure_ascii=False))

for t in candidates[:20]:
    try:
        cur.execute(f"SELECT COUNT(*) c FROM `{t}`")
        c = cur.fetchone()['c']
        print('COUNT', t, c)
    except Exception as e:
        print('COUNT_ERR', t, str(e))

for t in candidates[:12]:
    cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name=%s
    ORDER BY ordinal_position
    """, (t,))
    cols = cur.fetchall()
    print('COLS', t, json.dumps(cols, ensure_ascii=False))

likely = [t for t in candidates if any(k in t.lower() for k in ['position', 'holding', 'portfolio'])]
for t in likely[:8]:
    cur.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name=%s
    """, (t,))
    cols = [r['column_name'] for r in cur.fetchall()]
    order_col = None
    for c in ['updated_at', 'as_of', 'date', 'created_at', 'timestamp', 'id']:
        if c in cols:
            order_col = c
            break
    q = f"SELECT * FROM `{t}`"
    if order_col:
        q += f" ORDER BY `{order_col}` DESC"
    q += " LIMIT 5"
    try:
        cur.execute(q)
        rows = cur.fetchall()
        print('SAMPLE', t, json.dumps(rows, ensure_ascii=False, default=str))
    except Exception as e:
        print('SAMPLE_ERR', t, str(e))

cur.close()
conn.close()
