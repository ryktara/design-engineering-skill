"use client";

import * as React from "react";
import { CircleCheck, CircleMinus, Clock, Mail, RotateCcw, UserMinus, X, type LucideIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StatusBadge, type StatusTone } from "@/components/billing/status-badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { InviteMemberDialog } from "@/components/members/invite-member-dialog";
import { cn } from "@/lib/utils";
import { formatDate } from "@/lib/billing";
import { INVITE_EXPIRY_DAYS, roleLabel, type Member, type MemberRole } from "@/lib/members";

interface Props {
  members: Member[];
  seatsPurchased: number;
}

// Same status vocabulary (label + tone + distinct icon shape) as the billing seat table, so a member
// reads the same on both pages and colour is never the only cue.
const memberStatus: Record<Member["status"], { label: string; tone: StatusTone; icon: LucideIcon }> = {
  active: { label: "Active", tone: "success", icon: CircleCheck },
  invited: { label: "Invited", tone: "warning", icon: Clock },
  deactivated: { label: "Deactivated", tone: "neutral", icon: CircleMinus },
};

export function MembersTable({ members: initial, seatsPurchased }: Props) {
  const [members, setMembers] = React.useState(initial);
  const [status, setStatus] = React.useState("");
  const [pendingRemove, setPendingRemove] = React.useState<Member | null>(null);
  const removeTriggerRef = React.useRef<HTMLButtonElement | null>(null);
  const headingRef = React.useRef<HTMLHeadingElement | null>(null);

  const inUse = members.filter((m) => m.status !== "deactivated").length;
  const pending = members.filter((m) => m.status === "invited").length;
  const seatsAvailable = Math.max(0, seatsPurchased - inUse);

  function invite(email: string, role: Exclude<MemberRole, "owner">) {
    const id = `inv_${Date.now().toString(36)}`;
    // Pending invites sit at the top so the person who just sent one sees it land.
    setMembers((prev) => [{ id, name: null, email, role, status: "invited", lastActiveAt: null }, ...prev]);
    setStatus(`Invite sent to ${email} as ${roleLabel[role]}. It expires in ${INVITE_EXPIRY_DAYS} days.`);
  }

  function resend(m: Member) {
    setStatus(`Invite resent to ${m.email}.`);
  }

  function revoke(m: Member) {
    setMembers((prev) => prev.filter((x) => x.id !== m.id));
    setStatus(`Invite to ${m.email} was revoked. The seat is available again.`);
    headingRef.current?.focus();
  }

  function changeRole(m: Member, role: MemberRole) {
    setMembers((prev) => prev.map((x) => (x.id === m.id ? { ...x, role } : x)));
    setStatus(`${m.name ?? m.email} is now ${roleLabel[role]}.`);
  }

  function confirmRemove() {
    if (!pendingRemove) return;
    const m = pendingRemove;
    setMembers((prev) => prev.map((x) => (x.id === m.id ? { ...x, status: "deactivated" } : x)));
    setStatus(`${m.name ?? m.email} was removed. Their seat is available again.`);
    setPendingRemove(null);
  }

  function reactivate(m: Member) {
    setMembers((prev) => prev.map((x) => (x.id === m.id ? { ...x, status: "active" } : x)));
    setStatus(`${m.name ?? m.email} was reactivated.`);
  }

  return (
    <section aria-labelledby="members-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="members-heading" ref={headingRef} tabIndex={-1} className="text-lg font-semibold tracking-tight outline-none">
            Members
          </h2>
          <p className="text-sm text-muted-foreground">
            <span className="font-medium tabular-nums text-foreground">{inUse}</span> of <span className="tabular-nums">{seatsPurchased}</span>{" "}
            seats in use{pending > 0 && <>, {pending} pending {pending === 1 ? "invite" : "invites"}</>}. Invited people hold a seat until they
            accept or the invite expires.
          </p>
        </div>
        <InviteMemberDialog members={members} seatsAvailable={seatsAvailable} onInvite={invite} />
      </div>

      <div className="rounded-lg border">
        <Table aria-labelledby="members-heading">
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead scope="col">Member</TableHead>
              <TableHead scope="col" className="hidden md:table-cell">
                Role
              </TableHead>
              <TableHead scope="col" className="hidden sm:table-cell">
                Status
              </TableHead>
              <TableHead scope="col" className="hidden lg:table-cell">
                Last active
              </TableHead>
              <TableHead scope="col" className="text-right">
                <span className="sr-only sm:not-sr-only">Actions</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {members.map((m) => {
              const label = m.name ?? m.email;
              const st = memberStatus[m.status];
              const removable = m.role !== "owner" && m.status === "active";
              const roleControl =
                m.role === "owner" || m.status === "deactivated" ? (
                  <span>{roleLabel[m.role]}</span>
                ) : (
                  <select
                    aria-label={`Role for ${label}`}
                    value={m.role}
                    onChange={(e) => changeRole(m, e.target.value as MemberRole)}
                    className="h-11 rounded-md border border-input bg-background px-2 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring md:h-8"
                  >
                    <option value="admin">Admin</option>
                    <option value="member">Member</option>
                    <option value="viewer">Viewer</option>
                  </select>
                );
              return (
                <TableRow key={m.id} className={cn(m.status === "deactivated" && "text-muted-foreground")}>
                  <TableCell>
                    <div className="flex min-w-0 flex-col">
                      <span className="truncate font-medium text-foreground">
                        {m.name ?? <span className="italic text-muted-foreground">Pending invite</span>}
                      </span>
                      <span className="truncate text-xs text-muted-foreground">{m.email}</span>
                      <div className="mt-2 flex items-center gap-2 text-xs md:hidden">
                        {roleControl}
                        <span className="sm:hidden">
                          <StatusBadge tone={st.tone} icon={st.icon}>
                            {st.label}
                          </StatusBadge>
                        </span>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">{roleControl}</TableCell>
                  <TableCell className="hidden sm:table-cell">
                    <StatusBadge tone={st.tone} icon={st.icon}>
                      {st.label}
                    </StatusBadge>
                  </TableCell>
                  <TableCell className="hidden tabular-nums lg:table-cell">
                    {m.lastActiveAt ? formatDate(m.lastActiveAt) : <span className="text-muted-foreground">—</span>}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1 [&>button]:max-sm:size-11 [&>button]:max-sm:px-0">
                      {m.status === "invited" && (
                        <>
                          <Button variant="ghost" size="sm" onClick={() => resend(m)} aria-label={`Resend invite to ${m.email}`}>
                            <Mail aria-hidden="true" />
                            <span className="hidden sm:inline">Resend</span>
                          </Button>
                          <Button variant="ghost" size="sm" onClick={() => revoke(m)} aria-label={`Revoke invite to ${m.email}`}>
                            <X aria-hidden="true" />
                            <span className="hidden sm:inline">Revoke</span>
                          </Button>
                        </>
                      )}
                      {m.status === "deactivated" && (
                        <Button variant="ghost" size="sm" onClick={() => reactivate(m)} aria-label={`Reactivate ${label}`}>
                          <RotateCcw aria-hidden="true" />
                          <span className="hidden sm:inline">Reactivate</span>
                        </Button>
                      )}
                      {removable && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-destructive hover:text-destructive"
                          onClick={(e) => {
                            removeTriggerRef.current = e.currentTarget;
                            setPendingRemove(m);
                          }}
                          aria-label={`Remove ${label}`}
                        >
                          <UserMinus aria-hidden="true" />
                          <span className="hidden sm:inline">Remove</span>
                        </Button>
                      )}
                      {m.role === "owner" && <span className="px-2 text-xs text-muted-foreground">Owner</span>}
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      <p role="status" aria-live="polite" className="sr-only">
        {status}
      </p>

      <Dialog open={pendingRemove !== null} onOpenChange={(o) => !o && setPendingRemove(null)}>
        <DialogContent
          role="alertdialog"
          onCloseAutoFocus={(e) => {
            // Return focus to the row action that opened it; if that button is gone, land on the heading.
            e.preventDefault();
            const t = removeTriggerRef.current;
            if (t && document.contains(t)) t.focus();
            else headingRef.current?.focus();
          }}
        >
          <DialogHeader>
            <DialogTitle>Remove {pendingRemove?.name ?? pendingRemove?.email}?</DialogTitle>
            <DialogDescription>
              They lose access immediately and their seat becomes available. You can reactivate them later from this list.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button variant="destructive" onClick={confirmRemove}>
              Remove member
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </section>
  );
}
