# Reed Agent OS v1 实施记录（Day8-10：参数兼容修复 + 一致性强化 + 可靠性收口）

- 日期：2026-02-24
- 执行位置：`/home/ubuntu/.openclaw/workspace/ops/reed-agent-os`
- 约束执行：未改敏感配置；默认 dry-run；失败模拟使用 invalid target，无真实外发成功

## 1) 改动清单

### A. `scripts/send_telegram.py`
1. 新增 openclaw CLI 参数兼容探测：
   - 自动执行：`openclaw message send --help`
   - 识别并选择参数：
     - account: `--account-id` / `--accountId`
     - target: `--target` / `--to`
     - message: `--message` / `--text`
2. 探测结果缓存：`state/cli_capabilities.json`
3. 统一错误分类：接入 `config/error-classifier.json`
4. receipt 增强：
   - `message_id`
   - `reconciliation.message_id_check`（`available/missing/skipped_dry_run`）
   - `cli_capabilities_path`

### B. `config/error-classifier.json`（新增）
- 配置化 retryable/fatal 映射：
  - `exit_codes`
  - `stderr_keywords`
  - `step_overrides`（`generate_daily_summary` 强制 fatal，`write_kb` 指定 fatal rc）

### C. `scripts/error_classifier.py`（新增）
- 封装可复用分类器：`classify(step_name, returncode, stderr)`
- 已在 `orchestrate_daily.py` + `send_telegram.py` 使用

### D. `scripts/orchestrate_daily.py`
- 移除硬编码分类逻辑，改为配置驱动
- run report 增加：
  - `classifier_config`
  - `artifacts.cli_capabilities`

### E. `scripts/write_kb.py`
- receipt 增加 `sha256`（markdown 内容 hash）

### F. `scripts/verify_dual_write.py`
新增校验：
1. KB hash 校验（`kb_receipt.sha256` vs 文件 sha256）
2. Telegram `message_id` 对账：
   - dry-run => `skipped_dry_run`
   - 非 dry-run 且 success=true 时要求 `message_id`
3. 输出增强：
   - 人类摘要（`PASS/FAIL + reasons`）
   - 机器可读 JSON（`--output`）

### G. `README.md`
补充：
- Day8-10 能力说明
- 常见故障排查
- 验收标准清单

---

## 2) 验证命令与关键输出

### 验证 a) 全 dry-run 成功链路
命令：
```bash
python3 scripts/orchestrate_daily.py \
  --phase morning \
  --topic day8-10-smoke-a \
  --max-attempts 2 \
  --retry-base-seconds 0.2
```
关键输出：
- `[orchestrate_daily] success=True`
- `report=/.../reports/run-report-20260224-172113.json`

说明：主链路 dry-run 可跑通。

### 验证 b) 模拟失败并入队
命令：
```bash
python3 scripts/send_telegram.py \
  --text "[day8-10] simulate failure enqueue" \
  --target telegram:invalid_target \
  --no-dry-run
```
关键输出：
- `ERROR send failed rc=1 class=fatal`
- `queued pending task: .../queue/telegram_pending/telegram-pending-20260224-172117.json`
- `receipt written: .../logs/telegram-receipt-20260224-172117.json`

说明：失败后可自动入队，receipt/queue 闭环有效。

### 验证 c) replay 后状态变化验证
1) 先 dry-run replay：
```bash
python3 scripts/replay_telegram_queue.py --dry-run
```
关键输出：
- `dry_run=True queue_count=3`
- `DRY-RUN replay ... attempt=2`

2) 再执行一次 no-dry-run（limit=1，仍用 invalid target）：
```bash
python3 scripts/replay_telegram_queue.py --no-dry-run --limit 1
```
关键输出：
- `dry_run=False queue_count=1`
- `replayed failed, keep in queue: ...telegram-pending-20260224-171653.json`
- 新增 pending：`queue/telegram_pending/telegram-pending-20260224-172133.json`

状态变化：
- replay 后 pending 计数变化（新增重试任务），失败任务保留，符合补偿队列语义。

### 验证 d) verify 增强项（KB hash + message_id 对账 + JSON 输出）
命令：
```bash
python3 scripts/orchestrate_daily.py \
  --phase evening \
  --topic day8-10-smoke-c \
  --no-dry-run \
  --target telegram:invalid_target \
  --max-attempts 2 \
  --retry-base-seconds 0.2

python3 scripts/verify_dual_write.py \
  --report reports/run-report-20260224-172150.json \
  --output logs/verify-day8-10-smoke-c.json \
  --pretty
```
关键输出（节选）：
- `FAIL: telegram receipt exists but success=false; telegram message_id missing for non-dry-run receipt`
- `"kb_hash_check": "match"`
- `"telegram_message_id_reconciled": "missing"`
- `machine-readable output written: logs/verify-day8-10-smoke-c.json`

说明：可识别“KB 成功 + Telegram 失败”的不一致，并输出可机读结果。

### 验证 e) CLI 能力缓存
文件：`state/cli_capabilities.json`
关键内容（节选）：
```json
{
  "tool": "openclaw message send",
  "flags": {
    "account": "--account-id",
    "target": "--target",
    "message": "--message"
  }
}
```

---

## 3) 关键产物路径

- 配置：`ops/reed-agent-os/config/error-classifier.json`
- 脚本：
  - `ops/reed-agent-os/scripts/error_classifier.py`
  - `ops/reed-agent-os/scripts/send_telegram.py`
  - `ops/reed-agent-os/scripts/orchestrate_daily.py`
  - `ops/reed-agent-os/scripts/write_kb.py`
  - `ops/reed-agent-os/scripts/verify_dual_write.py`
- 文档：`ops/reed-agent-os/README.md`
- 验证输出：
  - `ops/reed-agent-os/state/cli_capabilities.json`
  - `ops/reed-agent-os/logs/verify-day8-10-smoke-c.json`
  - `ops/reed-agent-os/reports/run-report-20260224-172113.json`
  - `ops/reed-agent-os/reports/run-report-20260224-172150.json`

---

## 4) 遗留风险

1. 当前 openclaw CLI message send 输出格式未完全稳定，`message_id` 解析依赖 stdout/stderr 文本模式，存在版本漂移风险。
2. replay 在失败时会由 `send_telegram.py` 再次入队，可能导致队列膨胀；后续应增加去重键/回退策略。
3. dry-run 链路不会真实生成 Telegram message_id，对“全链路强一致”只能做结构级验证，仍需受控真实环境验收。

---

## 5) Day11-12 建议

1. 引入 queue 去重与最大重放次数（含 dead-letter queue），防止失败放大。
2. 统一 Telegram 回执结构（强制 JSON 输出 message_id），移除正则兜底解析。
3. 增加自动化回归（至少覆盖：参数兼容探测、retryable 分类、verify hash/message_id 三类断言）。
