---
name: agent-network
description: Build and operate a cross-gateway AgentNetwork using Discord as the message bus and GitHub as shared state storage. Use when registering agents, syncing roster snapshots, handling admin offline/remove, and coordinating @agent tasks with lightweight #meta tracking.
---

# AgentNetwork

Use this skill to run multi-agent coordination across different gateways.

## Architecture

- **Transport:** Discord team channel (human-readable, @agent routing)
- **Shared state:** Git repo (registry + heartbeat state)
- **Protocol:** natural language + lightweight `#meta`

Example task message:

```text
@jesse 请做 BTC 风险扫描
#meta task_id=tsk_20260301_001 type=TASK from=maya to=jesse
```

## Git shared-state location

Edit `references/git-config.json` first.

Fields:
- `repo_url`: GitHub repo URL for shared state
- `local_path`: local checkout path on this machine
- `branch`: default `main`

## Discord mention identity (required)

For precise cross-agent routing, every agent record must include Discord IDs:

- `discord_user_id` (required): user/bot ID for exact mention (`<@ID>`)
- `discord_channel_id` (required): target team channel ID for routing

Never rely on plain-text `@name` for automation.

## Manual commands

```bash
python skills/agent-network/scripts/network.py init
python skills/agent-network/scripts/network.py register --agent-id maya --name Maya --role orchestrator --gateway gw-vps --node ip-172-31-21-161 --discord-user-id 1471167332133900351 --discord-channel-id 1471363336192131276
python skills/agent-network/scripts/network.py heartbeat --agent-id maya --status online
python skills/agent-network/scripts/network.py snapshot
python skills/agent-network/scripts/network.py offline --agent-id linus --reason "admin action"
python skills/agent-network/scripts/network.py remove --agent-id linus
```

## Sync policy

Use two layers:

1) **Event layer (real-time):** after register/offline/remove, post protocol JSON to Discord team channel immediately. After `register`, notify **other agents** in registry (`notify_mentions`), not self.
2) **Reconcile layer (daily):** each agent performs one daily registry sync in heartbeat flow (`git pull --rebase` + refresh local cache).

On every mutation:
1. `git pull --rebase`
2. update `registry/agent-registry.json`
3. `git add -A && git commit`
4. `git push`
5. on conflict: retry up to 3 times

## Admin policy

- Agents can `register/heartbeat`.
- Admin (Reed) handles `offline/remove`.
- Treat `agent_id` as unique.
