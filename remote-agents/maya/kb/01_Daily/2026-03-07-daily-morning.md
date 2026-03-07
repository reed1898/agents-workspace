# 2026-03-07 daily-morning (morning)

- generated_at_utc: 2026-03-07T00:30:04.583218+00:00
- status: success

## Highlights
- 窗口内运行 2 次，成功 2 次（成功率 100.0%）。
- KB 写入成功 2 次；生成步骤成功 2 次。
- Telegram 发送尝试 2 次，成功 2 次，失败 0 次（成功率 100.0%）。

## Risks
- 当前待重放 Telegram 队列 1 条，存在消息延迟风险。

## Actions
- 优先清理 pending 队列（当前 1 条），执行 replay 并核对 receipt。
- 检查最近失败 run-report 的 error_class 与 stderr 关键字，确认是否可重试故障。
- 持续跟踪 send_telegram 参数探测结果（cli_capabilities.json），避免 CLI 参数漂移。

## Raw JSON
```json
{
  "status": "success",
  "data": {
    "report_type": "daily",
    "phase": "morning",
    "topic": "daily-morning",
    "date": "2026-03-07",
    "generated_at_utc": "2026-03-07T00:30:04.583218+00:00",
    "highlights": [
      "窗口内运行 2 次，成功 2 次（成功率 100.0%）。",
      "KB 写入成功 2 次；生成步骤成功 2 次。",
      "Telegram 发送尝试 2 次，成功 2 次，失败 0 次（成功率 100.0%）。"
    ],
    "risks": [
      "当前待重放 Telegram 队列 1 条，存在消息延迟风险。"
    ],
    "actions": [
      "优先清理 pending 队列（当前 1 条），执行 replay 并核对 receipt。",
      "检查最近失败 run-report 的 error_class 与 stderr 关键字，确认是否可重试故障。",
      "持续跟踪 send_telegram 参数探测结果（cli_capabilities.json），避免 CLI 参数漂移。"
    ],
    "artifacts": [
      "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/reports",
      "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_pending",
      "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_sent"
    ],
    "metrics": {
      "window": {
        "phase": "morning",
        "start_utc": "2026-03-06T00:30:04.580086+00:00",
        "end_utc": "2026-03-07T00:30:04.580086+00:00"
      },
      "runs": {
        "total": 2,
        "successful": 2,
        "success_rate_percent": 100.0,
        "generate_success": 2,
        "kb_success": 2
      },
      "telegram": {
        "attempted": 2,
        "success": 2,
        "failed": 0,
        "success_rate_percent": 100.0,
        "pending_queue": 1,
        "sent_archive": 3,
        "avg_attempts_per_run": 1.0
      },
      "sources": {
        "reports_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/reports",
        "pending_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_pending",
        "sent_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_sent",
        "reports_loaded": 26,
        "reports_in_window": 2
      }
    }
  },
  "error": null,
  "next_action": {
    "type": "continue",
    "target": "write_kb",
    "reason": "日报已根据真实运行数据生成，进入 KB 写入步骤"
  }
}
```
