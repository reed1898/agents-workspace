# HEARTBEAT.md

## OpenClaw Contributor - Auto Tasks

X/Twitter scans and X Lists digests are now handled by dedicated Cron jobs.
Heartbeat should not proactively push those reports.

### PR Status Check (1x daily)
- Check if any submitted PRs have new comments/reviews
- If review feedback exists, address it
