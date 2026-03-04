#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str) -> None:
    print(f"[verify_dual_write] {msg}")


def latest_report(reports_dir: Path) -> Path | None:
    files = sorted(reports_dir.glob("run-report-*.json"))
    return files[-1] if files else None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify dual-write consistency: KB + Telegram + report completeness")
    parser.add_argument("--work-dir", default="/home/ubuntu/.openclaw/workspace/ops/reed-agent-os")
    parser.add_argument("--report", default="", help="Optional run report path (default: latest)")
    parser.add_argument("--output", default="", help="Optional machine-readable JSON output file")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = Path(args.work_dir)
    reports_dir = root / "reports"
    report_path = Path(args.report) if args.report else latest_report(reports_dir)

    result = {
        "tool": "verify_dual_write",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "report_path": str(report_path) if report_path else None,
        "pass": True,
        "reasons": [],
        "checks": {
            "run_report_complete": False,
            "kb_file_exists": False,
            "kb_hash_check": "missing",
            "telegram_receipt_exists": False,
            "telegram_receipt_success": False,
            "telegram_message_id_reconciled": "missing",
        },
        "evidence": {
            "kb_file": None,
            "kb_sha256": None,
            "kb_receipt_sha256": None,
            "telegram_receipt": None,
            "telegram_message_id": None,
            "dry_run": None,
        },
        "summary": "",
    }

    if not report_path or not report_path.exists():
        result["pass"] = False
        result["reasons"].append("run report missing")
        result["summary"] = "FAIL: run report missing"
        emit(result, args)
        return 2

    report = json.loads(report_path.read_text(encoding="utf-8"))
    required_steps = ["generate_daily_summary", "write_kb", "send_telegram"]
    if all(s in report.get("steps", {}) for s in required_steps) and "artifacts" in report:
        result["checks"]["run_report_complete"] = True
    else:
        result["pass"] = False
        result["reasons"].append("run report incomplete: missing required steps/artifacts")

    artifacts = report.get("artifacts", {})
    kb_receipt_path = Path(artifacts.get("kb_receipt", "")) if artifacts.get("kb_receipt") else None
    telegram_receipt_path = Path(artifacts.get("telegram_receipt", "")) if artifacts.get("telegram_receipt") else None

    kb_target = None
    kb_receipt_sha256 = None
    if kb_receipt_path and kb_receipt_path.exists():
        kb_receipt = json.loads(kb_receipt_path.read_text(encoding="utf-8"))
        kb_target = kb_receipt.get("target")
        kb_receipt_sha256 = kb_receipt.get("sha256")
    if kb_target and Path(kb_target).exists():
        kb_path = Path(kb_target)
        result["checks"]["kb_file_exists"] = True
        file_sha = sha256_file(kb_path)
        result["evidence"]["kb_file"] = str(kb_path)
        result["evidence"]["kb_sha256"] = file_sha
        result["evidence"]["kb_receipt_sha256"] = kb_receipt_sha256
        if kb_receipt_sha256:
            if kb_receipt_sha256 == file_sha:
                result["checks"]["kb_hash_check"] = "match"
            else:
                result["checks"]["kb_hash_check"] = "mismatch"
                result["pass"] = False
                result["reasons"].append("KB hash mismatch: receipt sha256 != file sha256")
        else:
            result["checks"]["kb_hash_check"] = "missing"
            result["pass"] = False
            result["reasons"].append("KB hash missing in receipt")
    else:
        result["pass"] = False
        result["reasons"].append("KB file missing or kb receipt missing target")

    if telegram_receipt_path and telegram_receipt_path.exists():
        result["checks"]["telegram_receipt_exists"] = True
        tg_receipt = json.loads(telegram_receipt_path.read_text(encoding="utf-8"))
        result["evidence"]["telegram_receipt"] = str(telegram_receipt_path)
        result["evidence"]["dry_run"] = tg_receipt.get("dry_run")
        result["evidence"]["telegram_message_id"] = tg_receipt.get("message_id")

        if tg_receipt.get("success") is True:
            result["checks"]["telegram_receipt_success"] = True
        else:
            result["pass"] = False
            result["reasons"].append("telegram receipt exists but success=false")

        if tg_receipt.get("dry_run") is True:
            result["checks"]["telegram_message_id_reconciled"] = "skipped_dry_run"
        else:
            if tg_receipt.get("message_id"):
                result["checks"]["telegram_message_id_reconciled"] = "ok"
            else:
                result["checks"]["telegram_message_id_reconciled"] = "missing"
                result["pass"] = False
                result["reasons"].append("telegram message_id missing for non-dry-run receipt")
    else:
        result["pass"] = False
        result["reasons"].append("telegram receipt missing")

    if result["pass"]:
        result["summary"] = "PASS: dual-write consistency checks passed"
    else:
        result["summary"] = "FAIL: " + "; ".join(result["reasons"])

    emit(result, args)
    return 0 if result["pass"] else 1


def emit(result: dict, args: argparse.Namespace) -> None:
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"machine-readable output written: {out}")

    print(result["summary"])
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    raise SystemExit(main())
