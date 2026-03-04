---
name: trading-journal
description: Save and retrieve trading insights/summaries to the OpenClaw workspace (Git-synced) as structured Markdown entries. Use when the user says “记录交易感悟/总结/复盘/规则/错误”, wants to search past insights, or wants a weekly digest.
---

# Trading Journal (Git-synced)

Goal: capture short trading insights quickly, store them in the workspace (so `claw-roam` syncs across devices), and make them easy to search and reuse later.

## Files

- Raw log: `~/.openclaw/workspace/trading/insights.md`
- Distilled rules: `~/.openclaw/workspace/trading/rules.md`

## Quick capture (recommended)

Use the helper command (installed as `trade-log`):

```bash
trade-log add "你的感悟..." --tags "心理,执行" --style "A,B" --type insight
```

Types:
- `insight` (默认)
- `summary`
- `rule`
- `mistake`
- `review`

Styles (optional):
- `A` = 日内/短线
- `B` = 波段/趋势

## Search / list

```bash
trade-log recent 20
trade-log search "追涨" --limit 20
trade-log week
trade-log digest-week --out ./trading/weekly-digest.md
trade-log stats
```

## Workflow when user chats (LLM auto-classify + minimal confirmation)

Mode A: When the user sends any trading-related message (even without a prefix), treat it as a candidate journal entry.

### Trading-related detection (heuristic, prefer recall)

Default: **err on the side of saving** if the message contains any of:
- common symbols: BTC/ETH/QQQ/SPY/NQ/ES/HSI/恒生/A股/上证/深证/创业板/期货/期权
- trading words: 交易/入场/出场/止损/止盈/仓位/回撤/趋势/波段/日内/做多/做空/突破/回踩/确认/复盘/情绪/FOMO

Do **not** save if:
- the user explicitly says “不记录/别记/只是闲聊”

### Capture
1) Use the LLM to infer:
   - type: insight|summary|rule|mistake|review
   - style: A (日内/短线) and/or B (波段/趋势)
   - tags: short comma-separated Chinese tags (3-8)
   - (optional) symbol / tf if mentioned
   - one-liner summary for search
2) Append via:

```bash
trade-log add "<raw>" --tags "<tags>" --style "<style>" --type "<type>" --one "<one>" [--symbol XXX] [--tf XXX]
```

3) Reply by **echoing the saved entry** (markdown block) so the user can see exactly what was stored.
- Show ONLY the entry just saved (header + metadata + raw), not the whole file.

4) Then add a **short commentary** on the insight (2-6 bullets):
- Make it more executable (what to do next time)
- Add boundary conditions / common traps
- If relevant, give a 5-second pre-trade checklist

5) Ask at most 1 clarifying question only when categorization is ambiguous.

### Retrieval (chat)
If the user asks “查一下/搜索/最近几条/上周总结”，use:
- `trade-log search`
- `trade-log recent`
- `trade-log week`
- `trade-log digest-week`

Then summarize results in chat.

## Weekly digest (manual)

When asked to do a weekly digest:
1) Filter entries by date range (grep timestamps)
2) Deduplicate similar items
3) Propose 3-10 distilled rules to move into `trading/rules.md`
