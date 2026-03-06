#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"
VENV_PY="$VENV_DIR/bin/python"

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

parse_host_port() {
  local url="$1"
  local default_port="$2"
  "$VENV_PY" - <<'PY' "$url" "$default_port"
import sys
from urllib.parse import urlparse
url = sys.argv[1]
default_port = int(sys.argv[2])
p = urlparse(url)
host = p.hostname or "localhost"
port = p.port or default_port
print(f"{host}:{port}")
PY
}

parse_db_type() {
  local url="$1"
  "$VENV_PY" - <<'PY' "$url"
import sys
from urllib.parse import urlparse
url = sys.argv[1]
p = urlparse(url)
scheme = (p.scheme or "").split("+")[0]
print(scheme)
PY
}

parse_db_auth() {
  local url="$1"
  "$VENV_PY" - <<'PY' "$url"
import sys
from urllib.parse import urlparse
url = sys.argv[1]
p = urlparse(url)
user = p.username or ""
password = p.password or ""
print(f"{user}\t{password}")
PY
}

[[ -d "$BACKEND_DIR" ]] || fail "Missing backend directory: $BACKEND_DIR"

if [[ ! -x "$VENV_PY" ]]; then
  fail "Missing backend/venv. Create it with Python 3.11+ first."
fi

PY_VERSION="$("$VENV_PY" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
PY
)"
PY_MAJOR="${PY_VERSION%%.*}"
PY_MINOR="${PY_VERSION#*.}"
PY_MINOR="${PY_MINOR%%.*}"
if [[ "$PY_MAJOR" -lt 3 || ( "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 11 ) ]]; then
  fail "backend/venv uses Python $PY_VERSION; Python 3.11+ is required."
fi

if [[ ! -f "$BACKEND_DIR/.env" ]]; then
  if [[ -f "$BACKEND_DIR/.env.example" ]]; then
    fail "Missing backend/.env. Copy backend/.env.example to backend/.env and fill in values."
  fi
  fail "Missing backend/.env and backend/.env.example"
fi

set -a
# shellcheck disable=SC1091
source "$BACKEND_DIR/.env"
set +a

# Proxy settings (override by exporting http_proxy/https_proxy before running).
export http_proxy="${http_proxy:-http://127.0.0.1:10020}"
export https_proxy="${https_proxy:-http://127.0.0.1:10020}"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"
export no_proxy="${no_proxy:-localhost,127.0.0.1}"
export NO_PROXY="$no_proxy"

[[ -n "${DATABASE_URL:-}" ]] || fail "DATABASE_URL is not set in backend/.env"
[[ -n "${REDIS_URL:-}" ]] || fail "REDIS_URL is not set in backend/.env"

DB_TYPE="$(parse_db_type "$DATABASE_URL")"
DB_DEFAULT_PORT=5432
if [[ "$DB_TYPE" == "mysql" ]]; then
  DB_DEFAULT_PORT=3306
fi

DB_HOST_PORT="$(parse_host_port "$DATABASE_URL" "$DB_DEFAULT_PORT")"
DB_HOST="${DB_HOST_PORT%:*}"
DB_PORT="${DB_HOST_PORT##*:}"

REDIS_HOST_PORT="$(parse_host_port "$REDIS_URL" 6379)"
REDIS_HOST="${REDIS_HOST_PORT%:*}"
REDIS_PORT="${REDIS_HOST_PORT##*:}"

if [[ "$DB_TYPE" == "postgresql" || "$DB_TYPE" == "postgres" ]]; then
  if command -v pg_isready >/dev/null 2>&1; then
    if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
      warn "PostgreSQL is not ready at $DB_HOST:$DB_PORT"
      warn "Start it and rerun this script."
      exit 1
    fi
  else
    warn "pg_isready not found; checking port $DB_HOST:$DB_PORT"
    if command -v nc >/dev/null 2>&1; then
      if ! nc -z "$DB_HOST" "$DB_PORT" >/dev/null 2>&1; then
        warn "PostgreSQL port is not reachable at $DB_HOST:$DB_PORT"
        exit 1
      fi
    fi
  fi
elif [[ "$DB_TYPE" == "mysql" ]]; then
  if command -v mysqladmin >/dev/null 2>&1; then
    DB_AUTH="$(parse_db_auth "$DATABASE_URL")"
    DB_USER="${DB_AUTH%%$'\t'*}"
    DB_PASS="${DB_AUTH#*$'\t'}"
    MYSQLADMIN_CMD=(mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER")
    if [[ -n "$DB_PASS" ]]; then
      MYSQLADMIN_CMD+=("-p$DB_PASS")
    fi
    if ! "${MYSQLADMIN_CMD[@]}" >/dev/null 2>&1; then
      warn "MySQL is not ready at $DB_HOST:$DB_PORT"
      warn "Start it and rerun this script."
      exit 1
    fi
  else
    warn "mysqladmin not found; checking port $DB_HOST:$DB_PORT"
    if command -v nc >/dev/null 2>&1; then
      if ! nc -z "$DB_HOST" "$DB_PORT" >/dev/null 2>&1; then
        warn "MySQL port is not reachable at $DB_HOST:$DB_PORT"
        exit 1
      fi
    fi
  fi
else
  warn "Unknown database scheme '$DB_TYPE'; skipping DB readiness check."
fi

if command -v redis-cli >/dev/null 2>&1; then
  if ! redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping >/dev/null 2>&1; then
    warn "Redis is not responding at $REDIS_HOST:$REDIS_PORT"
    warn "Start it and rerun this script."
    exit 1
  fi
else
  warn "redis-cli not found; checking port $REDIS_HOST:$REDIS_PORT"
  if command -v nc >/dev/null 2>&1; then
    if ! nc -z "$REDIS_HOST" "$REDIS_PORT" >/dev/null 2>&1; then
      warn "Redis port is not reachable at $REDIS_HOST:$REDIS_PORT"
      exit 1
    fi
  fi
fi

check_port_free 8000

cd "$BACKEND_DIR"
"$VENV_PY" -m pip install -r requirements.txt
"$VENV_PY" -m alembic upgrade head

CELERY_LOGLEVEL="${CELERY_LOGLEVEL:-info}"
LOG_DIR="$BACKEND_DIR/logs"
LOG_FILE="$LOG_DIR/celery.log"
mkdir -p "$LOG_DIR"
echo "Starting Celery worker... (logs: $LOG_FILE)"
"$VENV_PY" -m celery -A app.core.celery_app.celery_app worker -l "$CELERY_LOGLEVEL" >>"$LOG_FILE" 2>&1 &
CELERY_PID=$!

cleanup() {
  if [[ -n "${CELERY_PID:-}" ]]; then
    kill "$CELERY_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

"$VENV_PY" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
