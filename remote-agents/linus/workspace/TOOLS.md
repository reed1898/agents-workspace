# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

### Cloudflare 使用约束（必须遵守）
- **永远不要批量操作超过免费层限额**
- R2: 单次上传不超过 100 个对象，总存储不超过 5GB（给 10GB 留余量）
- Workers: 不部署高频轮询或无限循环的 Worker
- D1: 批量写入前先估算行数，不超过 5万行/次
- Workers AI: 生图/推理按需调用，不搞批量循环
- **每次操作前检查当前用量**：`wrangler r2 bucket list` 等
- 有疑问先问 Reed，不要自作主张搞大规模操作

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

Add whatever helps you do your job. This is your cheat sheet.
