"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";

const tabs = ["heartbeat", "crons", "runtime", "events"] as const;

export function DetailTabs() {
  const search = useSearchParams();
  const pathname = usePathname();
  const current = search.get("tab") ?? "heartbeat";

  return (
    <div className="flex flex-wrap gap-2">
      {tabs.map((tab) => {
        const active = current === tab;
        const href = `${pathname}?tab=${tab}`;
        return (
          <Link
            key={tab}
            href={href}
            className={`rounded-lg px-3 py-1.5 text-sm capitalize transition ${
              active ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            {tab}
          </Link>
        );
      })}
    </div>
  );
}
