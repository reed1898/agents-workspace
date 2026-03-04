# Reed Agent OS v1 可执行清单

> 版本：v1.0  
> 日期：2026-02-24  
> 适用对象：Reed 个人 Agent 运行体系  
> 语言与输出偏好：中文；知识库落地路径 `/home/ubuntu/.openclaw/kb`；关键报告执行“双写”（Telegram + KB）

---

## 0. 目标与原则

### 0.1 目标
建立一套可持续运行、可观测、可回放的 Agent OS：
1. 日常任务自动化执行（采集、整理、提醒、汇报）
2. 所有关键输出结构化沉淀到 KB
3. 对外通知（Telegram）与内部沉淀（KB）同步一致

### 0.2 原则
- **先落地再优化**：先跑通，再提高精度与覆盖。
- **单一事实源**：KB 文件是审计与复盘依据。
- **结构化优先**：统一 Skill I/O JSON，便于串联与监控。
- **失败可恢复**：内置重试、降级、人工接管机制。

---

## 1. 目录结构建议（KB + Workspace）

> 核心：把“执行日志”“策略配置”“日报周报”分层，避免混杂。

```text
/home/ubuntu/.openclaw/
├── kb/
│   ├── 00_Inbox/                       # 临时输入、待分类材料
│   ├── 01_Daily/                       # 每日运行记录/日报
│   ├── 02_Weekly/                      # 周报、周复盘
│   ├── 03_Projects/                    # 项目专题（每项目一个目录）
│   ├── 90_Templates/                   # 模板库（日报、周报、复盘、告警）
│   ├── 99_Ops/                         # 运行文档、SOP、告警策略
│   └── metrics/                        # KPI 数据快照（json/csv）
└── workspace/
    ├── AGENTS.md
    ├── TOOLS.md
    ├── memory/
    ├── orchestrator/
    │   ├── jobs/                       # 任务定义（daily/weekly）
    │   ├── skills/                     # 各 skill 的包装与适配
    │   ├── pipelines/                  # 编排流程
    │   └── logs/                       # 运行日志（可按日切分）
    └── scripts/
        ├── write_kb_report.sh          # 落地 KB 报告
        └── send_telegram_report.sh      # 发 Telegram 报告
```

**命名约定：**
- 日报：`YYYY-MM-DD-<topic>.md`
- 周报：`YYYY-Www-<topic>.md`
- 任务日志：`run-YYYYMMDD-HHMMSS.json`

---

## 2. 统一 Skill I/O JSON 规范

> 所有 skill 输入输出统一结构，降低编排复杂度。

### 2.1 标准响应结构

```json
{
  "status": "success",
  "data": {
    "result": "...",
    "artifacts": [],
    "metrics": {}
  },
  "error": null,
  "next_action": {
    "type": "continue",
    "target": "next_skill_name",
    "reason": "数据完整，进入下一步"
  }
}
```

### 2.2 字段定义
- `status`：`success | retryable_error | fatal_error | partial_success`
- `data`：成功或部分成功的数据载荷（可为空对象，不可省略）
- `error`：失败详情（对象或 null）
  - `code`：错误码（如 `TIMEOUT`, `RATE_LIMIT`, `VALIDATION_FAILED`）
  - `message`：可读错误信息
  - `details`：上下文（HTTP 状态、异常堆栈摘要、输入片段）
- `next_action`：编排器决策建议
  - `type`：`continue | retry | fallback | escalate | stop`
  - `target`：下一 skill/流程节点
  - `reason`：决策理由

### 2.3 失败示例

```json
{
  "status": "retryable_error",
  "data": {},
  "error": {
    "code": "TIMEOUT",
    "message": "上游服务 10s 未响应",
    "details": {
      "service": "calendar_sync",
      "timeout_ms": 10000
    }
  },
  "next_action": {
    "type": "retry",
    "target": "calendar_sync",
    "reason": "超时错误可重试"
  }
}
```

