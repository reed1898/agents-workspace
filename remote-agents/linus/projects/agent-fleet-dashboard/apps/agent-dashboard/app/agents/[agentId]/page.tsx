import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";
import { DetailTabs } from "@/components/ui/tabs";
import { Card, CardTitle } from "@/components/ui/card";
import { getFleetData } from "@/lib/data-source";

type Props = {
  params: { agentId: string };
  searchParams: { tab?: string };
};

function fmtDate(value?: string) {
  if (!value) return "-";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString();
}

function kvRow(label: string, value?: string | number | null) {
  return (
    <div className="grid grid-cols-3 gap-3 border-b border-slate-800 py-2 text-sm" key={label}>
      <div className="text-slate-400">{label}</div>
      <div className="col-span-2 text-slate-100">{value ?? "-"}</div>
    </div>
  );
}

export default async function AgentDetailPage({ params, searchParams }: Props) {
  const data = await getFleetData();
  const agent = data.agents.find((a) => a.id === params.agentId);
  if (!agent) return notFound();

  const tab = searchParams.tab ?? "heartbeat";

  const heartbeat = data.heartbeats[agent.id];
  const cronState = data.crons[agent.id];
  const runtime = data.runtime[agent.id];
  const events = data.events.filter((e) => e.agent_id === agent.id).slice(0, 50);

  const tabNode = {
    heartbeat: (
      <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
        {kvRow("Agent", heartbeat?.agent_id ?? agent.id)}
        {kvRow("Enabled", heartbeat?.status ? "yes" : "-")}
        {kvRow("Interval", heartbeat?.interval_sec ? `${heartbeat.interval_sec}s` : "-")}
        {kvRow("Last Seen", fmtDate(heartbeat?.last_seen))}
        <div className="pt-2 text-xs text-slate-400">Heartbeat state from shared data source.</div>
      </div>
    ),
    crons: (
      <div className="space-y-3">
        {!cronState?.jobs?.length && <div className="text-sm text-slate-400">No cron jobs found.</div>}
        {cronState?.jobs?.map((job) => (
          <div key={`${job.name}-${job.last_run_at}`} className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
            <div className="flex items-center justify-between gap-4">
              <div className="text-sm font-medium text-slate-100">{job.name}</div>
              <div className={`rounded px-2 py-1 text-xs ${job.consecutive_failures >= 3 ? "bg-red-500/20 text-red-200" : "bg-emerald-500/20 text-emerald-200"}`}>
                failures: {job.consecutive_failures}
              </div>
            </div>
            <div className="mt-3 space-y-1 text-sm">
              <div className="text-slate-300">Schedule: <span className="text-slate-100">{job.schedule ?? "-"}</span></div>
              <div className="text-slate-300">Last run: <span className="text-slate-100">{fmtDate(job.last_run_at)}</span></div>
              <div className="text-slate-300">Last status: <span className="text-slate-100">{job.last_status ?? "-"}</span></div>
            </div>
          </div>
        ))}
      </div>
    ),
    runtime: (
      <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
        {kvRow("Host", runtime?.runtime?.host)}
        {kvRow("Model", runtime?.runtime?.model)}
        {kvRow("Channel", runtime?.runtime?.channel)}
        {kvRow("Uptime", runtime?.runtime?.uptime_sec ? `${runtime.runtime.uptime_sec}s` : "-")}
        {kvRow("OpenClaw Status", runtime?.runtime?.last_openclaw_status_raw ?? "-")}
      </div>
    ),
    events: (
      <div className="space-y-2">
        {!events.length && <div className="text-sm text-slate-400">No events for this agent.</div>}
        {events.map((e, idx) => (
          <div key={`${e.ts}-${idx}`} className="rounded-xl border border-slate-800 bg-slate-950/40 p-3">
            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
              <span>{fmtDate(e.ts)}</span>
              <span className="rounded bg-slate-800 px-1.5 py-0.5">{e.type}</span>
              <span
                className={`rounded px-1.5 py-0.5 ${
                  e.level === "error" ? "bg-red-500/20 text-red-200" : e.level === "warn" ? "bg-amber-500/20 text-amber-200" : "bg-emerald-500/20 text-emerald-200"
                }`}
              >
                {e.level}
              </span>
            </div>
            <div className="mt-1 text-sm text-slate-100">{e.message}</div>
          </div>
        ))}
      </div>
    ),
  }[tab] ?? <div className="text-sm text-slate-300">Unknown tab</div>;

  return (
    <main className="space-y-4">
      <Card>
        <CardTitle>{agent.name}</CardTitle>
        <p className="text-sm text-slate-300">{agent.role}</p>
      </Card>
      <DetailTabs />
      <Card>{tabNode}</Card>
    </main>
  );
}
