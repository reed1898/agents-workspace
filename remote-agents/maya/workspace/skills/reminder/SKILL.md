---
name: reminder
summary: Natural-language reminders → save to your workspace → schedule Telegram+Discord notifications (24h/1h/10m by default).
description: Natural-language reminder secretary: capture events into git-synced workspace (data/logic separated), schedule reminder notifications via OpenClaw cron (Telegram+Discord), and answer "what's coming up" queries. Use when user mentions meetings, birthdays, deadlines, or asks for schedule/plans.
tags: [reminder, schedule, cron, telegram, discord, secretary]
---

# Reminder (secretary)

A lightweight personal secretary for OpenClaw:
- Tell it events in natural language (Chinese/English).
- It extracts structured info and stores it in your workspace (so Git/`claw-roam` can sync across devices).
- It schedules reminders using OpenClaw `cron`, and delivers notifications to **Telegram + Discord**.

Default delivery targets (this workspace):
- Telegram (Maya): `telegram:869269685`
- Discord reminders channel: `discord:1471563067367100547`

## What it does

- Capture events from chat (meetings / birthdays / deadlines)
- Store events in a **workspace data file** (easy to back up & sync via Git/`claw-roam`)
- Schedule reminder notifications using OpenClaw `cron` (Telegram + Discord)
- Answer queries like "我最近有什么安排/计划？"

## Data (separated from skill)

This skill contains **no personal event data**.

User data lives in the workspace at:
- Events file: `~/.openclaw/workspace/reminders/events.yml`

Template (shipped with the skill):
- `skills/reminder/assets/events.template.yml`

## Config (env)

- `REMINDER_TZ` (default: `Asia/Shanghai`)
- `REMINDER_OFFSETS_MINUTES` (default: `1440,60,10` for 24h/1h/10m)

## Capture behavior

When user says something like:
- "后天上午10点有个会"
- "下个月2号我妈生日"
- "周五下午三点交报告"

Do:
1) Parse the event:
   - title
   - start datetime (Shanghai)
   - notes (optional)
   - reminders offsets (default 24h/1h/10m)
   - repeat (optional: yearly/monthly/weekly)
2) If key info is ambiguous (e.g. '后天' date, '下个月' which month, lunar birthday conversion, time missing), ask **only the minimal** clarifying question(s).
3) Write/update the event in `reminders/events.yml`.
4) **CRITICAL**: Create `cron` jobs for each reminder time using the `cron` tool.

- Set `delivery.mode: "none"` (avoid duplicate delivery).
- In the payload, use `message.broadcast` to send to BOTH:
  - `telegram:869269685`
  - `discord:1471563067367100547`

Example cron job shape:

```json5
{
  enabled: true,
  name: "Reminder: {event_title} ({offset_label})",
  sessionTarget: "isolated",
  wakeMode: "now",
  delivery: { mode: "none" },
  schedule: { kind: "at", at: "<ISO timestamp>" },
  payload: {
    kind: "agentTurn",
    message: "你是提醒通知助手。\n\n1) 组织提醒正文（包含：事件标题/时间/距离事件多久）。\n2) 用 message.broadcast 同时发送到 discord:1471563067367100547 与 telegram:869269685。\n3) 最后回复 NO_REPLY。"
  }
}
```

5) Confirm to user with the resolved datetime + all scheduled reminder times.

## Implementation Details

### When adding a new reminder:

1. **Parse user input** to extract:
   - Title (what is the event)
   - Date/time (when)
   - Any special notes

2. **Generate event ID**: Format `meet-YYYYMMDD-HHMM` or similar

3. **Write to events.yml**:
```yaml
- id: meet-20260208-1000
  title: 会
  start: 2026-02-08T10:00:00+08:00
  notes: ""
  reminders: [1440, 60, 10]  # 24h, 1h, 10m before
```

4. **Create cron jobs** using the `cron` tool:
   - Calculate reminder timestamps: `start_time - offset`
   - Create one job per reminder offset
   - Job name format: `Reminder: {title} ({offset_desc})`
   - Payload must use `message` tool to send to telegram

5. **Confirm to user**:
   - Event title and datetime
   - List of scheduled reminders with exact times
   - Event ID for future reference

### When listing/querying reminders:

Read `reminders/events.yml`, filter upcoming events, and summarize.

### When canceling/deleting:

1. Remove from `events.yml`
2. Find and remove associated cron jobs using `cron list` + `cron remove`

## Reply style

- After scheduling: reply briefly with the resolved datetime + confirmation of all reminder times.
- For cancellations/changes: confirm what was changed and whether cron jobs were removed/replaced.

## Queries

If user asks:
- "我最近有什么安排？"
- "下周有什么？"

Then read `reminders/events.yml`, compute upcoming items (Shanghai time), and summarize.

## Notes / safety

- Never commit machine-specific secrets (keep them in `LOCAL_CONFIG.md`, already gitignored).
- For lunar birthdays: store the canonical lunar date + the computed solar date for the target year; ask how to handle leap months when needed.
- Always confirm the reminder times with the user after scheduling.
- Use `wakeMode: "now"` for reminder cron jobs to ensure timely delivery.
