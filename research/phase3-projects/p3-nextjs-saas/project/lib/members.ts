import { getSeats, type Seat, type SeatRole, type SeatStatus } from "@/lib/billing";

// The team roster is the same list the billing page counts as seats; one source of truth, read-only here.
export type Member = Seat;
export type MemberRole = SeatRole;
export type MemberStatus = SeatStatus;

export const roleLabel: Record<MemberRole, string> = { owner: "Owner", admin: "Admin", member: "Member", viewer: "Viewer" };

// Roles that can be granted through an invite (owner is transferred, never invited).
export const invitableRoles: { value: Exclude<MemberRole, "owner">; label: string; description: string }[] = [
  { value: "admin", label: "Admin", description: "Manages members, billing and workspace settings." },
  { value: "member", label: "Member", description: "Creates and edits invoices and inventory." },
  { value: "viewer", label: "Viewer", description: "Read-only access to invoices and inventory." },
];

export const INVITE_EXPIRY_DAYS = 7;

export async function getMembers(): Promise<Member[]> {
  return getSeats();
}

// Same permissive shape browsers use for type=email, plus a dot in the domain so "name@localhost" is caught.
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export function validateInviteEmail(raw: string, existing: Pick<Member, "email" | "status">[]): string | null {
  const email = raw.trim();
  if (!email) return "Enter an email address.";
  if (!EMAIL.test(email)) return "Enter a valid email address, like name@company.com.";
  const hit = existing.find((m) => m.email.toLowerCase() === email.toLowerCase());
  if (hit?.status === "invited") return `${hit.email} already has a pending invite.`;
  if (hit) return `${hit.email} is already a member.`;
  return null;
}
