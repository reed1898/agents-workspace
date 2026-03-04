# Reed Agent OS v1 实施记录（Day4-5）

- 日期：2026-02-24
- 范围：Day4-5（日报双写闭环：KB 落盘 + Telegram 回执）
- 执行位置：`/home/ubuntu/.openclaw/workspace/ops/reed-agent-os`
- 安全约束：默认 dry-run；本次未发送真实外部 Telegram 消息

## 本次改动

### 1) 增量改造 `write_kb.py`
文件：`ops/reed-agent-os/scripts/write_kb.py`

新增能力：
- 保持 `--dry-run` 默认开启，支持 `--no-dry-run` 真实落盘
- 增加失败返回码：
  - `2` 输入文件不存在
  - `3` 输入 JSON 非法
  - `4` Markdown 渲染失败
  - `5` 文件写入失败
- 增加错误日志：`ops/reed-agent-os/logs/write_kb.error.log`
- 新增 `--receipt-path`，可输出 KB 写入回执 JSON（给编排脚本统一汇总）

### 2) 新增 `send_telegram.py`
文件：`ops/reed-agent-os/scripts/send_telegram.py`

功能：
- 参数支持：
  - `--text` 或 `--input-json`（二选一）
  - `--account-id`（默认 `maya`）
  - `--target`（默认 `telegram:869269685`）
  - `--dry-run/--no-dry-run`（默认 dry-run）
- `--input-json` 模式自动从日报 JSON 渲染文本
- 真实发送（`--no-dry-run`）时：优先通过子进程调用
  - `openclaw message send --account-id ... --target ... --message ...`
- 无论 dry-run 还是真实发送，都会在 `ops/reed-agent-os/logs/` 下写回执：
  - `telegram-receipt-YYYYmmdd-HHMMSS.json`

### 3) 新增 `orchestrate_daily.py`
文件：`ops/reed-agent-os/scripts/orchestrate_daily.py`

编排链路：
1. `generate_daily_summary.py`
2. `write_kb.py`
3. `send_telegram.py`

输出：
- 统一 run report：`ops/reed-agent-os/reports/run-report-*.json`
- 过程产物落 `ops/reed-agent-os/logs/`：summary JSON、KB receipt、Telegram receipt

### 4) 目录补充
- 新增：`ops/reed-agent-os/logs/`
- 新增：`ops/reed-agent-os/reports/`

## Smoke 验证

### a) 全 dry-run 跑通 orchestrate_daily.py
命令：
```bash
cd /home/ubuntu/.openclaw/workspace/ops/reed-agent-os
python3 scripts/orchestrate_daily.py --phase morning --topic day4-5-smoke --dry-run
```
关键输出：
- `[orchestrate_daily] report=/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/reports/run-report-20260224-171126.json`
- `[orchestrate_daily] success=True`

### b) KB 真实落盘（no-dry-run）
命令：
```bash
cd /home/ubuntu/.openclaw/workspace/ops/reed-agent-os
python3 scripts/generate_daily_summary.py --phase evening --topic day4-5-real-kb --output /tmp/reed-day45-real.json --pretty
python3 scripts/write_kb.py --input-json /tmp/reed-day45-real.json --no-dry-run
```
关键输出：
- `[write_kb] dry_run=False`
- `[write_kb] written: /home/ubuntu/.openclaw/kb/01_Daily/2026-02-24-day4-5-real-kb.md`

### c) Telegram 保持 dry-run（不外发）并生成回执日志
命令：
```bash
cd /home/ubuntu/.openclaw/workspace/ops/reed-agent-os
python3 scripts/send_telegram.py --text "[smoke] day4-5 telegram dry-run receipt" --dry-run
```
关键输出：
- `[send_telegram] dry_run=True`
- `[send_telegram] receipt written: /home/ubuntu/.openclaw/workspace/ops/reed-agent-os/logs/telegram-receipt-20260224-171127.json`

## 已知风险

1. `send_telegram.py` 在 `--no-dry-run` 下依赖本机 `openclaw` CLI 与 message 通道可用性；若 CLI 不可用会失败返回。
2. 当前回执是“发送命令执行结果”级别，尚未对 Telegram 平台 message_id 做强校验与反查。
3. `orchestrate_daily.py` 目前为串行同步调用，尚未加入重试/退避/补偿队列。

## Day6-7 建议

1. 在 `orchestrate_daily.py` 加入 retry/backoff（仅对 retryable 错误）与失败分类。
2. 增加双写一致性校验：KB 文件 hash + Telegram receipt 结构化字段（message_id/target/timestamp）。
3. 实装降级路径：Telegram 失败时写入待补发队列，保障“先 KB 成功，再补发外发”。
