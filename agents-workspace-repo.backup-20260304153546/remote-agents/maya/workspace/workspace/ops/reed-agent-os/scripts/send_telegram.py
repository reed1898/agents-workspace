#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from error_classifier import ErrorClassifier


DEFAULT_ROOT = Path("/home/ubuntu/.openclaw/workspace/ops/reed-agent-os")


def log(msg: str) -> None:
    print(f"[send_telegram] {msg}")


def load_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    data = payload.get("data", {})
    date_str = data.get("date", "")
    topic = data.get("topic", "daily-ops")
    phase = data.get("phase", "unknown")
    highlights = data.get("highlights", [])
    risks = data.get("risks", [])
    actions = data.get("actions", [])

    lines = [f"日报 {date_str} | {topic} | {phase}", "", "Highlights:"]
    lines.extend([f"- {h}" for h in highlights] if highlights else ["- (none)"])
    lines.append("")
    lines.append("Risks:")
    lines.extend([f"- {r}" for r in risks] if risks else ["- (none)"])
    lines.append("")
    lines.append("Actions:")
    lines.extend([f"- {a}" for a in actions] if actions else ["- (none)"])
    return "\n".join(lines)


def detect_cli_capabilities(state_dir: Path) -> dict:
    state_dir.mkdir(parents=True, exist_ok=True)
    cache_path = state_dir / "cli_capabilities.json"

    proc = subprocess.run(["openclaw", "message", "send", "--help"], capture_output=True, text=True)
    help_text = (proc.stdout or "") + "\n" + (proc.stderr or "")

    def pick(*candidates: str) -> str:
        for c in candidates:
            if c in help_text:
                return c
        return candidates[0]

    capabilities = {
        "tool": "openclaw message send",
        "detected_at_utc": datetime.now(timezone.utc).isoformat(),
        "returncode": proc.returncode,
        "flags": {
            "account": pick("--account", "--account-id", "--accountId"),
            "channel": pick("--channel"),
            "target": pick("--target", "--to"),
            "message": pick("--message", "--text"),
        },
    }
    cache_path.write_text(json.dumps(capabilities, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return capabilities


def extract_message_id(stdout: str, stderr: str) -> str | None:
    blob = "\n".join([stdout or "", stderr or ""]).strip()
    if not blob:
        return None

    # try JSON lines
    for line in blob.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for key in ("message_id", "messageId", "id"):
            val = obj.get(key)
            if val is not None:
                return str(val)

    m = re.search(r"(?:message[_-]?id|msg[_-]?id|id)\s*[:=]\s*([A-Za-z0-9_-]+)", blob, re.IGNORECASE)
    return m.group(1) if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Send daily report to Telegram via OpenClaw message tool.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Plain text to send")
    group.add_argument("--input-json", help="Path to daily summary JSON; text will be rendered")
    parser.add_argument("--account-id", "--account", dest="account_id", default="maya", help="OpenClaw account id")
    parser.add_argument("--target", "--to", dest="target", default="telegram:869269685", help="Message target")
    parser.add_argument("--channel", default="telegram", help="Channel name when multiple channels are configured")
    parser.add_argument("--logs-dir", default=str(DEFAULT_ROOT / "logs"), help="Logs directory")
    parser.add_argument("--queue-dir", default=str(DEFAULT_ROOT / "queue" / "telegram_pending"), help="Pending queue directory")
    parser.add_argument("--state-dir", default=str(DEFAULT_ROOT / "state"), help="State directory")
    parser.add_argument("--classifier-config", default=str(DEFAULT_ROOT / "config" / "error-classifier.json"), help="Error classifier mapping")
    parser.add_argument("--receipt-path", default="", help="Optional explicit receipt output path")
    parser.add_argument("--attempt", type=int, default=1, help="Attempt index for this send")
    parser.add_argument("--run-id", default="", help="Orchestrator run id")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=True, help="Dry-run mode (default: true)")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Disable dry-run and send externally")
    args = parser.parse_args()

    classifier = ErrorClassifier.from_file(args.classifier_config)

    logs_dir = Path(args.logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    queue_dir = Path(args.queue_dir)
    queue_dir.mkdir(parents=True, exist_ok=True)
    state_dir = Path(args.state_dir)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    receipt_path = Path(args.receipt_path) if args.receipt_path else (logs_dir / f"telegram-receipt-{ts}.json")

    text = load_text(args)
    capabilities = detect_cli_capabilities(state_dir)
    flags = capabilities.get("flags", {})

    receipt = {
        "tool": "send_telegram",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "account_id": args.account_id,
        "target": args.target,
        "channel": args.channel,
        "attempt": args.attempt,
        "run_id": args.run_id,
        "text_preview": text[:200],
        "success": False,
        "error_class": None,
        "message_id": None,
        "reconciliation": {"message_id_check": "pending"},
        "cli_capabilities_path": str(state_dir / "cli_capabilities.json"),
        "command": None,
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "queued_pending": None,
    }

    if args.dry_run:
        log("dry_run=True")
        log(f"target={args.target}")
        log("dry-run preview (first 10 lines):")
        print("\n".join(text.splitlines()[:10]))
        receipt["success"] = True
        receipt["returncode"] = 0
        receipt["reconciliation"]["message_id_check"] = "skipped_dry_run"
    else:
        cmd = [
            "openclaw",
            "message",
            "send",
            flags.get("account", "--account"),
            args.account_id,
            flags.get("channel", "--channel"),
            args.channel,
            flags.get("target", "--target"),
            args.target,
            flags.get("message", "--message"),
            text,
        ]
        receipt["command"] = cmd
        log("dry_run=False, calling OpenClaw message send")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        receipt["stdout"] = proc.stdout
        receipt["stderr"] = proc.stderr
        receipt["returncode"] = proc.returncode
        receipt["success"] = proc.returncode == 0
        if proc.returncode == 0:
            receipt["message_id"] = extract_message_id(proc.stdout, proc.stderr)
            receipt["reconciliation"]["message_id_check"] = "available" if receipt["message_id"] else "missing"
            log("message sent successfully")
        else:
            receipt["error_class"] = classifier.classify("send_telegram", proc.returncode, proc.stderr)
            log(f"ERROR send failed rc={proc.returncode} class={receipt['error_class']}")
            pending_payload = {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "run_id": args.run_id,
                "attempt": args.attempt,
                "next_attempt": args.attempt + 1,
                "error_class": receipt["error_class"],
                "last_error": (proc.stderr or proc.stdout or "").strip()[:500],
                "account_id": args.account_id,
                "target": args.target,
                "text": text,
            }
            pending_path = queue_dir / f"telegram-pending-{ts}.json"
            pending_path.write_text(json.dumps(pending_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            receipt["queued_pending"] = str(pending_path)
            log(f"queued pending task: {pending_path}")

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"receipt written: {receipt_path}")
    return 0 if receipt["success"] else 6


if __name__ == "__main__":
    raise SystemExit(main())
