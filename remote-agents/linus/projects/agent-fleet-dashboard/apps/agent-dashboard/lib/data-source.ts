import { z } from "zod";
import { mockFleetData } from "@/lib/mock-data";
import { FleetData } from "@/types/data";

const sourceMode = process.env.NEXT_PUBLIC_DATA_SOURCE_MODE ?? "local";

const registrySchema = z.object({
  updated_at: z.string(),
  agents: z.union([
    z.array(z.object({ id: z.string(), name: z.string(), role: z.string(), description: z.string().optional(), owner: z.string().optional() })),
    z.record(z.object({ name: z.string().optional(), role: z.string().optional(), description: z.string().optional(), owner: z.string().optional() }))
  ])
});

type Registry = z.infer<typeof registrySchema>;

function normalizeAgents(reg: Registry): FleetData["agents"] {
  return Array.isArray(reg.agents)
    ? reg.agents
    : Object.entries(reg.agents).map(([id, value]) => ({
        id,
        name: value.name ?? id,
        role: value.role ?? "Unknown",
        description: value.description,
        owner: value.owner
      }));
}

async function loadFromLocal(root: string): Promise<FleetData> {
  const fs = await import("node:fs/promises");
  const path = await import("node:path");

  const readJson = async (p: string) => JSON.parse(await fs.readFile(p, "utf8"));
  const readMaybe = async (p: string) => {
    try {
      return await fs.readFile(p, "utf8");
    } catch {
      return null;
    }
  };

  const regRaw = await readJson(path.join(root, "registry/agent-registry.json"));
  const reg = registrySchema.parse(regRaw);
  const agents = normalizeAgents(reg);

  const heartbeats: FleetData["heartbeats"] = {};
  const crons: FleetData["crons"] = {};
  const runtime: FleetData["runtime"] = {};

  for (const a of agents) {
    const hb = await readMaybe(path.join(root, `state/heartbeats/${a.id}.json`));
    if (hb) heartbeats[a.id] = JSON.parse(hb);
    const cr = await readMaybe(path.join(root, `state/crons/${a.id}.json`));
    if (cr) crons[a.id] = JSON.parse(cr);
    const rt = await readMaybe(path.join(root, `state/runtime/${a.id}.json`));
    if (rt) runtime[a.id] = JSON.parse(rt);
  }

  const eventsRaw = (await readMaybe(path.join(root, "events/events.jsonl"))) ?? "";
  const events = eventsRaw
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line))
    .sort((a, b) => new Date(b.ts).getTime() - new Date(a.ts).getTime());

  const versionRaw = (await readMaybe(path.join(root, "meta/schema-version.json"))) ?? "{}";
  const version = JSON.parse(versionRaw);

  return {
    updatedAt: reg.updated_at,
    schemaVersion: version.version ?? "unknown",
    agents,
    heartbeats,
    crons,
    runtime,
    events
  };
}

async function loadFromGitHub(owner: string, repo: string, branch: string, token: string): Promise<FleetData> {
  const readPath = async (p: string): Promise<string> => {
    const url = `https://api.github.com/repos/${owner}/${repo}/contents/${p}?ref=${branch}`;
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json" },
      cache: "no-store"
    });
    if (!res.ok) throw new Error(`GitHub read failed for ${p}: ${res.status}`);
    const body = (await res.json()) as { content: string; encoding: string };
    const base64 = body.content.replace(/\n/g, "");
    return Buffer.from(base64, "base64").toString("utf8");
  };

  const regRaw = JSON.parse(await readPath("registry/agent-registry.json"));
  const reg = registrySchema.parse(regRaw);
  const agents = normalizeAgents(reg);

  const heartbeats: FleetData["heartbeats"] = {};
  const crons: FleetData["crons"] = {};
  const runtime: FleetData["runtime"] = {};

  for (const a of agents) {
    for (const [kind, store] of [
      ["heartbeats", heartbeats],
      ["crons", crons],
      ["runtime", runtime]
    ] as const) {
      try {
        const content = await readPath(`state/${kind}/${a.id}.json`);
        store[a.id] = JSON.parse(content);
      } catch {
        // optional data
      }
    }
  }

  let events: FleetData["events"] = [];
  try {
    events = (await readPath("events/events.jsonl"))
      .split("\n")
      .filter(Boolean)
      .map((line) => JSON.parse(line));
  } catch {
    // optional
  }

  let schemaVersion = "unknown";
  try {
    schemaVersion = JSON.parse(await readPath("meta/schema-version.json")).version;
  } catch {
    // optional
  }

  return {
    updatedAt: reg.updated_at,
    schemaVersion,
    agents,
    heartbeats,
    crons,
    runtime,
    events
  };
}

async function loadFromCloudflare(endpoint: string, token: string): Promise<FleetData> {
  const res = await fetch(`${endpoint.replace(/\/$/, "")}/fleet`, {
    headers: { authorization: `Bearer ${token}` },
    cache: "no-store"
  });
  if (!res.ok) {
    throw new Error(`Cloudflare fleet read failed: ${res.status}`);
  }
  return (await res.json()) as FleetData;
}

export async function getFleetData(): Promise<FleetData> {
  try {
    if (sourceMode === "cloudflare") {
      const endpoint = process.env.FLEET_API_ENDPOINT;
      const token = process.env.DASHBOARD_READ_TOKEN;
      if (endpoint && token) return await loadFromCloudflare(endpoint, token);
    }

    if (sourceMode === "github") {
      const owner = process.env.GITHUB_REPO_OWNER;
      const repo = process.env.GITHUB_REPO_NAME;
      const branch = process.env.GITHUB_REPO_BRANCH ?? "main";
      const token = process.env.GITHUB_TOKEN;
      if (owner && repo && token) return await loadFromGitHub(owner, repo, branch, token);
    }

    const localRoot = (process.env.AGENT_DATA_LOCAL_ROOT ?? "~/.openclaw/shared/agent-network-data").replace("~", process.env.HOME ?? "");
    return await loadFromLocal(localRoot);
  } catch {
    return mockFleetData;
  }
}
