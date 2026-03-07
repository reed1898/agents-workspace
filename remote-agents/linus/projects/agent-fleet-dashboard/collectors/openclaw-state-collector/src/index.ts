import { execSync } from "node:child_process";
import { appendFile, readFile, writeFile } from "node:fs/promises";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

type CronJob = {
  name: string;
  schedule?: string;
  source: "openclaw" | "system";
  job_id?: string;
  next_run_at?: string;
  last_run_at: string;
  last_status?: string;
  consecutive_failures: number;
  last_error?: string | null;
};

type AgentRecord = {
  id: string;
  name: string;
  role: string;
};

const env = {
  root: (process.env.COLLECTOR_DATA_ROOT ?? "~/.openclaw/shared/agent-network-data").replace("~", process.env.HOME ?? ""),
  appendEvents: (process.env.COLLECTOR_APPEND_EVENTS ?? "true") === "true",
  gitSync: (process.env.COLLECTOR_GIT_SYNC ?? "false") === "true",
  gitRemote: process.env.COLLECTOR_GIT_REMOTE ?? "origin",
  gitBranch: process.env.COLLECTOR_GIT_BRANCH ?? "main",
  reportMode: process.env.REPORT_MODE ?? "local",
  reportEndpoint: process.env.REPORT_ENDPOINT,
  reportToken: process.env.REPORT_TOKEN,
  agentId: process.env.AGENT_ID ?? "linus",
  agentName: process.env.AGENT_NAME ?? "Linus",
  agentRole: process.env.AGENT_ROLE ?? "Builder",
  heartbeatIntervalSec: Number(process.env.HEARTBEAT_INTERVAL_SEC ?? "60") || 60
};

function ensureDirs(root: string) {
  ["registry", "state/heartbeats", "state/crons", "state/runtime", "events", "meta"].forEach((p) => {
    mkdirSync(path.join(root, p), { recursive: true });
  });
}

function run(cmd: string, cwd?: string): string {
  return execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], cwd });
}

function parseOpenclawStatus(raw: string): { host?: string; model?: string; channel?: string } {
  const get = (key: string) => raw.match(new RegExp(`${key}=([^|\\n]+)`))?.[1]?.trim();
  return { host: get("host"), model: get("model"), channel: get("channel") };
}

function safeJson<T>(file: string, fallback: T): T {
  try {
    return JSON.parse(readFileSync(file, "utf8")) as T;
  } catch {
    return fallback;
  }
}

function parseOpenclawCronJobs(now: string): CronJob[] {
  try {
    const raw = run("openclaw cron list --json");
    const parsed = JSON.parse(raw) as {
      jobs?: Array<{
        id?: string;
        name?: string;
        schedule?: { kind?: string; expr?: string; everyMs?: number; tz?: string };
        state?: {
          nextRunAtMs?: number;
          lastRunAtMs?: number;
          lastStatus?: string;
          consecutiveErrors?: number;
          lastError?: string;
        };
      }>;
    };

    return (parsed.jobs ?? []).map((job) => {
      let schedule = "unknown";
      if (job.schedule?.kind === "cron" && job.schedule.expr) {
        schedule = job.schedule.tz ? `${job.schedule.expr} @ ${job.schedule.tz}` : job.schedule.expr;
      } else if (job.schedule?.kind === "every" && job.schedule.everyMs) {
        schedule = `every ${Math.round(job.schedule.everyMs / 1000)}s`;
      }

      return {
        name: job.name ?? job.id ?? "openclaw-job",
        source: "openclaw",
        job_id: job.id,
        schedule,
        next_run_at: job.state?.nextRunAtMs ? new Date(job.state.nextRunAtMs).toISOString() : undefined,
        last_run_at: job.state?.lastRunAtMs ? new Date(job.state.lastRunAtMs).toISOString() : now,
        last_status: job.state?.lastStatus ?? "idle",
        consecutive_failures: job.state?.consecutiveErrors ?? 0,
        last_error: job.state?.lastError ?? null
      };
    });
  } catch {
    return [];
  }
}

function parseSystemCronJobs(now: string): CronJob[] {
  try {
    const raw = run("crontab -l");
    const lines = raw
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#"));

    return lines.map((line, idx) => {
      const parts = line.split(/\s+/);
      const schedule = parts.slice(0, 5).join(" ");
      const command = parts.slice(5).join(" ");
      const shortCmd = command.length > 96 ? `${command.slice(0, 96)}...` : command;
      return {
        name: `crontab-${idx + 1}`,
        source: "system",
        schedule,
        last_run_at: now,
        last_status: "unknown",
        consecutive_failures: 0,
        last_error: null,
        job_id: shortCmd
      };
    });
  } catch {
    return [];
  }
}

type Snapshot = {
  now: string;
  agent: AgentRecord;
  registry: { updated_at: string; agents: AgentRecord[] };
  heartbeat: {
    agent_id: string;
    last_seen: string;
    interval_sec: number;
    status: string;
  };
  cron: {
    agent_id: string;
    jobs: CronJob[];
  };
  runtime: {
    agent_id: string;
    runtime: Record<string, unknown>;
  };
  event: {
    ts: string;
    agent_id: string;
    type: string;
    level: "info" | "warn" | "error";
    message: string;
  };
};

