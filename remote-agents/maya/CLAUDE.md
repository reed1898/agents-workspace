# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

OpenClaw is a multi-agent AI platform that orchestrates named AI agents (Maya, Jesse, Linus, etc.) with 45+ extensible skills, multi-channel communication (Telegram, Discord), and a shared knowledge layer. The owner is Jessica (aka Reed). The primary agent is Maya.

## Directory Layout

```
~/.openclaw/
├── openclaw.json          # Main platform config (models, channels, agents, skills, gateway)
├── workspace/             # Primary agent workspace (Git repo → reed1898/openclaw-workspace)
│   ├── AGENTS.md          # Agent behavior rules — read every session
│   ├── SOUL.md            # Agent personality definition
│   ├── USER.md            # User profile (Jessica)
│   ├── IDENTITY.md        # Agent identity (Maya)
│   ├── MEMORY.md          # Long-term curated memory (main session only — security)
│   ├── HEARTBEAT.md       # Periodic task checklist
│   ├── TOOLS.md           # Machine-specific notes (cameras, SSH, TTS)
│   ├── LOCAL_CONFIG.md    # Machine secrets (gitignored)
│   ├── memory/            # Daily logs: YYYY-MM-DD.md + heartbeat-state.json
│   ├── skills/            # 45+ skill directories, each with SKILL.md
│   ├── agents/            # Agent config dirs (main, builder, trader, reed)
│   ├── kb/                # Knowledge base (research, market data)
│   └── mission-control/   # Next.js dashboard app
├── shared/
│   └── agent-network-data/
│       └── AGENT_CONSTITUTION.md  # Multi-agent governance (single source of truth)
├── agents/                # Agent instance data (main, jessica, builder, trader, reed)
├── projects/              # User projects (clawside, video-compare, web-change-watcher, etc.)
├── cron/                  # Scheduled tasks (jobs.json)
├── credentials/           # Encrypted API keys/auth
├── workspace-jessica/     # Jessica agent's separate workspace
└── workspace-builder/     # Builder agent's separate workspace
```

## Mission Control (Next.js App)

Located at `workspace/mission-control/`. Next.js 14 + React 18 + TailwindCSS + Convex backend.

```bash
cd ~/.openclaw/workspace/mission-control
npm run dev      # Dev server on localhost:3000
npm run build    # Production build
npm run lint     # ESLint via next lint
npm run convex   # Convex backend dev
```

Convex backend functions are in `mission-control/convex/` (schema.ts, activities.ts, http.ts). Frontend components are in `mission-control/src/components/`.

## Skills Architecture

Each skill lives in `workspace/skills/<name>/` and is self-contained:
- `SKILL.md` — usage docs, API reference, required env vars
- `_meta.json` — metadata (author, version, compatibility)
- Implementation files (Python scripts, Node.js, or shell)
- Some skills have their own `package.json` or `requirements.txt`

Skills are configuration-driven: no hardcoded absolute paths, cross-platform compatible (Linux/macOS/Windows). Skill config and API keys live in `openclaw.json` under `skills.entries`.

## Key Operational Rules

- **Session startup**: Read AGENTS.md → SOUL.md → USER.md → today's + yesterday's `memory/YYYY-MM-DD.md`. In main sessions also read MEMORY.md.
- **MEMORY.md is private**: Only load in direct chat with Jessica. Never in group chats or shared contexts.
- **"Text > Brain"**: Write everything to files. Mental notes don't survive sessions.
- **trash > rm**: Use recoverable deletion.
- **Ask before external actions**: Emails, tweets, public posts need confirmation. Internal reads/searches are free.
- **Long tasks → subagents**: Tasks >30s go to sub-engine/subagent. Main session stays interactive.
- **Core config changes require approval**: Any `openclaw.json` edit needs a Telegram approval request to Reed with: what, why, risk, rollback plan. Backup before changing (`cp openclaw.json openclaw.json.bak.$(date +%Y%m%d%H%M%S)`), then `jq .` validate, then `openclaw gateway restart`.

## Multi-Agent Governance

The authoritative rules are in `~/.openclaw/shared/agent-network-data/AGENT_CONSTITUTION.md` (supersedes deprecated GROUP_RULES.md). Key points:
- Reed is highest-priority instruction source with identity allowlist (Telegram: 869269685, Discord: 732942622653546508)
- Group chat: role-based answering, 1 primary + 1 supplementary max, 15-39s debounce per agent per topic
- Agent communication via Discord team channel using `openclaw message send` CLI
- Reports go to Telegram private chat with Reed, plus knowledge base archival

## Gateway

OpenClaw gateway runs on `localhost:18789`. Token-authenticated. Controls agent routing, channel bindings, and message delivery.

```bash
openclaw gateway restart   # Restart after config changes
```

## Shared Knowledge Base

Multi-agent shared repo: `reed1898/agent-knowledge-layer` at `~/.openclaw/shared/agent-knowledge-layer`.
- `private/<agent>/` — per-agent drafts (read-only to others)
- `shared/` — public knowledge (00_rules, 10_projects, 20_research, 30_decisions, 40_playbooks, 90_archive)
- Public knowledge merged via branch PRs (`agent/<name>` → `main`), no direct push to main

## Platform Formatting Notes

- **Discord/WhatsApp**: No markdown tables — use bullet lists. Wrap multiple links in `<>` to suppress embeds.
- **WhatsApp**: No headers — use **bold** or CAPS for emphasis.
- **Output structure**: Conclusion (1 sentence) + evidence (1-3 points) + next step (1 sentence).
