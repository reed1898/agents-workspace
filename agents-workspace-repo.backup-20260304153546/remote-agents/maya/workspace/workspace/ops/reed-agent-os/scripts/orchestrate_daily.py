#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from error_classifier import ErrorClassifier


def log(msg: str) -> None:
    print(f"[orchestrate_daily] {msg}")


def run_cmd(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def classify_error(step_name: str, result: dict, classifier: ErrorClassifier) -> str:
    if result.get("ok"):
        return "none"
    return classifier.classify(step_name, result.get("returncode"), result.get("stderr") or "")


def run_with_retry(step_name: str, cmd: list[str], max_attempts: int, backoff_base_seconds: float, classifier: ErrorClassifier) -> dict:
    attempts = []
    for i in range(1, max_attempts + 1):
        result = run_cmd(cmd)
        error_class = classify_error(step_name, result, classifier)
        result["attempt"] = i
        result["error_class"] = error_class
        attempts.append(result)

        if result["ok"]:
            return {
                "ok": True,
                "attempts": attempts,
                "attempt_count": i,
                "final_error_class": "none",
            }

        if error_class != "retryable" or i >= max_attempts:
            return {
                "ok": False,
                "attempts": attempts,
                "attempt_count": i,
                "final_error_class": error_class,
            }

        sleep_s = backoff_base_seconds * (2 ** (i - 1))
        log(f"step={step_name} attempt={i} retryable_error, backoff={sleep_s:.2f}s")
        time.sleep(sleep_s)

    return {"ok": False, "attempts": attempts, "attempt_count": len(attempts), "final_error_class": "fatal"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Orchestrate daily flow: generate -> write_kb -> send_telegram")
    parser.add_argument("--phase", default="morning", choices=["morning", "midday", "evening"])
    parser.add_argument("--topic", default="daily-ops")
    parser.add_argument("--work-dir", default="/home/ubuntu/.openclaw/workspace/ops/reed-agent-os")
    parser.add_argument("--account-id", default="maya")
    parser.add_argument("--target", default="telegram:869269685")
    parser.add_argument("--classifier-config", default="", help="Error classifier mapping path")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--retry-base-seconds", type=float, default=1.0)
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    args = parser.parse_args()

    root = Path(args.work_dir)
    scripts = root / "scripts"
    logs_dir = root / "logs"
    reports_dir = root / "reports"
    queue_dir = root / "queue" / "telegram_pending"
    state_dir = root / "state"
    logs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    queue_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    classifier_path = args.classifier_config or str(root / "config" / "error-classifier.json")
    classifier = ErrorClassifier.from_file(classifier_path)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"daily-{ts}-{args.phase}-{args.topic}"
    summary_json = logs_dir / f"{run_id}-summary.json"
    kb_receipt = logs_dir / f"{run_id}-write-kb-receipt.json"
    telegram_receipt = logs_dir / f"{run_id}-telegram-receipt.json"

    report = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "topic": args.topic,
        "dry_run": args.dry_run,
        "max_attempts": args.max_attempts,
        "retry_base_seconds": args.retry_base_seconds,
        "classifier_config": classifier_path,
        "steps": {},
        "artifacts": {
            "summary_json": str(summary_json),
            "kb_receipt": str(kb_receipt),
            "telegram_receipt": str(telegram_receipt),
            "pending_queue_dir": str(queue_dir),
            "cli_capabilities": str(state_dir / "cli_capabilities.json"),
        },
        "success": False,
    }

    py = "python3"

    cmd_generate = [
        py,
        str(scripts / "generate_daily_summary.py"),
        "--phase",
        args.phase,
        "--topic",
        args.topic,
        "--output",
        str(summary_json),
        "--pretty",
    ]
    step_generate = run_with_retry("generate_daily_summary", cmd_generate, args.max_attempts, args.retry_base_seconds, classifier)
    report["steps"]["generate_daily_summary"] = step_generate
    if not step_generate["ok"]:
        return finalize(report, reports_dir)

    cmd_write = [
        py,
        str(scripts / "write_kb.py"),
        "--input-json",
        str(summary_json),
        "--receipt-path",
        str(kb_receipt),
    ]
    if not args.dry_run:
        cmd_write.append("--no-dry-run")
    step_write = run_with_retry("write_kb", cmd_write, args.max_attempts, args.retry_base_seconds, classifier)
    report["steps"]["write_kb"] = step_write
    if not step_write["ok"]:
        return finalize(report, reports_dir)

    cmd_send = [
        py,
        str(scripts / "send_telegram.py"),
        "--input-json",
        str(summary_json),
        "--account-id",
        args.account_id,
        "--target",
        args.target,
        "--logs-dir",
        str(logs_dir),
        "--queue-dir",
        str(queue_dir),
        "--state-dir",
        str(state_dir),
        "--classifier-config",
        classifier_path,
        "--receipt-path",
        str(telegram_receipt),
        "--attempt",
        "1",
        "--run-id",
        run_id,
    ]
    if not args.dry_run:
        cmd_send.append("--no-dry-run")
    step_send = run_with_retry("send_telegram", cmd_send, args.max_attempts, args.retry_base_seconds, classifier)
    report["steps"]["send_telegram"] = step_send

    report["success"] = step_generate["ok"] and step_write["ok"] and step_send["ok"]
    return finalize(report, reports_dir)


def finalize(report: dict, reports_dir: Path) -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_path = reports_dir / f"run-report-{ts}.json"
    report["report_path"] = str(report_path)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[orchestrate_daily] report={report_path}")
    print(f"[orchestrate_daily] success={report.get('success', False)}")

    return 0 if report.get("success", False) else 10


if __name__ == "__main__":
    raise SystemExit(main())
