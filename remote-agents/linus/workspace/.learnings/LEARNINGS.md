# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---

## [LRN-20260307-001] best_practice

**Logged**: 2026-03-07T10:35:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
Self-improvement outputs were not visible because workspace-level `.learnings/` was missing.

### Details
The skill existed under `skills/self-improving-agent/`, but no shared `.learnings/` directory was present at workspace root. As a result, there was no obvious place to inspect latest logs during daily usage, creating the impression that the skill had no recent result.

### Suggested Action
Always initialize workspace-level `.learnings/` during setup and verify scripts with one positive run (activator) and one simulated error run (error-detector).

### Metadata
- Source: conversation
- Related Files: .learnings/LEARNINGS.md, .learnings/ERRORS.md, .learnings/FEATURE_REQUESTS.md
- Tags: self-improvement, visibility, setup, workspace

### Resolution
- **Resolved**: 2026-03-07T10:32:00+08:00
- **Notes**: Created workspace `.learnings/` and validated both self-improving-agent scripts.

---

