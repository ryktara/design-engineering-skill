import type { Metadata } from "next";
import { CreditCard } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PlanComparison } from "@/components/billing/plan-comparison";
import { SeatTable } from "@/components/billing/seat-table";
import { InvoiceHistory } from "@/components/billing/invoice-history";
import { formatDate, formatMoney, getInvoices, getSeats, getSubscription, plans } from "@/lib/billing";

export const metadata: Metadata = { title: "Billing · Settings · Acme Console" };

export default async function BillingSettingsPage() {
  const [subscription, seats, invoices] = await Promise.all([getSubscription(), getSeats(), getInvoices()]);
  const plan = plans.find((p) => p.id === subscription.planId)!;
  const seatsInUse = seats.filter((s) => s.status !== "deactivated").length;
  const monthlyCents = plan.pricePerSeat[subscription.cycle] * subscription.seatsPurchased * 100;
  const openInvoice = invoices.find((i) => i.status === "open" || i.status === "past_due");

  return (
    <div className="space-y-10">
      <section aria-labelledby="summary-heading" className="rounded-lg border">
        <h2 id="summary-heading" className="sr-only">
          Current subscription
        </h2>
        <dl className="grid divide-y sm:grid-cols-2 sm:divide-x sm:divide-y-0 lg:grid-cols-4">
          <div className="p-4">
            <dt className="text-xs font-medium text-muted-foreground">Current plan</dt>
            <dd className="mt-1 text-base font-semibold">{plan.name}</dd>
            <dd className="text-xs text-muted-foreground">Billed {subscription.cycle === "annual" ? "annually" : "monthly"}</dd>
          </div>
          <div className="p-4">
            <dt className="text-xs font-medium text-muted-foreground">Seats</dt>
            <dd className="mt-1 text-base font-semibold tabular-nums">
              {seatsInUse} <span className="font-normal text-muted-foreground">/ {subscription.seatsPurchased}</span>
            </dd>
            <dd className="text-xs text-muted-foreground">{subscription.seatsPurchased - seatsInUse} available</dd>
          </div>
          <div className="p-4">
            <dt className="text-xs font-medium text-muted-foreground">Next charge</dt>
            <dd className="mt-1 text-base font-semibold tabular-nums">{formatMoney(monthlyCents)}</dd>
            <dd className="text-xs text-muted-foreground">on {formatDate(subscription.renewsAt)}</dd>
          </div>
          <div className="flex items-start justify-between gap-3 p-4">
            <div>
              <dt className="text-xs font-medium text-muted-foreground">Payment method</dt>
              <dd className="mt-1 flex items-center gap-1.5 text-base font-semibold">
                <CreditCard className="size-4 text-muted-foreground" aria-hidden="true" />
                {subscription.paymentMethod.brand} ···· {subscription.paymentMethod.last4}
              </dd>
              <dd className="text-xs text-muted-foreground">
                Expires {String(subscription.paymentMethod.expMonth).padStart(2, "0")}/{subscription.paymentMethod.expYear}
              </dd>
            </div>
            <Button variant="outline" size="sm" className="shrink-0">
              Update
            </Button>
          </div>
        </dl>
        {openInvoice && (
          <div className="flex flex-wrap items-center justify-between gap-2 border-t bg-muted/40 px-4 py-2 text-sm">
            <p>
              Invoice <span className="font-mono text-xs">{openInvoice.id}</span> for {formatMoney(openInvoice.amountCents)} is{" "}
              {openInvoice.status === "past_due" ? <span className="font-medium text-destructive">past due</span> : "open"}.
            </p>
            <a
              href={openInvoice.pdfUrl}
              download
              className="-mx-2 inline-flex h-9 items-center rounded-md px-2 font-medium underline-offset-4 outline-none hover:underline focus-visible:ring-2 focus-visible:ring-ring"
            >
              Download invoice
            </a>
          </div>
        )}
      </section>

      <PlanComparison plans={plans} currentPlanId={subscription.planId} currentCycle={subscription.cycle} seatsInUse={seatsInUse} />

      <SeatTable seats={seats} seatsPurchased={subscription.seatsPurchased} />

      <InvoiceHistory invoices={invoices} />
    </div>
  );
}