async function collectSnapshot(): Promise<Snapshot> {
  const now = new Date().toISOString();
  const agent: AgentRecord = { id: env.agentId, name: env.agentName, role: env.agentRole };

  let statusRaw = "";
  let statusParsed: { host?: string; model?: string; channel?: string } = {};
  try {
    statusRaw = run("openclaw status");
    statusParsed = parseOpenclawStatus(statusRaw);
  } catch {
    statusRaw = "openclaw status unavailable";
  }

  const hbStatePath = path.join(process.env.HOME ?? "", ".openclaw/workspace/memory/heartbeat-state.json");
  const heartbeatState = existsSync(hbStatePath) ? safeJson<{ lastChecks?: Record<string, number> }>(hbStatePath, {}) : {};

  const openclawJobs = parseOpenclawCronJobs(now);
  const systemJobs = parseSystemCronJobs(now);
  const allJobs = [...openclawJobs, ...systemJobs];

  return {
    now,
    agent,
    registry: {
      updated_at: now,
      agents: [agent]
    },
    heartbeat: {
      agent_id: agent.id,
      last_seen: now,
      interval_sec: env.heartbeatIntervalSec,
      status: "ok"
    },
    cron: {
      agent_id: agent.id,
      jobs:
        allJobs.length > 0
          ? allJobs
          : [
              {
                name: "collector-fallback",
                source: "system",
                schedule: "manual",
                last_run_at: now,
                last_status: "ok",
                consecutive_failures: 0,
                last_error: null
              }
            ]
    },
    runtime: {
      agent_id: agent.id,
      runtime: {
        host: statusParsed.host,
        model: statusParsed.model,
        channel: statusParsed.channel,
        uptime_sec: process.uptime(),
        last_openclaw_status_raw: statusRaw,
        heartbeat_state_last_checks: heartbeatState.lastChecks ?? {}
      }
    },
    event: {
      ts: now,
      agent_id: agent.id,
      type: "collector_run",
      level: "info",
      message: `collector synced cron(openclaw=${openclawJobs.length}, system=${systemJobs.length})`
    }
  };
}

async function writeLocal(snapshot: Snapshot) {
  ensureDirs(env.root);

  const registryPath = path.join(env.root, "registry/agent-registry.json");
  const current = safeJson<{ updated_at?: string; agents?: AgentRecord[] }>(registryPath, { agents: [] });
  const merged = new Map<string, AgentRecord>();
  for (const a of current.agents ?? []) merged.set(a.id, a);
  merged.set(snapshot.agent.id, snapshot.agent);

  await writeFile(
    registryPath,
    JSON.stringify({ updated_at: snapshot.now, agents: Array.from(merged.values()) }, null, 2)
  );

  await writeFile(path.join(env.root, `state/heartbeats/${snapshot.agent.id}.json`), JSON.stringify(snapshot.heartbeat, null, 2));
  await writeFile(path.join(env.root, `state/crons/${snapshot.agent.id}.json`), JSON.stringify(snapshot.cron, null, 2));
  await writeFile(path.join(env.root, `state/runtime/${snapshot.agent.id}.json`), JSON.stringify(snapshot.runtime, null, 2));

  await writeFile(path.join(env.root, "meta/schema-version.json"), JSON.stringify({ version: "1.1.0", updated_at: snapshot.now }, null, 2));
  if (env.appendEvents) {
    await appendFile(path.join(env.root, "events/events.jsonl"), `${JSON.stringify(snapshot.event)}\n`);
  }
}

async function reportCloudflare(snapshot: Snapshot) {
  if (!env.reportEndpoint || !env.reportToken) {
    throw new Error("REPORT_ENDPOINT and REPORT_TOKEN are required for REPORT_MODE=cloudflare");
  }

  const payload = {
    agent_id: snapshot.agent.id,
    registry: snapshot.registry,
    heartbeat: snapshot.heartbeat,
    cron: snapshot.cron,
    runtime: snapshot.runtime,
    events: env.appendEvents ? [snapshot.event] : []
  };

  const res = await fetch(`${env.reportEndpoint.replace(/\/$/, "")}/ingest`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${env.reportToken}`
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Cloudflare ingest failed: ${res.status} ${body}`);
  }
}

async function maybeGitSync(now: string) {
  if (!env.gitSync || env.reportMode !== "local") return;

  try {
    run(`git -C ${env.root} pull --rebase ${env.gitRemote} ${env.gitBranch}`);
    const changes = run(`git -C ${env.root} status --porcelain`);
    if (changes.trim()) {
      run(`git -C ${env.root} add .`);
      run(`git -C ${env.root} commit -m "chore: sync agent network state"`);
      run(`git -C ${env.root} push ${env.gitRemote} ${env.gitBranch}`);
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    await appendFile(
      path.join(env.root, "events/events.jsonl"),
      `${JSON.stringify({ ts: now, agent_id: env.agentId, type: "git_sync", level: "warn", message })}\n`
    );
  }
}

async function collect() {
  const snapshot = await collectSnapshot();

  if (env.reportMode === "cloudflare") {
    await reportCloudflare(snapshot);
  } else {
    await writeLocal(snapshot);
  }

  await maybeGitSync(snapshot.now);
  process.stdout.write(`Collected state for ${snapshot.agent.id} at ${snapshot.now} using mode=${env.reportMode}\n`);
}

collect().catch((err) => {
  process.stderr.write(`${err instanceof Error ? err.stack : String(err)}\n`);
  process.exit(1);
});
