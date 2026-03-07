export type HealthLevel = "green" | "yellow" | "red";

export interface AgentRegistryItem {
  id: string;
  name: string;
  role: string;
  description?: string;
  owner?: string;
}

export interface HeartbeatState {
  agent_id: string;
  last_seen: string;
  interval_sec: number;
  status?: string;
}

export interface CronJobState {
  name: string;
  schedule?: string;
  consecutive_failures: number;
  last_run_at: string;
  last_status?: string;
}

export interface CronState {
  agent_id: string;
  jobs: CronJobState[];
}

export interface RuntimeState {
  agent_id: string;
  runtime: {
    host?: string;
    model?: string;
    uptime_sec?: number;
    channel?: string;
    last_openclaw_status_raw?: string;
  };
}

export interface EventItem {
  ts: string;
  agent_id: string;
  type: string;
  level: "info" | "warn" | "error";
  message: string;
  meta?: Record<string, unknown>;
}

export interface FleetData {
  updatedAt: string;
  schemaVersion: string;
  agents: AgentRegistryItem[];
  heartbeats: Record<string, HeartbeatState>;
  crons: Record<string, CronState>;
  runtime: Record<string, RuntimeState>;
  events: EventItem[];
}
