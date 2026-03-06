$headers = @{ "Content-Type" = "application/json"; "Accept-Encoding" = "identity" }

# 1. Trending TOP10
$body1 = '{"rankType":10,"period":50,"sortBy":0,"page":1,"size":10}'
$r1 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list' -Method POST -Headers $headers -Body $body1
$r1 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_trending.json"

# 2. Smart Money Inflow SOL
$body2 = '{"chainId":"CT_501","period":"24h","tagType":2}'
$r2 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/tracker/wallet/token/inflow/rank/query' -Method POST -Headers $headers -Body $body2
$r2 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_inflow_sol.json"

# 3. Smart Money Inflow BSC
$body3 = '{"chainId":"56","period":"24h","tagType":2}'
$r3 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/tracker/wallet/token/inflow/rank/query' -Method POST -Headers $headers -Body $body3
$r3 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_inflow_bsc.json"

# 4. Smart Money Signal SOL
$body4 = '{"smartSignalType":"","page":1,"pageSize":10,"chainId":"CT_501"}'
$r4 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' -Method POST -Headers $headers -Body $body4
$r4 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_signal_sol.json"

# 5. Smart Money Signal BSC
$body5 = '{"smartSignalType":"","page":1,"pageSize":10,"chainId":"56"}'
$r5 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' -Method POST -Headers $headers -Body $body5
$r5 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_signal_bsc.json"

# 6. Meme new tokens
$body6 = '{"chainId":"CT_501","rankType":10,"limit":5}'
$r6 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list' -Method POST -Headers $headers -Body $body6
$r6 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_meme_new.json"

# 7. Meme migrating tokens
$body7 = '{"chainId":"CT_501","rankType":20,"limit":5}'
$r7 = Invoke-RestMethod -Uri 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list' -Method POST -Headers $headers -Body $body7
$r7 | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 "$PSScriptRoot\api_meme_migrate.json"

Write-Host "ALL_DONE"
