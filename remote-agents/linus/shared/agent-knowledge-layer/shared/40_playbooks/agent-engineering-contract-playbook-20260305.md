# Agent Engineering Contract Playbook (for Reed)

> Source basis: systematicls《How To Be A World-Class Agentic Engineer》+ current OpenClaw workflow practice
> Created: 2026-03-05

## 1) Task Contract First (before any implementation)

For each task, write one compact contract:

- Goal: what "done" means in one sentence
- Scope: what is in / out
- Stack decision: exact approach (no open-ended research in implement phase)
- Acceptance:
  - tests pass
  - key logs/screenshots attached
  - change summary + rollback note

Template:

```md
Task: <name>
Goal: <single concrete outcome>
In scope: <A,B,C>
Out of scope: <X,Y>
Implementation decision: <exact stack/approach>
Acceptance: [ ] tests pass [ ] evidence attached [ ] summary + rollback
```

## 2) Split Research and Implementation

- Session A: research options + choose one decision
- Session B (fresh context): implement only the chosen decision
- Never mix "explore all options" with "ship now" in the same execution context

## 3) Prompting Rule (reduce sycophancy)

- Avoid: "find bugs" / "prove this is wrong"
- Prefer neutral: "trace logic and report all findings with confidence"
- Require evidence line per finding: file + line + why it matters

## 4) Completion Gate (hard stop)

A task is not complete unless all are true:

1. Contract acceptance items all checked
2. No unresolved failing tests
3. No "TODO later" left in critical paths
4. One-paragraph delivery note for handoff

## 5) Session Strategy

- One contract = one focused session
- Long 24h sessions only for monitoring/orchestration, not for core implementation
- If context gets noisy: compact + re-read only contract + relevant files

## 6) Weekly Hygiene (30 min)

- Merge duplicated rules
- Remove contradictory rules
- Archive stale skills
- Keep only high-frequency, high-ROI skills active

## 7) Reed-specific quick defaults

- Preference: concise, no fluff, no performative wording
- Reporting style: conclusion first, then evidence
- Time expectation: always include ETA/risk when task may slip

---

## Fast Use

When starting a new build task, copy section 1 template and fill it in first. Then run section 2 workflow.
