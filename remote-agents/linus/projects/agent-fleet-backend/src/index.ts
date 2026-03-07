interface Env {
  FLEET_KV: KVNamespace;
  INGEST_TOKEN: string;
  READ_TOKEN?: string;
  EVENTS_MAX?: string;
}

type JsonMap = Record<string, unknown>;

type Heartbeat = {
  agent_id: string;
  last_seen: string;
  interval_sec: number;
  status?: string;
};

type Cron = {
  agent_id: string;
  jobs: Array<{
    name: string;
    schedule?: string;
    consecutive_failures: number;
    last_run_at: string;
    last_status?: string;
  }>;
};

type Runtime = {
  agent_id: string;
  runtime: JsonMap;
};

type FleetEvent = {
  ts: string;
  agent_id: string;
  type: string;
  level: "info" | "warn" | "error";
  message: string;
  meta?: JsonMap;
};

type Agent = {
  id: string;
  name?: string;
  role?: string;
  description?: string;
  owner?: string;
};

type Registry = {
  updated_at?: string;
  agents: Agent[] | Record<string, Agent>;
};

type IngestPayload = {
  agent_id: string;
  registry?: Registry;
  heartbeat?: Heartbeat;
  cron?: Cron;
  runtime?: Runtime;
  event?: FleetEvent;
  events?: FleetEvent[];
};

const KEY = {
  registry: "fleet:registry",
  eventsRecent: "fleet:events:recent",
  updatedAt: "fleet:updated_at"
};

const json = (data: unknown, status = 200): Response =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
  });

const unauthorized = (message: string): Response => json({ ok: false, error: message }, 401);
const badRequest = (message: string): Response => json({ ok: false, error: message }, 400);

function parseBearer(req: Request): string | null {
  const header = req.headers.get("authorization");
  if (!header) return null;
  const [kind, token] = header.split(" ");
  if (kind?.toLowerCase() !== "bearer" || !token) return null;
  return token;
}

function authed(req: Request, expected: string | undefined): boolean {
  if (!expected) return false;
  const got = parseBearer(req);
  return got === expected;
}

function normalizeRegistryAgents(registry: Registry): Agent[] {
  if (Array.isArray(registry.agents)) return registry.agents;
  return Object.entries(registry.agents).map(([id, value]) => ({ ...value, id }));
}

