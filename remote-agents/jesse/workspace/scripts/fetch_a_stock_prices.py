import urllib.request, json, ssl

symbols = [
    '002050','300065','600118','600877','601698','688048','688102',
    '000547','000592','002291','002410','002606','002809','300077',
    '300136','300170','300433','300442','300762','600105','600633',
    '600763','603778','603919','688568'
]

# Use Tencent stock API
def to_tencent(code):
    c = code
    if c.startswith('6') or c.startswith('5') or c.startswith('9'):
        return 'sh' + c
    else:
        return 'sz' + c

tencent_codes = ','.join([to_tencent(s) for s in symbols])
url = f'https://qt.gtimg.cn/q={tencent_codes}'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('gbk')

for line in raw.strip().split('\n'):
    line = line.strip()
    if not line or '=' not in line:
        continue
    # format: v_shXXXXXX="1~name~code~price~yesterday_close~open~..."
    parts = line.split('=')
    if len(parts) < 2:
        continue
    data = parts[1].strip('"').strip(';').strip('"')
    fields = data.split('~')
    if len(fields) < 50:
        continue
    name = fields[1]
    code = fields[2]
    price = fields[3]       # latest
    yesterday = fields[4]   # yesterday close
    open_p = fields[5]
    high = fields[33] if len(fields) > 33 else fields[3]
    low = fields[34] if len(fields) > 34 else fields[3]
    volume = fields[6]      # volume (hands)
    turnover = fields[37] if len(fields) > 37 else '-'
    chg = fields[31] if len(fields) > 31 else '-'         # change amount
    chg_pct = fields[32] if len(fields) > 32 else '-'     # change %
    high = fields[33] if len(fields) > 33 else '-'
    low = fields[34] if len(fields) > 34 else '-'
    
    print(f"{code} | {name} | close={price} | chg={chg_pct}% | yesterday={yesterday} | open={open_p} | high={high} | low={low}")
