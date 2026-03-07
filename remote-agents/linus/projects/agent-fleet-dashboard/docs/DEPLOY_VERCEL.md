# Deploy on Vercel

## Prereqs

- Vercel CLI installed and logged in: `vercel login`
- Run from app folder: `apps/agent-dashboard`

## Link and deploy

```bash
cd apps/agent-dashboard
vercel link --yes
vercel --prod
```

## Required env vars

Set in Vercel project settings or CLI:

```bash
vercel env add NEXT_PUBLIC_DATA_SOURCE_MODE production
vercel env add FLEET_API_ENDPOINT production
vercel env add DASHBOARD_READ_TOKEN production

# optional fallback modes
vercel env add AGENT_DATA_LOCAL_ROOT production
vercel env add GITHUB_REPO_OWNER production
vercel env add GITHUB_REPO_NAME production
vercel env add GITHUB_REPO_BRANCH production
vercel env add GITHUB_TOKEN production
```

Recommended for Vercel-hosted app:
- Use `NEXT_PUBLIC_DATA_SOURCE_MODE=cloudflare`
- Keep `DASHBOARD_READ_TOKEN` server-side only

## Redeploy

```bash
vercel --prod
```
