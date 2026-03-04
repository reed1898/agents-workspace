# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

OpenClaw agent workspace for **小洪 (Xiaohong)** — Reed's AI familiar (数字分身). This is not a traditional software project; it's a live agent operating environment with persistent memory, skills, scheduled tasks, and multi-agent coordination.

## Key Files (Session Startup)

Every session, the agent reads these in order:
1. `workspace/SOUL.md` — personality and behavioral rules
2. `workspace/USER.md` — Reed's profile and preferences
3. `workspace/memory/YYYY-MM-DD.md` — recent daily logs (today + yesterday)
4. `workspace/MEMORY.md` — curated long-term memory (**main sessions only**, never in group chats for privacy)

## Architecture

```
~/.openclaw/
├── openclaw.json          # Central config (auth, channels, models, gateway, skill env)
├── workspace/             # Primary agent workspace
│   ├── SOUL.md / USER.md / IDENTITY.md / MEMORY.md  # Agent identity & context
│   ├── memory/            # Daily logs (YYYY-MM-DD.md) + heartbeat-state.json
│   ├── skills/            # 15 installed skills (each has SKILL.md + _meta.json)
│   └── scripts/           # Bash automation (daily-summary.sh)
├── agents/main/sessions/  # JSONL conversation logs (one file per session)
├── shared/
│   ├── agent-network-data/     # Multi-agent governance (AGENT_CONSTITUTION.md)
│   └── agent-knowledge-layer/  # Git-based shared knowledge (branch: agent/xiaohong)
├── remote-agents/         # Synced workspaces for Maya, Jesse, Linus (read-only via Syncthing)
├── cron/jobs.json         # Scheduled tasks (security scans, daily reports, KB sync, evolution)
├── memory/main.sqlite     # Long-term memory database
├── browser/               # Browserbase/Stagehand automation data
├── credentials/           # Encrypted credentials
└── identity/              # Device keypair
```

## Memory Hierarchy

- **Session logs** (JSONL): raw conversation history, ephemeral
- **Daily memory** (`workspace/memory/YYYY-MM-DD.md`): what happened today
- **Long-term memory** (`workspace/MEMORY.md`): curated facts and lessons — loaded only in direct chats with Reed
- **SQLite** (`memory/main.sqlite`): indexed persistent facts

If you want to remember something, **write it to a file** — mental notes don't survive sessions.

## Skill System

Skills live in `workspace/skills/<name>/`. Each skill has:
- `SKILL.md` — markdown doc defining when/how to use the skill
- `_meta.json` — ownership, slug, version, publishedAt
- Optional: `assets/`, `scripts/`, `package.json`

Skills are published to **clawhub** (internal registry). Install with `clawhub install <name>`, search with `clawhub search`.

Notable skills: `browse` (Stagehand/Browserbase automation), `reminder` (natural language reminders via Telegram), `multi-source-news-digest` (Python, 109+ RSS sources), `x-post-automation` / `x-tweet-fetcher` (Twitter), `volcengine-stt` (speech-to-text).

## Multi-Agent Network

- **Primary**: 小洪 (Xiaohong) — this workspace
- **Remote agents**: Maya, Jesse, Linus — synced via Syncthing over tailscale (receive-only)
- **Knowledge layer**: Git repo at `shared/agent-knowledge-layer/` with branch model (`agent/<name>` → `main` via PR)
- **Daily summary script** (`scripts/daily-summary.sh`): scans remote agent session logs, generates markdown reports, commits to knowledge layer

## Scheduled Tasks (cron/jobs.json)

- `daily-report` — 08:15 CST: generates daily work report, sends to Reed via Telegram
- `daily-agent-summary` — 02:00 CST: runs `daily-summary.sh`, summarizes all agent work
- `security-scan-morning/evening` — 07:00 / 21:20 CST: system + skill security audit
- `agent-network-sync` — every 4h: git pull shared repos
- `kb-hourly-closed-loop` — every hour: sync main→agent branch, commit, push, create PRs
- `evolver-hourly` — 03:00-06:00 CST: self-improvement tasks
- `reed-hourly-proactive-checkin` — every hour: status update if Reed hasn't messaged recently

## Channels

- **Telegram** (primary): bot token in openclaw.json, Reed's chatId: `869269685`
- **Discord**: multiple guilds/channels
- **Web**: local gateway at `127.0.0.1:18789` (token auth)

## Key Conventions

- **Language**: Reed communicates in Chinese; workspace docs are mixed Chinese/English
- **Timezone**: Asia/Shanghai (GMT+8), Reed's hours: 08:30–01:30
- **Safety**: `trash` > `rm`; ask before any external action (emails, tweets, public posts); private data never leaks to group chats
- **Platform formatting**: no markdown tables on Discord/WhatsApp; wrap multiple Discord links in `<>` to suppress embeds
- **macOS note**: use `base64 -i` instead of `base64 -w 0` (volcengine-stt compatibility)
- **Browser automation**: Stagehand CLI + Browserbase Functions; after `stagehand fn init`, must immediately fix `package.json` (see `skills/browse/SKILL.md` Step 3)
