# MEMORY.md

<!-- AGENT_NETWORK_CONSTITUTION_INDEX:START -->
## Agent Network Constitution（Single Source of Truth）
- Canonical file: `C:\Users\RainH\.openclaw\shared\agent-network-data\AGENT_CONSTITUTION.md`
- All agents must read this file before responding in group/network contexts.
- If conflict exists between local memory notes and this constitution, constitution wins.
- Do not duplicate full constitution text in `MEMORY.md`; keep only index + effective-date notes.
- Effective baseline: AGENT_CONSTITUTION.md v1.3 (2026-03-02).
<!-- AGENT_NETWORK_CONSTITUTION_INDEX:END -->

## Preferences
- 语音转文字默认使用 `volcengine-stt` skill（用户 Reed 于 2026-03-03 明确要求）。
- 当 Reed 询问“我的持仓情况”时，必须基于数据库实时查询结果回答（数据源：`trading_notes`），禁止凭印象或猜测。
- 美股盘面分析禁止使用 stooq 快照源（时效/准确性不足，已被 Reed 明确要求移除）。

## Cron 自适应规则
- **Timeout 自动调整**：如果某个 cron 任务实际耗时超过 timeout 的 70%，主动上调 timeout（×1.5），不等超时才反应。
- **超时后自动恢复**：任务超时后，下次触发前自动检查并放大 timeout。
- **重型任务拆分**：盘前深度扫描提前执行（A股06:00、美股19:00），盘前总结只补实时数据。
- **KB 自动合并**：agent/jesse 分支积压超过 10 个 commit 时，自动 merge 到 main 并 push，不等 Reed 指示。
- Reed 明确要求：timeout 这类运维参数应该自己进化，不要让他来指定具体值。

## Trading Rules（Reed 明确指令）
- **财报前清仓原则**（2026-03-06）：Reed 明确要求财报发布前清仓股票，不赌财报。盘前扫描必须查询每只持仓的下次财报日期，5个交易日内有财报的标的需 🔴❗ 醒目预警。
- **分批止盈策略**：对基本面不确定的标的，优先分批止盈而非一次性操作。
- **美股交易时间**（2026-03-05更新）：北京时间 22:30 开盘，次日 05:00 收盘。盘前 17:00-22:30，盘后 05:00-09:00。
- **盘前个股深度扫描**（2026-03-06）：A股/美股每日开盘前必须对每只持仓做逐只深度扫描，覆盖：管理层变动、股权变动、收购并购、财报日期、分析师评级、诉讼监管、行业政策、技术面关键位。

## DB Schema Notes
- `positions` 表字段：id, account_id, symbol, quantity, average_cost, current_price, unrealized_pnl, unrealized_pnl_percent, entry_price, holding_days, is_closed, ...
- `trade_accounts` 表字段：id, user_id, account_name, account_type, broker, cash_balance, cash_currency, ...
- 查询持仓需 JOIN：`positions p JOIN trade_accounts a ON p.account_id = a.id WHERE p.is_closed=0 AND a.account_type='us_stock'`（或 'a_stock'）
- ⚠️ `positions` 表没有 account_type 字段，必须通过 JOIN trade_accounts 获取
