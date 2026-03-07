import { CronState, HeartbeatState, HealthLevel } from "@/types/data";

export function evaluateHealth(heartbeat?: HeartbeatState, cron?: CronState): { level: HealthLevel; reasons: string[] } {
  const now = Date.now();
  const reasons: string[] = [];
  let level: HealthLevel = "green";

  if (heartbeat) {
    const lastSeenMs = new Date(heartbeat.last_seen).getTime();
    const ageMs = now - lastSeenMs;
    if (ageMs > 10 * 60_000) {
      level = "yellow";
      reasons.push("last_seen > 10min");
    }
    if (ageMs > heartbeat.interval_sec * 2 * 1000) {
      level = level === "green" ? "yellow" : level;
      reasons.push("heartbeat overdue > 2x interval");
    }
  } else {
    level = "yellow";
    reasons.push("missing heartbeat");
  }

  if (cron?.jobs.some((job) => job.consecutive_failures >= 3)) {
    level = "red";
    reasons.push("cron consecutive_failures >= 3");
  }

  return { level, reasons };
}

export function isStale(updatedAt: string): boolean {
  return Date.now() - new Date(updatedAt).getTime() > 5 * 60_000;
}
