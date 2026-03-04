---
name: discord-agent-registry
description: Manage cross-gateway agent registration and roster sync over a shared Discord team channel. Use when maintaining multi-agent presence (register, admin offline/remove, snapshot broadcast, heartbeat updates) where Discord is the only inter-gateway communication path.
---

# Discord Agent Registry

Use this skill to maintain a manual-but-reliable cross-gateway registry in one Discord channel.

## Source of truth

- Registry file: `skills/discord-agent-registry/registry/agents.json`
- Only one orchestrator (recommended: Maya) should write this file.

## Message protocol (Discord channel)

Send JSON in code blocks.

- `REGISTER`
- `HEARTBEAT`
- `REGISTRY_SNAPSHOT`
- `ADMIN_OFFLINE`

Required fields:
- `v`, `msg_id`, `type`, `ts`

## Manual operations

Use script:

```bash
python skills/discord-agent-registry/scripts/registry.py register \
  --agent-id jesse --name Jesse --role trader --gateway gw-mac --node Reed-Mac

python skills/discord-agent-registry/scripts/registry.py offline --agent-id linus --reason "admin removed"

python skills/discord-agent-registry/scripts/registry.py heartbeat --agent-id maya --status online

python skills/discord-agent-registry/scripts/registry.py snapshot
```

For Discord broadcast, copy generated JSON and post to your team channel.

## Rules

1. Treat `agent_id` as unique key.
2. Update `last_seen` on register/heartbeat.
3. Mark offline if no heartbeat (recommended timeout: 180s).
4. Snapshot `version` must increment on every state change.
5. Ignore duplicate `msg_id` downstream (idempotency).
