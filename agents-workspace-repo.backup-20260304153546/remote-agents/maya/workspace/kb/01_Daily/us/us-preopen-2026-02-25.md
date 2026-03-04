# 美股开盘前持仓提醒（逐持仓深度分析）- 2026-02-25

> 数据源：trading_notes（MySQL，positions，is_closed=0，`^[A-Z]+$` 美股代码全量）+ `analyze_stock.sh` 逐持仓 JSON。
> 覆盖范围：CEG / TDY / TQQQ（3/3，全量覆盖，无抽样）。

## 【我的持仓总览】
- 持仓明细：**CEG、TDY、TQQQ**
- 持仓数量：**3 只**；合计股数：**121**
- 估算持仓成本（按 average_cost）：**$10,457.60**
- 估算持仓市值（按库内 current_price）：**$10,934.96**
- 估算浮盈：**+$477.36（+4.56%）**
- 持仓数据最近更新时间：**2026-02-09 14:25:09 UTC**（库内价格较旧，信息有限，保守判断）

## 【逐持仓结论清单】（每只1行建议）
- **CEG**：高位震荡（trend=sideways，RSI14=69.17），短线**观望为主/冲高减仓**，不追高。
- **TDY**：多头结构仍在（trend=uptrend，RSI14=68.01），**持有为主**，仅在放量确认后小幅加。
- **TQQQ**：趋势偏弱（trend=downtrend，SMA20<SMA50），优先**减仓控波动**，反弹不过压制位不加。

## 【重点新闻/事件摘要】（每只1句影响）
- **CEG**：结构化 news 为空，今晚主要交易影响来自技术位与风险偏好（信息不足，保守判断）。
- **TDY**：结构化 news 为空，若无新增事件则按趋势跟随与量价确认执行（信息不足，保守判断）。
- **TQQQ**：结构化 news 为空，核心仍是纳指方向与波动放大效应（信息不足，保守判断）。

## 【今晚操作计划】（加仓/减仓/清仓/观望触发条件）
- **CEG（现价312.64，SMA20=280.89，SMA50=316.41）**
  - 加仓触发：放量站上并稳住 **316.4（SMA50）**。
  - 减仓触发：冲高回落且15-30分钟失守 **312-316 区间**。
  - 清仓触发：放量跌破当日关键低点且1小时内无法收复。
  - 观望条件：量能不足、上下影拉扯明显。

- **TDY（现价683.22，SMA20=646.42，SMA50=583.58）**
  - 加仓触发：放量突破日内新高并回踩不破。
  - 减仓触发：跌破 **646（SMA20）** 且反抽不过。
  - 清仓触发：放量跌破前低并持续弱于行业/指数。
  - 观望条件：高位缩量横盘、波动收敛。

- **TQQQ（现价49.78，SMA20=51.24，SMA50=52.79）**
  - 加仓触发：仅当放量重回 **51.2** 上方并站稳（激进仓位≤5%）。
  - 减仓触发：反弹无量、在 **51.2/52.8** 下方受压。
  - 清仓触发：放量跌破日内关键低点或纳指转弱共振下行。
  - 观望条件：方向不明时不加杠杆，优先控回撤。

---
执行说明：已逐一调用 `bash /home/ubuntu/.openclaw/workspace/skills/stock_analysis/scripts/analyze_stock.sh <symbol>`，并读取 JSON 的 valuation / technical / news / risks / catalysts / scores / conclusion 字段；news 缺失项均按“信息不足，保守判断”。

JSON输出路径：
- CEG: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/CEG_20260225T140211Z.json`
- TDY: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TDY_20260225T140213Z.json`
- TQQQ: `/home/ubuntu/.openclaw/workspace/skills/stock_analysis/outputs/TQQQ_20260225T140214Z.json`
