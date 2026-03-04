#!/usr/bin/env bash
set -euo pipefail

# Sync ~/.openclaw into a dedicated git repo, excluding logs/session data.
SRC_DIR="${HOME}/.openclaw"
REPO_DIR="${HOME}/.openclaw/agents-workspace-repo"
STAGE_DIR="${HOME}/.openclaw/.sync-staging"
REMOTE_URL="git@github.com:reed1898/agents-workspace.git"
BRANCH="main"

mkdir -p "${STAGE_DIR}"

if [ ! -d "${REPO_DIR}/.git" ]; then
  git clone "${REMOTE_URL}" "${REPO_DIR}"
fi

# Keep local branch aligned with remote if it already exists.
if git -C "${REPO_DIR}" ls-remote --exit-code --heads origin "${BRANCH}" >/dev/null 2>&1; then
  git -C "${REPO_DIR}" fetch origin "${BRANCH}"
  git -C "${REPO_DIR}" checkout "${BRANCH}" 2>/dev/null || git -C "${REPO_DIR}" checkout -b "${BRANCH}" "origin/${BRANCH}"
  git -C "${REPO_DIR}" pull --rebase origin "${BRANCH}"
else
  git -C "${REPO_DIR}" checkout -B "${BRANCH}"
fi

rsync -a --delete \
  --exclude "logs/" \
  --exclude "**/logs/" \
  --exclude "session/" \
  --exclude "sessions/" \
  --exclude "session-logs/" \
  --exclude "**/session/" \
  --exclude "**/sessions/" \
  --exclude "**/session-logs/" \
  --exclude "credentials/" \
  --exclude "**/credentials/" \
  --exclude "openclaw.json" \
  --exclude "openclaw.json.*" \
  --exclude "**/openclaw.json" \
  --exclude "**/openclaw.json.*" \
  --exclude "**/auth-profiles.json" \
  --exclude "agents-workspace-repo/" \
  --exclude ".sync-staging/" \
  --exclude ".git/" \
  "${SRC_DIR}/" "${STAGE_DIR}/"

rsync -a --delete --exclude ".git/" "${STAGE_DIR}/" "${REPO_DIR}/"

if [ ! -f "${REPO_DIR}/.gitignore" ]; then
  cat > "${REPO_DIR}/.gitignore" <<'EOF'
logs/
**/logs/
session/
sessions/
session-logs/
**/session/
**/sessions/
**/session-logs/
credentials/
**/credentials/
openclaw.json
openclaw.json.*
**/openclaw.json
**/openclaw.json.*
**/auth-profiles.json
EOF
fi

git -C "${REPO_DIR}" add -A
if ! git -C "${REPO_DIR}" diff --cached --quiet; then
  git -C "${REPO_DIR}" commit -m "sync openclaw workspace $(date '+%Y-%m-%d %H:%M:%S')"
  git -C "${REPO_DIR}" push origin "${BRANCH}"
else
  echo "No changes to sync."
fi
