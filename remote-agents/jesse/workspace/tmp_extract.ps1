Write-Host "=== TRENDING TOP10 ==="
$j = Get-Content "$PSScriptRoot\api_trending.json" -Raw | ConvertFrom-Json
foreach ($t in $j.data.tokens) {
    Write-Host ("{0} | Price:{1} | 24h:{2}% | MCap:{3} | Vol24h:{4}" -f $t.symbol, $t.price, $t.percentChange24h, $t.marketCap, $t.volume24h)
}

Write-Host ""
Write-Host "=== SMART MONEY INFLOW SOL TOP10 ==="
$j2 = Get-Content "$PSScriptRoot\api_inflow_sol.json" -Raw | ConvertFrom-Json
$i = 0
foreach ($t in $j2.data) {
    if ($i -ge 10) { break }
    Write-Host ("{0} | SOL | Inflow:{1} | Price:{2} | 24h:{3}% | MCap:{4}" -f $t.tokenName, $t.inflow, $t.price, $t.priceChangeRate, $t.marketCap)
    $i++
}

Write-Host ""
Write-Host "=== SMART MONEY INFLOW BSC TOP10 ==="
$j3 = Get-Content "$PSScriptRoot\api_inflow_bsc.json" -Raw | ConvertFrom-Json
$i = 0
foreach ($t in $j3.data) {
    if ($i -ge 10) { break }
    Write-Host ("{0} | BSC | Inflow:{1} | Price:{2} | 24h:{3}% | MCap:{4}" -f $t.tokenName, $t.inflow, $t.price, $t.priceChangeRate, $t.marketCap)
    $i++
}

Write-Host ""
Write-Host "=== SIGNAL SOL ==="
$j4 = Get-Content "$PSScriptRoot\api_signal_sol.json" -Raw | ConvertFrom-Json
foreach ($t in $j4.data) {
    Write-Host ("{0} | {1} | Alert:{2} | Now:{3} | MaxGain:{4} | SM:{5} | Exit:{6}% | {7}" -f $t.ticker, $t.direction, $t.alertPrice, $t.currentPrice, $t.maxGain, $t.smartMoneyCount, $t.exitRate, $t.status)
}

Write-Host ""
Write-Host "=== SIGNAL BSC ==="
$j5 = Get-Content "$PSScriptRoot\api_signal_bsc.json" -Raw | ConvertFrom-Json
foreach ($t in $j5.data) {
    Write-Host ("{0} | {1} | Alert:{2} | Now:{3} | MaxGain:{4} | SM:{5} | Exit:{6}% | {7}" -f $t.ticker, $t.direction, $t.alertPrice, $t.currentPrice, $t.maxGain, $t.smartMoneyCount, $t.exitRate, $t.status)
}

Write-Host ""
Write-Host "=== MEME NEW ==="
$j6 = Get-Content "$PSScriptRoot\api_meme_new.json" -Raw | ConvertFrom-Json
foreach ($t in $j6.data) {
    Write-Host ("{0} | Price:{1} | MCap:{2} | Progress:{3}% | Holders:{4} | DevSell:{5}%" -f $t.symbol, $t.price, $t.marketCap, $t.progress, $t.holders, $t.devSellPercent)
}

Write-Host ""
Write-Host "=== MEME MIGRATE ==="
$j7 = Get-Content "$PSScriptRoot\api_meme_migrate.json" -Raw | ConvertFrom-Json
foreach ($t in $j7.data) {
    Write-Host ("{0} | Price:{1} | MCap:{2} | Progress:{3}% | Holders:{4} | DevSell:{5}%" -f $t.symbol, $t.price, $t.marketCap, $t.progress, $t.holders, $t.devSellPercent)
}
