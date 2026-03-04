# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## Moltbook (every 4+ hours)
If 4+ hours since lastMoltbookCheck:
1) Fetch https://www.moltbook.com/heartbeat.md and follow it.
2) Also send Reed a short "Moltbook 热门速览" using **hot + 时间窗过滤**（近24小时内新增或显著上涨优先，避免长期霸榜重复）。
   - Format: title + author + score/comments + link.
   - Use Moltbook API with the stored API key.
   - IMPORTANT: only call https://www.moltbook.com/api/v1/* (with www).
3) Update lastMoltbookCheck timestamp in memory/heartbeat-state.json

## Evolver Review (every 4+ hours)
If 4+ hours since lastEvolverReviewCheck:
1) Run in workspace:
   - cd /home/ubuntu/.openclaw/workspace/skills/evolver
   - node index.js --review
2) If output includes proposed file/config changes:
   - Send Reed a Telegram approval request summary:
     - What will change (files)
     - Why
     - Risk level (low/medium/high)
     - Ask for explicit reply: 同意 / 拒绝
   - Do NOT apply changes before explicit approval.
3) If no actionable changes, stay silent (NO_REPLY).
4) Update lastEvolverReviewCheck timestamp in memory/heartbeat-state.json
