# Operations Runbook

## State contract paths

### Local/Git mode

- `registry/agent-registry.json`
- `state/heartbeats/<agent_id>.json`
- `state/crons/<agent_id>.json`
- `state/runtime/<agent_id>.json`
- `events/events.jsonl`
- `meta/schema-version.json`

### Cloudflare KV mode

- `fleet:registry`
- `fleet:heartbeat:<agent_id>`
- `fleet:cron:<agent_id>`
- `fleet:runtime:<agent_id>`
- `fleet:events:recent`
- `fleet:updated_at`

## Collector usage

```bash
npm run -w collectors/openclaw-state-collector build
npm run -w collectors/openclaw-state-collector collect
```

Collector behavior:
- Parses `openclaw status` for runtime basics when available
- Reads local `~/.openclaw/workspace/memory/heartbeat-state.json` if present
- Aggregates cron from `crontab -l`, else fallback synthetic status
- `REPORT_MODE=local`: writes local JSON state under `COLLECTOR_DATA_ROOT`
- `REPORT_MODE=cloudflare`: POSTs to Worker `/ingest` with bearer token
- Optional git sync only applies to local mode

## Cron install (every 2 minutes)

```bash
npm run -w collectors/openclaw-state-collector install-cron
```

## Health rules used by dashboard

- last_seen > 10min => offline warn
- heartbeat overdue > 2x interval => heartbeat warn
- consecutive_failures >= 3 => cron critical

## Troubleshooting

- Empty dashboard: run collector once to seed state
- Stale banner: verify collector schedule and Worker availability
- Cloudflare mode failures: check `REPORT_ENDPOINT`, `REPORT_TOKEN`, `DASHBOARD_READ_TOKEN`
- GitHub mode failures: check token and repo/branch env vars
