import { cn } from "@/lib/utils";
import { formatCount } from "@/lib/usage";

// Progress to a target: one measure bar with the numeric value, the whole, and a projection tick.
// Same meter semantics as the seat usage bar on the billing page (role="meter" + aria-valuetext),
// so colour is never the only cue — the label carries the numbers (WCAG 1.4.1).
export function QuotaMeter({
  used,
  quota,
  projected,
  label,
}: {
  used: number;
  quota: number;
  projected?: number;
  label: string;
}) {
  const pct = quota > 0 ? Math.min(100, Math.round((used / quota) * 100)) : 0;
  const projectedPct = projected !== undefined && quota > 0 ? Math.min(100, Math.round((projected / quota) * 100)) : null;
  const tone = pct >= 100 ? "bg-destructive" : pct >= 90 ? "bg-warning" : "bg-primary";

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1 text-sm">
        <span>
          <span className="font-medium tabular-nums text-foreground">{formatCount(used)}</span>{" "}
          <span className="text-muted-foreground">of {formatCount(quota)} calls included</span>
        </span>
        <span className="tabular-nums text-muted-foreground">{pct}% used</span>
      </div>
      <div
        role="meter"
        aria-label={label}
        aria-valuemin={0}
        aria-valuemax={quota}
        aria-valuenow={used}
        aria-valuetext={`${formatCount(used)} of ${formatCount(quota)} calls, ${pct} percent of the plan quota`}
        className="relative h-2 w-full overflow-hidden rounded-full bg-muted"
      >
        <div className={cn("h-full rounded-full", tone)} style={{ width: `${pct}%` }} />
        {projectedPct !== null && projectedPct > pct && (
          // Target tick: where this month lands at the current rate.
          <div
            aria-hidden="true"
            className="absolute top-0 h-full w-0.5 bg-foreground/60"
            style={{ left: `calc(${projectedPct}% - 1px)` }}
          />
        )}
      </div>
      {projectedPct !== null && (
        <p className="text-xs text-muted-foreground">
          Marker shows the projected end-of-month total at the current rate:{" "}
          <span className="tabular-nums">{formatCount(projected!)}</span> calls ({projectedPct}% of the quota).
        </p>
      )}
    </div>
  );
}
