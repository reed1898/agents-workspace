#!/bin/bash
# Apply openclaw patches after npm update
# Usage: bash ~/.openclaw/patches/apply.sh
#
# Patches @buape/carbon RequestClient.js to route Discord REST API
# calls through the proxy configured in openclaw.json (channels.discord.proxy).

OPENCLAW_DIR=$(dirname "$(readlink -f "$(which openclaw)")")/../lib/node_modules/openclaw
if [ ! -d "$OPENCLAW_DIR" ]; then
  OPENCLAW_DIR=/opt/homebrew/lib/node_modules/openclaw
fi
if [ ! -d "$OPENCLAW_DIR" ]; then
  OPENCLAW_DIR=/usr/local/lib/node_modules/openclaw
fi

TARGET="$OPENCLAW_DIR/node_modules/@buape/carbon/dist/src/classes/RequestClient.js"

if [ ! -f "$TARGET" ]; then
  echo "ERROR: $TARGET not found"
  exit 1
fi

# Remove old patch if present (re-apply cleanly)
if grep -q "_ocConfig" "$TARGET"; then
  echo "Removing old patch..."
  # Restore from backup if available, otherwise strip patch lines
  if [ -f "${TARGET}.orig" ]; then
    cp "${TARGET}.orig" "$TARGET"
  else
    sed -i '' '/^import { ProxyAgent } from "undici";$/d' "$TARGET"
    sed -i '' '/^import { readFileSync } from "node:fs";$/d' "$TARGET"
    sed -i '' '/^import { join } from "node:path";$/d' "$TARGET"
    sed -i '' '/^import { homedir } from "node:os";$/d' "$TARGET"
    sed -i '' '/^const _ocConfig/d' "$TARGET"
    sed -i '' '/^const _proxyUrl/d' "$TARGET"
    sed -i '' '/^const _proxyDispatcher/d' "$TARGET"
    # Remove dispatcher spread from fetch call
    sed -i '' 's/, \.\.\.(_proxyDispatcher ? { dispatcher: _proxyDispatcher } : {})//' "$TARGET"
  fi
elif grep -q "_proxyDispatcher" "$TARGET"; then
  echo "Removing legacy patch..."
  sed -i '' '/^import { ProxyAgent } from "undici";$/d' "$TARGET"
  sed -i '' '/^const _proxyUrl/d' "$TARGET"
  sed -i '' '/^const _proxyDispatcher/d' "$TARGET"
  sed -i '' 's/, \.\.\.(_proxyDispatcher ? { dispatcher: _proxyDispatcher } : {})//' "$TARGET"
fi

# Save a clean backup
cp "$TARGET" "${TARGET}.orig"

# Apply: add imports and proxy config reader after line 2
PATCH_LINES='import { ProxyAgent } from "undici";\
import { readFileSync } from "node:fs";\
import { join } from "node:path";\
import { homedir } from "node:os";\
const _ocConfig = (() => { try { return JSON.parse(readFileSync(join(homedir(), ".openclaw", "openclaw.json"), "utf8")); } catch { return {}; } })();\
const _proxyUrl = _ocConfig?.channels?.discord?.proxy || process.env.https_proxy || process.env.HTTPS_PROXY || process.env.http_proxy || process.env.HTTP_PROXY || "";\
const _proxyDispatcher = _proxyUrl ? new ProxyAgent(_proxyUrl) : null;'

sed -i '' "2a\\
${PATCH_LINES}
" "$TARGET"

# Add dispatcher to fetch call
sed -i '' 's/signal: this.abortController.signal$/signal: this.abortController.signal, ...(_proxyDispatcher ? { dispatcher: _proxyDispatcher } : {})/' "$TARGET"

# Verify
if grep -q "_proxyDispatcher" "$TARGET" && grep -q "_ocConfig" "$TARGET"; then
  echo "Patch applied successfully to $TARGET"
  echo "Proxy: reads channels.discord.proxy from ~/.openclaw/openclaw.json"
else
  echo "ERROR: Patch failed"
  [ -f "${TARGET}.orig" ] && cp "${TARGET}.orig" "$TARGET"
  exit 1
fi
