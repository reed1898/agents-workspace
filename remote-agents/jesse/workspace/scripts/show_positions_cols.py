import pymysql
conn=pymysql.connect(host='18.224.71.149',port=3308,user='trading',password='zIcyT=hj=C5',database='trading_notes',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
cur=conn.cursor();cur.execute('SHOW COLUMNS FROM positions')
print([r['Field'] for r in cur.fetchall()])
cur.close();conn.close()
