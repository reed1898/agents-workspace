# Reed Agent OS v1（Day1-3 Implementation Skeleton）

本目录提供 Day1-3 的可运行骨架：目录、Schema、脚本 CLI、示例 cron 配置。

## 目录

- `config/kpi.schema.json`：KPI 快照结构定义（3 项 KPI）
- `config/skill-io.schema.json`：统一 Skill I/O JSON 结构定义
- `scripts/generate_daily_summary.py`：生成日报 JSON skeleton
- `scripts/collect_kpi.py`：采集/计算 3 项 KPI skeleton
- `scripts/write_kb.py`：将日报写入 KB（默认 dry-run）
- `examples/cron-jobs.json`：Cron 任务示例（>=5 条）

## 运行要求

- Python 3.9+
- 仅使用标准库（无额外依赖）

## 快速开始

```bash
cd /home/ubuntu/.openclaw/workspace/ops/reed-agent-os
python3 scripts/generate_daily_summary.py --phase morning --pretty
python3 scripts/collect_kpi.py --pretty
python3 scripts/write_kb.py --input-json /tmp/reed-daily.json --dry-run
```

## CLI 说明

### 1) 生成日报 skeleton

```bash
python3 scripts/generate_daily_summary.py \
  --phase morning \
  --topic daily-ops \
  --output /tmp/reed-daily.json \
  --pretty
```

输出：标准 Skill I/O 风格 JSON，包含 `status/data/error/next_action` 以及日报基本字段。

### 2) 采集 KPI skeleton（3 项）

```bash
python3 scripts/collect_kpi.py \
  --log-dir /home/ubuntu/.openclaw/workspace/orchestrator/logs \
  --output /tmp/reed-kpi.json \
  --pretty
```

KPI 包含：
- `daily_success_rate`
- `dual_write_consistency`
- `e2e_report_latency`

说明：当前为 Day1-3 骨架实现，若日志不存在则返回安全默认值并标注 `skeleton_mode=true`。

### 3) 写入 KB（默认 dry-run 安全模式）

```bash
python3 scripts/write_kb.py \
  --input-json /tmp/reed-daily.json \
  --kb-root /home/ubuntu/.openclaw/kb \
  --dry-run
```

默认行为：**dry-run=true**（不落盘，仅打印计划写入路径和 markdown 预览）。

若需真实落盘：

```bash
python3 scripts/write_kb.py --input-json /tmp/reed-daily.json --no-dry-run
```

## 安全与约束

- 默认 dry-run，避免误写
- 仅操作本地 workspace / kb 路径
- 不触发外部消息发送
- stdout 输出关键日志，便于审计

## Day1-3 范围说明

已完成：
- 基础目录与命名
- Skill I/O Schema
- KPI Schema（3 项）
- Daily 主链路骨架（生成日报 JSON + 写 KB）
- 本地可执行 smoke test

未完成（Day4+）：
- Telegram 双写真实集成
- 重试/降级/升级全策略自动化
- 周报聚合与一致性 hash 对账

---

## Day8-10 增强（参数兼容 + 一致性 + 可靠性）

### 新增/强化能力

1. `send_telegram.py` 参数兼容探测
   - 启动时自动执行：`openclaw message send --help`
   - 自动选择兼容参数：`--account-id/--accountId`、`--target/--to`、`--message/--text`
   - 探测结果落盘：`state/cli_capabilities.json`

2. 可维护错误分类（retryable/fatal）
   - 新增配置：`config/error-classifier.json`
   - `orchestrate_daily.py` 与 `send_telegram.py` 统一使用映射规则
   - 分类依据：`exit code + stderr 关键字 + step override`

3. 双写一致性校验增强
   - `write_kb.py` receipt 新增 `sha256`
   - `verify_dual_write.py` 增加：
     - KB hash 校验（receipt sha256 vs 文件 sha256）
     - Telegram `message_id` 对账（dry-run 标记 `skipped_dry_run`）
     - machine-readable 输出：`--output <json>`
     - 人类摘要：`PASS/FAIL + reasons`

### 常见故障排查

- **问题 1：Telegram 发送失败并入队**
  - 现象：receipt `success=false` 且存在 `queued_pending`
  - 检查：
    - `logs/*telegram-receipt*.json` 中 `error_class`
    - `queue/telegram_pending/*.json` 是否生成
  - 处理：
    - 先 `python3 scripts/replay_telegram_queue.py --dry-run`
    - 再 `python3 scripts/replay_telegram_queue.py --no-dry-run`

- **问题 2：CLI 参数不兼容**
  - 现象：stderr 出现 `unknown option` / 参数报错
  - 检查：
    - `state/cli_capabilities.json` 中 flags 是否正确
    - 本机 `openclaw message send --help` 输出是否变更
  - 处理：
    - 重新执行 `send_telegram.py` 触发自动探测并覆盖缓存

- **问题 3：verify 报 KB hash mismatch**
  - 现象：`kb_hash_check = mismatch`
  - 检查：
    - KB 文件是否被外部修改
    - 是否使用旧 receipt 对比新文件
  - 处理：
    - 重新跑一轮 `orchestrate_daily.py` 生成新 receipt + 新报告

- **问题 4：verify 报 message_id missing（非 dry-run）**
  - 现象：Telegram success=true 但无 `message_id`
  - 检查：
    - `send_telegram.py` receipt 的 `stdout/stderr`
    - openclaw 输出是否包含消息 ID 字段
  - 处理：
    - 升级 message 输出解析规则，或在发送侧补齐结构化回执

### 验收标准（Day8-10）

- [ ] `send_telegram.py` 可自动识别 CLI 参数并写入 `state/cli_capabilities.json`
- [ ] `config/error-classifier.json` 生效，重试/致命分类可配置
- [ ] `verify_dual_write.py` 同时输出：机器 JSON + 人类摘要
- [ ] 校验包含 KB hash 与 Telegram message_id（dry-run 可跳过并标记）
- [ ] 端到端 smoke 覆盖：
  - a) 全 dry-run 成功链路
  - b) 失败入队
  - c) replay 后状态变化可验证
