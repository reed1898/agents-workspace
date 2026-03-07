import Link from "next/link";

export const dynamic = "force-dynamic";
import { TopBanner } from "@/components/top-banner";
import { Card } from "@/components/ui/card";
import { getFleetData } from "@/lib/data-source";
import { evaluateHealth } from "@/lib/health";
import { formatAgo } from "@/lib/utils";

function statusTone(level: "green" | "yellow" | "red") {
  if (level === "red") return "bg-red-500/20 text-red-200";
  if (level === "yellow") return "bg-amber-500/20 text-amber-200";
  return "bg-emerald-500/20 text-emerald-200";
}

function deriveConnectivity(heartbeatLastSeen?: string, intervalSec?: number, rawStatus?: string) {
  const raw = (rawStatus ?? "").toLowerCase();
  if (raw.includes("openclaw status unavailable")) {
    return "unknown" as const;
  }
  if (raw.includes("reachable") || raw.includes("dashboard") || raw.includes("openclaw status")) {
    return "online" as const;
  }
  if (!heartbeatLastSeen || !intervalSec) return "unknown" as const;
  const deltaMs = Date.now() - new Date(heartbeatLastSeen).getTime();
  return deltaMs > intervalSec * 2 * 1000 ? "offline" : "online";
}

export default async function HomePage() {
  const data = await getFleetData();
  const agents = data.agents.slice(0, 4);

  return (
    <main className="space-y-4">
      <TopBanner updatedAt={data.updatedAt} />

      <Card className="overflow-x-auto">
        <div className="min-w-[980px]">
          <div className="grid grid-cols-6 gap-3 border-b border-slate-800 pb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            <div>Agent</div>
            <div>Status</div>
            <div>Last Seen</div>
            <div>Heartbeat</div>
            <div>Cron</div>
            <div>Error / Notes</div>
          </div>

          <div className="divide-y divide-slate-800/70">
            {agents.map((agent) => {
              const heartbeat = data.heartbeats[agent.id];
              const cron = data.crons[agent.id];
              const runtime = data.runtime[agent.id];
              const health = evaluateHealth(heartbeat, cron);
              const failedJobs = cron?.jobs?.filter((j) => (j.last_status ?? "").toLowerCase() === "fail").length ?? 0;

              return (
                <Link key={agent.id} href={`/agents/${agent.id}`} className="grid grid-cols-6 gap-3 py-3 text-sm transition hover:bg-slate-900/50">
                  <div>
                    <div className="flex items-center gap-2 font-medium text-slate-100">
                      <span>{agent.id}</span>
                      {(() => {
                        const connectivity = deriveConnectivity(heartbeat?.last_seen, heartbeat?.interval_sec, runtime?.runtime?.last_openclaw_status_raw);
                        const dot = connectivity === "online" ? "bg-emerald-400" : connectivity === "offline" ? "bg-red-400" : "bg-slate-400";
                        const label = connectivity.toUpperCase();
                        return (
                          <span className="inline-flex items-center gap-1 text-[11px] text-slate-300">
                            <span className={`h-2 w-2 rounded-full ${dot}`} />
                            {label}
                          </span>
                        );
                      })()}
                    </div>
                    <div className="text-xs text-slate-400">{agent.name} · {agent.role}</div>
                  </div>

                  <div>
                    <span className={`rounded px-2 py-1 text-xs font-medium ${statusTone(health.level)}`}>{health.level.toUpperCase()}</span>
                  </div>

                  <div className="text-slate-200">{heartbeat ? formatAgo(heartbeat.last_seen) : "-"}</div>

                  <div className="text-slate-200">
                    {heartbeat?.interval_sec ? `${heartbeat.interval_sec}s` : "-"}
                    <div className="text-xs text-slate-400">last: {heartbeat ? formatAgo(heartbeat.last_seen) : "-"}</div>
                  </div>

                  <div className="text-slate-200">
                    fail jobs: {failedJobs}
                    <div className="text-xs text-slate-400">total: {cron?.jobs?.length ?? 0}</div>
                  </div>

                  <div className="text-slate-300">
                    {health.reasons.length > 0 ? (
                      <span className="rounded bg-amber-500/20 px-2 py-1 text-xs text-amber-200">{health.reasons.length} issue(s)</span>
                    ) : (
                      <span className="rounded bg-emerald-500/20 px-2 py-1 text-xs text-emerald-200">clean</span>
                    )}
                    <div className="mt-1 text-xs text-slate-400">click row for details</div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </Card>
    </main>
  );
}
