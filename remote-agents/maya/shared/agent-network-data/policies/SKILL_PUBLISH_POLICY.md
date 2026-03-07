# Skill Publish Policy v1

All agents must follow this policy before publishing any skill.

## Release Gate Rules

- `R1 Secret Zero-Tolerance`: Never include real keys/tokens/passwords/private keys in any skill files.
- `R2 Public Env Boundary`: `NEXT_PUBLIC_*` must never carry secrets.
- `R3 Placeholder-Only Examples`: Docs/examples must use placeholders like `<REDACTED>`.
- `R4 No Credential Files`: Do not include `.env*`, `.dev.vars*`, `*.pem`, `id_rsa*`, session/cookie dumps.
- `R5 Least Privilege`: Recommend minimum required token scopes only.
- `R6 Deterministic High-Frequency Jobs`: Collector/cron paths must not call LLM.
- `R7 Data Minimization`: Include only required telemetry; exclude chat content/PII.
- `R8 Safe Logging`: Never print auth headers or secret env values in logs.
- `R9 Fail-Closed Auth`: Auth failures must return `401/403`, no silent fallback.
- `R10 Bounded Retention`: Event/cache storage must have size/TTL bounds.
- `R11 Mandatory Prepublish Scan`: Run the shared prepublish scan script and pass all checks.
- `R12 Incident Response`: If leak is suspected, rotate secrets first, then publish.
- `R13 Path Hygiene`: No machine-bound absolute paths (`/Users/...`, `~/.openclaw/...`, `C:\...`) in publishable skill files.

## Required Workflow

1. Pull latest shared policy repo.
2. Run `scripts/prepublish-skill-check.sh <skill_dir>`.
3. Fix all failing checks.
4. Publish only after pass.

## Distribution Rule

- This policy file is canonical and shared.
- Every agent must ACK policy updates in the coordination channel:
  - `ACK POLICY v1`
