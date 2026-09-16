"use client";

import * as React from "react";
import { Ban, ChevronDown, CircleAlert, CircleCheck, CircleDashed, Download, FileText, type LucideIcon } from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
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

// Rows shown before "Show all" expands the list (exceptions are always shown on top of this).
const INITIAL_ROWS = 12;

interface Group {
  key: string;
  label: string;
  invoices: Invoice[];
  attention?: boolean;
}

// Scan structure for long histories: invoices that need attention (open / past due) first, then
// everything else grouped by year with a per-year total so the eye has anchors instead of 30 uniform rows.
function groupInvoices(invoices: Invoice[]): Group[] {
  const sorted = [...invoices].sort((a, b) => b.issuedAt.localeCompare(a.issuedAt));
  const attention = sorted.filter((i) => i.status === "open" || i.status === "past_due");
  const rest = sorted.filter((i) => !(i.status === "open" || i.status === "past_due"));
  const byYear = new Map<string, Invoice[]>();
  for (const inv of rest) {
    const year = inv.issuedAt.slice(0, 4);
    byYear.set(year, [...(byYear.get(year) ?? []), inv]);
  }
  const groups: Group[] = [];
  if (attention.length) groups.push({ key: "attention", label: "Needs attention", invoices: attention, attention: true });
  for (const [year, list] of byYear) groups.push({ key: year, label: year, invoices: list });
  return groups;
}

function yearTotal(list: Invoice[]) {
  return list.filter((i) => i.status === "paid").reduce((sum, i) => sum + i.amountCents, 0);
}

