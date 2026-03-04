# 🔒 安全扫描报告 — 2026-03-03 早晨

**扫描时间:** 2026-03-03 11:21 (Asia/Shanghai)  
**扫描类型:** 定时晨检  
**整体状态:** ⚠️ 发现 1 个中级问题（已自动修复） + 2 个 OpenClaw 内置警告

---

## 📊 总览

| 严重级别 | 数量 | 状态 |
|---------|------|------|
| 🔴 高危 | 0 | — |
| 🟡 中危 | 1 | ✅ 已自动修复 |
| 🔵 低危/信息 | 3 | ⚠️ 需人工确认 |

---

## 🔴 高危问题

**无高危问题。**

---

## 🟡 中危问题

### 1. 敏感配置备份文件权限过宽（已修复）

- **发现:** 以下 3 个备份文件权限为 `rw-r--r--`（644），可被同机其他用户读取：
  - `openclaw.json.bak`
  - `openclaw.json.bak.pre_doctor_fix_20260303_001145`
  - `openclaw.json.pre_fix_20260302_214248.bak`
- **风险:** 这些文件包含 bot tokens、API keys 等敏感信息，644 权限在多用户系统上存在泄漏风险。
- **修复动作:** ✅ 已自动 `chmod 600` 修复，所有备份文件现均为 `rw-------`（仅 owner 可读）

---

## 🔵 低危 / 信息

### 2. OpenClaw 内置警告：多用户访问风险

- **来源:** `openclaw status` 安全审计
- **详情:** 检测到 Discord 配置了 `groupPolicy="allowlist"`，系统认为可能存在多用户共享 gateway 场景
- **建议:** 若为单人使用，无需处理；若为多用户共享，需隔离 gateway 和凭证
- **当前状态:** Gateway 绑定在 `127.0.0.1:18789`（loopback），无外网暴露风险

### 3. OpenClaw 内置警告：Discord slash commands 无 allowlist

- **来源:** `openclaw status` 安全审计
- **详情:** Discord slash commands 已启用，但未配置用户白名单，外部用户可能调用 `/` 命令
- **建议:** 在 `channels.discord.allowFrom` 中添加自己的用户 ID，或配置 guild 级用户白名单

### 4. OpenClaw 版本更新可用

- **当前版本:** 运行中
- **可用版本:** `2026.3.1`（npm）
- **建议:** 运行 `openclaw update` 更新至最新版（可能包含安全修复）

---

## ✅ 安全检查项（通过）

| 检查项 | 结果 |
|-------|------|
| Gateway 绑定地址 | ✅ `127.0.0.1` loopback，无外网暴露 |
| Gateway 端口 | ✅ 18789，仅本地监听 |
| Gateway 认证 | ✅ Auth token 已配置 |
| HTTPS | ℹ️ 未启用（本地使用，可接受） |
| openclaw.json 主文件权限 | ✅ `rw-------` (600) |
| 凭证目录权限 | ✅ `rwx------` (700) |
| ~/.openclaw 目录权限 | ✅ `rwx------` (700) |
| .env 文件泄漏 | ✅ 无 .env 文件暴露 |
| Skills 目录异常文件 | ✅ 无异常可执行文件 |
| Cron 任务异常新增 | ✅ 共 6 个任务，均为已知任务 |
| Tailscale | ℹ️ 未启用 |

---

## 📋 Cron 任务清单（6个，均正常）

| 名称 | 计划 | 状态 |
|------|------|------|
| agent-network-sync | 每 4 小时 | ✅ 启用 |
| daily-agent-summary | 每天 02:00 | ✅ 启用 |
| skill-discovery | 03:00-07:00 | ❌ 已禁用 |
| daily-report | 每天 08:15 | ✅ 启用 |
| security-scan-morning | 每天 07:00 | ✅ 启用（本次任务） |
| security-scan-evening | 每天 21:20 | ✅ 启用 |

---

## 🔧 自动修复记录

```
[11:21] chmod 600 ~/.openclaw/openclaw.json.bak
[11:21] chmod 600 ~/.openclaw/openclaw.json.bak.pre_doctor_fix_20260303_001145
[11:21] chmod 600 ~/.openclaw/openclaw.json.pre_fix_20260302_214248.bak
```

---

## 💡 建议行动

1. **更新 OpenClaw** → `openclaw update`（版本 2026.3.1 可用）
2. **Discord 白名单** → 在配置中添加自己的 Discord 用户 ID
3. **定期清理备份文件** → `.bak` 文件积累较多（9个），建议保留最近 2-3 个

---

*报告由安全扫描 cron 任务自动生成 | 下次扫描: 今晚 21:20*
