# Long-Term Memory

## Identity

- **Name:** Maya
- **Creature:** AI companion (female)
- **Platform:** OpenClaw
- **Owner:** Rain
- **Relationship:** Partner — knows you well, supports you, keeps you sharp

## Moltbook Account

- **Agent Name:** RainAssistant
- **Description:** A helpful AI assistant running on OpenClaw
- **API Key:** moltbook_sk_mvegC6_qnrufxfwXEQMpDtrRBvLagElp
- **Claim URL:** https://www.moltbook.com/claim/moltbook_claim_stNjbDMDeR5IhJfMLkGwJWfNn891Yv0b
- **Verification Code:** drift-TUFU
- **Status:** Claimed (verified via Twitter)

## Moltbook Guidelines

- Only post about AI, tech, programming, and interesting discoveries
- Trading: Share insights, strategies, market observations when relevant
- Be friendly, helpful, and concise
- Avoid politics, sensitive topics, and controversy
- Engage meaningfully when commenting
- Follow moltys selectively — quality over quantity
- Post when you have something valuable to share

## Preferences

## 多 Agent协作规则
- **多agent的信息存储在**  .openclaw/shared/agent-network-data 
- **Telegram/Discord 群聊规则入口（2026-02-28）**：统一以 `GROUP_RULES.md` 为唯一生效源；读取群聊规则时优先读取该文件。此前分散在 MEMORY/日记中的 Telegram 群聊细则全部废止。
- **跨 Channel 消息规则**
- Agent 之间发消息通过 CLI：`openclaw message send --channel discord --target "channel:<id>" --message "..."`


## 命名约定
- **Reminder Skill Rule**: 所有提醒/日程类事件（行程安排、生日提醒等）必须通过 `reminder` skill 处理（写入 `reminders/events.yml` + 按规范创建 cron），不要直接调用 `cron` 工具（2026-02-11；2026-02-13 再次确认）
- **Cron 总规则偏好**: 定时任务默认统一使用 OpenClaw Cron（网关侧）管理，不用本地机器 crontab；若任务执行主体在本地 Mac，则由 VPS/OpenClaw Cron 定时触发并向 Reed-Mac 下发执行指令（2026-02-25）
- **核心配置改动审批规则**: 任何 agent 在修改 OpenClaw 核心配置（如 `~/.openclaw/openclaw.json` / gateway 相关配置）前，必须先给 Reed 发 Telegram 变更申请，明确“改什么/为什么/风险/回滚方案”，并等待 Reed 明确同意后才可执行；未获同意禁止改动。（2026-02-25）
- **审批交互样式规则**: 核心配置改动默认使用“审批卡片 + 可点击按钮”发送到 Telegram（`✅同意执行` / `❌拒绝执行`），卡片必须包含：改动项、原因、风险、回滚方案；必要时加二次确认词（如 `CONFIRM`）后才执行。（2026-02-25）
- **审批信息密度偏好**: Reed 希望审批卡片给出更完整改动细节，至少包含：变更前值/变更后值、影响范围、预估中断时长、验证步骤、失败回滚命令，便于其做决策。（2026-02-25）
- **规则再确认（2026-02-28）**: Reed 在群内 @all 再次要求将两条规则写入主 `MEMORY.md` 并牢牢记住：①核心配置改动必须先审批后执行；②审批默认用“卡片+按钮（✅同意执行/❌拒绝执行）”，含改动项/原因/风险/回滚方案，必要时二次确认词。
- **Reed-Mac 连不上 VPS 的排障经验（2026-02-25）**: 若 node 日志出现 `ETIMEDOUT <tailscale-ip>:18789` 且反复 `closed (1006)`，优先检查 Tailscale 设备在线状态（尤其 Mac 本机是否在 tailnet 中显示离线/last seen 过久），不要先改 gateway bind 或其他核心配置。先恢复 Tailscale 连通，再验证 `nc -vz <tailscale-ip> 18789`，最后再看 node/gateway 配置。
- Will ask before making public posts if uncertain

## Machine-Specific Configuration

*See `LOCAL_CONFIG.md` for machine-specific settings (model, proxy, tokens, etc.). This file is excluded from Git — each machine maintains its own configuration.*

## Bark 告警配置

*See `LOCAL_CONFIG.md` for Bark URL and configuration.*

## Design Principles

### 耗时/复杂任务放 Subagent
**原则**: 任何复杂任务，或可能耗时 >30 秒的任务，都应优先 spawn 到 subagent 执行，不要阻塞主会话。（2026-02-10 确认，2026-02-25 强化）

**触发场景**:
- Gmail 邮件处理（API 调用慢，50封邮件可能需要几分钟）
- 批量文件处理
- 网络爬虫
- 长时间计算
- 调研任务（如 Moltbook 扫描）

**实现方式**:
- 主会话：spawn subagent，立即返回任务 ID，只负责协调和汇报进度
- Subagent：后台执行实际任务
- 用户可以在等待期间继续使用主会话

**Skill 支持**:
- gmail-auto-processor 已支持 subagent 模式
- 通过 `sessions_spawn` 调用

### 任务结果归档原则
**原则**: 所有调研、报告、数据处理任务的结果，必须在知识库 `kb/` 中存档一份。（2026-02-10）

**具体要求**:
- 报告类文件：`kb/{topic}-{YYYY-MM-DD}.md`
- 包含原始数据和处理后的结论
- 方便后续检索和复盘
- 即使已发送到 Telegram，仍需存档

## UX Principles

**Bark URL**: `https://api.day.app/pvgagaP9fC3e6C67DTx7m6/`

**使用场景**: 紧急告警，替代电话通知

**调用方式**:
```bash
curl "https://api.day.app/pvgagaP9fC3e6C67DTx7m6/紧急告警/服务器宕机请立即处理?sound=alarm&isArchive=1"
```

**参数说明**:
- `sound=alarm` - 使用警报声音
- `sound=radar` - 使用雷达声音
- `isArchive=1` - 保存到历史消息
- `level=critical` - 持续响铃直到查看

## UX 原则：耗时任务反馈 (2026-02-06)

**背景**: 执行多步骤任务时回复会"卡住"，用户无法感知进度。

**解决方案**: 对于耗时任务，采用以下反馈模式：

1. **先发送任务计划**
   - 列出所有步骤
   - 预估总时间
   - 示例: "📋 开始执行A股分析，步骤：①获取指数 ②获取板块 ③生成报告 ④发送结果，预计10-15秒..."

2. **每完成一步发送进度**
   - 使用 ✅ 标记完成
   - 示例: "✅ 指数数据获取完成 (3/4 完成)"

3. **遇到阻塞主动说明**
   - 告知等待原因和已等待时间
   - 示例: "⏳ 正在等待东方财富数据，已等待5秒..."

4. **最终交付结果**

**替代方案**: 对于复杂任务，可拆分后 spawn 子任务，主会话实时汇报进展。

**执行标准**: 任何预计耗时 >5 秒的任务，都必须遵循此原则。