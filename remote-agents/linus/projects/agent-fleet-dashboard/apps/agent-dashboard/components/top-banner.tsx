import { isStale } from "@/lib/health";
import { formatAgo } from "@/lib/utils";

export function TopBanner({ updatedAt }: { updatedAt: string }) {
  const stale = isStale(updatedAt);

  return (
    <div className={`mb-6 rounded-xl border px-4 py-3 text-sm ${stale ? "border-amber-500/40 bg-amber-500/10 text-amber-200" : "border-emerald-500/30 bg-emerald-500/10 text-emerald-200"}`}>
      Data last updated {formatAgo(updatedAt)} ({new Date(updatedAt).toLocaleString()}) · {stale ? "STALE (>5m)" : "fresh"}
    </div>
  );
}
