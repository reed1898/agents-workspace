#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: volc-stt-openclaw.sh <media-path>" >&2
  exit 1
fi

MEDIA_PATH="$1"
BASE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_SCRIPT="$BASE_DIR/skills/volcengine-stt/scripts/transcribe.sh"

if [[ ! -f "$SKILL_SCRIPT" ]]; then
  echo "volcengine-stt script not found: $SKILL_SCRIPT" >&2
  exit 1
fi

OUT_PATH="$($SKILL_SCRIPT "$MEDIA_PATH")"

if [[ -z "$OUT_PATH" || ! -f "$OUT_PATH" ]]; then
  echo "transcription output missing: $OUT_PATH" >&2
  exit 1
fi

cat "$OUT_PATH"
