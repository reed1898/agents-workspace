import urllib.request, json, ssl, sys

sys.stdout.reconfigure(encoding='utf-8')

symbols_sh = ['600118','600877','601698','688048','688102','600105','600633','600763','603778','603919','688568']
symbols_sz = ['002050','300065','000547','000592','002291','002410','002606','002809','300077','300136','300170','300433','300442','300762']

codes = []
for s in symbols_sh:
    codes.append('sh' + s)
for s in symbols_sz:
    codes.append('sz' + s)

url = 'https://hq.sinajs.cn/list=' + ','.join(codes)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn'
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('gbk')

for line in raw.strip().split('\n'):
    line = line.strip()
    if not line or '=' not in line:
        continue
    var_part, data_part = line.split('=', 1)
    code = var_part.split('_')[-1]
    data = data_part.strip('"').strip(';').strip('"')
    fields = data.split(',')
    if len(fields) > 1:
        name = fields[0]
        print(f"{code} -> {name}")
