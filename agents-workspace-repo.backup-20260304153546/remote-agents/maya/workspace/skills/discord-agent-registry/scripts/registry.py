#!/usr/bin/env python3
import argparse
import json
import os
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REG_DIR = os.path.join(BASE_DIR, "registry")
REG_PATH = os.path.join(REG_DIR, "agents.json")


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_registry():
    if not os.path.exists(REG_PATH):
        return {"version": 0, "updated_at": now_iso(), "agents": {}}
    with open(REG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(data):
    os.makedirs(REG_DIR, exist_ok=True)
    data["updated_at"] = now_iso()
    with open(REG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def bump(data):
    data["version"] = int(data.get("version", 0)) + 1


def envelope(msg_type, payload):
    return {
        "v": 1,
        "msg_id": str(uuid.uuid4()),
        "type": msg_type,
        "ts": now_iso(),
        "payload": payload,
    }


def cmd_register(args):
    reg = load_registry()
    reg["agents"][args.agent_id] = {
        "agent_id": args.agent_id,
        "name": args.name,
        "role": args.role,
        "gateway": args.gateway,
        "node": args.node,
        "status": "online",
        "last_seen": now_iso(),
    }
    bump(reg)
    save_registry(reg)
    print(json.dumps(envelope("REGISTER", reg["agents"][args.agent_id]), ensure_ascii=False, indent=2))


def cmd_offline(args):
    reg = load_registry()
    if args.agent_id in reg["agents"]:
        reg["agents"][args.agent_id]["status"] = "offline"
        reg["agents"][args.agent_id]["offline_reason"] = args.reason
        reg["agents"][args.agent_id]["last_seen"] = now_iso()
        bump(reg)
        save_registry(reg)
        print(json.dumps(envelope("ADMIN_OFFLINE", reg["agents"][args.agent_id]), ensure_ascii=False, indent=2))
    else:
        raise SystemExit(f"agent_id not found: {args.agent_id}")


def cmd_heartbeat(args):
    reg = load_registry()
    if args.agent_id not in reg["agents"]:
        raise SystemExit(f"agent_id not found: {args.agent_id}")
    reg["agents"][args.agent_id]["status"] = args.status
    reg["agents"][args.agent_id]["last_seen"] = now_iso()
    bump(reg)
    save_registry(reg)
    print(json.dumps(envelope("HEARTBEAT", {
        "agent_id": args.agent_id,
        "status": args.status,
        "last_seen": reg["agents"][args.agent_id]["last_seen"],
    }), ensure_ascii=False, indent=2))


def cmd_snapshot(_args):
    reg = load_registry()
    payload = {
        "version": reg.get("version", 0),
        "updated_at": reg.get("updated_at"),
        "agents": list(reg.get("agents", {}).values()),
    }
    print(json.dumps(envelope("REGISTRY_SNAPSHOT", payload), ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="Discord agent registry helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register")
    r.add_argument("--agent-id", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--role", required=True)
    r.add_argument("--gateway", required=True)
    r.add_argument("--node", required=True)
    r.set_defaults(func=cmd_register)

    o = sub.add_parser("offline")
    o.add_argument("--agent-id", required=True)
    o.add_argument("--reason", default="admin offline")
    o.set_defaults(func=cmd_offline)

    h = sub.add_parser("heartbeat")
    h.add_argument("--agent-id", required=True)
    h.add_argument("--status", default="online", choices=["online", "degraded", "offline"])
    h.set_defaults(func=cmd_heartbeat)

    s = sub.add_parser("snapshot")
    s.set_defaults(func=cmd_snapshot)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
