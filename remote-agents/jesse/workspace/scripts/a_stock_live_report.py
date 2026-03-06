import pymysql
from urllib.request import urlopen
from decimal import Decimal

conn=pymysql.connect(host='18.224.71.149',port=3308,user='trading',password='zIcyT=hj=C5',database='trading_notes',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
cur=conn.cursor()
cur.execute('''
SELECT ta.account_name, p.symbol, p.quantity, p.average_cost
FROM positions p
LEFT JOIN trade_accounts ta ON ta.id=p.account_id
WHERE IFNULL(p.is_closed,0)=0 AND ta.account_type='a_stock'
ORDER BY p.symbol
''')
rows=cur.fetchall()
cur.close(); conn.close()

symbols=[r['symbol'] for r in rows if r.get('symbol')]

# to tencent codes
codes=[]
map_code={}
for s in symbols:
    ss=s.upper()
    if ss.endswith('.SH'):
        c='sh'+ss.split('.')[0]
    elif ss.endswith('.SZ'):
        c='sz'+ss.split('.')[0]
    else:
        continue
    codes.append(c)
    map_code[c]=ss

quotes={}
for i in range(0,len(codes),40):
    batch=codes[i:i+40]
    if not batch: continue
    url='https://qt.gtimg.cn/q='+','.join(batch)
    txt=urlopen(url,timeout=8).read().decode('gbk','ignore')
    for line in txt.strip().split('\n'):
        if '="' not in line: continue
        left,right=line.split('="',1)
        code=left.replace('v_','').strip()
        body=right.rstrip('";')
        parts=body.split('~')
        if len(parts)<6: continue
        name=parts[1]
        sym=parts[2]
        try:
            price=float(parts[3])
            # full quote uses index 31/32 for change and pct
            chg=float(parts[31]) if len(parts)>32 else float(parts[4])
            pct=float(parts[32]) if len(parts)>32 else float(parts[5])
        except:
            continue
        quotes[map_code.get(code, sym)]={'name':name,'price':price,'chg':chg,'pct':pct}

out=[]
for r in rows:
    s=r['symbol'].upper()
    q=quotes.get(s)
    if not q: continue
    qty=float(r.get('quantity') or 0)
    cost=float(r.get('average_cost') or 0)
    mv=qty*q['price']
    upnl=(q['price']-cost)*qty if qty and cost else None
    out.append({
        'symbol':s,'name':q['name'],'pct':q['pct'],'price':q['price'],
        'qty':qty,'cost':cost,'mv':mv,'upnl':upnl
    })

out_sorted=sorted(out,key=lambda x:x['pct'],reverse=True)
print('COUNT',len(out_sorted))
print('TOP_UP')
for r in out_sorted[:5]:
    print(r)
print('TOP_DOWN')
for r in out_sorted[-5:]:
    print(r)

# weighted avg change by market value
total_mv=sum(r['mv'] for r in out_sorted)
if total_mv>0:
    wchg=sum(r['mv']*r['pct'] for r in out_sorted)/total_mv
    print('WEIGHTED_PCT',round(wchg,3))
else:
    print('WEIGHTED_PCT',None)

# aggregate pnl vs cost
pnls=[r['upnl'] for r in out_sorted if r['upnl'] is not None]
print('TOTAL_UPNL', round(sum(pnls),2) if pnls else None)
