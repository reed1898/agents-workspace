#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <skill_dir>"
  exit 2
fi

SKILL_DIR="$1"
if [[ ! -d "$SKILL_DIR" ]]; then
  echo "[FAIL] Skill directory not found: $SKILL_DIR"
  exit 2
fi

echo "[INFO] Running prepublish checks for: $SKILL_DIR"

FAIL=0

check_no_match() {
  local name="$1"
  local pattern="$2"
  if rg -n --hidden -S "$pattern" "$SKILL_DIR" >/tmp/prepublish_match.$$ 2>/dev/null; then
    echo "[FAIL] $name"
    cat /tmp/prepublish_match.$$
    FAIL=1
  else
    echo "[PASS] $name"
  fi
}

check_no_files() {
  local name="$1"
  local pattern="$2"
  if rg --files "$SKILL_DIR" | rg -n "$pattern" >/tmp/prepublish_files.$$ 2>/dev/null; then
    echo "[FAIL] $name"
    cat /tmp/prepublish_files.$$
    FAIL=1
  else
    echo "[PASS] $name"
  fi
}

# R1: secret-like content
check_no_match "No secret-like patterns" '(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY|Bearer[[:space:]]+[A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9_-]{20,})'

# R13: absolute paths (Unix + tilde + Windows drive)
check_no_match "No absolute machine paths" '(/Users/|~/.openclaw/|[A-Za-z]:\\\\)'

# R4: banned credential files
check_no_files "No credential files" '(^|/)(\.env(\..*)?$|\.dev\.vars(\..*)?$|.*\.pem$|id_rsa.*$|.*credentials.*$|.*cookies.*$|.*session.*$)'

# R2: NEXT_PUBLIC carrying secret-like names
if rg -n --hidden -S 'NEXT_PUBLIC_.*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)' "$SKILL_DIR" >/tmp/prepublish_public.$$ 2>/dev/null; then
  echo "[FAIL] NEXT_PUBLIC secret boundary"
  cat /tmp/prepublish_public.$$
  FAIL=1
else
  echo "[PASS] NEXT_PUBLIC secret boundary"
fi

# R3: placeholder recommendation check (warn-only)
if rg -n --hidden -S '(TOKEN=|SECRET=|PASSWORD=|API_KEY=)' "$SKILL_DIR" >/tmp/prepublish_placeholder.$$ 2>/dev/null; then
  if rg -n --hidden -S '<REDACTED>|<TOKEN>|<INGEST_TOKEN>|<READ_TOKEN>' "$SKILL_DIR" >/dev/null 2>&1; then
    echo "[PASS] Placeholder examples present"
  else
    echo "[WARN] Sensitive var names found but no obvious placeholder examples"
    cat /tmp/prepublish_placeholder.$$
  fi
else
  echo "[PASS] No sensitive var assignments found"
fi

rm -f /tmp/prepublish_match.$$ /tmp/prepublish_files.$$ /tmp/prepublish_public.$$ /tmp/prepublish_placeholder.$$ || true

if [[ "$FAIL" -ne 0 ]]; then
  echo "[RESULT] FAILED"
  exit 1
fi

echo "[RESULT] PASSED"