---

## 3. Orchestrator 日/周任务编排模板

## 3.1 日任务模板（Daily）

**执行窗口建议（UTC）：** 01:00 / 09:00 / 16:30

1. `collect_inputs`
   - 采集：邮件摘要、日程、待办、消息摘要
2. `normalize_and_dedup`
   - 结构化、去重、优先级排序
3. `generate_daily_brief`
   - 形成中文日报（重点/风险/建议）
4. `dual_write_report`
   - 同步写入：Telegram + KB（`/home/ubuntu/.openclaw/kb/01_Daily/`）
5. `checkpoint_metrics`
   - 记录执行耗时、成功率、告警次数

**Daily 输出最小集合：**
- 当日日报 `.md`
- 运行日志 `.json`
- KPI 快照（追加写入 `kb/metrics/`）

## 3.2 周任务模板（Weekly）

**执行窗口建议（UTC）：** 每周一 02:30

1. `aggregate_daily_reports`
   - 汇总过去 7 天日报
2. `extract_weekly_kpis`
   - 计算 3 项 KPI（见第 5 节）
3. `generate_weekly_review`
   - 产出周复盘（成果/问题/下周计划）
4. `dual_write_weekly_report`
   - Telegram 摘要 + KB 全量文档（`02_Weekly`）
5. `open_action_items`
   - 生成下周待办清单（可作为 orchestrator 输入）

---

## 4. 失败重试与降级策略

## 4.1 重试策略（Retry）
- 适用：`retryable_error`（网络抖动、超时、限流）
- 策略：指数退避 + 抖动
  - 第 1 次：30s
  - 第 2 次：120s
  - 第 3 次：300s
- 最大重试次数：3 次；超过后进入降级或人工升级

## 4.2 降级策略（Fallback）
- 外部 API 不可用 → 使用最近一次缓存快照（标注“缓存数据，非实时”）
- 多源采集失败 → 仅保留核心源（如日程 + 待办）继续生成简版日报
- Telegram 发送失败 → 先确保 KB 写入成功，再排队待发送（补发任务）

## 4.3 人工升级（Escalation）
触发条件（任一满足）：
1. 同一任务连续失败 >= 3 次
2. 关键链路（写 KB）失败
3. 数据校验失败且无法自动修复

升级动作：
- 产出 `incident-YYYYMMDD-HHMM.md`
- 记录错误上下文、重试轨迹、建议处理动作
- 下次调度前先执行 `health_check`

---

## 5. KPI 定义与采集方式（3项）

## KPI-1：任务成功率（Daily Success Rate）
- 定义：`成功任务数 / 总任务数 * 100%`
- 目标：`>= 95%`
- 采集：从 orchestrator 每次运行日志提取 `status=success` 计数，按日汇总到 `kb/metrics/daily-success-rate.json`

## KPI-2：双写一致率（Telegram-KB Consistency）
- 定义：`当日已双写报告数 / 应双写报告数 * 100%`
- 目标：`= 100%`
- 采集：对比 Telegram 发送回执 ID 与 KB 文件落地记录（文件名+hash）

## KPI-3：端到端时延（E2E Report Latency）
- 定义：从任务触发到双写完成的耗时（P50/P95）
- 目标：`P50 < 3 分钟，P95 < 8 分钟`
- 采集：在 `collect_inputs` 开始与 `dual_write_report` 结束打点，写入 `kb/metrics/latency.jsonl`

---

## 6. 14 天落地计划（按天）

### Day 1
- 建立目录结构、模板文件、命名规范
- 明确日报/周报最小字段

### Day 2
- 定义 Skill I/O JSON 并在 1-2 个核心 skill 落地
- 增加基础校验器（status/data/error/next_action）

### Day 3
- 打通 Daily 主链路（采集→整理→生成日报）
- 实现本地日志落盘

### Day 4
- 接入 KB 写入模块（`01_Daily`）
- 增加写入失败告警

