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

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Trading DB (Reed)

> Never store plaintext secrets in workspace files. Use OS environment variables.

### Required ENV keys (namespaced)

- `TRADING_NOTES_DATABASE_URL`
  - Full SQLAlchemy-style DSN for this specific DB.
  - Format: `mysql+pymysql://<user>:<password>@<host>:<port>/<database>`
- `TRADING_NOTES_MYSQL_HOST`
  - MySQL host/IP.
- `TRADING_NOTES_MYSQL_PORT`
  - MySQL port (string), e.g. `3306` or custom port.
- `TRADING_NOTES_MYSQL_DATABASE`
  - Database name (current: `trading_notes`).
- `TRADING_NOTES_MYSQL_USER`
  - DB username.
- `TRADING_NOTES_MYSQL_PASSWORD`
  - DB password.

### Usage rule

- For any “我的持仓情况 / 持仓追踪 / 盘后持仓表现” request, query DB first from these namespaced ENV keys, then summarize.
- Generic keys (`DATABASE_URL`, `MYSQL_*`) are deprecated and should stay unset to avoid collisions with other databases.
- If required ENV keys are missing, report missing key names explicitly and request refresh once.

## Git Operations
- 本机没有 gh CLI，不要尝试。直接用 git 命令操作（merge/push/rebase）。
- KB 合并流程：git checkout main → pull → merge agent/jesse → push → checkout agent/jesse → rebase main。

Add whatever helps you do your job. This is your cheat sheet.
