import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatCount, type KeyUsage } from "@/lib/usage";

// Compare categories: horizontal bars sorted by value, zero-based, single colour, value labels
// outside the bar. The bar lives inside a real table cell so the numbers are readable without it.
export function UsageByKey({ byKey, total }: { byKey: KeyUsage[]; total: number }) {
  const rows = [...byKey].sort((a, b) => b.calls - a.calls);
  const max = Math.max(...rows.map((r) => r.calls), 1);

  if (rows.length === 0) {
    return (
      <div className="rounded-lg border border-dashed p-6 text-sm text-muted-foreground">
        No API keys have made calls in this period.
      </div>
    );
  }

  return (
    <div className="rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent">
            <TableHead scope="col">Key</TableHead>
            <TableHead scope="col" className="w-1/2">
              Share of calls
            </TableHead>
            <TableHead scope="col" className="text-right">
              Calls
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((r) => {
            const share = total > 0 ? Math.round((r.calls / total) * 100) : 0;
            return (
              <TableRow key={r.keyId}>
                <TableCell className="font-medium">{r.name}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <div aria-hidden="true" className="h-2 w-full max-w-56 overflow-hidden rounded-full bg-muted">
                      <div className="h-full bg-primary" style={{ width: `${Math.round((r.calls / max) * 100)}%` }} />
                    </div>
                    <span className="shrink-0 text-xs tabular-nums text-muted-foreground">{share}%</span>
                  </div>
                </TableCell>
                <TableCell className="text-right tabular-nums">{formatCount(r.calls)}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
