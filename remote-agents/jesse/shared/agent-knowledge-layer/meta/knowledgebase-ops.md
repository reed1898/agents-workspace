# Knowledgebase Ops (Jesse)

## Branch policy
- Stable branch: `main`
- Working branch: `agent/jesse`
- Shared knowledge changes must go via PR to `main`.

## Daily flow
1. `git checkout agent/jesse`
2. `git pull --rebase origin agent/jesse`
3. Write drafts in `private/jesse/`
4. Commit + push `agent/jesse`

## Promote to shared
1. Refine content into `shared/*`
2. Commit on `agent/jesse`
3. Open PR: `agent/jesse -> main`

## Safety
- Never force-push `main`
- No secrets/tokens in repository files
