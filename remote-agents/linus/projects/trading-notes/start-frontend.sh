#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

warn() {
  echo "WARNING: $*" >&2
}

require_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || fail "Missing required command: $cmd"
}

check_port_free() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    if lsof -iTCP:"$port" -sTCP:LISTEN -n -P >/dev/null 2>&1; then
      echo "ERROR: Port $port is already in use:" >&2
      lsof -iTCP:"$port" -sTCP:LISTEN -n -P >&2 || true
      exit 1
    fi
  elif command -v nc >/dev/null 2>&1; then
    if nc -z localhost "$port" >/dev/null 2>&1; then
      fail "Port $port is already in use"
    fi
  fi
}

[[ -d "$FRONTEND_DIR" ]] || fail "Missing frontend directory: $FRONTEND_DIR"

require_cmd node
require_cmd npm

if [[ ! -f "$FRONTEND_DIR/.env.local" ]]; then
  warn "Missing frontend/.env.local. See QUICKSTART.md for required values."
fi

check_port_free 3000

cd "$FRONTEND_DIR"
if [[ ! -d "node_modules" ]]; then
  npm install
fi

exec npm run dev
