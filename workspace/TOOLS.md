# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## STT (语音转文字)

- **默认使用**: volcengine-stt (火山引擎)
- **脚本路径**: `~/.openclaw/workspace/skills/volcengine-stt/scripts/transcribe.sh`
- **配置位置**: `openclaw.json` → `skills.entries["volcengine-stt"]`
- **注意**: macOS 上已修复 base64 兼容性问题（用 `base64 -i` 替代 `base64 -w 0`）

## 代理 (VPN)

- **软件**: QuickQ
- **端口不固定**，每次需用 `lsof | grep quickqser` 检测
- **用途**: 访问被墙的服务（Google API、GitHub 等）
- **注意**: gws 等 CLI 工具需要手动设置 `https_proxy`/`http_proxy`，不会自动走系统代理
- **gws-proxy.sh 已内置自动检测逻辑**

## GWS (Google Workspace CLI)

- **认证方式**: OAuth2 手动 token + refresh_token
- **credentials**: `~/Library/Application Support/gws/credentials.json`
- **client_secret**: `~/.openclaw/config/gws/` → 软链接到 `~/Library/Application Support/gws/client_secret.json`
- **包装脚本**: `~/.openclaw/workspace/scripts/gws-proxy.sh`（自动带代理 + token 刷新）
- **Gmail 账号**: fishwarter@gmail.com
- **已授权 scope**: `https://mail.google.com/`

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
