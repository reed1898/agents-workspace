# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Directory Is

`~/.openclaw` is the **user data directory** for an OpenClaw personal AI assistant gateway. It is NOT the source repository. The installed package lives at `/usr/local/lib/node_modules/openclaw`.

This directory contains runtime configuration, credentials, agent workspace, memory, skills, and patches — everything the gateway needs at runtime.

## Directory Layout

- `openclaw.json` — main gateway config (channels, models, auth, skills, gateway settings). **Contains secrets — never commit or expose.**
- `workspace/` — agent workspace (git repo); contains `AGENTS.md`, `IDENTITY.md`, `SOUL.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`, skills, scripts, projects
- `credentials/` — channel credentials and pairing data
- `devices/` — paired device info (iOS/Android nodes)
- `agents/` — agent definitions
- `memory/` — agent memory and context files
- `logs/` — gateway logs
- `media/` — temporary media files
- `cron/` — cron job definitions
- `patches/` — local patches (e.g. `carbon-proxy.patch` with `apply.sh`)
- `browser/` — browser profiles for Playwright-based browser tool
- `telegram/` — Telegram session data
- `delivery-queue/` — pending message deliveries
- `subagents/` — subagent state

## Common Commands

```bash
# Restart the gateway (launchd service)
launchctl kickstart -k gui/501/ai.openclaw.gateway

# Check gateway health
openclaw health

# Run diagnostics
openclaw doctor

# Send a message via Discord (requires proxy)
https_proxy=http://127.0.0.1:10902 openclaw message send --channel discord --target <channel_id> -m "..."

# Send a message via Telegram
openclaw message send --channel telegram --target <chat_id> -m "..."

# Talk to the agent from CLI
openclaw agent --message "..."

# View gateway logs (today's date)
# Logs at /tmp/openclaw/openclaw-YYYY-MM-DD.log

# Validate config
openclaw config validate
```

## Configuration (openclaw.json)

Key sections:
- `agents.defaults.model` — primary model + fallback chain
- `agents.defaults.models` — model alias mappings (provider/model → alias)
- `channels.telegram` / `channels.discord` — channel configs with tokens, proxy, group settings
- `gateway` — port (18789), bind mode, auth token
- `talk` — TTS provider config (ElevenLabs)
- `skills.entries` — skill-specific env vars
- `session.dmScope` — DM session isolation strategy

## Network Notes

- Gateway binds to loopback on port **18789** with token auth
- Discord and Telegram both use proxy `http://127.0.0.1:10902` (required for Discord connectivity)
- The proxy port may change; check `openclaw.json` for current value

## Workspace (workspace/)

The workspace is a git repo the agent uses. It contains:
- Agent persona files (`IDENTITY.md`, `SOUL.md`, `AGENTS.md`)
- `MEMORY.md` — agent's persistent memory
- `HEARTBEAT.md` — agent's recent activity log
- `skills/` — workspace-level skills
- `scripts/` — user scripts the agent can invoke
- `projects/` — agent project files

## Patches

`patches/apply.sh` applies local patches to the installed openclaw package. Used for local modifications (e.g. proxy support patches) that haven't been upstreamed yet.

## Development (Source)

If working on the openclaw source itself (not this data dir):

```bash
# Source repo
git clone https://github.com/openclaw/openclaw.git && cd openclaw

# Build & dev
pnpm install && pnpm ui:build && pnpm build
pnpm gateway:watch          # auto-reload dev loop

# Quality
pnpm check                  # format + lint + all checks
pnpm format                 # oxfmt
pnpm lint                   # oxlint --type-aware
pnpm lint:fix               # auto-fix lint issues

# Tests
pnpm test                   # parallel test suite
pnpm test:fast              # unit tests only
pnpm test:watch             # watch mode
pnpm test:e2e               # end-to-end tests
pnpm test:coverage          # coverage report

# Code constraints
# Max 500 lines per TS file (enforced by check:loc)
```

Tools: TypeScript 5.9, ESM, pnpm 10, Node ≥22, Vitest, oxlint, oxfmt.