export function InvoiceHistory({ invoices }: { invoices: Invoice[] }) {
  const [expanded, setExpanded] = React.useState(invoices.length <= INITIAL_ROWS + 4);
  const groups = React.useMemo(() => groupInvoices(invoices), [invoices]);
  const attentionCount = groups.find((g) => g.attention)?.invoices.length ?? 0;

  // Collapsed view keeps every exception plus the most recent INITIAL_ROWS regular rows; groups that end up empty are dropped.
  const visibleGroups = React.useMemo(() => {
    if (expanded) return groups;
    let budget = INITIAL_ROWS;
    return groups
      .map((g) => {
        if (g.attention) return g;
        const take = g.invoices.slice(0, Math.max(0, budget));
        budget -= take.length;
        return { ...g, invoices: take };
      })
      .filter((g) => g.invoices.length > 0);
  }, [groups, expanded]);
  const visibleCount = visibleGroups.reduce((n, g) => n + g.invoices.length, 0);
  const hiddenCount = invoices.length - visibleCount;

  // One Tab stop for the table (same roving-row pattern as the seat table); arrows move between rows,
  // Enter downloads the focused row's PDF, Right/Left reach the download link. Download links stay real <a download>.
  const tableRef = React.useRef<HTMLTableElement | null>(null);
  const [activeId, setActiveId] = React.useState<string>(() => groups[0]?.invoices[0]?.id ?? "");
  const showAllRef = React.useRef<HTMLButtonElement | null>(null);

  function rows(): HTMLTableRowElement[] {
    return tableRef.current ? [...tableRef.current.querySelectorAll<HTMLTableRowElement>("tr[data-invoice-id]")] : [];
  }
  function focusRow(row: HTMLTableRowElement | undefined) {
    if (!row) return;
    setActiveId(row.dataset.invoiceId!);
    row.focus();
  }
  function onKeyDown(e: React.KeyboardEvent<HTMLTableElement>) {
    const target = e.target as HTMLElement;
    const row = target.closest<HTMLTableRowElement>("tr[data-invoice-id]");
    if (!row) return;
    const all = rows();
    const i = all.indexOf(row);
    const link = row.querySelector<HTMLAnchorElement>("a[download]");
    switch (e.key) {
      case "ArrowDown":
        focusRow(all[Math.min(i + 1, all.length - 1)]);
        break;
      case "ArrowUp":
        focusRow(all[Math.max(i - 1, 0)]);
        break;
      case "Home":
        focusRow(all[0]);
        break;
      case "End":
        focusRow(all[all.length - 1]);
        break;
      case "ArrowRight":
        link?.focus();
        break;
      case "ArrowLeft":
      case "Escape":
        if (target === row) return;
        row.focus();
        break;
      case "Enter":
        if (target === row) link?.click();
        else return;
        break;
      default:
        return;
    }
    e.preventDefault();
  }
  function onFocus(e: React.FocusEvent<HTMLTableElement>) {
    const row = (e.target as HTMLElement).closest<HTMLTableRowElement>("tr[data-invoice-id]");
    if (row && row.dataset.invoiceId !== activeId) setActiveId(row.dataset.invoiceId!);
  }

  // After expanding, keep focus in the table (the "Show all" button unmounts).
  const firstNewIdRef = React.useRef<string | null>(null);
  function showAll() {
    const shown = new Set(visibleGroups.flatMap((g) => g.invoices.map((i) => i.id)));
    firstNewIdRef.current = groups.flatMap((g) => g.invoices).find((i) => !shown.has(i.id))?.id ?? null;
    setExpanded(true);
  }
  React.useEffect(() => {
    if (!expanded || !firstNewIdRef.current) return;
    const row = rows().find((r) => r.dataset.invoiceId === firstNewIdRef.current);
    firstNewIdRef.current = null;
    if (row) focusRow(row);
  }, [expanded]); // eslint-disable-line react-hooks/exhaustive-deps

  const colCount = 6;

  return (
    <section aria-labelledby="invoices-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="invoices-heading" tabIndex={-1} className="text-lg font-semibold tracking-tight outline-none">
            Invoice history
          </h2>
          <p className="text-sm text-muted-foreground">Amounts in USD. Receipts are also emailed to billing@acme.example.</p>
        </div>
        {invoices.length > 0 && (
          <p className="text-sm text-muted-foreground tabular-nums" aria-live="polite">
            <span className="font-medium text-foreground">{invoices.length}</span> invoices
            {attentionCount > 0 && (
              <>
                {" · "}
                <span className="font-medium text-destructive">{attentionCount}</span> need{attentionCount === 1 ? "s" : ""} attention
              </>
            )}
          </p>
        )}
      </div>

      {invoices.length === 0 ? (
        <div className="flex flex-col items-center gap-2 rounded-lg border border-dashed p-10 text-center">
          <FileText className="size-6 text-muted-foreground" aria-hidden="true" />
          <p className="text-sm font-medium">No invoices yet</p>
          <p className="text-sm text-muted-foreground">Your first invoice is issued at the start of the next billing period.</p>
        </div>
      ) : (
        <>
          <p id="invoices-grid-keys" className="sr-only">
            Invoice table. Use Up and Down arrows to move between invoices, Enter to download the focused invoice, Right arrow to reach its
            download link, Tab to leave the table.
          </p>
          {/* overflow-x-clip (not auto) keeps the header sticky to the page instead of the primitive's own scroll box; columns already collapse below sm/md. Below sm the four remaining columns need 8 px cell padding to fit 358 px without clipping the year total. */}
          <div className="rounded-lg border [&>div]:overflow-x-clip [&>div]:overflow-y-visible max-sm:[&_th]:px-2 max-sm:[&_td]:px-2">
            <Table
              ref={tableRef}
              role="grid"
              aria-labelledby="invoices-heading"
              aria-describedby="invoices-grid-keys"
              aria-rowcount={invoices.length + 1}
              onKeyDown={onKeyDown}
              onFocus={onFocus}
            >
              <TableHeader className="sticky top-0 z-10 bg-background [&_tr]:border-b">
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
              {/* One <tbody> per group so the group row is the head of its own row group. Group rows are deliberately not sticky: Chromium does not constrain a sticky <tr> to its <tbody>, so stacked group rows overlap at every transition; the year is already on every row (Issued column / stacked date), so only the column header needs to stick. */}
              {visibleGroups.map((group) => (
                <TableBody key={group.key} className="[&_tr:last-child]:border-b">
                    {/* Group anchor row: one per year, with the year's invoice count and paid total. */}
                    <TableRow className="border-b bg-muted hover:bg-muted">
                      <TableHead scope="rowgroup" colSpan={colCount} className="h-8 text-xs">
                        <div className="flex items-center justify-between gap-3">
                          <span className={cn("flex items-center gap-1.5", group.attention ? "text-destructive" : "text-foreground")}>
                            {group.attention && <CircleAlert className="size-3.5" strokeWidth={2.25} aria-hidden="true" />}
                            {group.label}
                            <span className="font-normal text-muted-foreground tabular-nums">
                              · {group.invoices.length} {group.invoices.length === 1 ? "invoice" : "invoices"}
                            </span>
                          </span>
                          {!group.attention && (
                            <span className="font-normal text-muted-foreground tabular-nums">
                              Paid <span className="text-foreground">{formatMoney(yearTotal(group.invoices))}</span>
                            </span>
                          )}
                        </div>
                      </TableHead>
                    </TableRow>
                    {group.invoices.map((inv) => {
                      const st = invoiceStatus[inv.status];
                      const index = invoices.findIndex((i) => i.id === inv.id);
                      return (
                        <TableRow
                          key={inv.id}
                          data-invoice-id={inv.id}
                          aria-rowindex={index + 2}
                          aria-label={`${inv.id}, ${inv.periodLabel}, ${formatMoney(inv.amountCents, inv.currency)}, ${st.label}`}
                          tabIndex={inv.id === activeId ? 0 : -1}
                          className={cn(
                            "outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring focus-within:bg-muted/50",
                            inv.status === "void" && "text-muted-foreground"
                          )}
                        >
                          <TableCell role="gridcell">
                            <span className="whitespace-nowrap font-mono text-xs sm:text-sm">{inv.id}</span>
                            <span className="block text-xs text-muted-foreground tabular-nums sm:hidden">{formatDate(inv.issuedAt)}</span>
                          </TableCell>
                          <TableCell role="gridcell" className="hidden whitespace-nowrap tabular-nums sm:table-cell">
                            {formatDate(inv.issuedAt)}
                          </TableCell>
                          <TableCell role="gridcell" className="hidden md:table-cell">
                            {inv.periodLabel}
                          </TableCell>
                          <TableCell
                            role="gridcell"
                            className={cn("whitespace-nowrap text-right font-medium tabular-nums", inv.status === "void" && "line-through decoration-muted-foreground/60 font-normal")}
                          >
                            {formatMoney(inv.amountCents, inv.currency)}
                          </TableCell>
                          <TableCell role="gridcell">
                            <StatusBadge tone={st.tone} icon={st.icon}>
                              {st.label}
                            </StatusBadge>
                          </TableCell>
                          <TableCell role="gridcell" className="text-right">
                            <a
                              href={inv.pdfUrl}
                              download
                              tabIndex={-1}
                              aria-label={`Download invoice ${inv.id} (PDF)`}
                              className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "max-sm:size-11 max-sm:px-0")}
                            >
                              <Download aria-hidden="true" />
                              <span className="hidden sm:inline">PDF</span>
                            </a>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                </TableBody>
              ))}
            </Table>
            {!expanded && hiddenCount > 0 && (
              <div className="flex items-center justify-between gap-3 border-t px-3 py-2 text-sm text-muted-foreground">
                <span className="tabular-nums">
                  Showing {visibleCount} of {invoices.length}
                </span>
                <Button ref={showAllRef} variant="ghost" size="sm" onClick={showAll} className="-mr-1">
                  <ChevronDown aria-hidden="true" />
                  Show all {invoices.length} invoices
                </Button>
              </div>
            )}
          </div>
        </>
      )}
    </section>
  );
}
