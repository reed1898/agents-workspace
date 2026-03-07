# Agent Fleet Dashboard 需求说明（v1）

## 0. 目标

为现有 4 个 OpenClaw agents 建一个统一 Dashboard，集中查看：

1) Agent 在线状态  
2) 心跳（heartbeat）配置与最近执行  
3) Cron 任务状态（next run / last run / failures）  
4) 关键运行信息（版本、模型、最近错误）  
5) 最近事件流（上线/离线/异常/恢复）

> 约束：以 `~/.openclaw/shared/agent-network-data` 作为统一状态源（Git-backed）。

---

## 1. 非目标（v1 不做）

- 不做远程控制（不在 dashboard 上直接启停 agent/cron）
- 不做复杂权限系统（先只读 + 简单 token）
- 不做历史大盘分析（先保留最近 N 条事件）
- 不接入数据库（先用 Git + JSON 文件）

---

## 2. 总体架构

### 2.1 数据流（推荐）

- 每个 agent 本地跑一个 `collector`（1~5 分钟）
- collector 采集本机状态 → 写入共享仓库 JSON
- `git pull --rebase && commit && push`
- Dashboard 服务只读共享仓库并渲染

### 2.2 信号分层

- **实时事件**：Discord（广播）
- **可追溯状态**：agent-network-data（落盘）
- Dashboard 以落盘为准，必要时显示“最后同步时间”

---

## 3. 目录与数据规范（必须）

共享仓库：`~/.openclaw/shared/agent-network-data`

```txt
registry/
  agent-registry.json
state/
  heartbeats/
    <agent_id>.json
  crons/
    <agent_id>.json
  runtime/
    <agent_id>.json
events/
  events.jsonl
meta/
  schema-version.json
```

### 3.1 `registry/agent-registry.json`
每个 agent 静态信息（已有则复用）：
- `agent_id`（唯一）
- `name`
- `role`
- `gateway`
- `node`
- `discord_user_id`
- `discord_channel_id`
- `enabled` (bool)

### 3.2 `state/heartbeats/<agent_id>.json`
```json
{
  "agent_id": "maya",
  "heartbeat_enabled": true,
  "heartbeat_interval_sec": 3600,
  "last_heartbeat_at": "2026-03-07T04:00:00Z",
  "last_check_items": ["email", "calendar"],
  "heartbeat_file_hash": "sha256:...",
  "updated_at": "2026-03-07T04:01:02Z"
}
```

### 3.3 `state/crons/<agent_id>.json`
```json
{
  "agent_id": "maya",
  "jobs": [
    {
      "job_id": "cron_xxx",
      "name": "moltbook-check",
      "schedule": "*/15 * * * *",
      "next_run_at": "2026-03-07T04:15:00Z",
      "last_run_at": "2026-03-07T04:00:05Z",
      "last_status": "ok",
      "consecutive_failures": 0,
      "last_error": null
    }
  ],
  "updated_at": "2026-03-07T04:01:05Z"
}
```

### 3.4 `state/runtime/<agent_id>.json`
```json
{
  "agent_id": "maya",
  "openclaw_version": "2026.3.2",
  "model_default": "openai-codex/gpt-5.3-codex",
  "sessions_active": 3,
  "last_error_summary": null,
  "host": "ip-172-31-21-161",
  "updated_at": "2026-03-07T04:01:06Z"
}
```

### 3.5 `events/events.jsonl`
每行一个事件：
```json
{"ts":"2026-03-07T04:00:05Z","agent_id":"maya","type":"HEARTBEAT_OK","level":"info","msg":"heartbeat completed"}
{"ts":"2026-03-07T04:02:10Z","agent_id":"linus","type":"CRON_FAIL","level":"warn","msg":"job x failed: timeout"}
```

---

## 4. Dashboard 功能需求（v1）

### 4.1 总览页（Fleet Overview）
- 4 个 agent 卡片
- 每卡显示：
  - online/offline（按 `last_seen` 推断）
  - last_seen 距今
  - 心跳间隔与最近心跳
  - cron 异常数（last_status=fail）
  - 最近错误摘要

状态色：
- 绿：健康
- 黄：有 warn（如 heartbeat 延迟）
- 红：离线或 cron 连续失败>=3

### 4.2 Agent 详情页
- Tabs:
  1) Heartbeat
  2) Crons
  3) Runtime
  4) Events(仅该 agent)

### 4.3 事件流页
- 最近 50/200 条
- 按 type/agent/level 过滤
- 支持复制原始 JSON

### 4.4 健康规则（内置）
- `last_seen > 10min` => offline warn
- `heartbeat overdue > 2 * interval` => heartbeat warn
- `consecutive_failures >= 3` => cron critical

---

## 5. 技术实现要求

### 5.1 前端/后端栈
- Next.js 14+（App Router）
- TypeScript
- UI: shadcn/ui + Tailwind
- 图表：Recharts（可选）
- 数据读取：Server-side 直接读本地克隆目录（Vercel 用 API 拉取）

### 5.2 数据获取模式（两种二选一）
A. **本地部署模式**：dashboard 与 shared repo 同机，直接读文件。  
B. **Vercel 模式（推荐给 Linus）**：
- 用 GitHub API 读取 JSON 文件内容（PAT 只读）
- 或定时同步到 `public/cache/*.json`（ISR）

### 5.3 安全
- 只读 token
- 环境变量管理：
  - `GITHUB_TOKEN`
  - `GITHUB_REPO`
  - `GITHUB_BRANCH`
- 不在前端暴露 token
- 页面可加简单访问密码（basic auth 或 middleware token）

---

## 6. Collector（每个 agent 本地）

脚本职责：
1. 执行 `openclaw status` 解析 heartbeat/版本/sessions  
2. 读取本地 heartbeat 执行状态文件（如 `memory/heartbeat-state.json`）  
3. 汇总 cron 任务状态（来自本地已知任务源）  
4. 写对应 `state/.../<agent_id>.json`  
5. 追加 `events.jsonl`（可选）  
6. push 到 shared repo

运行方式：
- OpenClaw cron 每 2 分钟执行一次 collector

---

## 7. 可观测性与告警（v1）

- Dashboard 顶部显示：
  - 数据更新时间
  - 数据是否 staled（>5 分钟未更新）
- 告警输出（先做 webhook stub）：
  - 规则触发时写事件；后续可接 Telegram

---

## 8. 验收标准（DoD）

1) 能看到 4 个 agent 卡片，状态正确  
2) 每个 agent 可查看 heartbeat / crons / runtime 明细  
3) 事件流可过滤并显示最近 50 条  
4) 任意 agent 停止上报 10 分钟后显示 offline  
5) cron 连续失败 3 次显示红色 critical  
6) Vercel 可部署，环境变量配置后可访问  
7) README 写清部署、配置、故障排查

---

## 9. 交付物清单

- `apps/agent-dashboard/`（Next.js 项目）
- `collectors/openclaw-state-collector/`（Node/Python 均可）
- `schemas/*.schema.json`（状态文件 schema）
- `docs/DEPLOY_VERCEL.md`
- `docs/OPERATIONS.md`
- 示例 `.env.example`

---

## 10. 里程碑（建议）

- M1（0.5天）：schema + mock 数据 + 总览页
- M2（0.5天）：详情页 + 事件流 + 健康规则
- M3（0.5天）：collector 接真数据 + push 流程
- M4（0.5天）：Vercel 部署 + README + 验收
