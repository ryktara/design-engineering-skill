import { Ban, CircleAlert, CircleCheck, CircleDashed, Download, FileText, type LucideIcon } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { StatusBadge, type StatusTone } from "@/components/billing/status-badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { formatDate, formatMoney, type Invoice, type InvoiceStatus } from "@/lib/billing";

const invoiceStatus: Record<InvoiceStatus, { label: string; tone: StatusTone; icon: LucideIcon }> = {
  paid: { label: "Paid", tone: "success", icon: CircleCheck },
  open: { label: "Open", tone: "info", icon: CircleDashed },
  past_due: { label: "Past due", tone: "destructive", icon: CircleAlert },
  void: { label: "Void", tone: "neutral", icon: Ban },
};

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
                    <StatusBadge tone={invoiceStatus[inv.status].tone} icon={invoiceStatus[inv.status].icon}>
                      {invoiceStatus[inv.status].label}
                    </StatusBadge>
                  </TableCell>
                  <TableCell className="text-right">
                    {/* Same ghost row-action style as the seat table; 44 px target below sm */}
                    <a
                      href={inv.pdfUrl}
                      download
                      aria-label={`Download invoice ${inv.id} (PDF)`}
                      className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "max-sm:size-11 max-sm:px-0")}
                    >
                      <Download aria-hidden="true" />
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
