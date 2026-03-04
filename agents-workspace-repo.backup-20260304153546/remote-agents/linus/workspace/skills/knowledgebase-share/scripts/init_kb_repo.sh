#!/usr/bin/env bash
set -euo pipefail

KB_PATH="/home/ubuntu/.openclaw/kb"
REPO_URL=""
BRANCH="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --kb) KB_PATH="$2"; shift 2 ;;
    --repo) REPO_URL="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO_URL" ]]; then
  echo "ERROR: --repo <github_repo_url> required"
  exit 1
fi

mkdir -p "$KB_PATH"
if [[ ! -d "$KB_PATH/.git" ]]; then
  git -C "$KB_PATH" init
fi

git -C "$KB_PATH" remote remove origin >/dev/null 2>&1 || true
git -C "$KB_PATH" remote add origin "$REPO_URL"

git -C "$KB_PATH" checkout -B "$BRANCH"

echo "Initialized KB repo"
echo "kb=$KB_PATH"
echo "origin=$REPO_URL"
echo "branch=$BRANCH"
