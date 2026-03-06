#!/bin/bash
# Trading Notes 环境变量模板
# 填入真实值后 source 或加到 ~/.zshrc

# ── 必填 ──
export TRADING_NOTES_DATABASE_URL="postgresql://user:pass@host:5432/trading_notes"
export TRADING_NOTES_ENCRYPTION_KEY="<Fernet base64 key>"
export TRADING_NOTES_SECRET_KEY="<64 char hex string>"

# ── Gmail 同步（国泰海通）需要 ──
export GOOGLE_GMAIL_CLIENT_ID="<your-google-client-id>.apps.googleusercontent.com"
export GOOGLE_GMAIL_CLIENT_SECRET="<your-google-client-secret>"

# ── 代理（如果需要访问境外 API）──
# export HTTPS_PROXY=socks5://127.0.0.1:10023
# export HTTP_PROXY=socks5://127.0.0.1:10023
