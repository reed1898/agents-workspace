$ErrorActionPreference = 'Stop'

$stateDir = Join-Path $HOME '.openclaw'
$logDir = Join-Path $stateDir 'logs'
$logFile = Join-Path $logDir 'gateway-watchdog.log'
$stateFile = Join-Path $stateDir 'gateway-watchdog.state.json'
$configPath = Join-Path $stateDir 'openclaw.json'
$gatewayCmdPath = Join-Path $stateDir 'gateway.cmd'
$port = 18789
$alertThreshold = 3
$alertCooldownMinutes = 30

if (-not (Test-Path $logDir)) {
  New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-WatchdogLog {
  param([string]$Message)
  $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  Add-Content -Path $logFile -Value "[$ts] $Message"
}

function Load-WatchdogState {
  if (-not (Test-Path $stateFile)) {
    return @{
      failCount = 0
      lastFailureAt = $null
      lastAlertAt = $null
    }
  }
  try {
    $rawState = Get-Content $stateFile -Raw | ConvertFrom-Json
    return @{
      failCount = if ($null -ne $rawState.failCount) { [int]$rawState.failCount } else { 0 }
      lastFailureAt = if ($null -ne $rawState.lastFailureAt) { [string]$rawState.lastFailureAt } else { $null }
      lastAlertAt = if ($null -ne $rawState.lastAlertAt) { [string]$rawState.lastAlertAt } else { $null }
    }
  }
  catch {
    Write-WatchdogLog "State file is invalid, resetting: $($_.Exception.Message)"
    return @{
      failCount = 0
      lastFailureAt = $null
      lastAlertAt = $null
    }
  }
}

function Save-WatchdogState {
  param([hashtable]$State)
  ($State | ConvertTo-Json -Depth 5) | Set-Content -Path $stateFile -Encoding UTF8
}

function Get-TelegramAlertTarget {
  if (-not (Test-Path $configPath)) {
    return $null
  }
  try {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $botToken = $config.channels.telegram.botToken
    $chatId = $config.channels.telegram.allowFrom[0]
    if ([string]::IsNullOrWhiteSpace($botToken) -or [string]::IsNullOrWhiteSpace([string]$chatId)) {
      return $null
    }
    return @{
      botToken = $botToken
      chatId = [string]$chatId
    }
  }
  catch {
    Write-WatchdogLog "Failed to read Telegram target from config: $($_.Exception.Message)"
    return $null
  }
}

function Send-TelegramAlert {
  param([string]$Message)
  $target = Get-TelegramAlertTarget
  if ($null -eq $target) {
    Write-WatchdogLog "Telegram alert target not configured; skipping alert."
    return $false
  }
  try {
    $uri = "https://api.telegram.org/bot$($target.botToken)/sendMessage"
    $body = @{
      chat_id = $target.chatId
      text = $Message
      disable_web_page_preview = $true
    }
    Invoke-RestMethod -Method Post -Uri $uri -Body $body -TimeoutSec 15 | Out-Null
    Write-WatchdogLog "Telegram alert sent."
    return $true
  }
  catch {
    Write-WatchdogLog "Telegram alert failed: $($_.Exception.Message)"
    return $false
  }
}

function Register-Failure {
  param([hashtable]$State, [string]$Reason)
  $State.failCount = [int]$State.failCount + 1
  $State.lastFailureAt = (Get-Date).ToString('o')
  Write-WatchdogLog "Failure #$($State.failCount): $Reason"

  if ([int]$State.failCount -ge $alertThreshold) {
    $now = Get-Date
    $canAlert = $true
    if ($State.lastAlertAt) {
      try {
        $lastAlert = [datetime]$State.lastAlertAt
        if (($now - $lastAlert).TotalMinutes -lt $alertCooldownMinutes) {
          $canAlert = $false
        }
      }
      catch {
        $canAlert = $true
      }
    }

    if ($canAlert) {
      $msg = "OpenClaw gateway watchdog warning: restart check failed $($State.failCount) times. Last reason: $Reason"
      if (Send-TelegramAlert -Message $msg) {
        $State.lastAlertAt = $now.ToString('o')
      }
    }
  }
}

function Reset-FailureState {
  param([hashtable]$State)
  if ([int]$State.failCount -gt 0) {
    Write-WatchdogLog "Gateway recovered after $($State.failCount) failure(s)."
  }
  $State.failCount = 0
  $State.lastFailureAt = $null
}

try {
  $state = Load-WatchdogState
  $conn = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort $port -State Listen -ErrorAction SilentlyContinue
  if ($null -eq $conn) {
    Write-WatchdogLog "Gateway not listening on 127.0.0.1:$port, attempting start."
    openclaw gateway start *> $null
    Start-Sleep -Seconds 3
    $quickCheck = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($null -eq $quickCheck -and (Test-Path $gatewayCmdPath)) {
      Write-WatchdogLog "Gateway still down after service start; launching gateway.cmd fallback."
      Start-Process -FilePath $gatewayCmdPath -WorkingDirectory $stateDir -WindowStyle Hidden | Out-Null
    }
    $isListening = $false
    foreach ($i in 1..30) {
      Start-Sleep -Seconds 1
      $after = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort $port -State Listen -ErrorAction SilentlyContinue
      if ($null -ne $after) {
        $isListening = $true
        break
      }
    }
    if (-not $isListening) {
      Write-WatchdogLog "Start attempt finished but port $port is still down after 30s."
      Register-Failure -State $state -Reason "Port $port still down after start attempt"
      Save-WatchdogState -State $state
      exit 1
    }
    Write-WatchdogLog "Gateway started successfully."
    Reset-FailureState -State $state
    Save-WatchdogState -State $state
  }
  else {
    Reset-FailureState -State $state
    Save-WatchdogState -State $state
  }
}
catch {
  Write-WatchdogLog "Watchdog error: $($_.Exception.Message)"
  $state = Load-WatchdogState
  Register-Failure -State $state -Reason $_.Exception.Message
  Save-WatchdogState -State $state
  exit 1
}
