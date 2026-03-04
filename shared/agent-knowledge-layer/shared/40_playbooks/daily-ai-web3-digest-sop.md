# Daily AI/Web3 Digest SOP

## Goal
Deliver one practical daily digest for Reed (AI/Web3 first), plus 1-2 X-ready content drafts.

## Stack
- Signal collection: `skills/veille`
- Supplemental aggregation: `skills/multi-source-news-digest`
- Content shaping: `skills/social-media-management` + `skills/content-writing-thought-leadership`

## Daily Schedule (Asia/Shanghai)
- 08:30: Collect + deduplicate
- 08:35: Rank + shortlist
- 08:45: Produce Reed digest
- 09:00: Produce X post drafts

## Runbook

### 1) Collect with Veille (primary)
```bash
cd /Users/rain/.openclaw/workspace/skills/veille/scripts
python3 veille.py fetch --hours 24 --filter-seen --filter-topic > /tmp/veille-raw.json
```

### 2) Collect with Multi-source (secondary)
```bash
cd /Users/rain/.openclaw/workspace/skills/multi-source-news-digest
python3 skill.py refresh
python3 skill.py digest > /tmp/multi-digest.txt
```

### 3) Build final shortlist (manual rule)
Pick Top 10 by this order:
1. AI agent/product release with strong adoption signal
2. Web3 infra/protocol/regulation with direct market impact
3. Security/compliance event with near-term risk
4. Funding/M&A only if it changes market structure

For each selected item, keep:
- Headline
- Source URL
- One-line "why it matters"
- Tag: `AI`, `Web3`, `Security`, `Market`

### 4) Reed digest output format
Use this fixed structure:
- Must-read 3
- AI opportunities/risks
- Web3 opportunities/risks
- Today actions (max 3)

### 5) X draft generation
For 1-2 selected items, generate:
- Short post: 100-180 Chinese chars, direct POV
- Insight post: 300-500 Chinese chars, with clear stance

Guardrails:
- No weak neutral tone; must have a position
- No fake numbers; if uncertain, say uncertain
- End with one sharp question or one actionable suggestion

## Quality bar
- If fewer than 5 high-quality items, send "light day" digest, do not pad
- Every claim must be link-backed
- Avoid repeating same story from multiple sources unless angle differs

## Outputs
- Reed daily digest text
- Two X-ready drafts
- Optional archive file in workspace: `reports/daily/YYYY-MM-DD.md`
