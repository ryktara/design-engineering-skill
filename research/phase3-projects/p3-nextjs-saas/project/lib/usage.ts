import type { PlanId } from "@/lib/billing";

// API-call quota that comes with each plan, per billing month.
export const planCallQuota: Record<PlanId, number> = {
  starter: 50_000,
  team: 250_000,
  business: 2_000_000,
};

export interface UsageDay {
  date: string; // ISO date
  calls: number;
}

export interface KeyUsage {
  keyId: string;
  name: string;
  calls: number;
}

export interface UsagePeriod {
  planId: PlanId;
  periodStart: string; // ISO date, inclusive
  periodEnd: string; // ISO date, exclusive (next renewal of the usage month)
  asOf: string; // ISO timestamp the counters were last aggregated
  daily: UsageDay[]; // one entry per elapsed day of the current period
  byKey: KeyUsage[];
}

// Fixture: September 2026, 15 of 30 days elapsed — same fixed clock as lib/billing.ts.
const dailyCalls = [
  6120, 7340, 5980, 4110, 3620, 8020, 9140, 8760, 7480, 6910, 5230, 4020, 9880, 11240, 10460,
];

const period: UsagePeriod = {
  planId: "team",
  periodStart: "2026-09-01",
  periodEnd: "2026-10-01",
  asOf: "2026-09-15T09:40:00Z",
  daily: dailyCalls.map((calls, i) => ({
    date: `2026-09-${String(i + 1).padStart(2, "0")}`,
    calls,
  })),
  byKey: [
    { keyId: "key_01", name: "Production server", calls: 93520 },
    { keyId: "key_02", name: "Reporting export", calls: 14790 },
    { keyId: "key_03", name: "Old CI runner", calls: 0 },
  ],
};

// Simulated data access; in the real app this hits the metering service.
export async function getUsagePeriod(): Promise<UsagePeriod> {
  return period;
}

export function totalCalls(days: UsageDay[]) {
  return days.reduce((sum, d) => sum + d.calls, 0);
}

export function daysInPeriod(period: Pick<UsagePeriod, "periodStart" | "periodEnd">) {
  const ms = new Date(period.periodEnd).getTime() - new Date(period.periodStart).getTime();
  return Math.round(ms / 86_400_000);
}

// Straight-line projection from the elapsed days; rounded to whole calls.
export function projectedCalls(used: number, elapsedDays: number, totalDays: number) {
  if (elapsedDays <= 0) return 0;
  return Math.round((used / elapsedDays) * totalDays);
}

export function formatCount(n: number, locale: string = "en-US") {
  return new Intl.NumberFormat(locale).format(n);
}

export function formatPeriodLabel(iso: string, locale: string = "en-US") {
  return new Intl.DateTimeFormat(locale, { year: "numeric", month: "long" }).format(new Date(iso));
}

export function formatDayLabel(iso: string, locale: string = "en-US") {
  return new Intl.DateTimeFormat(locale, { month: "short", day: "numeric" }).format(new Date(iso));
}

export function formatAsOf(iso: string, locale: string = "en-US") {
  return new Intl.DateTimeFormat(locale, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(
    new Date(iso)
  );
}
