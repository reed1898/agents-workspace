import { FleetData } from "@/types/data";

const now = new Date();

export const mockFleetData: FleetData = {
  updatedAt: now.toISOString(),
  schemaVersion: "1.0.0",
  agents: [
    { id: "linus", name: "Linus", role: "Builder", description: "Main build copilot" },
    { id: "atlas", name: "Atlas", role: "Ops", description: "Infra and deployment" },
    { id: "echo", name: "Echo", role: "Comms", description: "Messaging and summary" },
    { id: "nova", name: "Nova", role: "Research", description: "External intel" }
  ],
  heartbeats: {
    linus: { agent_id: "linus", last_seen: new Date(now.getTime() - 2 * 60_000).toISOString(), interval_sec: 120 },
    atlas: { agent_id: "atlas", last_seen: new Date(now.getTime() - 6 * 60_000).toISOString(), interval_sec: 120 },
    echo: { agent_id: "echo", last_seen: new Date(now.getTime() - 13 * 60_000).toISOString(), interval_sec: 120 },
    nova: { agent_id: "nova", last_seen: new Date(now.getTime() - 1 * 60_000).toISOString(), interval_sec: 120 }
  },
  crons: {
    linus: { agent_id: "linus", jobs: [{ name: "daily-digest", schedule: "0 9 * * *", consecutive_failures: 0, last_run_at: now.toISOString(), last_status: "ok" }] },
    atlas: { agent_id: "atlas", jobs: [{ name: "backup", schedule: "*/30 * * * *", consecutive_failures: 1, last_run_at: now.toISOString(), last_status: "warn" }] },
    echo: { agent_id: "echo", jobs: [{ name: "event-sync", schedule: "*/5 * * * *", consecutive_failures: 3, last_run_at: now.toISOString(), last_status: "error" }] },
    nova: { agent_id: "nova", jobs: [{ name: "trend-scan", schedule: "0 * * * *", consecutive_failures: 0, last_run_at: now.toISOString(), last_status: "ok" }] }
  },
  runtime: {
    linus: { agent_id: "linus", runtime: { host: "Rain2018", model: "gpt-5", channel: "webchat", uptime_sec: 8400 } },
    atlas: { agent_id: "atlas", runtime: { host: "VPS-01", model: "gpt-4.1", channel: "discord", uptime_sec: 4200 } },
    echo: { agent_id: "echo", runtime: { host: "Rain2018", model: "gpt-4.1-mini", channel: "telegram", uptime_sec: 2000 } },
    nova: { agent_id: "nova", runtime: { host: "Rain2018", model: "gpt-5-mini", channel: "webchat", uptime_sec: 900 } }
  },
  events: [
    { ts: now.toISOString(), agent_id: "linus", type: "heartbeat", level: "info", message: "Heartbeat received" },
    { ts: now.toISOString(), agent_id: "echo", type: "cron", level: "error", message: "event-sync failed 3 times" },
    { ts: now.toISOString(), agent_id: "atlas", type: "runtime", level: "warn", message: "Runtime reconnect took 8s" }
  ]
};
