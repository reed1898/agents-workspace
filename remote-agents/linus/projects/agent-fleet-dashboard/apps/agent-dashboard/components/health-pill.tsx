import { Badge } from "@/components/ui/badge";
import { HealthLevel } from "@/types/data";

export function HealthPill({ level }: { level: HealthLevel }) {
  const classes = {
    green: "bg-emerald-500/20 text-emerald-300",
    yellow: "bg-amber-500/20 text-amber-300",
    red: "bg-rose-500/20 text-rose-300"
  };
  return <Badge className={classes[level]}>{level.toUpperCase()}</Badge>;
}
