#!/usr/bin/env python3
import argparse
import base64
import json
import os
import time
import uuid
import urllib.request
from pathlib import Path


def load_openclaw_cfg():
    cfg_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    if not cfg_path:
        home = os.path.expanduser("~")
        cfg_path = os.path.join(home, ".openclaw", "openclaw.json")
    p = Path(cfg_path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def cfg_get(cfg, path, default=""):
    cur = cfg
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--out", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--language", default="")
    ap.add_argument("--resource-id", default="")
    ap.add_argument("--app-id", default="")
    ap.add_argument("--access-token", default="")
    ap.add_argument("--poll-timeout", type=int, default=90)
    ap.add_argument("--poll-interval", type=int, default=2)
    args = ap.parse_args()

    audio = Path(args.audio)
    if not audio.exists():
        raise SystemExit(f"Audio file not found: {audio}")

    cfg = load_openclaw_cfg()
    env = cfg_get(cfg, ["env", "vars"], {}) if cfg else {}
    skill_cfg = cfg_get(cfg, ["skills", "entries", "volcengine-stt"], {}) if cfg else {}

    app_id = args.app_id or os.environ.get("VOLC_APP_ID") or env.get("VOLC_APP_ID") or skill_cfg.get("appId", "")
    access_token = args.access_token or os.environ.get("VOLC_ACCESS_TOKEN") or env.get("VOLC_ACCESS_TOKEN") or skill_cfg.get("accessToken", "")
    resource_id = args.resource_id or os.environ.get("VOLC_RESOURCE_ID") or env.get("VOLC_RESOURCE_ID") or skill_cfg.get("resourceId", "volc.seedasr.auc")

    if not app_id or not access_token:
        raise SystemExit("Missing VOLC_APP_ID/VOLC_ACCESS_TOKEN")

    out = args.out
    if not out:
        out = str(audio.with_suffix(".json" if args.json else ".txt"))

    ext = audio.suffix.lower().lstrip(".")
    if ext in ("oga", "opus"):
        fmt = "ogg"
    elif ext in ("wav", "mp3", "ogg"):
        fmt = ext
    else:
        fmt = "mp3"
    codec = "opus" if fmt == "ogg" else "raw"

    req_id = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "X-Api-App-Key": app_id,
        "X-Api-Access-Key": access_token,
        "X-Api-Resource-Id": resource_id,
        "X-Api-Request-Id": req_id,
        "X-Api-Sequence": "-1",
    }

    b64 = base64.b64encode(audio.read_bytes()).decode("ascii")
    request_body = {
        "user": {"uid": app_id},
        "audio": {"data": b64, "format": fmt, "codec": codec},
        "request": {"model_name": "bigmodel", "enable_itn": True, "enable_punc": True},
    }
    if args.language:
        request_body["request"]["language"] = args.language

    def post(url, payload):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            code = resp.getheader("X-Api-Status-Code") or ""
            body = resp.read().decode("utf-8", "ignore")
            return code, body

    submit_code, _ = post("https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit", request_body)
    if submit_code != "20000000":
        raise SystemExit(f"Submit failed: {submit_code}")

    start = time.time()
    raw = "{}"
    while True:
        q_code, raw = post("https://openspeech.bytedance.com/api/v3/auc/bigmodel/query", {})
        if q_code == "20000000":
            break
        if q_code not in ("20000001", "20000002"):
            raise SystemExit(f"Query failed: {q_code}")
        if time.time() - start >= args.poll_timeout:
            raise SystemExit(f"Query timeout after {args.poll_timeout}s")
        time.sleep(args.poll_interval)

    obj = json.loads(raw) if raw else {}
    if args.json:
        Path(out).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        text = (obj.get("result") or {}).get("text") or obj.get("text") or ""
        Path(out).write_text(text, encoding="utf-8")

    print(out)


if __name__ == "__main__":
    main()
