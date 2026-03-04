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

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
