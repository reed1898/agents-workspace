#!/bin/bash
# Apply openclaw patches after npm update
# Usage: bash ~/.openclaw/patches/apply.sh

OPENCLAW_DIR=$(dirname "$(readlink -f "$(which openclaw)")")/../lib/node_modules/openclaw
if [ ! -d "$OPENCLAW_DIR" ]; then
  OPENCLAW_DIR=/opt/homebrew/lib/node_modules/openclaw
fi

TARGET="$OPENCLAW_DIR/node_modules/@buape/carbon/dist/src/classes/RequestClient.js"
PATCH_FILE="$HOME/.openclaw/patches/carbon-proxy.patch"

if [ ! -f "$TARGET" ]; then
  echo "ERROR: $TARGET not found"
  exit 1
fi

# Check if already patched
if grep -q "_readDiscordProxyFromConfig" "$TARGET"; then
  echo "Already patched, skipping."
  exit 0
fi

if [ ! -f "$PATCH_FILE" ]; then
  echo "ERROR: patch file not found: $PATCH_FILE"
  exit 1
fi

if ! command -v patch >/dev/null 2>&1; then
  echo "ERROR: 'patch' command not found."
  exit 1
fi

if ! patch --dry-run -p1 -d "$OPENCLAW_DIR" < "$PATCH_FILE" >/dev/null 2>&1; then
  echo "ERROR: patch dry-run failed (version mismatch or already partially patched)."
  exit 1
fi

patch -p1 -d "$OPENCLAW_DIR" < "$PATCH_FILE" >/dev/null

# Verify
if grep -q "_readDiscordProxyFromConfig" "$TARGET"; then
  echo "Patch applied successfully to $TARGET"
else
  echo "ERROR: Patch failed"
  exit 1
fi
