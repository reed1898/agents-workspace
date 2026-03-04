# OpenClaw Security Report (Evening)

- Date: 2026-03-04
- Timezone: Asia/Shanghai
- Scan time: 21:20
- Host: Rain2025.local (macOS arm64)

## Scope
1. `openclaw status` health check
2. Gateway config security (bind/port/auth)
3. Sensitive data exposure review in `~/.openclaw/openclaw.json`
4. Skills directory anomaly/permission check
5. Cron job anomaly check
6. Low-risk auto-remediation

## Checks Performed
- Ran `openclaw status`
- Parsed `~/.openclaw/openclaw.json` for gateway and secret fields
- Audited file permissions for config/backup files
- Scanned skills directory for:
  - world-writable files/dirs
  - setuid/setgid files
  - non-owner files
  - suspicious symlinks and large binaries
- Compared `~/.openclaw/cron/jobs.json` with `~/.openclaw/cron/jobs.json.bak` for unexpected additions/removals
- Reviewed cron file permissions and tightened where needed

## Findings (by severity)

### High
- None.

### Medium
1. Plaintext secrets are present in local config files (expected but sensitive).
   - `~/.openclaw/openclaw.json` contains inline secret values:
     - `gateway.auth.token`
     - `channels.discord.accounts.default.token`
     - `talk.apiKey`
   - Mirror copies also exist under `~/.openclaw/agents-workspace-repo/openclaw.json*` and backup trees.
   - Current mitigations are good: files are mode `600` and openclaw config files are ignored by git in the workspace repo.
   - Risk: local compromise or accidental file sharing can expose credentials.

### Low
1. Cron definitions were world-readable (`644`) before remediation.
   - Affected files:
     - `~/.openclaw/cron/jobs.json`
     - `~/.openclaw/cron/jobs.json.bak`
     - `~/.openclaw/agents-workspace-repo/cron/jobs.json`
     - `~/.openclaw/agents-workspace-repo/cron/jobs.json.bak`

## Auto-Fixes Applied (low risk)
- Tightened cron file permissions from `644` -> `600` for all four files above.
- Post-fix verification: all now `-rw-------`.

## Detailed Results
- OpenClaw health: gateway running, reachable on loopback `127.0.0.1:18789`, auth mode token enabled.
- Gateway exposure: bind is `loopback`; no direct non-local bind detected.
- OpenClaw status security summary: `0 critical / 1 warn / 1 info`.
  - Warning is a trust-boundary warning for potential multi-user/group setup (Discord allowlist context), not an immediate exploit finding.
- Skills directory (`~/.openclaw/workspace/skills`):
  - No world-writable files/dirs
  - No setuid/setgid files
  - No non-owner entries
  - One symlink under a local `node_modules` package (`feishu-evolver-wrapper/node_modules/evolver -> ../../evolver`), appears expected for local package linking
  - No oversized binaries (>20MB)
- Cron anomaly check:
  - Current jobs count equals backup (10)
  - No added/removed jobs detected

## Recommended Next Actions
1. Rotate gateway/channel/API secrets on a regular cadence (or immediately if this machine has been shared).
2. Prefer env-based secret injection where possible to reduce plaintext secret footprint in config backups.
3. Consider pruning stale backup trees that contain historical config snapshots with secrets.
4. Keep running morning/evening security scans and monitor for new cron entries.

## Verdict
- No high-severity issue detected.
- Security baseline is acceptable after low-risk permission hardening.
- Status: security check passed.
