# 美股开盘前持仓提醒（逐持仓深度分析）- 2026-02-23

> 数据源：trading_notes（MySQL，positions，is_closed=0，美股代码全量）+ `analyze_stock.sh` 逐持仓 JSON。
> 覆盖范围：CEG / TDY / TQQQ（3/3，全量覆盖，无抽样）。

## 【我的持仓总览】
- 持仓明细：**CEG、TDY、TQQQ**
- 持仓数量：**3 只**；合计股数：**121**
- 估算持仓市值（按库内 current_price）：**$11,181.96**
- 估算持仓成本（按 average_cost）：**$10,457.31**
- 持仓数据最近更新时间：**2026-02-09 14:25:09 UTC**（存在时效滞后，**保守判断**）。

## 【逐持仓结论清单】（每只1行建议）
- **CEG**：综合中性偏多（总分68.6，trend=sideways），仅在放量突破再小步加仓；否则以观望为主（保守判断）。
- **TDY**：综合中性偏多（总分60.5，trend=uptrend），可继续持有，回踩不破SMA20再考虑小幅加仓（保守判断）。
- **TQQQ**：综合偏弱（总分56.3，trend=downtrend），未收复SMA20前优先风控，反弹受阻可减仓（保守判断）。

## 【重点新闻/事件摘要】（每只1句影响）
- **CEG**：结构化新闻字段为空，短线主要由技术位与市场风险偏好驱动（信息不足，保守判断）。
- **TDY**：结构化新闻字段为空，当前上行结构仍在但估值不低，追高性价比一般（信息不足，保守判断）。
- **TQQQ**：结构化新闻字段为空，作为高杠杆ETF对纳指波动敏感，盘初方向选择决定当晚收益波动（信息不足，保守判断）。

## 【今晚操作计划】（加仓/减仓/清仓/观望触发条件）
- **CEG（SMA20=279.28，SMA50=318.70，RSI14=56.58）**
  - 加仓触发：放量站上并稳定于SMA20上方。
  - 减仓触发：冲高回落且再度跌回SMA20下方。
  - 清仓触发：有效跌破前低/风控线且30-60分钟无法收复。
  - 观望条件：横盘震荡（sideways）且量能不足。

- **TDY（SMA20=639.55，SMA50=577.05，RSI14=67.47）**
  - 加仓触发：回踩SMA20不破并重新放量上攻。
  - 减仓触发：高位放量滞涨或跌破SMA20并弱反抽。
  - 清仓触发：趋势失效（连续失守关键均线并无法收回）。
  - 观望条件：接近高位且量价背离信号出现。

- **TQQQ（SMA20=51.81，SMA50=53.08，RSI14=40.18）**
  - 加仓触发：至少收复SMA20并出现连续强势K线确认。
  - 减仓触发：反弹至SMA20附近受阻或跌破当日关键支撑。
  - 清仓触发：放量跌破前低且纳指同步走弱。
  - 观望条件：弱势震荡、方向不明时不抢反弹。

---
执行说明：已严格按要求逐一调用 `analyze_stock.sh <symbol>` 并读取 JSON 的 valuation / technical / news / risks / catalysts / scores / conclusion 字段；新闻缺失部分统一按“信息不足，保守判断”处理。

JSON输出路径：
- CEG: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/CEG_20260223T140142Z.json`
- TDY: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TDY_20260223T140143Z.json`
- TQQQ: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TQQQ_20260223T140144Z.json`
