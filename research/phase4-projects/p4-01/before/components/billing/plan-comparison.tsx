"use client";

import * as React from "react";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { BillingCycle, Plan, PlanId } from "@/lib/billing";

interface Props {
  plans: Plan[];
  currentPlanId: PlanId;
  currentCycle: BillingCycle;
  seatsInUse: number;
}

export function PlanComparison({ plans, currentPlanId, currentCycle, seatsInUse }: Props) {
  const [cycle, setCycle] = React.useState<BillingCycle>(currentCycle);
  const currentIndex = plans.findIndex((p) => p.id === currentPlanId);

  return (
    <section aria-labelledby="plans-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="plans-heading" className="text-lg font-semibold tracking-tight">
            Plans
          </h2>
          <p className="text-sm text-muted-foreground">Per seat, billed {cycle === "annual" ? "annually" : "monthly"}. Changes apply at the next renewal.</p>
        </div>
        <div role="group" aria-label="Billing cycle" className="inline-flex rounded-md border bg-muted p-0.5 text-sm">
          {(["monthly", "annual"] as BillingCycle[]).map((c) => (
            <button
              key={c}
              type="button"
              aria-pressed={cycle === c}
              onClick={() => setCycle(c)}
              className={cn(
                "h-8 rounded-[calc(var(--radius)-4px)] px-3 outline-none transition-colors focus-visible:ring-2 focus-visible:ring-ring",
                cycle === c ? "bg-background font-medium text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
              )}
            >
              {c === "monthly" ? "Monthly" : "Annual"}
              {c === "annual" && <span className="ml-1 text-xs text-success">-15%</span>}
            </button>
          ))}
        </div>
      </div>

      <ul className="grid gap-4 md:grid-cols-3" aria-label="Available plans">
        {plans.map((plan, i) => {
          const isCurrent = plan.id === currentPlanId;
          const exceedsSeats = plan.seatLimit !== null && seatsInUse > plan.seatLimit;
          const action = isCurrent ? "current" : i < currentIndex ? "downgrade" : "upgrade";
          return (
            <li
              key={plan.id}
              aria-current={isCurrent ? "true" : undefined}
              className={cn(
                "relative flex flex-col rounded-lg border bg-card p-5 text-card-foreground",
                isCurrent ? "border-primary ring-1 ring-primary" : "border-border"
              )}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <h3 className="text-base font-semibold">{plan.name}</h3>
                  <p className="mt-1 min-h-10 text-sm text-muted-foreground">{plan.description}</p>
                </div>
                {isCurrent && (
                  <Badge variant="default" className="shrink-0 gap-1">
                    <Check className="size-3" aria-hidden="true" />
                    Current
                  </Badge>
                )}
              </div>
              <p className="mt-4 flex items-baseline gap-1">
                <span className="text-3xl font-semibold tabular-nums tracking-tight">${plan.pricePerSeat[cycle]}</span>
                <span className="text-sm text-muted-foreground">/ seat / month</span>
              </p>
              <p className="text-xs text-muted-foreground">
                {plan.seatLimit === null ? "Unlimited seats" : `Up to ${plan.seatLimit} seats`}
              </p>
              <ul className="mt-4 flex-1 space-y-2 text-sm">
                {plan.features.map((f) => (
                  <li key={f} className="flex gap-2">
                    <Check className="mt-0.5 size-4 shrink-0 text-success" aria-hidden="true" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-5">
                {action === "current" ? (
                  <Button variant="outline" className="w-full" disabled aria-disabled="true">
                    Current plan
                  </Button>
                ) : (
                  <Button
                    variant={action === "upgrade" ? "default" : "outline"}
                    className={cn("w-full", exceedsSeats && "opacity-60")}
                    aria-disabled={exceedsSeats || undefined}
                    onClick={(e) => exceedsSeats && e.preventDefault()}
                    aria-describedby={exceedsSeats ? `${plan.id}-limit` : undefined}
                  >
                    {action === "upgrade" ? `Upgrade to ${plan.name}` : `Downgrade to ${plan.name}`}
                  </Button>
                )}
                {exceedsSeats && (
                  <p id={`${plan.id}-limit`} className="mt-2 text-xs text-warning">
                    You have {seatsInUse} seats in use; remove {seatsInUse - (plan.seatLimit ?? 0)} to downgrade.
                  </p>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
