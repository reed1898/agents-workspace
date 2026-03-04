# 美股开盘前持仓提醒（逐持仓深度分析）- 2026-02-24

> 数据源：trading_notes（MySQL，us_stock，is_closed=0，美股代码全量）+ `analyze_stock.sh` 逐持仓 JSON。
> 覆盖范围：CEG / TDY / TQQQ（3/3，全量覆盖，无抽样）。

## 【我的持仓总览】
- 持仓明细：**CEG、TDY、TQQQ**
- 持仓数量：**3 只**；合计股数：**121**
- 估算持仓市值（按库内 current_price）：**$10,934.96**
- 估算持仓成本（按 average_cost）：**$10,457.60**
- 持仓数据最近更新时间：**2026-02-09 14:25:08 UTC**（若与盘前行情有偏差，保守判断）。

## 【逐持仓结论清单】（每只1行建议）
- **CEG**：持有为主，回踩确认可小加（总分68.6，trend=sideways）。
- **TDY**：持有为主，回踩确认可小加（总分60.5，trend=uptrend）。
- **TQQQ**：减仓/观望，先控风险（总分56.3，trend=downtrend）。

## 【重点新闻/事件摘要】（每只1句影响）
- **CEG**：结构化新闻为空，短线主要跟随技术位与市场风险偏好（信息不足，保守判断）。
- **TDY**：结构化新闻为空，短线主要跟随技术位与市场风险偏好（信息不足，保守判断）。
- **TQQQ**：结构化新闻为空，短线主要跟随技术位与市场风险偏好（信息不足，保守判断）。

## 【今晚操作计划】（加仓/减仓/清仓/观望触发条件）
- **CEG（SMA20=279.52，SMA50=317.4，RSI14=61.6，trend=sideways）**
  - 加仓触发：放量突破关键均线（优先SMA20）并站稳。
  - 减仓触发：冲高回落且失守SMA20，或弱势反抽不过前高。
  - 清仓触发：放量跌破前低/风控线且30-60分钟无法收复。
  - 观望条件：量能不足、方向不明时等待确认（保守判断）。

- **TDY（SMA20=642.64，SMA50=580.24，RSI14=71.88，trend=uptrend）**
  - 加仓触发：放量突破关键均线（优先SMA20）并站稳。
  - 减仓触发：冲高回落且失守SMA20，或弱势反抽不过前高。
  - 清仓触发：放量跌破前低/风控线且30-60分钟无法收复。
  - 观望条件：量能不足、方向不明时等待确认（保守判断）。

- **TQQQ（SMA20=51.5，SMA50=52.93，RSI14=33.49，trend=downtrend）**
  - 加仓触发：放量突破关键均线（优先SMA20）并站稳。
  - 减仓触发：冲高回落且失守SMA20，或弱势反抽不过前高。
  - 清仓触发：放量跌破前低/风控线且30-60分钟无法收复。
  - 观望条件：量能不足、方向不明时等待确认（保守判断）。

---
执行说明：已逐一调用 `analyze_stock.sh <symbol>` 并读取 JSON 的 valuation / technical / news / risks / catalysts / scores / conclusion 字段；新闻缺失项按“信息不足，保守判断”处理。

JSON输出路径：
- CEG: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/CEG_20260224T140234Z.json`
- TDY: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TDY_20260224T140235Z.json`
- TQQQ: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TQQQ_20260224T140236Z.json`
