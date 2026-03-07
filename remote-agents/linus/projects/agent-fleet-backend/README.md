# Agent Fleet Backend

Cloudflare Worker + KV backend for high-frequency fleet status updates.

## Endpoints

- `POST /ingest` - collector ingest (Bearer token required)
- `GET /fleet` - aggregate fleet snapshot for dashboard (Bearer read token)
- `GET /health` - service health

## KV keys

- `fleet:registry`
- `fleet:heartbeat:<agent_id>`
- `fleet:cron:<agent_id>`
- `fleet:runtime:<agent_id>`
- `fleet:events:recent`
- `fleet:updated_at`

## Setup

1. Create KV namespace:
   - `wrangler kv namespace create FLEET_KV`
2. Put namespace id into `wrangler.jsonc`.
3. Copy local secrets:
   - `cp .dev.vars.example .dev.vars`
4. Local dev:
   - `npm install`
   - `npm run dev`

## Deploy

- `npm run deploy`

## Auth model (v1)

- `/ingest` expects `Authorization: Bearer $INGEST_TOKEN`
- `/fleet` expects `Authorization: Bearer $READ_TOKEN`
- If `READ_TOKEN` is not set, fallback to `INGEST_TOKEN`
