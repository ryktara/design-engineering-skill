export type PlanId = "starter" | "team" | "business";
export type BillingCycle = "monthly" | "annual";

export interface Plan {
  id: PlanId;
  name: string;
  description: string;
  pricePerSeat: { monthly: number; annual: number }; // USD per seat per month
  seatLimit: number | null; // null = unlimited
  features: string[];
}

export type SeatRole = "owner" | "admin" | "member" | "viewer";
export type SeatStatus = "active" | "invited" | "deactivated";

export interface Seat {
  id: string;
  name: string | null;
  email: string;
  role: SeatRole;
  status: SeatStatus;
  lastActiveAt: string | null; // ISO date
}

export type InvoiceStatus = "paid" | "open" | "past_due" | "void";

export interface Invoice {
  id: string; // e.g. INV-2026-0042
  issuedAt: string; // ISO date
  periodLabel: string;
  amountCents: number;
  currency: "USD";
  status: InvoiceStatus;
  pdfUrl: string;
}

export interface Subscription {
  planId: PlanId;
  cycle: BillingCycle;
  seatsPurchased: number;
  renewsAt: string;
  paymentMethod: { brand: string; last4: string; expMonth: number; expYear: number };
}

export const plans: Plan[] = [
  {
    id: "starter",
    name: "Starter",
    description: "For small teams getting invoices out the door.",
    pricePerSeat: { monthly: 12, annual: 10 },
    seatLimit: 5,
    features: ["Up to 5 seats", "Invoices and inventory", "Email support", "30-day audit log"],
  },
  {
    id: "team",
    name: "Team",
    description: "Roles, approvals and integrations for growing teams.",
    pricePerSeat: { monthly: 24, annual: 20 },
    seatLimit: 25,
    features: ["Up to 25 seats", "Roles and approval flows", "Accounting integrations", "1-year audit log", "Priority support"],
  },
  {
    id: "business",
    name: "Business",
    description: "SSO, unlimited seats and dedicated support.",
    pricePerSeat: { monthly: 42, annual: 36 },
    seatLimit: null,
    features: ["Unlimited seats", "SAML SSO and SCIM", "Custom data retention", "Dedicated success manager", "99.9% uptime SLA"],
  },
];

const subscription: Subscription = {
  planId: "team",
  cycle: "annual",
  seatsPurchased: 10,
  renewsAt: "2027-03-01",
  paymentMethod: { brand: "Visa", last4: "4242", expMonth: 8, expYear: 2028 },
};

const seats: Seat[] = [
  { id: "u_01", name: "Priya Natarajan", email: "priya@acme.example", role: "owner", status: "active", lastActiveAt: "2026-09-09T08:12:00Z" },
  { id: "u_02", name: "Marcus Ellery", email: "marcus@acme.example", role: "admin", status: "active", lastActiveAt: "2026-09-08T17:40:00Z" },
  { id: "u_03", name: "Sofía Reyes", email: "sofia@acme.example", role: "member", status: "active", lastActiveAt: "2026-09-09T06:02:00Z" },
  { id: "u_04", name: "Tomasz Wierzbicki", email: "tomasz@acme.example", role: "member", status: "active", lastActiveAt: "2026-09-05T11:25:00Z" },
  { id: "u_05", name: "Amara Okafor", email: "amara@acme.example", role: "member", status: "active", lastActiveAt: "2026-08-29T14:00:00Z" },
  { id: "u_06", name: "Jun Sato", email: "jun@acme.example", role: "viewer", status: "active", lastActiveAt: "2026-09-01T09:15:00Z" },
  { id: "u_07", name: null, email: "finance-contractor@partner.example", role: "viewer", status: "invited", lastActiveAt: null },
  { id: "u_08", name: "Lena Hoffmann", email: "lena@acme.example", role: "member", status: "deactivated", lastActiveAt: "2026-06-12T10:30:00Z" },
];

const invoices: Invoice[] = [
  { id: "INV-2026-0042", issuedAt: "2026-09-01", periodLabel: "Sep 2026", amountCents: 20000, currency: "USD", status: "open", pdfUrl: "/invoices/INV-2026-0042.pdf" },
  { id: "INV-2026-0037", issuedAt: "2026-08-01", periodLabel: "Aug 2026", amountCents: 20000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0037.pdf" },
  { id: "INV-2026-0031", issuedAt: "2026-07-01", periodLabel: "Jul 2026", amountCents: 18000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0031.pdf" },
  { id: "INV-2026-0026", issuedAt: "2026-06-01", periodLabel: "Jun 2026", amountCents: 18000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0026.pdf" },
  { id: "INV-2026-0019", issuedAt: "2026-05-01", periodLabel: "May 2026", amountCents: 16000, currency: "USD", status: "past_due", pdfUrl: "/invoices/INV-2026-0019.pdf" },
  { id: "INV-2026-0012", issuedAt: "2026-04-01", periodLabel: "Apr 2026", amountCents: 16000, currency: "USD", status: "void", pdfUrl: "/invoices/INV-2026-0012.pdf" },
];

// Simulated data access; in the real app these hit the billing provider.
export async function getSubscription(): Promise<Subscription> {
  return subscription;
}
export async function getSeats(): Promise<Seat[]> {
  return seats;
}
export async function getInvoices(): Promise<Invoice[]> {
  return invoices;
}

export function formatMoney(cents: number, currency: string = "USD", locale: string = "en-US") {
  return new Intl.NumberFormat(locale, { style: "currency", currency, minimumFractionDigits: 2 }).format(cents / 100);
}

export function formatDate(iso: string, locale: string = "en-US") {
  return new Intl.DateTimeFormat(locale, { year: "numeric", month: "short", day: "numeric" }).format(new Date(iso));
}
