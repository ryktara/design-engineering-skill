import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatCount, formatDayLabel, type UsageDay } from "@/lib/usage";

// Calls per day, zero-based, chronological (order is meaningful, so it is not sorted by value),
// one colour, no 3D, no rounded ends. The chart is decorative for assistive tech; the same numbers
// are available in the table below it, which is the accessible alternative.
export function DailyUsageChart({ days }: { days: UsageDay[] }) {
  if (days.length === 0) {
    return (
      <div className="rounded-lg border border-dashed p-6 text-sm text-muted-foreground">
        No calls recorded yet in this billing period. Daily volume appears here once your keys start receiving traffic.
      </div>
    );
  }

  const max = Math.max(...days.map((d) => d.calls), 1);
  const peak = days.reduce((a, b) => (b.calls > a.calls ? b : a));

  return (
    <figure className="space-y-3">
      <div className="rounded-lg border p-4">
        <ul aria-hidden="true" className="flex h-32 items-end gap-1">
          {days.map((d) => (
            <li
              key={d.date}
              className="flex h-full flex-1 items-end"
              title={`${formatDayLabel(d.date)}: ${formatCount(d.calls)}`}
            >
              <div
                className="w-full bg-primary"
                style={{ height: `${Math.max(2, Math.round((d.calls / max) * 100))}%` }}
              />
            </li>
          ))}
        </ul>
        <div aria-hidden="true" className="mt-2 flex justify-between text-xs tabular-nums text-muted-foreground">
          <span>{formatDayLabel(days[0].date)}</span>
          <span>{formatDayLabel(days[days.length - 1].date)}</span>
        </div>
      </div>
      <figcaption className="text-xs text-muted-foreground">
        Calls per day, {formatDayLabel(days[0].date)} to {formatDayLabel(days[days.length - 1].date)}. Busiest day{" "}
        {formatDayLabel(peak.date)} with <span className="tabular-nums">{formatCount(peak.calls)}</span> calls.
      </figcaption>
      <details className="rounded-lg border">
        <summary className="cursor-pointer px-4 py-3 text-sm font-medium outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring">
          Daily figures
        </summary>
        <div className="border-t">
          <Table>
            <TableCaption className="mb-4 mt-0 px-3">API calls per day in this billing period.</TableCaption>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead scope="col">Day</TableHead>
                <TableHead scope="col" className="text-right">
                  Calls
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {days.map((d) => (
                <TableRow key={d.date}>
                  <TableCell>{formatDayLabel(d.date)}</TableCell>
                  <TableCell className="text-right tabular-nums">{formatCount(d.calls)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </details>
    </figure>
  );
}
