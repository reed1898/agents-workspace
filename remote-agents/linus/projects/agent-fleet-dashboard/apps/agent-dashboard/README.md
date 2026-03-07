# Agent Dashboard App

Next.js 14 App Router dashboard for OpenClaw fleet state.

## Setup

1. From repo root install deps:
   - `npm install`
2. Copy env:
   - `cp .env.example .env.local`
3. Ensure selected data source is configured.

## Run

- Dev: `npm run -w apps/agent-dashboard dev`
- Build: `npm run -w apps/agent-dashboard build`
- Start: `npm run -w apps/agent-dashboard start`
- Typecheck: `npm run -w apps/agent-dashboard typecheck`

## Data source modes

- `NEXT_PUBLIC_DATA_SOURCE_MODE=local` (default)
  - reads files from `AGENT_DATA_LOCAL_ROOT`
- `NEXT_PUBLIC_DATA_SOURCE_MODE=github`
  - server-side fetch from GitHub Contents API with `GITHUB_TOKEN`
- `NEXT_PUBLIC_DATA_SOURCE_MODE=cloudflare`
  - server-side fetch from Worker `GET /fleet`
  - requires `FLEET_API_ENDPOINT` and `DASHBOARD_READ_TOKEN`

If data read fails, app falls back to built-in mock data for UI continuity.
