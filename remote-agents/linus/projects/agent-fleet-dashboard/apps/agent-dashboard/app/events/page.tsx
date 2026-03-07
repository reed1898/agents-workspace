import { getFleetData } from "@/lib/data-source";

export const dynamic = "force-dynamic";
import { Card } from "@/components/ui/card";

type Props = {
  searchParams: {
    type?: string;
    agent?: string;
    level?: string;
    limit?: string;
  };
};

export default async function EventsPage({ searchParams }: Props) {
  const data = await getFleetData();
  const limit = searchParams.limit === "200" ? 200 : 50;

  const filtered = data.events
    .filter((e) => (searchParams.type ? e.type === searchParams.type : true))
    .filter((e) => (searchParams.agent ? e.agent_id === searchParams.agent : true))
    .filter((e) => (searchParams.level ? e.level === searchParams.level : true))
    .slice(0, limit);

  return (
    <main className="space-y-4">
      <Card className="overflow-x-auto">
        <form className="grid min-w-[760px] grid-cols-5 gap-2 text-sm">
          <input name="type" defaultValue={searchParams.type} placeholder="type" className="rounded bg-slate-800 px-2 py-1" />
          <input name="agent" defaultValue={searchParams.agent} placeholder="agent id" className="rounded bg-slate-800 px-2 py-1" />
          <select name="level" defaultValue={searchParams.level ?? ""} className="rounded bg-slate-800 px-2 py-1">
            <option value="">all levels</option>
            <option value="info">info</option>
            <option value="warn">warn</option>
            <option value="error">error</option>
          </select>
          <select name="limit" defaultValue={String(limit)} className="rounded bg-slate-800 px-2 py-1">
            <option value="50">recent 50</option>
            <option value="200">recent 200</option>
          </select>
          <button className="rounded bg-emerald-600 px-3 py-1 text-white">Apply</button>
        </form>
      </Card>

      <Card className="overflow-x-auto">
        <div className="min-w-[980px]">
          <div className="grid grid-cols-6 gap-3 border-b border-slate-800 pb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            <div>Time</div>
            <div>Agent</div>
            <div>Type</div>
            <div>Level</div>
            <div className="col-span-2">Message</div>
          </div>

          <div className="divide-y divide-slate-800/70">
            {filtered.map((event, idx) => (
              <div key={`${event.ts}-${idx}`} className="grid grid-cols-6 gap-3 py-3 text-sm">
                <div className="text-slate-300">{new Date(event.ts).toLocaleString()}</div>
                <div className="text-slate-100">{event.agent_id}</div>
                <div className="text-slate-100">{event.type}</div>
                <div>
                  <span
                    className={`rounded px-2 py-1 text-xs ${
                      event.level === "error"
                        ? "bg-red-500/20 text-red-200"
                        : event.level === "warn"
                          ? "bg-amber-500/20 text-amber-200"
                          : "bg-emerald-500/20 text-emerald-200"
                    }`}
                  >
                    {event.level}
                  </span>
                </div>
                <div className="col-span-2 text-slate-200">{event.message}</div>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </main>
  );
}
