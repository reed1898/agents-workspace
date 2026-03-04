#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法: $0 <symbol> [--out-dir DIR] [--sample]"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/stock_analyzer.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[错误] 未找到 python3。请先安装 Python 3。"
  exit 2
fi

python3 "${PY_SCRIPT}" "$@"
