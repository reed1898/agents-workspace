#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import uuid
import time
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(__file__))
CFG = os.path.join(BASE, "references", "git-config.json")


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def git(cmd, cwd, check=False):
    r = subprocess.run(["git", *cmd], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or f"git {' '.join(cmd)} failed")
    return r


def repo_info():
    cfg = load_json(CFG)
    repo = cfg["repo_url"]
    path = cfg["local_path"]
    branch = cfg.get("branch", "main")
    reg_path = os.path.join(path, "registry", "agent-registry.json")
    return repo, path, branch, reg_path


def ensure_repo():
    repo, path, branch, reg_path = repo_info()
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        git(["clone", repo, path], cwd=os.path.dirname(path), check=True)
    # make sure branch is up to date
    git(["fetch", "origin", branch], cwd=path)
    git(["checkout", branch], cwd=path)
    git(["pull", "--rebase", "origin", branch], cwd=path)
    if not os.path.exists(reg_path):
        save_json(reg_path, {"version": 0, "updated_at": now_iso(), "agents": {}})
        git(["add", "registry/agent-registry.json"], cwd=path)
        git(["commit", "-m", "chore(agent-network): initialize registry"], cwd=path)
        git(["push", "origin", branch], cwd=path)
    return path, branch, reg_path


def bump(reg):
    reg["version"] = int(reg.get("version", 0)) + 1
    reg["updated_at"] = now_iso()


def meta(msg_type, payload):
    return {
        "v": 1,
        "msg_id": str(uuid.uuid4()),
        "type": msg_type,
        "ts": now_iso(),
        "payload": payload,
    }


def apply_and_sync(mutator, commit_msg, retries=3):
    path, branch, reg_path = ensure_repo()

    for _ in range(retries):
        git(["pull", "--rebase", "origin", branch], cwd=path)
        reg = load_json(reg_path)
        result_payload = mutator(reg)
        save_json(reg_path, reg)

        git(["add", "registry/agent-registry.json"], cwd=path)
        c = git(["commit", "-m", commit_msg], cwd=path)
        if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
            time.sleep(0.5)
            continue

        p = git(["push", "origin", branch], cwd=path)
        if p.returncode == 0:
            return result_payload

        # push failed, retry after refresh
        git(["reset", "--hard", "HEAD~1"], cwd=path)
        time.sleep(0.5)

    raise SystemExit("sync failed after retries")


def cmd_init(_):
    path, branch, reg_path = ensure_repo()
    print(json.dumps({"ok": True, "repo": path, "branch": branch, "registry": reg_path}, ensure_ascii=False))


def cmd_register(a):
    def mut(reg):
        reg.setdefault("agents", {})[a.agent_id] = {
            "agent_id": a.agent_id,
            "name": a.name,
            "role": a.role,
            "gateway": a.gateway,
            "node": a.node,
            "discord_user_id": a.discord_user_id,
            "discord_channel_id": a.discord_channel_id,
            "status": "online",
            "last_seen": now_iso(),
        }
        bump(reg)
        return reg["agents"][a.agent_id]

    payload = apply_and_sync(mut, f"chore(registry): register {a.agent_id}")

    # Build notify list for "all other agents" in network (with Discord IDs)
    _, _, reg_path = ensure_repo()
    reg = load_json(reg_path)
    others = []
    mentions = []
    for aid, info in reg.get("agents", {}).items():
        if aid == a.agent_id:
            continue
        duid = (info or {}).get("discord_user_id", "")
        if duid:
            others.append(aid)
            mentions.append(f"<@{duid}>")

    payload["notify_agent_ids"] = others
    payload["notify_mentions"] = mentions
    print(json.dumps(meta("REGISTER", payload), ensure_ascii=False, indent=2))


def cmd_heartbeat(a):
    def mut(reg):
        if a.agent_id not in reg.get("agents", {}):
            raise SystemExit("agent_id not found")
        reg["agents"][a.agent_id]["status"] = a.status
        reg["agents"][a.agent_id]["last_seen"] = now_iso()
        bump(reg)
        return {"agent_id": a.agent_id, "status": a.status, "last_seen": reg["agents"][a.agent_id]["last_seen"]}

    payload = apply_and_sync(mut, f"chore(registry): heartbeat {a.agent_id}")
    print(json.dumps(meta("HEARTBEAT", payload), ensure_ascii=False, indent=2))


def cmd_snapshot(_):
    _, _, reg_path = ensure_repo()
    reg = load_json(reg_path)
    payload = {
        "version": reg.get("version", 0),
        "updated_at": reg.get("updated_at"),
        "agents": list(reg.get("agents", {}).values()),
    }
    print(json.dumps(meta("REGISTRY_SNAPSHOT", payload), ensure_ascii=False, indent=2))


def cmd_offline(a):
    def mut(reg):
        if a.agent_id not in reg.get("agents", {}):
            raise SystemExit("agent_id not found")
        reg["agents"][a.agent_id]["status"] = "offline"
        reg["agents"][a.agent_id]["offline_reason"] = a.reason
        reg["agents"][a.agent_id]["last_seen"] = now_iso()
        bump(reg)
        return reg["agents"][a.agent_id]

    payload = apply_and_sync(mut, f"chore(registry): offline {a.agent_id}")
    print(json.dumps(meta("ADMIN_OFFLINE", payload), ensure_ascii=False, indent=2))


def cmd_remove(a):
    def mut(reg):
        if a.agent_id not in reg.get("agents", {}):
            raise SystemExit("agent_id not found")
        removed = reg["agents"].pop(a.agent_id)
        bump(reg)
        return removed

    payload = apply_and_sync(mut, f"chore(registry): remove {a.agent_id}")
    print(json.dumps(meta("ADMIN_REMOVE", payload), ensure_ascii=False, indent=2))


def cmd_git_sync(_):
    path, branch, _ = ensure_repo()
    ok = git(["pull", "--rebase", "origin", branch], cwd=path).returncode == 0
    print("ok" if ok else "failed")


def main():
    p = argparse.ArgumentParser(description="AgentNetwork registry helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    x = sub.add_parser("init"); x.set_defaults(func=cmd_init)

    r = sub.add_parser("register")
    r.add_argument("--agent-id", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--role", required=True)
    r.add_argument("--gateway", required=True)
    r.add_argument("--node", required=True)
    r.add_argument("--discord-user-id", required=True)
    r.add_argument("--discord-channel-id", required=True)
    r.set_defaults(func=cmd_register)

    h = sub.add_parser("heartbeat")
    h.add_argument("--agent-id", required=True)
    h.add_argument("--status", default="online", choices=["online", "degraded", "offline"])
    h.set_defaults(func=cmd_heartbeat)

    s = sub.add_parser("snapshot"); s.set_defaults(func=cmd_snapshot)

    o = sub.add_parser("offline")
    o.add_argument("--agent-id", required=True)
    o.add_argument("--reason", default="admin action")
    o.set_defaults(func=cmd_offline)

    d = sub.add_parser("remove")
    d.add_argument("--agent-id", required=True)
    d.set_defaults(func=cmd_remove)

    g = sub.add_parser("git-sync")
    g.set_defaults(func=cmd_git_sync)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
