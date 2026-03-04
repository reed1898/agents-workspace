#!/usr/bin/env python3
import argparse
import hashlib
import json
import traceback
from datetime import datetime, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_INPUT_NOT_FOUND = 2
EXIT_INPUT_JSON_INVALID = 3
EXIT_RENDER_FAILED = 4
EXIT_WRITE_FAILED = 5


def log(msg: str) -> None:
    print(f"[write_kb] {msg}")


def append_error_log(log_file: Path, message: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} ERROR {message}\n")


def render_markdown(payload: dict) -> str:
    data = payload.get("data", {})
    date_str = data.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    phase = data.get("phase", "unknown")
    topic = data.get("topic", "daily-ops")
    generated_at = data.get("generated_at_utc", "")
    highlights = data.get("highlights", [])
    risks = data.get("risks", [])
    actions = data.get("actions", [])

    lines = [
        f"# {date_str} {topic} ({phase})",
        "",
        f"- generated_at_utc: {generated_at}",
        f"- status: {payload.get('status', 'unknown')}",
        "",
        "## Highlights",
    ]
    lines.extend([f"- {h}" for h in highlights] if highlights else ["- (none)"])

    lines += ["", "## Risks"]
    lines.extend([f"- {r}" for r in risks] if risks else ["- (none)"])

    lines += ["", "## Actions"]
    lines.extend([f"- {a}" for a in actions] if actions else ["- (none)"])

    lines += ["", "## Raw JSON", "```json", json.dumps(payload, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write daily summary JSON into KB markdown file.")
    parser.add_argument("--input-json", required=True, help="Path to daily summary JSON")
    parser.add_argument("--kb-root", default="/home/ubuntu/.openclaw/kb", help="KB root path")
    parser.add_argument("--logs-dir", default="/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/logs", help="Logs directory")
    parser.add_argument("--receipt-path", default="", help="Optional receipt JSON path")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=True, help="Dry-run mode (default: true)")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Disable dry-run and write file")
    args = parser.parse_args()

    error_log = Path(args.logs_dir) / "write_kb.error.log"
    receipt = {
        "tool": "write_kb",
        "success": False,
        "dry_run": args.dry_run,
        "input_json": args.input_json,
        "target": None,
        "sha256": None,
        "error": None,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    try:
        input_path = Path(args.input_json)
        if not input_path.exists():
            msg = f"input file not found: {input_path}"
            log(f"ERROR {msg}")
            append_error_log(error_log, msg)
            receipt["error"] = {"code": "INPUT_NOT_FOUND", "message": msg}
            rc = EXIT_INPUT_NOT_FOUND
        else:
            try:
                payload = json.loads(input_path.read_text(encoding="utf-8"))
            except Exception as e:
                msg = f"invalid JSON in input file: {input_path} ({e})"
                log(f"ERROR {msg}")
                append_error_log(error_log, msg)
                receipt["error"] = {"code": "INPUT_JSON_INVALID", "message": msg}
                rc = EXIT_INPUT_JSON_INVALID
            else:
                try:
                    data = payload.get("data", {})
                    date_str = data.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                    topic = data.get("topic", "daily-ops")
                    output_name = f"{date_str}-{topic}.md"
                    output_path = Path(args.kb_root) / "01_Daily" / output_name
                    receipt["target"] = str(output_path)
                    md = render_markdown(payload)
                except Exception as e:
                    msg = f"render markdown failed: {e}"
                    log(f"ERROR {msg}")
                    append_error_log(error_log, msg)
                    append_error_log(error_log, traceback.format_exc())
                    receipt["error"] = {"code": "RENDER_FAILED", "message": msg}
                    rc = EXIT_RENDER_FAILED
                else:
                    log(f"dry_run={args.dry_run}")
                    log(f"target={output_path}")
                    receipt["sha256"] = hashlib.sha256(md.encode("utf-8")).hexdigest()

                    if args.dry_run:
                        preview = "\n".join(md.splitlines()[:20])
                        log("dry-run preview (first 20 lines):")
                        print(preview)
                        log("done (no file written)")
                        receipt["success"] = True
                        rc = EXIT_OK
                    else:
                        try:
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_text(md, encoding="utf-8")
                            log(f"written: {output_path}")
                            log("done")
                            receipt["success"] = True
                            rc = EXIT_OK
                        except Exception as e:
                            msg = f"write failed: {e}"
                            log(f"ERROR {msg}")
                            append_error_log(error_log, msg)
                            append_error_log(error_log, traceback.format_exc())
                            receipt["error"] = {"code": "WRITE_FAILED", "message": msg}
                            rc = EXIT_WRITE_FAILED
    finally:
        if args.receipt_path:
            rp = Path(args.receipt_path)
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
