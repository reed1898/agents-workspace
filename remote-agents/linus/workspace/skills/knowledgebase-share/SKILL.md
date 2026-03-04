---
name: knowledgebase-share
description: Operate a multi-agent shared knowledge layer backed by one GitHub repository. Use when setting up shared/private knowledge folders, enforcing branch+PR workflow, syncing branches, resolving merge conflicts, and standardizing how agents write/promote knowledge.
---

# Knowledgebase Share

Use this skill as the **single operating system** for multi-agent knowledge storage.

## Canonical storage

- One GitHub repo stores all knowledge data.
- Current canonical repo: `https://github.com/reed1898/agent-knowledge-layer`
- Local path (this host): `~/.openclaw/shared/agent-knowledge-layer`

## Repository model

```text
agent-knowledge-layer/
  private/<agent>/
  shared/
    00_rules/
    10_projects/
    20_research/
    30_decisions/
    40_playbooks/
    90_archive/
  meta/
  templates/
```

## Branch model

- `main`: stable shared knowledge
- `agent/<name>`: per-agent working branch
- Shared knowledge enters `main` only via PR

## Operating rules

1. Pull/rebase before writing: `git pull --rebase origin <branch>`
2. Keep private drafts in `private/<agent>/`
3. Promote reusable content to `shared/` via PR
4. Never force-push `main`
5. No secrets/tokens in repository content
6. Resolve conflicts by preserving both versions first, then refactor

## Standard flows

### A) Agent daily write (private)
1. checkout `agent/<name>`
2. write to `private/<name>/...`
3. commit + push branch

### B) Promote to shared knowledge
1. copy/refine note into `shared/...`
2. commit on `agent/<name>`
3. open PR to `main`
4. merge after review

### C) Consume latest shared knowledge
1. checkout local branch
2. `git fetch origin`
3. rebase from latest `main`

## Minimal commands

```bash
# first-time clone
git clone https://github.com/reed1898/agent-knowledge-layer.git ~/.openclaw/shared/agent-knowledge-layer

# create agent branch
cd ~/.openclaw/shared/agent-knowledge-layer
git checkout -b agent/maya

# sync branch
git pull --rebase origin agent/maya

# push updates
git push origin agent/maya
```

## Boundary

- This skill governs **knowledge layer** operations only.
- Constitution / hard governance rules are maintained in the independent constitution system.