### Day 5
- 接入 Telegram 发送模块
- 完成首次“日报双写”

### Day 6
- 实装重试策略（指数退避 + 抖动）
- 回放 3 组失败样例

### Day 7
- 实装降级策略（缓存、简版报告）
- 验证在上游不可用时仍可出报告

### Day 8
- 建 KPI 采集管道与指标文件
- 产出首版 dashboard 数据源

### Day 9
- 梳理周任务流程（聚合日报→周复盘）
- 输出周报模板 v1

### Day 10
- 加入一致性校验（Telegram 回执 vs KB 文件 hash）
- 新增补发机制

### Day 11
- 异常分级与 incident 文档自动生成
- 打通人工接管入口

### Day 12
- 做一次全链路压测（至少 20 次任务）
- 记录瓶颈并优化

### Day 13
- 稳定性观察（成功率、时延、告警）
- 修复高频失败点 Top3

### Day 14
- 输出《v1 验收报告》与下一阶段 backlog
- 进入“稳定运行 + 周迭代”模式

---

## 7. 可直接用的 Cron 示例（>=5 条）

> 以下示例默认 Linux crontab（UTC），并在用途中标注目标。

### 7.1 早间日报生成（Daily Morning Brief）
```bash
0 1 * * * /home/ubuntu/.openclaw/workspace/scripts/run_daily_orchestrator.sh morning >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/cron.log 2>&1
```
用途：每日 01:00 生成早间简报并触发双写。

### 7.2 午间状态更新（Midday Checkpoint）
```bash
0 9 * * * /home/ubuntu/.openclaw/workspace/scripts/run_daily_orchestrator.sh midday >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/cron.log 2>&1
```
用途：每日 09:00 同步中段状态，补充上午变更。

### 7.3 傍晚收口报告（Evening Wrap-up）
```bash
30 16 * * * /home/ubuntu/.openclaw/workspace/scripts/run_daily_orchestrator.sh evening >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/cron.log 2>&1
```
用途：每日 16:30 输出收口摘要，确保日内闭环。

### 7.4 周复盘任务（Weekly Review）
```bash
30 2 * * 1 /home/ubuntu/.openclaw/workspace/scripts/run_weekly_orchestrator.sh >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/cron.log 2>&1
```
用途：每周一 02:30 汇总过去 7 天并生成周报双写。

### 7.5 双写补偿任务（Retry Telegram Delivery）
```bash
*/20 * * * * /home/ubuntu/.openclaw/workspace/scripts/retry_telegram_delivery.sh >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/retry.log 2>&1
```
用途：每 20 分钟扫描 Telegram 失败队列并补发，保障一致率。

### 7.6 健康检查任务（Health Check）
```bash
*/30 * * * * /home/ubuntu/.openclaw/workspace/scripts/health_check.sh >> /home/ubuntu/.openclaw/workspace/orchestrator/logs/health.log 2>&1
```
用途：每 30 分钟检查关键依赖、磁盘、脚本状态并在异常时告警。

---

## 8. 执行检查清单（上线前）

- [ ] 目录结构已创建且权限正确
- [ ] Skill I/O JSON 校验已启用
- [ ] Daily/Weekly 编排可独立执行
- [ ] 重试/降级/升级路径都已演练
- [ ] KPI 文件有持续写入
- [ ] Telegram + KB 双写链路通过至少 3 次真实验证

---

## 9. 下一阶段建议（v1→v1.1）

1. 引入统一任务 ID（trace_id）贯穿所有日志与报告。
2. KPI 增加“告警噪音率”和“人工接管耗时”。
3. 把高频失败场景固化为自动化回归测试。
4. 周报增加“计划-执行偏差”分析，提升决策质量。

---

**结论：** 本清单可直接作为 Reed 的 Agent OS v1 执行蓝图；优先完成双写闭环、失败可恢复、KPI 可观测三大能力，再逐步扩展自动化覆盖。