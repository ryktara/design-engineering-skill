import type { Metadata } from "next";
import { CreditCard, Download } from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PlanComparison } from "@/components/billing/plan-comparison";
import { SeatTable } from "@/components/billing/seat-table";
import { InvoiceHistory } from "@/components/billing/invoice-history";
import { formatDate, formatMoney, getInvoices, getSeats, getSubscription, plans } from "@/lib/billing";
import { cn } from "@/lib/utils";

export const metadata: Metadata = { title: "Billing · Settings · Acme Console" };

export default async function BillingSettingsPage() {
  const [subscription, seats, invoices] = await Promise.all([getSubscription(), getSeats(), getInvoices()]);
  const plan = plans.find((p) => p.id === subscription.planId)!;
  const seatsInUse = seats.filter((s) => s.status !== "deactivated").length;
  const monthlyCents = plan.pricePerSeat[subscription.cycle] * subscription.seatsPurchased * 100;
  const openInvoice = invoices.find((i) => i.status === "open" || i.status === "past_due");

  return (
    <div className="space-y-8">
      {/* Summary: same stat-card language as the dashboard (Card + CardDescription + CardTitle). */}
      <section aria-labelledby="summary-heading" className="space-y-4">
        <h2 id="summary-heading" className="sr-only">
          Current subscription
        </h2>
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Current plan</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd>{plan.name}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>Billed {subscription.cycle === "annual" ? "annually" : "monthly"}</dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Seats</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="tabular-nums">
                  {seatsInUse} <span className="font-normal text-muted-foreground">/ {subscription.seatsPurchased}</span>
                </dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>{subscription.seatsPurchased - seatsInUse} available</dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription asChild>
                <dt>Next charge</dt>
              </CardDescription>
              <CardTitle asChild>
                <dd className="tabular-nums">{formatMoney(monthlyCents)}</dd>
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>on {formatDate(subscription.renewsAt)}</dd>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex-row items-start justify-between space-y-0 pb-2">
              <div className="space-y-1.5">
                <CardDescription asChild>
                  <dt>Payment method</dt>
                </CardDescription>
                <CardTitle asChild>
                  <dd className="flex items-center gap-1.5">
                    <CreditCard className="size-4 text-muted-foreground" aria-hidden="true" />
                    {subscription.paymentMethod.brand} ···· {subscription.paymentMethod.last4}
                  </dd>
                </CardTitle>
              </div>
              <Button variant="outline" size="sm" className="shrink-0">
                Update
              </Button>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground">
              <dd>
                Expires {String(subscription.paymentMethod.expMonth).padStart(2, "0")}/{subscription.paymentMethod.expYear}
              </dd>
            </CardContent>
          </Card>
        </dl>
        {openInvoice && (
          <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border bg-muted/40 px-4 py-2 text-sm">
            <p>
              Invoice <span className="font-mono text-xs">{openInvoice.id}</span> for {formatMoney(openInvoice.amountCents)} is{" "}
              {openInvoice.status === "past_due" ? <span className="font-medium text-destructive">past due</span> : "open"}.
            </p>
            <a href={openInvoice.pdfUrl} download className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "-mx-2")}>
              <Download aria-hidden="true" />
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
