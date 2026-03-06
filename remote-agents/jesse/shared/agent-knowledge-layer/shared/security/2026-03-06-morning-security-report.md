# Morning Security Report

- Date: 2026-03-06 07:00 (Asia/Shanghai)
- Host: Rain2025.local (macOS 26.2 arm64)
- Scope: System security, OpenClaw security, installed skills security

## Executive Summary
- High: 2
- Medium: 3
- Low: 2 (1 auto-remediated)

## High

1) **Untrusted/dangerous skill patterns detected (`evolver`)**
- Evidence: `openclaw security audit --deep` reported **1 critical** with 26 critical findings under `/Users/rain/.openclaw/workspace/skills/evolver`.
- Risk: command execution + potential environment-variable harvesting + network send patterns may enable credential exfiltration or arbitrary execution.
- Impact: high, because this skill has code paths invoking shell/process operations.
- Recommendation:
  - Immediately disable/remove `evolver` from active usage until manual code review is complete.
  - If keeping it, run in strict sandbox and deny runtime/process tools by default.

2) **Firewall disabled on host**
- Evidence: `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate` => `Firewall is disabled (State=0)`.
- Risk: increases host network exposure if any service starts listening on non-loopback interfaces.
- Recommendation:
  - Enable macOS firewall and stealth mode.
  - Keep allow-list minimal (OpenClaw is already loopback-bound).

## Medium

1) **OpenClaw trust boundary warning (multi-user heuristic)**
- Evidence: `openclaw status` and `openclaw security audit --deep` warn that current setup may be used in multi-user contexts while default trust model is personal-assistant.
- Risk: permission boundary confusion if multiple users/channels are treated as trusted.
- Current config signals:
  - `agents.defaults.sandbox.mode = off`
  - runtime/process tools exposed in default contexts
- Recommendation:
  - For shared contexts, set sandbox to strict/all and reduce high-impact tools.
  - Separate gateways/OS users if untrusted participants may interact.

2) **Suspicious pattern in `reddit-search-but-free` skill**
- Evidence: audit warning: potential file-read + network-send pattern in `scripts/reddit.ts:10`.
- Risk: possible data exfiltration path if skill is modified/misused.
- Recommendation:
  - Review flagged code; keep skill disabled until review if not currently needed.

3) **Local dev service exposed on `0.0.0.0:8000` (non-OpenClaw)**
- Evidence: process list includes `uvicorn ... --host 0.0.0.0 --port 8000`.
- Risk: service reachable from LAN if host firewall is off.
- Recommendation:
  - Bind dev services to `127.0.0.1` unless remote access is required.

## Low

1) **Sensitive OAuth client secret file permission too broad (fixed)**
- Evidence before fix: `/Users/rain/.openclaw/config/gws/client_secret_*.json` was `-rw-r--r--`.
- Action taken: changed to `600`.
- Evidence after fix: now `-rw-------`.
- Result: auto-remediated.

2) **Security skill guidance not readable in this run context**
- Evidence: sandbox prevented reading `/opt/homebrew/lib/node_modules/openclaw/skills/healthcheck/SKILL.md`.
- Risk: low direct risk; reduces procedural consistency.
- Recommendation: allow read access to installed skill docs for cron security jobs.

## OpenClaw-Specific Risk Review

- Version: `2026.3.2` (CLI and status show latest channel current)
- Gateway exposure: loopback-only (`127.0.0.1:18789`), token auth enabled
- Tailscale mode: off
- Hooks/webhooks: disabled per audit info
- Noted config risk:
  - sandbox disabled globally in agent defaults
  - multiple channel integrations active (Telegram + Discord), so channel policy hygiene is important

## Skill Source & Trust Review

- Installed workspace skills count: 178 files across custom/local skill folders.
- Higher-risk custom skills (manual review priority):
  - `evolver` (critical findings)
  - `reddit-search-but-free` (warning finding)
- General dangerous-pattern grep also hit expected documentation/test examples; no additional immediate critical beyond audit output.

## Auto-Remediation Log

- `chmod 600 /Users/rain/.openclaw/config/gws/client_secret_*.json` (completed)

## Recommended Next Actions (today)

1. Disable/remove `evolver` until reviewed.
2. Enable macOS firewall + stealth mode.
3. Change default OpenClaw sandbox from `off` to stricter mode for shared surfaces.
4. Restrict any dev services from `0.0.0.0` to loopback where possible.
5. Review `reddit-search-but-free/scripts/reddit.ts:10` intent and data flow.
