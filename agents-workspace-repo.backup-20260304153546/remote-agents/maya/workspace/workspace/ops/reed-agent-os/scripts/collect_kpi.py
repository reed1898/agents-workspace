#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str) -> None:
    print(f"[collect_kpi] {msg}")


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def collect_from_logs(log_dir: Path) -> dict:
    # Day1-3 skeleton: if logs are absent, use safe defaults.
    # Future: parse run-*.json for real metrics.
    skeleton_mode = True
    total_tasks = 0
    successful_tasks = 0
    expected_reports = 0
    matched_reports = 0
    p50 = 0.0
    p95 = 0.0
    samples = 0

    if log_dir.exists() and any(log_dir.iterdir()):
        # Placeholder branch to show incremental extension point.
        skeleton_mode = True

    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "skeleton_mode": skeleton_mode,
        "daily_success_rate": {
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "rate_percent": safe_rate(successful_tasks, total_tasks),
            "target_percent": 95.0
        },
        "dual_write_consistency": {
            "expected_reports": expected_reports,
            "matched_reports": matched_reports,
            "rate_percent": safe_rate(matched_reports, expected_reports),
            "target_percent": 100.0
        },
        "e2e_report_latency": {
            "samples": samples,
            "p50_seconds": p50,
            "p95_seconds": p95,
            "target_p50_seconds": 180.0,
            "target_p95_seconds": 480.0
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect 3 KPI skeleton metrics.")
    parser.add_argument("--log-dir", default="/home/ubuntu/.openclaw/workspace/orchestrator/logs", help="Orchestrator log directory")
    parser.add_argument("--output", default="", help="Optional output file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty JSON output")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    log(f"log_dir={log_dir}")
    payload = collect_from_logs(log_dir)
    content = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
        log(f"written output: {out_path}")
    else:
        print(content)

    log("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
