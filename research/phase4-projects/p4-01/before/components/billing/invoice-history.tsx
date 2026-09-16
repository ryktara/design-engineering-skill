import { Download, FileText } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatDate, formatMoney, type Invoice, type InvoiceStatus } from "@/lib/billing";

export function InvoiceHistory({ invoices }: { invoices: Invoice[] }) {
  return (
    <section aria-labelledby="invoices-heading" className="space-y-4">
      <div>
        <h2 id="invoices-heading" className="text-lg font-semibold tracking-tight">
          Invoice history
        </h2>
        <p className="text-sm text-muted-foreground">Amounts in USD. Receipts are also emailed to billing@acme.example.</p>
      </div>

      {invoices.length === 0 ? (
        <div className="flex flex-col items-center gap-2 rounded-lg border border-dashed p-10 text-center">
          <FileText className="size-6 text-muted-foreground" aria-hidden="true" />
          <p className="text-sm font-medium">No invoices yet</p>
          <p className="text-sm text-muted-foreground">Your first invoice is issued at the start of the next billing period.</p>
        </div>
      ) : (
        <div className="rounded-lg border">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead scope="col">Invoice</TableHead>
                <TableHead scope="col" className="hidden sm:table-cell">
                  Issued
                </TableHead>
                <TableHead scope="col" className="hidden md:table-cell">
                  Period
                </TableHead>
                <TableHead scope="col" className="whitespace-nowrap text-right">
                  Amount<span className="hidden md:inline"> (USD)</span>
                </TableHead>
                <TableHead scope="col">Status</TableHead>
                <TableHead scope="col" className="text-right">
                  <span className="sr-only">Download</span>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {invoices.map((inv) => (
                <TableRow key={inv.id}>
                  <TableCell>
                    <span className="whitespace-nowrap font-mono text-xs sm:text-sm">{inv.id}</span>
                    <span className="block text-xs text-muted-foreground sm:hidden">{formatDate(inv.issuedAt)}</span>
                  </TableCell>
                  <TableCell className="hidden tabular-nums sm:table-cell">{formatDate(inv.issuedAt)}</TableCell>
                  <TableCell className="hidden md:table-cell">{inv.periodLabel}</TableCell>
                  <TableCell className="text-right font-medium tabular-nums">{formatMoney(inv.amountCents, inv.currency)}</TableCell>
                  <TableCell>
                    <InvoiceStatusBadge status={inv.status} />
                  </TableCell>
                  <TableCell className="text-right">
                    <a
                      href={inv.pdfUrl}
                      download
                      aria-label={`Download invoice ${inv.id} (PDF)`}
                      className="inline-flex h-8 items-center justify-center gap-1.5 rounded-md px-2 text-sm text-foreground underline-offset-4 outline-none hover:underline focus-visible:ring-2 focus-visible:ring-ring max-sm:size-11 max-sm:px-0"
                    >
                      <Download className="size-4" aria-hidden="true" />
                      <span className="hidden sm:inline">PDF</span>
                    </a>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </section>
  );
}

function InvoiceStatusBadge({ status }: { status: InvoiceStatus }) {
  switch (status) {
    case "paid":
      return (
        <Badge variant="outline" className="gap-1.5 border-success/40 text-success">
          <span className="size-1.5 rounded-full bg-success" aria-hidden="true" />
          Paid
        </Badge>
      );
    case "open":
      return <Badge variant="secondary">Open</Badge>;
    case "past_due":
      return (
        <Badge variant="outline" className="gap-1.5 border-destructive/40 text-destructive">
          <span className="size-1.5 rounded-full bg-destructive" aria-hidden="true" />
          Past due
        </Badge>
      );
    case "void":
      return (
        <Badge variant="outline" className="text-muted-foreground">
          Void
        </Badge>
      );
  }
}