function isObject(v: unknown): v is JsonMap {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function parseIngestPayload(value: unknown): { ok: true; payload: IngestPayload } | { ok: false; error: string } {
  if (!isObject(value)) return { ok: false, error: "Payload must be a JSON object" };
  if (typeof value.agent_id !== "string" || !value.agent_id.trim()) {
    return { ok: false, error: "agent_id is required" };
  }

  const payload: IngestPayload = { agent_id: value.agent_id };

  if (value.registry !== undefined) {
    if (!isObject(value.registry) || (value.registry as Registry).agents === undefined) {
      return { ok: false, error: "registry must contain agents" };
    }
    payload.registry = value.registry as Registry;
  }
  if (value.heartbeat !== undefined) payload.heartbeat = value.heartbeat as Heartbeat;
  if (value.cron !== undefined) payload.cron = value.cron as Cron;
  if (value.runtime !== undefined) payload.runtime = value.runtime as Runtime;
  if (value.event !== undefined) payload.event = value.event as FleetEvent;
  if (value.events !== undefined) {
    if (!Array.isArray(value.events)) return { ok: false, error: "events must be an array" };
    payload.events = value.events as FleetEvent[];
  }

  return { ok: true, payload };
}

async function readJsonFromKV<T>(kv: KVNamespace, key: string, fallback: T): Promise<T> {
  const raw = await kv.get(key);
  if (!raw) return fallback;
  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

async function appendEvents(kv: KVNamespace, incoming: FleetEvent[], max: number): Promise<FleetEvent[]> {
  if (incoming.length === 0) return readJsonFromKV<FleetEvent[]>(kv, KEY.eventsRecent, []);
  const existing = await readJsonFromKV<FleetEvent[]>(kv, KEY.eventsRecent, []);
  const merged = [...incoming, ...existing]
    .sort((a, b) => Date.parse(b.ts) - Date.parse(a.ts))
    .slice(0, max);
  await kv.put(KEY.eventsRecent, JSON.stringify(merged));
  return merged;
}

async function collectFleet(kv: KVNamespace): Promise<JsonMap> {
  const registry = await readJsonFromKV<Registry | null>(kv, KEY.registry, null);
  const updatedAt = (await kv.get(KEY.updatedAt)) ?? new Date(0).toISOString();
  const events = await readJsonFromKV<FleetEvent[]>(kv, KEY.eventsRecent, []);

  const agents = registry ? normalizeRegistryAgents(registry) : [];
  const heartbeats: Record<string, Heartbeat> = {};
  const crons: Record<string, Cron> = {};
  const runtime: Record<string, Runtime> = {};

  await Promise.all(
    agents.map(async (agent) => {
      const id = agent.id;
      if (!id) return;
      const [hb, cr, rt] = await Promise.all([
        kv.get(`fleet:heartbeat:${id}`),
        kv.get(`fleet:cron:${id}`),
        kv.get(`fleet:runtime:${id}`)
      ]);
      if (hb) heartbeats[id] = JSON.parse(hb) as Heartbeat;
      if (cr) crons[id] = JSON.parse(cr) as Cron;
      if (rt) runtime[id] = JSON.parse(rt) as Runtime;
    })
  );

  return {
    updatedAt,
    schemaVersion: "kv-v1",
    agents,
    heartbeats,
    crons,
    runtime,
    events
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const method = request.method.toUpperCase();

    if (url.pathname === "/health" && method === "GET") {
      return json({ ok: true, service: "agent-fleet-backend", now: new Date().toISOString() });
    }

    if (url.pathname === "/ingest" && method === "POST") {
      if (!authed(request, env.INGEST_TOKEN)) return unauthorized("invalid ingest token");

      let body: unknown;
      try {
        body = await request.json();
      } catch {
        return badRequest("invalid JSON body");
      }

      const parsed = parseIngestPayload(body);
      if (!parsed.ok) return badRequest(parsed.error);

      const { payload } = parsed;
      const now = new Date().toISOString();
      const writes: Array<Promise<void>> = [];

      if (payload.registry) {
        const existing = await readJsonFromKV<Registry | null>(env.FLEET_KV, KEY.registry, null);
        const mergedById = new Map<string, Agent>();
        for (const a of existing ? normalizeRegistryAgents(existing) : []) mergedById.set(a.id, a);
        for (const a of normalizeRegistryAgents(payload.registry)) mergedById.set(a.id, { ...mergedById.get(a.id), ...a });
        writes.push(
          env.FLEET_KV.put(
            KEY.registry,
            JSON.stringify({ updated_at: payload.registry.updated_at ?? now, agents: Array.from(mergedById.values()) })
          )
        );
      }
      if (payload.heartbeat) writes.push(env.FLEET_KV.put(`fleet:heartbeat:${payload.agent_id}`, JSON.stringify(payload.heartbeat)));
      if (payload.cron) writes.push(env.FLEET_KV.put(`fleet:cron:${payload.agent_id}`, JSON.stringify(payload.cron)));
      if (payload.runtime) writes.push(env.FLEET_KV.put(`fleet:runtime:${payload.agent_id}`, JSON.stringify(payload.runtime)));

      const events = [payload.event, ...(payload.events ?? [])].filter((e): e is FleetEvent => Boolean(e));
      await Promise.all(writes);
      await appendEvents(env.FLEET_KV, events, Number(env.EVENTS_MAX ?? "200") || 200);
      await env.FLEET_KV.put(KEY.updatedAt, now);

      return json({ ok: true, updated_at: now, writes: writes.length, events: events.length });
    }

    if (url.pathname === "/fleet" && method === "GET") {
      const readToken = env.READ_TOKEN || env.INGEST_TOKEN;
      if (!authed(request, readToken)) return unauthorized("invalid read token");
      const fleet = await collectFleet(env.FLEET_KV);
      return json(fleet);
    }

    return json({ ok: false, error: "not found" }, 404);
  }
};
