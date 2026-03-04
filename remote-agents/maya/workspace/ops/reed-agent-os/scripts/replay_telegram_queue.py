#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str) -> None:
    print(f"[replay_telegram_queue] {msg}")


def run_cmd(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay pending telegram queue tasks.")
    parser.add_argument("--work-dir", default="/home/ubuntu/.openclaw/workspace/ops/reed-agent-os")
    parser.add_argument("--queue-dir", default="", help="Override pending queue dir")
    parser.add_argument("--logs-dir", default="", help="Override logs dir")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    args = parser.parse_args()

    root = Path(args.work_dir)
    queue_dir = Path(args.queue_dir) if args.queue_dir else (root / "queue" / "telegram_pending")
    logs_dir = Path(args.logs_dir) if args.logs_dir else (root / "logs")
    sent_dir = root / "queue" / "telegram_sent"
    queue_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    sent_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(queue_dir.glob("*.json"))[: args.limit]
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    summary = {
        "tool": "replay_telegram_queue",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "queue_dir": str(queue_dir),
        "count": len(files),
        "results": [],
    }

    log(f"dry_run={args.dry_run} queue_count={len(files)}")
    for file in files:
        payload = json.loads(file.read_text(encoding="utf-8"))
        account_id = payload.get("account_id", "maya")
        target = payload.get("target", "telegram:869269685")
        text = payload.get("text", "")
        attempt = int(payload.get("next_attempt", payload.get("attempt", 1)))
        run_id = payload.get("run_id", "")

        if args.dry_run:
            item = {
                "file": str(file),
                "would_send": True,
                "account_id": account_id,
                "target": target,
                "attempt": attempt,
                "text_preview": text[:120],
            }
            summary["results"].append(item)
            log(f"DRY-RUN replay {file.name} -> {target} attempt={attempt}")
            continue

        receipt_path = logs_dir / f"replay-telegram-receipt-{run_ts}-{file.stem}.json"
        cmd = [
            "python3",
            str(root / "scripts" / "send_telegram.py"),
            "--text",
            text,
            "--account-id",
            account_id,
            "--target",
            target,
            "--logs-dir",
            str(logs_dir),
            "--queue-dir",
            str(queue_dir),
            "--receipt-path",
            str(receipt_path),
            "--attempt",
            str(attempt),
            "--run-id",
            run_id,
            "--no-dry-run",
        ]
        result = run_cmd(cmd)
        result["file"] = str(file)
        result["receipt_path"] = str(receipt_path)
        summary["results"].append(result)

        if result["ok"]:
            archived = sent_dir / file.name
            file.rename(archived)
            log(f"replayed success, moved to {archived}")
        else:
            log(f"replayed failed, keep in queue: {file}")

    out_path = logs_dir / f"replay-telegram-queue-{run_ts}.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"summary written: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
