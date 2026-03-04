---
name: knowledgebase-share
description: Share and sync a multi-agent Obsidian knowledge base across multiple physical hosts using GitHub as the single source of truth. Use when setting up cross-machine KB sync, standardizing vault structure, configuring safe pull/rebase/push workflow, handling merge conflicts, or operating daily sync for OpenClaw agents.
---

# Knowledgebase Share

Use this skill to run a stable **Obsidian + GitHub** shared knowledge base for multiple agents across multiple machines.

## Canonical model

- Treat one GitHub repo as the canonical source of truth.
- Keep local KB path at `/home/ubuntu/.openclaw/kb` on each host.
- Keep workspace symlink compatibility (`workspace/kb -> ../kb`).
- Use append-first writing style to reduce same-line conflicts.

## Standard structure

```text
kb/
  00_Inbox/
  01_Daily/
  02_AI/
  03_Investing/
  10_Projects/
  90_Agents/
    Maya/
    Jesse/
    Linus/
```

## Required operating rules

1. Pull before write window (or before batch commit): `git pull --rebase`.
2. Commit small, frequent, scoped changes.
3. Push after successful local validation.
4. Never force-push shared KB default branch.
5. On conflict, create a `conflict-<timestamp>.md` note and preserve both versions.

## Quick commands

Run from `scripts/`:

```bash
bash scripts/init_kb_repo.sh --kb /home/ubuntu/.openclaw/kb --repo <github_repo_url>
bash scripts/sync_kb.sh --kb /home/ubuntu/.openclaw/kb --mode safe
bash scripts/sync_kb.sh --kb /home/ubuntu/.openclaw/kb --mode commit --message "chore(kb): sync"
```

## Obsidian recommendations

- Open `/home/ubuntu/.openclaw/kb` directly as the vault.
- Enable daily notes and templates, but keep generated notes under standard folders.
- Prefer one-note-per-event and append logs to avoid conflict-heavy rewrites.

## Cron pattern (OpenClaw)

Recommended schedule examples:

- Every 30 min: safe sync (`--mode safe`) for pull/rebase/push with no auto-commit.
- Every 4h: status check report (ahead/behind/conflict signals).
- Daily: integrity check (`git fsck`, path rules, orphan conflict notes).

## Safety

- Never include secrets/tokens in note content.
- Reject pushes if unresolved merge markers exist (`<<<<<<<`, `=======`, `>>>>>>>`).
- Keep recovery snapshots via lightweight tags before bulk operations.
