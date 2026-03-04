#!/usr/bin/env bash
set -euo pipefail

KB_PATH="/home/ubuntu/.openclaw/kb"
MODE="safe"   # safe|commit|status
BRANCH="main"
MSG="chore(kb): sync"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --kb) KB_PATH="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --message) MSG="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ ! -d "$KB_PATH/.git" ]]; then
  echo "ERROR: $KB_PATH is not a git repo"
  exit 2
fi

has_markers() {
  grep -R --exclude-dir=.git -nE '^(<<<<<<<|=======|>>>>>>>)' "$KB_PATH" >/dev/null 2>&1
}

if [[ "$MODE" == "status" ]]; then
  git -C "$KB_PATH" fetch origin "$BRANCH" >/dev/null 2>&1 || true
  echo "--- git status ---"
  git -C "$KB_PATH" status -sb
  exit 0
fi

# Always pull/rebase first for shared repo safety
git -C "$KB_PATH" fetch origin "$BRANCH"
git -C "$KB_PATH" pull --rebase origin "$BRANCH"

if has_markers; then
  echo "ERROR: merge markers detected. resolve before push."
  exit 3
fi

if [[ "$MODE" == "commit" ]]; then
  if [[ -n "$(git -C "$KB_PATH" status --porcelain)" ]]; then
    git -C "$KB_PATH" add -A
    git -C "$KB_PATH" commit -m "$MSG" || true
  fi
fi

# push only if local branch has commits ahead or after rebase
git -C "$KB_PATH" push origin "$BRANCH"

echo "sync complete"
