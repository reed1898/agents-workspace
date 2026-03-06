# 2026-03-05 daily-morning (morning)

- generated_at_utc: 2026-03-05T00:30:35.207988+00:00
- status: success

## Highlights
- 窗口内运行 1 次，成功 1 次（成功率 100.0%）。
- KB 写入成功 1 次；生成步骤成功 1 次。
- Telegram 发送尝试 1 次，成功 1 次，失败 0 次（成功率 100.0%）。

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
    "date": "2026-03-05",
    "generated_at_utc": "2026-03-05T00:30:35.207988+00:00",
    "highlights": [
      "窗口内运行 1 次，成功 1 次（成功率 100.0%）。",
      "KB 写入成功 1 次；生成步骤成功 1 次。",
      "Telegram 发送尝试 1 次，成功 1 次，失败 0 次（成功率 100.0%）。"
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
        "start_utc": "2026-03-04T00:30:35.205383+00:00",
        "end_utc": "2026-03-05T00:30:35.205383+00:00"
      },
      "runs": {
        "total": 1,
        "successful": 1,
        "success_rate_percent": 100.0,
        "generate_success": 1,
        "kb_success": 1
      },
      "telegram": {
        "attempted": 1,
        "success": 1,
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
        "reports_loaded": 22,
        "reports_in_window": 1
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
