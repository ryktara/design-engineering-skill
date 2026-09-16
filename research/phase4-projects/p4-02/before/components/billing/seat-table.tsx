"use client";

import * as React from "react";
import { UserMinus, UserPlus, RotateCcw, Mail } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StatusBadge, type StatusTone } from "@/components/billing/status-badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import { formatDate, type Seat, type SeatRole } from "@/lib/billing";

interface Props {
  seats: Seat[];
  seatsPurchased: number;
}

const roleLabel: Record<SeatRole, string> = { owner: "Owner", admin: "Admin", member: "Member", viewer: "Viewer" };

export function SeatTable({ seats: initial, seatsPurchased }: Props) {
  const [seats, setSeats] = React.useState(initial);
  const [pendingRemove, setPendingRemove] = React.useState<Seat | null>(null);
  const [status, setStatus] = React.useState<string>("");
  const removeTriggerRef = React.useRef<HTMLButtonElement | null>(null);

  const inUse = seats.filter((s) => s.status !== "deactivated").length;
  const pct = Math.min(100, Math.round((inUse / seatsPurchased) * 100));

  function changeRole(id: string, role: SeatRole) {
    setSeats((prev) => prev.map((s) => (s.id === id ? { ...s, role } : s)));
    const seat = seats.find((s) => s.id === id);
    setStatus(`${seat?.name ?? seat?.email} is now ${roleLabel[role]}.`);
  }

  function confirmRemove() {
    if (!pendingRemove) return;
    setSeats((prev) => prev.map((s) => (s.id === pendingRemove.id ? { ...s, status: "deactivated" } : s)));
    setStatus(`${pendingRemove.name ?? pendingRemove.email} was removed. Their seat is now free.`);
    setPendingRemove(null);
  }

  function reactivate(seat: Seat) {
    setSeats((prev) => prev.map((s) => (s.id === seat.id ? { ...s, status: "active" } : s)));
    setStatus(`${seat.name ?? seat.email} was reactivated.`);
  }

  return (
    <section aria-labelledby="seats-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="seats-heading" tabIndex={-1} className="text-lg font-semibold tracking-tight outline-none">
            Seats
          </h2>
          <p className="text-sm text-muted-foreground">
            <span className="font-medium tabular-nums text-foreground">{inUse}</span> of{" "}
            <span className="tabular-nums">{seatsPurchased}</span> purchased seats in use. Invited users hold a seat until they decline.
          </p>
        </div>
        <Button size="sm">
          <UserPlus aria-hidden="true" />
          Invite member
        </Button>
      </div>

      <div className="flex items-center gap-3 text-xs text-muted-foreground">
        <div
          role="meter"
          aria-label="Seat usage"
          aria-valuemin={0}
          aria-valuemax={seatsPurchased}
          aria-valuenow={inUse}
          aria-valuetext={`${inUse} of ${seatsPurchased} seats`}
          className="h-1.5 w-40 overflow-hidden rounded-full bg-muted"
        >
          <div className={cn("h-full rounded-full", pct >= 90 ? "bg-warning" : "bg-primary")} style={{ width: `${pct}%` }} />
        </div>
        <span className="tabular-nums">{pct}% used</span>
      </div>

      <div className="rounded-lg border">
        <Table>
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
                Actions
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {seats.map((seat) => {
              const removable = seat.role !== "owner" && seat.status !== "deactivated";
              const label = seat.name ?? seat.email;
              const roleControl =
                seat.role === "owner" || seat.status === "deactivated" ? (
                  <span>{roleLabel[seat.role]}</span>
                ) : (
                  <select
                    aria-label={`Role for ${label}`}
                    value={seat.role}
                    onChange={(e) => changeRole(seat.id, e.target.value as SeatRole)}
                    className="h-11 rounded-md border border-input bg-background px-2 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring md:h-8"
                  >
                    <option value="admin">Admin</option>
                    <option value="member">Member</option>
                    <option value="viewer">Viewer</option>
                  </select>
                );
              return (
                <TableRow key={seat.id} className={cn(seat.status === "deactivated" && "text-muted-foreground")}>
                  <TableCell>
                    <div className="flex min-w-0 flex-col">
                      <span className="truncate font-medium text-foreground">{seat.name ?? <span className="italic text-muted-foreground">Pending invite</span>}</span>
                      <span className="truncate text-xs text-muted-foreground">{seat.email}</span>
                      <div className="mt-2 flex items-center gap-2 text-xs md:hidden">
                        {roleControl}
                        <span className="sm:hidden">
                          <StatusText status={seat.status} />
                        </span>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">{roleControl}</TableCell>
                  <TableCell className="hidden sm:table-cell">
                    <SeatStatusBadge status={seat.status} />
                  </TableCell>
                  <TableCell className="hidden tabular-nums lg:table-cell">
                    {seat.lastActiveAt ? formatDate(seat.lastActiveAt) : <span className="text-muted-foreground">—</span>}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1 [&>button]:max-sm:size-11 [&>button]:max-sm:px-0">
                      {seat.status === "invited" && (
                        <Button variant="ghost" size="sm" aria-label={`Resend invite to ${seat.email}`}>
                          <Mail aria-hidden="true" />
                          <span className="hidden sm:inline">Resend</span>
                        </Button>
                      )}
                      {seat.status === "deactivated" && (
                        <Button variant="ghost" size="sm" onClick={() => reactivate(seat)} aria-label={`Reactivate ${label}`}>
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
                            setPendingRemove(seat);
                          }}
                          aria-label={`Remove ${label}`}
                        >
                          <UserMinus aria-hidden="true" />
                          <span className="hidden sm:inline">Remove</span>
                        </Button>
                      )}
                      {seat.role === "owner" && <span className="px-2 text-xs text-muted-foreground">Owner</span>}
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
            // Return focus to the row action that opened the dialog (Radix only does this for DialogTrigger).
            e.preventDefault();
            const t = removeTriggerRef.current;
            if (t && document.contains(t)) t.focus();
            else document.getElementById("seats-heading")?.focus();
          }}
        >
          <DialogHeader>
            <DialogTitle>Remove {pendingRemove?.name ?? pendingRemove?.email}?</DialogTitle>
            <DialogDescription>
              They lose access immediately. Their seat becomes available and is not billed at the next renewal. You can reactivate them later.
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

function StatusText({ status }: { status: Seat["status"] }) {
  return <span>{seatStatus[status].label}</span>;
}

const seatStatus: Record<Seat["status"], { label: string; tone: StatusTone }> = {
  active: { label: "Active", tone: "success" },
  invited: { label: "Invited", tone: "warning" },
  deactivated: { label: "Deactivated", tone: "neutral" },
};

function SeatStatusBadge({ status }: { status: Seat["status"] }) {
  return <StatusBadge tone={seatStatus[status].tone}>{seatStatus[status].label}</StatusBadge>;
}
