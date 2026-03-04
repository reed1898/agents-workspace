#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_DATA_INSUFFICIENT = 11

DEFAULT_ROOT = Path("/home/ubuntu/.openclaw/workspace/ops/reed-agent-os")


def log(msg: str) -> None:
    print(f"[generate_daily_summary] {msg}")


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def load_run_reports(reports_dir: Path) -> list[dict]:
    reports: list[dict] = []
    for p in sorted(reports_dir.glob("run-report-*.json")):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            obj["__path"] = str(p)
            reports.append(obj)
        except Exception as e:
            log(f"skip invalid report: {p} ({e})")
    return reports


def in_window(dt: datetime | None, start: datetime, end: datetime) -> bool:
    if dt is None:
        return False
    return start <= dt <= end


def collect_metrics(root: Path, phase: str) -> dict:
    now = datetime.now(timezone.utc)
    if phase == "morning":
        start = now - timedelta(hours=24)
    elif phase == "evening":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start = now - timedelta(hours=8)

    reports_dir = root / "reports"
    pending_dir = root / "queue" / "telegram_pending"
    sent_dir = root / "queue" / "telegram_sent"

    reports = load_run_reports(reports_dir)
    in_scope = []
    for r in reports:
        ts = parse_iso(r.get("timestamp_utc"))
        if in_window(ts, start, now):
            in_scope.append(r)

    total_runs = len(in_scope)
    successful_runs = sum(1 for r in in_scope if bool(r.get("success")))

    send_attempted = 0
    send_success = 0
    send_fail = 0
    kb_success = 0
    generate_success = 0
    attempts_sum = 0

    for r in in_scope:
        steps = r.get("steps", {})
        if steps.get("generate_daily_summary", {}).get("ok"):
            generate_success += 1
        if steps.get("write_kb", {}).get("ok"):
            kb_success += 1

        send_step = steps.get("send_telegram")
        if isinstance(send_step, dict):
            send_attempted += 1
            if send_step.get("ok"):
                send_success += 1
            else:
                send_fail += 1
            attempts_sum += int(send_step.get("attempt_count", 0) or 0)

    pending_count = len(list(pending_dir.glob("telegram-pending-*.json"))) if pending_dir.exists() else 0
    sent_count = len(list(sent_dir.glob("telegram-pending-*.json"))) if sent_dir.exists() else 0

    def rate(n: int, d: int) -> float:
        return round((n / d) * 100, 2) if d > 0 else 0.0

    metrics = {
        "window": {
            "phase": phase,
            "start_utc": start.isoformat(),
            "end_utc": now.isoformat(),
        },
        "runs": {
            "total": total_runs,
            "successful": successful_runs,
            "success_rate_percent": rate(successful_runs, total_runs),
            "generate_success": generate_success,
            "kb_success": kb_success,
        },
        "telegram": {
            "attempted": send_attempted,
            "success": send_success,
            "failed": send_fail,
            "success_rate_percent": rate(send_success, send_attempted),
            "pending_queue": pending_count,
            "sent_archive": sent_count,
            "avg_attempts_per_run": round(attempts_sum / send_attempted, 2) if send_attempted > 0 else 0.0,
        },
        "sources": {
            "reports_dir": str(reports_dir),
            "pending_dir": str(pending_dir),
            "sent_dir": str(sent_dir),
            "reports_loaded": len(reports),
            "reports_in_window": total_runs,
        },
    }
    return metrics


