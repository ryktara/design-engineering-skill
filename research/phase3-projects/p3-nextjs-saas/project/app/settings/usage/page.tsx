import type { Metadata } from "next";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { QuotaMeter } from "@/components/usage/quota-meter";
import { DailyUsageChart } from "@/components/usage/daily-usage-chart";
import { UsageByKey } from "@/components/usage/usage-by-key";
import { getSubscription, plans } from "@/lib/billing";
import {
  daysInPeriod,
  formatAsOf,
  formatCount,
  formatPeriodLabel,
  getUsagePeriod,
  planCallQuota,
  projectedCalls,
  totalCalls,
} from "@/lib/usage";
import { cn } from "@/lib/utils";

export const metadata: Metadata = { title: "Usage · Settings · Acme Console" };

export default async function UsageSettingsPage() {
  const [subscription, usage] = await Promise.all([getSubscription(), getUsagePeriod()]);
  const plan = plans.find((p) => p.id === subscription.planId)!;
  const quota = planCallQuota[subscription.planId];
  const used = totalCalls(usage.daily);
  const totalDays = daysInPeriod(usage);
  const elapsedDays = usage.daily.length;
  const projected = projectedCalls(used, elapsedDays, totalDays);
  const pct = quota > 0 ? Math.round((used / quota) * 100) : 0;
  const remaining = Math.max(0, quota - used);
  const overQuota = used >= quota;
  const projectedOver = !overQuota && projected > quota;

  return (
    <div className="space-y-8">
      {/* Summary: same stat-card language as the dashboard and the billing page. */}
      <section aria-labelledby="usage-summary-heading" className="space-y-4">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h2 id="usage-summary-heading" className="text-lg font-semibold tracking-tight">
              {formatPeriodLabel(usage.periodStart)}
            </h2>
            <p className="text-sm text-muted-foreground">
              Day <span className="tabular-nums">{elapsedDays}</span> of <span className="tabular-nums">{totalDays}</span> in
              this billing period. Updated {formatAsOf(usage.asOf)}.
            </p>
          </div>
          <Link href="/settings/billing" className={cn(buttonVariants({ variant: "outline", size: "sm" }))}>
            Manage plan
          </Link>
        </div>

        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>API calls this month</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="text-2xl tabular-nums">{formatCount(used)}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>
                <span className="tabular-nums">{pct}%</span> of the {plan.name} quota
              </dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Included in {plan.name}</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="text-2xl tabular-nums">{formatCount(quota)}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>calls per billing month</dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Remaining</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="text-2xl tabular-nums">{formatCount(remaining)}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>until {formatPeriodLabel(usage.periodEnd)}</dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Projected this month</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="text-2xl tabular-nums">{formatCount(projected)}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>at the current daily rate</dd>
            </CardContent>
          </Card>
        </dl>

        <div className="rounded-lg border p-4">
          <QuotaMeter used={used} quota={quota} projected={projected} label="API calls against the plan quota" />
        </div>

        {(overQuota || projectedOver) && (
          <p
            className={cn(
              "flex flex-wrap items-center justify-between gap-2 rounded-lg border px-4 py-2 text-sm",
              overQuota ? "border-destructive/40" : "bg-muted/40"
            )}
          >
            <span>
              {overQuota ? (
                <>
                  You have used all <span className="tabular-nums">{formatCount(quota)}</span> calls included in {plan.name}.
                  Additional calls are billed at the overage rate.
                </>
              ) : (
                <>
                  At this rate you will pass the {plan.name} quota before {formatPeriodLabel(usage.periodEnd)}.
                </>
              )}
            </span>
            <Link href="/settings/billing" className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "-mx-2")}>
              Compare plans
            </Link>
          </p>
        )}
      </section>

      <section aria-labelledby="usage-daily-heading" className="space-y-4">
        <div>
          <h2 id="usage-daily-heading" className="text-lg font-semibold tracking-tight">
            Daily volume
          </h2>
          <p className="text-sm text-muted-foreground">Calls counted when the request reaches the API, including errors.</p>
        </div>
        <DailyUsageChart days={usage.daily} />
      </section>

      <section aria-labelledby="usage-by-key-heading" className="space-y-4">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h2 id="usage-by-key-heading" className="text-lg font-semibold tracking-tight">
              Calls by key
            </h2>
            <p className="text-sm text-muted-foreground">Which key is spending the quota.</p>
          </div>
          <Link href="/settings/api-keys" className={cn(buttonVariants({ variant: "outline", size: "sm" }))}>
            Manage API keys
          </Link>
        </div>
        <UsageByKey byKey={usage.byKey} total={used} />
      </section>
    </div>
  );
}
