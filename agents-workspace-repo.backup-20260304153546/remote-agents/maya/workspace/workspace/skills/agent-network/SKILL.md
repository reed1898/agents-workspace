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

**Hard rule:** all inter-agent communication must go through the Discord team channel using OpenClaw message CLI. Do not use direct cross-gateway sessions_send for this network.

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

## Discord send command (required)

For cross-agent notifications, send via OpenClaw CLI directly:

```bash
openclaw message send \
  --channel discord \
  --target "channel:<discord_channel_id>" \
  --message "<@user_id_a> <@user_id_b> ... your event text"
```

Example:

```bash
openclaw message send \
  --channel discord \
  --target "channel:1471363336192131276" \
  --message "<@1471167332133900351> <@1471349080847548466> Linus 已重新注册到 AgentNetwork"
```

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
2) **Receiver rule (mandatory):** when an agent receives a `REGISTER` broadcast from Discord, it must run `git pull --rebase` on shared state, refresh local roster cache, and send `ACK` message (include `msg_id/task_id`). Receiver does not rewrite full registry on ACK.
3) **Reconcile layer (daily):** each agent performs one daily registry sync in heartbeat flow (`git pull --rebase` + refresh local cache).

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
- Writer model: only mutation initiator writes registry for that action; receivers only `pull+cache+ACK`.
