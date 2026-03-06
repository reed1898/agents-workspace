#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/Users/rain/.openclaw/workspace"
EVOLVER_DIR="$WORKSPACE/skills/evolver"
KB_DIR="/Users/rain/.openclaw/shared/agent-knowledge-layer/private/xiaohong/evolver-nightly"
LOG_DIR="$WORKSPACE/reports/evolver-nightly"
DATE_TAG="$(date +%Y-%m-%d)"
TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$LOG_DIR/$TS"
REPORT_FILE="$RUN_DIR/report.md"

mkdir -p "$RUN_DIR"
mkdir -p "$KB_DIR"

cd "$WORKSPACE"

run_round() {
  local round="$1"
  local strategy="$2"
  local round_log="$RUN_DIR/round-${round}-${strategy}.log"

  {
    echo "### Round ${round} (${strategy})"
    echo "- Started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  } >> "$REPORT_FILE"

  if EVOLVE_STRATEGY="$strategy" node "$EVOLVER_DIR/index.js" run >"$round_log" 2>&1; then
    echo "- run: success" >> "$REPORT_FILE"
  else
    echo "- run: failed" >> "$REPORT_FILE"
    echo "- log: $round_log" >> "$REPORT_FILE"
    echo >> "$REPORT_FILE"
    return 1
  fi

  # Best effort extraction: capture cycle id and hand spawn line.
  local cycle_line
  cycle_line="$(rg -m1 "Cycle #[0-9]+" "$round_log" || true)"
  local spawn_line
  spawn_line="$(rg -m1 "sessions_spawn\(" "$round_log" || true)"

  if [[ -n "$cycle_line" ]]; then
    echo "- cycle: ${cycle_line}" >> "$REPORT_FILE"
  fi
  if [[ -n "$spawn_line" ]]; then
    echo "- hand: queued" >> "$REPORT_FILE"
  fi

  echo "- log: $round_log" >> "$REPORT_FILE"
  echo >> "$REPORT_FILE"
}

{
  echo "# Night Evolver Batch Report"
  echo
  echo "- Date: $DATE_TAG"
  echo "- Started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- Workspace: $WORKSPACE"
  echo
  echo "## Plan"
  echo "1. repair-only"
  echo "2. repair-only"
  echo "3. optimize"
  echo "4. optimize"
  echo "5. innovate"
  echo
  echo "## Results"
  echo
} > "$REPORT_FILE"

# 5 rounds: repair-only*2 + optimize*2 + innovate*1
set +e
run_round 1 repair-only
sleep 3
run_round 2 repair-only
sleep 3
run_round 3 optimize
sleep 3
run_round 4 optimize
sleep 3
run_round 5 innovate
set -e

{
  echo "## Consolidated Summary"
  echo "- Finished: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- Round logs: $RUN_DIR"
  echo "- Report file: $REPORT_FILE"
} >> "$REPORT_FILE"

KB_REPORT="$KB_DIR/${DATE_TAG}-${TS}.md"
cp "$REPORT_FILE" "$KB_REPORT"

echo "REPORT_PATH=$REPORT_FILE"
echo "KB_PATH=$KB_REPORT"
