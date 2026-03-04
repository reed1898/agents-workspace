#!/usr/bin/env bash
set -euo pipefail

missing=()
for cmd in python3 git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    missing+=("$cmd")
  fi
done

has_pip=1
python3 -m pip --version >/dev/null 2>&1 || has_pip=0

has_venv=1
python3 -m venv --help >/dev/null 2>&1 || has_venv=0

if [ ${#missing[@]} -gt 0 ]; then
  echo "[缺失系统命令] ${missing[*]}"
fi

if [ "$has_pip" -eq 0 ] || [ "$has_venv" -eq 0 ] || [ ${#missing[@]} -gt 0 ]; then
  echo "\n建议一键安装（Debian/Ubuntu）："
  echo "sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git"
fi

echo "\n检查结果："
echo "- python3: $(command -v python3 >/dev/null 2>&1 && echo ok || echo missing)"
echo "- pip: $([ "$has_pip" -eq 1 ] && echo ok || echo missing)"
echo "- venv: $([ "$has_venv" -eq 1 ] && echo ok || echo missing)"

echo "\n安装 Python 包（在线分析需要）："
echo "python3 -m pip install --user --upgrade pip --break-system-packages"
echo "python3 -m pip install --user --break-system-packages yfinance pandas numpy requests"

echo "\n无法 sudo 时的降级路径（推荐）："
echo "1) curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py"
echo "2) python3 /tmp/get-pip.py --user --break-system-packages"
echo "3) python3 -m pip install --user --break-system-packages yfinance pandas numpy requests"
echo "4) 若仍失败，使用离线模式：bash scripts/analyze_stock.sh AAPL --sample"
