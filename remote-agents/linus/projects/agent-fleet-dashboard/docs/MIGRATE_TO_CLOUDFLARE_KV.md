# Migrate Fleet State: Git Files -> Cloudflare KV

This migration keeps the dashboard UI unchanged while moving high-frequency state sync to Cloudflare Worker + KV.

## What changes

- Collector write path changes from local/git files to Worker `POST /ingest`
- Dashboard read path changes to Worker `GET /fleet`
- Git repo is no longer the source for fast-changing heartbeat/runtime/event state

## Step 1: Deploy backend

From `/Users/rain/.openclaw/projects/agent-fleet-backend`:

```bash
npm install
wrangler kv namespace create FLEET_KV
# put namespace id into wrangler.jsonc
cp .dev.vars.example .dev.vars
# fill INGEST_TOKEN and READ_TOKEN
npm run deploy
```

## Step 2: Configure collector

In dashboard project env:

```bash
REPORT_MODE=cloudflare
REPORT_ENDPOINT=https://<your-worker-domain>
REPORT_TOKEN=<INGEST_TOKEN>
AGENT_ID=linus
```

Then run once:

```bash
npm run -w collectors/openclaw-state-collector build
npm run -w collectors/openclaw-state-collector collect
```

## Step 3: Configure dashboard

Set server env for app (local `.env.local` or Vercel):

```bash
NEXT_PUBLIC_DATA_SOURCE_MODE=cloudflare
FLEET_API_ENDPOINT=https://<your-worker-domain>
DASHBOARD_READ_TOKEN=<READ_TOKEN>
```

## Step 4: Install cron (every 2 minutes)

```bash
npm run -w collectors/openclaw-state-collector install-cron
```

Equivalent crontab line:

```cron
*/2 * * * * cd /Users/rain/.openclaw/projects/agent-fleet-dashboard && npm run -w collectors/openclaw-state-collector collect >> ~/.openclaw/logs/collector.log 2>&1
```

## Rollback

- Collector: `REPORT_MODE=local`
- Dashboard: `NEXT_PUBLIC_DATA_SOURCE_MODE=local` or `github`
