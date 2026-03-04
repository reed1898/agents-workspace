@echo off
rem OpenClaw Gateway (v2026.2.26)
set "TMPDIR=C:\Users\RainH\AppData\Local\Temp"
set "PATH=C:\Python314\Scripts\;C:\Python314\;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Program Files\dotnet\;C:\Program Files\nodejs\;C:\ProgramData\chocolatey\bin;C:\Program Files\Git\cmd;C:\Users\RainH\AppData\Local\Microsoft\WindowsApps;C:\Users\RainH\AppData\Roaming\npm;C:\Users\RainH\AppData\Local\Programs\Microsoft VS Code\bin"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_GATEWAY_TOKEN=548aa4ea1abd9e2fed013328099742d89095138d568f3b64"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.2.26"
"C:\Program Files\nodejs\node.exe" C:\Users\RainH\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789
