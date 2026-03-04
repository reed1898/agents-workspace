# Reed Agent OS v1 实施记录（Day6-7：可靠性与补偿机制）

- 日期：2026-02-24
- 范围：Day6-7（失败可重试、双写可校验、发送可补偿）
- 执行位置：`/home/ubuntu/.openclaw/workspace/ops/reed-agent-os`
- 安全约束：未改敏感配置；验证以 dry-run/失败模拟为主；未发送真实外部消息

## 1) 改动清单

### A. `scripts/orchestrate_daily.py`（增量改造）
新增能力：
- 加入统一重试封装 `run_with_retry(...)`
- 指数退避：`backoff = base * 2^(attempt-1)`
- 最大重试次数：默认 `--max-attempts 3`
- 错误分类：`retryable / fatal / none`
  - `generate_daily_summary`：失败视为 fatal
  - `write_kb`：返回码 2/3/4/5 视为 fatal
  - `send_telegram`：基于 rc / stderr 关键字分类（timeout/rate-limit/network 等为 retryable）
- run report 增强：每个 step 记录 `attempts[]`、`attempt_count`、`final_error_class`

### B. `scripts/send_telegram.py`（补偿入队 + 回执增强）
新增能力：
- 新增参数：
  - `--queue-dir`（失败待补偿目录）
  - `--receipt-path`（显式回执路径）
  - `--attempt`（尝试次数）
  - `--run-id`（链路追踪）
- 回执新增字段：`attempt`、`error_class`、`queued_pending`
- 发送失败时自动写入：`queue/telegram_pending/telegram-pending-*.json`
  - 包含：`attempt/next_attempt/error_class/last_error/account_id/target/text`

### C. 新增 `scripts/replay_telegram_queue.py`
功能：
- 扫描 `queue/telegram_pending/*.json`
- 默认 `--dry-run`（只演示重放计划，不外发）
- `--no-dry-run` 时调用 `send_telegram.py` 重放
- 成功重放后将任务移动至：`queue/telegram_sent/`
- 输出重放汇总日志：`logs/replay-telegram-queue-*.json`

### D. 新增 `scripts/verify_dual_write.py`
功能：
- 校验 run report 完整性（必备 steps + artifacts）
- 校验 KB 文件存在（通过 kb_receipt target 反查）
- 校验 Telegram 回执存在且 success=true
- 输出一致性 JSON：`pass/fail + reasons + checks`

### E. 目录补充
已创建：
- `ops/reed-agent-os/queue/telegram_pending/`
- `ops/reed-agent-os/state/`
- （附加）`ops/reed-agent-os/queue/telegram_sent/`（重放成功归档）

---

## 2) 验证结果（至少 3 条）

### 验证 a) 模拟 Telegram 失败并进入 pending queue
命令：
```bash
python3 scripts/send_telegram.py \
  --text "[day6-7] simulate failure enqueue" \
  --target telegram:invalid_target \
  --no-dry-run
```
关键输出：
- `ERROR send failed rc=1 class=fatal`
- `queued pending task: .../queue/telegram_pending/telegram-pending-20260224-171653.json`
- `receipt written: .../logs/telegram-receipt-20260224-171653.json`

结论：失败可落队，补偿入口生效。

### 验证 b) replay_telegram_queue.py（dry-run）
命令：
```bash
python3 scripts/replay_telegram_queue.py --dry-run
```
关键输出：
- `dry_run=True queue_count=1`
- `DRY-RUN replay telegram-pending-20260224-171653.json -> telegram:invalid_target attempt=2`
- `summary written: .../logs/replay-telegram-queue-20260224-171655.json`

结论：重放扫描与任务解析逻辑正常，默认无外发。

### 验证 c) verify_dual_write.py 输出一致性结果
准备命令（生成含失败 Telegram 的 run report）：
```bash
python3 scripts/orchestrate_daily.py \
  --phase evening \
  --topic day6-7-reliability \
  --no-dry-run \
  --target telegram:invalid_target \
  --max-attempts 3 \
  --retry-base-seconds 0.2
```
校验命令：
```bash
python3 scripts/verify_dual_write.py \
  --report reports/run-report-20260224-171658.json \
  --pretty
```
关键输出（节选）：
```json
{
  "pass": false,
  "reasons": ["telegram receipt exists but success=false"],
  "checks": {
    "run_report_complete": true,
    "kb_file_exists": true,
    "telegram_receipt_exists": true,
    "telegram_receipt_success": false
  }
}
```

结论：双写校验能准确识别“KB 成功、Telegram 失败”的不一致状态。

---

## 3) 已知限制

1. 当前 `send_telegram.py` 真实发送路径依赖本机 `openclaw message send` CLI 参数兼容；若 CLI 版本参数差异，会直接失败并入队。
2. `retryable/fatal` 目前基于返回码和关键字启发式分类，后续可接入更稳定的错误码映射表。
3. `verify_dual_write.py` 当前校验“文件存在 + 回执 success”，尚未引入 KB 内容 hash 与 Telegram message_id 级对账。

## 4) Day8-10 建议

1. 将 KPI 采集从 skeleton 升级为真实解析：成功率、双写一致率、E2E 时延（P50/P95）。
2. 在双写校验中加入 `KB hash <-> Telegram receipt(message_id)` 的强一致对账。 
3. 增加失败场景回归样例（timeout/rate-limit/network）以覆盖 retryable 路径并做自动测试。
