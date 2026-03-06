$ErrorActionPreference = 'Stop'

try {
  $status = & openclaw gateway status 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0 -or $status -match 'offline|stopped|disconnected|error') {
    & openclaw gateway restart | Out-Null
  }
} catch {
  try { & openclaw gateway restart | Out-Null } catch {}
}
