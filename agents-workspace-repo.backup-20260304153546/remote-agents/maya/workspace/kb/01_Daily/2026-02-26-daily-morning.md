# 2026-02-26 daily-morning (morning)

- generated_at_utc: 2026-02-26T00:30:04.772622+00:00
- status: success

## Highlights
- 窗口内运行 3 次，成功 2 次（成功率 66.67%）。
- KB 写入成功 3 次；生成步骤成功 3 次。
- Telegram 发送尝试 3 次，成功 2 次，失败 1 次（成功率 66.67%）。

## Risks
- 窗口内总链路成功率 66.67%，低于 90% 目标。
- Telegram 发送成功率 66.67%，需排查账号/参数/网络。

## Actions
- 优先清理 pending 队列（当前 0 条），执行 replay 并核对 receipt。
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
    "date": "2026-02-26",
    "generated_at_utc": "2026-02-26T00:30:04.772622+00:00",
    "highlights": [
      "窗口内运行 3 次，成功 2 次（成功率 66.67%）。",
      "KB 写入成功 3 次；生成步骤成功 3 次。",
      "Telegram 发送尝试 3 次，成功 2 次，失败 1 次（成功率 66.67%）。"
    ],
    "risks": [
      "窗口内总链路成功率 66.67%，低于 90% 目标。",
      "Telegram 发送成功率 66.67%，需排查账号/参数/网络。"
    ],
    "actions": [
      "优先清理 pending 队列（当前 0 条），执行 replay 并核对 receipt。",
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
        "start_utc": "2026-02-25T00:30:04.765487+00:00",
        "end_utc": "2026-02-26T00:30:04.765487+00:00"
      },
      "runs": {
        "total": 3,
        "successful": 2,
        "success_rate_percent": 66.67,
        "generate_success": 3,
        "kb_success": 3
      },
      "telegram": {
        "attempted": 3,
        "success": 2,
        "failed": 1,
        "success_rate_percent": 66.67,
        "pending_queue": 0,
        "sent_archive": 3,
        "avg_attempts_per_run": 1.0
      },
      "sources": {
        "reports_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/reports",
        "pending_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_pending",
        "sent_dir": "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/queue/telegram_sent",
        "reports_loaded": 8,
        "reports_in_window": 3
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
