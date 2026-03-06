# Morning Security Report - 2026-03-04 07:00 (Asia/Shanghai)

## Scope
- Host security check: exposure surface, service status, abnormal ports, permission risks
- OpenClaw security check: version/risk audit/config/auth/exposure strategy
- Skill security check: source trust, suspicious scripts, dangerous commands, privilege boundaries

## Executive Summary
- High: 1
- Medium: 2
- Low: 1 (auto-fixed)

## Findings

### High
1. **Malicious-pattern skill detected: `feishu-evolver-wrapper`**
   - Source: `openclaw security audit --deep`
   - 12 critical findings (dangerous exec + dynamic code execution + env harvesting/network send).
   - Risk: arbitrary command execution and possible credential exfiltration.
   - Recommendation: immediately quarantine/remove `~/.openclaw/workspace/skills/feishu-evolver-wrapper` and rotate exposed secrets.

### Medium
1. **Multi-user trust-boundary risk**
   - Source: `openclaw security audit --deep`
   - Current setup has Discord allowlist group targets and `agents.defaults.sandbox.mode="off"` with runtime/fs tools available.
   - Risk: if any allowlisted actor/session is compromised, host-level impact is possible.
   - Recommendation: move to `agents.defaults.sandbox.mode="all"`, minimize runtime tools, keep `tools.fs.workspaceOnly=true`.

2. **Sensitive tokens are stored in plaintext config**
   - Source: `~/.openclaw/openclaw.json` contains Telegram/Discord/gateway/talk/STT tokens.
   - File permission is strict (`600`), but plaintext at-rest risk remains.
   - Recommendation: migrate to env/auth profile where possible; rotate high-value tokens after handling High item.

### Low (Auto-fixed)
1. **Cron config file permissions too broad**
   - Before: `~/.openclaw/cron/jobs.json` and `.bak` were `644`.
   - Action: changed to `600`.
   - Verification: `stat` confirms both now `-rw-------`.

## OpenClaw Health & Exposure Notes
- `openclaw status`: gateway is local mode, loopback bind (`127.0.0.1`), auth token enabled.
- `openclaw doctor`: legacy session key canonicalization + 1 orphan transcript + Discord probe timeout (Telegram OK).
- Memory semantic search provider not fully configured (operational gap, not direct exploit).

## Skill Security Review
- `openclaw security audit --deep` flagged:
  - High risk: `feishu-evolver-wrapper`
  - Warning: `reddit-research` (potential file-read + network-send path, needs manual line review)
- Additional grep checks found normal subprocess usage in `veille`/`multi-source-news-digest`; no immediate confirmed exploit from sampled lines.

## Auto-remediation Log
- 2026-03-04 07:00 CST
  - `chmod 600 ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.bak`

## Residual Risks / Limitations
- Host port enumeration tools (`lsof`, `netstat`) are unavailable in this runtime, so abnormal-port validation relied on OpenClaw audit/status instead of full socket-level inventory.

## Immediate Action Plan (Priority Order)
1. Quarantine/remove `feishu-evolver-wrapper`.
2. Rotate credentials/tokens possibly touched by that skill.
3. Enable stricter sandbox profile (`agents.defaults.sandbox.mode="all"`) and reduce high-impact tools for shared contexts.
4. Review flagged `reddit-research` line(s) and confirm intended behavior.
