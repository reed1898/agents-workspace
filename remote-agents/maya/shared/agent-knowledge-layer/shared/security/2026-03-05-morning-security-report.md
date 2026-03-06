# Morning Security Report - 2026-03-05 07:00 (Asia/Shanghai)

## Scope
1. System security inspection: host exposure, service status, abnormal ports, permission risk.
2. OpenClaw risk inspection: vulnerability/audit alerts, update status, config/auth exposure strategy.
3. Skill safety inspection: source trust, suspicious scripts, dangerous command patterns, privilege boundary risks.

## Auto-fixes Applied (Low Risk)
- Executed `openclaw security audit --fix`.
- Hardened local OpenClaw file permissions automatically:
  - `~/.openclaw/agents/main` -> `700`
  - `~/.openclaw/agents/main/sessions` -> `700`
  - multiple `~/.openclaw/agents/main/sessions/*.jsonl` -> `600`
- No service restarts, firewall changes, or network policy changes were made.

## Findings by Severity

### High
1. **Untrusted-surface skill flagged as critical by OpenClaw deep audit**
   - Skill: `feishu-evolver-wrapper`
   - Location: `/Users/rain/.openclaw/workspace/skills/feishu-evolver-wrapper`
   - Scanner result: 12 critical hits (`dangerous-exec`, `dynamic-code-execution`, `env-harvesting`).
   - Representative files: `exec_cache.js`, `index.js`, `skills_monitor.js`, `export_history.js`, `visualize_dashboard.js`.
   - Risk: command execution + env access + network send can become credential exfiltration / remote execution chain.
   - Current action: flagged for immediate quarantine/disable decision (not auto-removed to avoid breaking intentional workflows).

2. **Host has multiple non-loopback listening ports while macOS Application Firewall is disabled**
   - Firewall: `socketfilterfw --getglobalstate` => disabled.
   - Non-loopback listeners include:
     - `*:5000`, `*:7000` (`ControlCe`)
     - `*:22000` (`syncthing`)
     - `*:3306`, `*:33060` (`mysqld`)
     - `*:58645` (`rapportd`)
     - `*:61348` (`AiCoin`)
   - Risk: larger LAN attack surface; if network trust boundary is weak, lateral movement risk increases.

### Medium
1. **OpenClaw trust model mismatch warning (`multi_user_heuristic`)**
   - Deep audit warns gateway may have multi-user reachability while runtime/file tools are powerful and sandbox not fully enforced for all contexts.
   - Key context from audit: `agents.defaults` exposes `exec/process` + `read/write/edit` with `sandbox=off`.
   - Risk: acceptable for single trusted operator; risky if any untrusted shared access exists.

2. **Skill `reddit-search-but-free` marked suspicious (1 warning)**
   - Location: `/Users/rain/.openclaw/workspace/skills/reddit-search-but-free/scripts/reddit.ts:10`
   - Pattern: potential file-read + network-send path.
   - Risk: likely benign for this class of skill, but needs explicit source review.

3. **OpenClaw deep status probe intermittent timeout**
   - `openclaw status --deep` returned gateway timeout once.
   - Baseline `openclaw status` and `openclaw health --json` still returned usable results.
   - Risk: operational observability gap if repeated.

### Low
1. **No world-writable or SUID files under `~/.openclaw` found in this check**.
2. **OpenClaw update status**
   - Channel: `stable`
   - Latest (npm): `2026.3.2`
   - Action: no forced update executed in this scan window.
3. **pf status could not be queried without elevated permission**
   - `pfctl -s info` returned permission denied.
   - This is a visibility limitation, not evidence of compromise.

## OpenClaw Security Snapshot
- `openclaw security audit --deep`: **1 critical / 2 warn / 1 info**.
- Browser control: enabled.
- Elevated tools: enabled.
- Hooks webhooks/internal: disabled.
- Attack surface summary (audit): group policy open=0, allowlist=2.

## Skill Trust Notes
- Both flagged skills include `.clawhub` metadata, but scanner severity indicates trust-by-source alone is insufficient.
- Recommendation:
  - `feishu-evolver-wrapper`: quarantine or uninstall unless actively required and code-reviewed.
  - `reddit-search-but-free`: keep with constrained usage, after targeted line review.

## Recommended Next Actions
1. Quarantine `feishu-evolver-wrapper` immediately (disable loading or move out of active skills path).
2. Re-enable macOS Application Firewall and validate allowlist rules for currently exposed services.
3. Restrict public/LAN listeners where possible (especially MySQL/Syncthing/control ports) to loopback or trusted interfaces.
4. If any shared-user context exists, enforce stricter sandbox defaults for OpenClaw runtime/file tools.
5. Re-run deep audit after mitigations and keep this report as baseline.

## Commands Executed (audit trail)
- `openclaw status`
- `openclaw status --deep`
- `openclaw security audit --deep`
- `openclaw security audit --fix`
- `openclaw update status`
- `openclaw health --json`
- `/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN`
- `/usr/sbin/lsof -nP -iUDP`
- `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
- `/sbin/pfctl -s info`
- `find ~/.openclaw -xdev -type f -perm -0002`
- `find ~/.openclaw -xdev -type f -perm -4000`
- targeted `rg` scans on `~/ .openclaw/workspace/skills/**` for dangerous patterns
