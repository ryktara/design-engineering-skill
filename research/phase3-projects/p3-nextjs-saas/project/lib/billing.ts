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
  // Fixture: 30 monthly invoices (Apr 2024 – Sep 2026), newest first; the billing page must scan well past 20 rows.
  { id: "INV-2026-0127", issuedAt: "2026-09-01", periodLabel: "Sep 2026", amountCents: 20000, currency: "USD", status: "open", pdfUrl: "/invoices/INV-2026-0127.pdf" },
  { id: "INV-2026-0122", issuedAt: "2026-08-01", periodLabel: "Aug 2026", amountCents: 20000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0122.pdf" },
  { id: "INV-2026-0117", issuedAt: "2026-07-01", periodLabel: "Jul 2026", amountCents: 20000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0117.pdf" },
  { id: "INV-2026-0112", issuedAt: "2026-06-01", periodLabel: "Jun 2026", amountCents: 18000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0112.pdf" },
  { id: "INV-2026-0107", issuedAt: "2026-05-01", periodLabel: "May 2026", amountCents: 18000, currency: "USD", status: "past_due", pdfUrl: "/invoices/INV-2026-0107.pdf" },
  { id: "INV-2026-0102", issuedAt: "2026-04-01", periodLabel: "Apr 2026", amountCents: 18000, currency: "USD", status: "void", pdfUrl: "/invoices/INV-2026-0102.pdf" },
  { id: "INV-2026-0097", issuedAt: "2026-03-01", periodLabel: "Mar 2026", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0097.pdf" },
  { id: "INV-2026-0092", issuedAt: "2026-02-01", periodLabel: "Feb 2026", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0092.pdf" },
  { id: "INV-2026-0087", issuedAt: "2026-01-01", periodLabel: "Jan 2026", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2026-0087.pdf" },
  { id: "INV-2025-0083", issuedAt: "2025-12-01", periodLabel: "Dec 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0083.pdf" },
  { id: "INV-2025-0079", issuedAt: "2025-11-01", periodLabel: "Nov 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0079.pdf" },
  { id: "INV-2025-0075", issuedAt: "2025-10-01", periodLabel: "Oct 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0075.pdf" },
  { id: "INV-2025-0071", issuedAt: "2025-09-01", periodLabel: "Sep 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0071.pdf" },
  { id: "INV-2025-0067", issuedAt: "2025-08-01", periodLabel: "Aug 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0067.pdf" },
  { id: "INV-2025-0063", issuedAt: "2025-07-01", periodLabel: "Jul 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0063.pdf" },
  { id: "INV-2025-0059", issuedAt: "2025-06-01", periodLabel: "Jun 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0059.pdf" },
  { id: "INV-2025-0055", issuedAt: "2025-05-01", periodLabel: "May 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0055.pdf" },
  { id: "INV-2025-0051", issuedAt: "2025-04-01", periodLabel: "Apr 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0051.pdf" },
  { id: "INV-2025-0047", issuedAt: "2025-03-01", periodLabel: "Mar 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0047.pdf" },
  { id: "INV-2025-0043", issuedAt: "2025-02-01", periodLabel: "Feb 2025", amountCents: 16000, currency: "USD", status: "void", pdfUrl: "/invoices/INV-2025-0043.pdf" },
  { id: "INV-2025-0039", issuedAt: "2025-01-01", periodLabel: "Jan 2025", amountCents: 16000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2025-0039.pdf" },
  { id: "INV-2024-0035", issuedAt: "2024-12-01", periodLabel: "Dec 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0035.pdf" },
  { id: "INV-2024-0031", issuedAt: "2024-11-01", periodLabel: "Nov 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0031.pdf" },
  { id: "INV-2024-0027", issuedAt: "2024-10-01", periodLabel: "Oct 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0027.pdf" },
  { id: "INV-2024-0023", issuedAt: "2024-09-01", periodLabel: "Sep 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0023.pdf" },
  { id: "INV-2024-0019", issuedAt: "2024-08-01", periodLabel: "Aug 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0019.pdf" },
  { id: "INV-2024-0015", issuedAt: "2024-07-01", periodLabel: "Jul 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0015.pdf" },
  { id: "INV-2024-0011", issuedAt: "2024-06-01", periodLabel: "Jun 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0011.pdf" },
  { id: "INV-2024-0007", issuedAt: "2024-05-01", periodLabel: "May 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0007.pdf" },
  { id: "INV-2024-0003", issuedAt: "2024-04-01", periodLabel: "Apr 2024", amountCents: 10000, currency: "USD", status: "paid", pdfUrl: "/invoices/INV-2024-0003.pdf" },
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