def build_success_payload(phase: str, topic: str, metrics: dict) -> dict:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    runs = metrics["runs"]
    tg = metrics["telegram"]

    highlights = [
        f"窗口内运行 {runs['total']} 次，成功 {runs['successful']} 次（成功率 {runs['success_rate_percent']}%）。",
        f"KB 写入成功 {runs['kb_success']} 次；生成步骤成功 {runs['generate_success']} 次。",
        f"Telegram 发送尝试 {tg['attempted']} 次，成功 {tg['success']} 次，失败 {tg['failed']} 次（成功率 {tg['success_rate_percent']}%）。",
    ]

    risks = []
    if tg["pending_queue"] > 0:
        risks.append(f"当前待重放 Telegram 队列 {tg['pending_queue']} 条，存在消息延迟风险。")
    if runs["success_rate_percent"] < 90:
        risks.append(f"窗口内总链路成功率 {runs['success_rate_percent']}%，低于 90% 目标。")
    if tg["attempted"] > 0 and tg["success_rate_percent"] < 90:
        risks.append(f"Telegram 发送成功率 {tg['success_rate_percent']}%，需排查账号/参数/网络。")
    if not risks:
        risks.append("当前窗口未发现显著新增风险，保持监控。")

    actions = [
        f"优先清理 pending 队列（当前 {tg['pending_queue']} 条），执行 replay 并核对 receipt。",
        "检查最近失败 run-report 的 error_class 与 stderr 关键字，确认是否可重试故障。",
        "持续跟踪 send_telegram 参数探测结果（cli_capabilities.json），避免 CLI 参数漂移。",
    ]

    return {
        "status": "success",
        "data": {
            "report_type": "daily",
            "phase": phase,
            "topic": topic,
            "date": date_str,
            "generated_at_utc": now.isoformat(),
            "highlights": highlights,
            "risks": risks,
            "actions": actions,
            "artifacts": [
                metrics["sources"]["reports_dir"],
                metrics["sources"]["pending_dir"],
                metrics["sources"]["sent_dir"],
            ],
            "metrics": metrics,
        },
        "error": None,
        "next_action": {
            "type": "continue",
            "target": "write_kb",
            "reason": "日报已根据真实运行数据生成，进入 KB 写入步骤",
        },
    }


def build_failure_payload(phase: str, topic: str, metrics: dict, reasons: list[str]) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "status": "failed",
        "data": {
            "report_type": "daily",
            "phase": phase,
            "topic": topic,
            "date": now.strftime("%Y-%m-%d"),
            "generated_at_utc": now.isoformat(),
            "highlights": [],
            "risks": [],
            "actions": [],
            "artifacts": [
                metrics["sources"]["reports_dir"],
                metrics["sources"]["pending_dir"],
                metrics["sources"]["sent_dir"],
            ],
            "metrics": metrics,
        },
        "error": {
            "code": "DATA_INSUFFICIENT",
            "message": "daily summary generation aborted due to insufficient source data",
            "reasons": reasons,
        },
        "next_action": {
            "type": "halt",
            "target": "generate_daily_summary",
            "reason": "数据不足，停止后续写 KB/发 Telegram，避免发送骨架占位内容",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate data-backed daily summary JSON format.")
    parser.add_argument("--phase", default="morning", choices=["morning", "midday", "evening"], help="Daily run phase")
    parser.add_argument("--topic", default="daily-ops", help="Report topic suffix")
    parser.add_argument("--work-dir", default=str(DEFAULT_ROOT), help="Reed Agent OS root path")
    parser.add_argument("--output", default="", help="Optional output file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty JSON output")
    args = parser.parse_args()

    metrics = collect_metrics(Path(args.work_dir), args.phase)

    reasons: list[str] = []
    if metrics["runs"]["total"] <= 0:
        reasons.append("no run-report data found in the selected time window")
    if metrics["runs"]["generate_success"] <= 0 and metrics["runs"]["kb_success"] <= 0:
        reasons.append("no successful generate/write evidence in selected window")

    if reasons:
        payload = build_failure_payload(args.phase, args.topic, metrics, reasons)
        exit_code = EXIT_DATA_INSUFFICIENT
        log(f"insufficient data: {'; '.join(reasons)}")
    else:
        payload = build_success_payload(args.phase, args.topic, metrics)
        exit_code = EXIT_OK

    content = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)

    log(f"phase={args.phase} topic={args.topic}")
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
        log(f"written output: {out_path}")
    else:
        print(content)

    log(f"done status={payload.get('status')} exit_code={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
