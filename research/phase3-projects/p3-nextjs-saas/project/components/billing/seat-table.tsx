"use client";

import * as React from "react";
import { UserMinus, UserPlus, RotateCcw, Mail, CircleCheck, Clock, CircleMinus, type LucideIcon } from "lucide-react";
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

const seatStatus: Record<Seat["status"], { label: string; tone: StatusTone; icon: LucideIcon }> = {
  active: { label: "Active", tone: "success", icon: CircleCheck },
  invited: { label: "Invited", tone: "warning", icon: Clock },
  deactivated: { label: "Deactivated", tone: "neutral", icon: CircleMinus },
};

// Interactive controls inside a row that are rendered (not display:none at this breakpoint) and enabled.
function rowControls(row: HTMLElement): HTMLElement[] {
  return [...row.querySelectorAll<HTMLElement>("button, select, a[href]")].filter(
    (el) => !el.hasAttribute("disabled") && el.getAttribute("aria-hidden") !== "true" && el.offsetParent !== null
  );
}

export function SeatTable({ seats: initial, seatsPurchased }: Props) {
  const [seats, setSeats] = React.useState(initial);
  const [pendingRemove, setPendingRemove] = React.useState<Seat | null>(null);
  const [status, setStatus] = React.useState<string>("");
  // Roving tabindex: exactly one row is in the Tab sequence; arrows move between rows and into row actions.
  const [activeId, setActiveId] = React.useState<string>(initial[0]?.id ?? "");
  const bodyRef = React.useRef<HTMLTableSectionElement | null>(null);
  const removeTriggerRef = React.useRef<HTMLButtonElement | null>(null);
  const removeRowIdRef = React.useRef<string | null>(null);

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

  function rows(): HTMLTableRowElement[] {
    return bodyRef.current ? [...bodyRef.current.querySelectorAll<HTMLTableRowElement>("tr[data-seat-id]")] : [];
  }

  function focusRow(row: HTMLTableRowElement | undefined) {
    if (!row) return;
    setActiveId(row.dataset.seatId!);
    row.focus();
  }

  function onGridKeyDown(e: React.KeyboardEvent<HTMLTableSectionElement>) {
    const target = e.target as HTMLElement;
    const row = target.closest<HTMLTableRowElement>("tr[data-seat-id]");
    if (!row) return;
    const all = rows();
    const i = all.indexOf(row);
    const onSelect = target.tagName === "SELECT";
    const controls = rowControls(row);
    const j = controls.indexOf(target);

    switch (e.key) {
      case "ArrowDown":
        if (onSelect) return; // native select uses Up/Down to change its value
        focusRow(all[Math.min(i + 1, all.length - 1)]);
        break;
      case "ArrowUp":
        if (onSelect) return;
        focusRow(all[Math.max(i - 1, 0)]);
        break;
      case "Home":
        if (onSelect) return;
        focusRow(all[0]);
        break;
      case "End":
        if (onSelect) return;
        focusRow(all[all.length - 1]);
        break;
      case "ArrowRight":
        if (controls.length === 0) return;
        (j < 0 ? controls[0] : controls[Math.min(j + 1, controls.length - 1)]).focus();
        break;
      case "ArrowLeft":
        if (j <= 0) row.focus();
        else controls[j - 1].focus();
        break;
      case "Escape":
        if (j >= 0) row.focus();
        else return;
        break;
      default:
        return;
    }
    e.preventDefault();
  }

  // Keep the Tab re-entry point on the row the user last worked in (also after a pointer click).
  function onGridFocus(e: React.FocusEvent<HTMLTableSectionElement>) {
    const row = (e.target as HTMLElement).closest<HTMLTableRowElement>("tr[data-seat-id]");
    if (row && row.dataset.seatId !== activeId) setActiveId(row.dataset.seatId!);
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

      <p id="seats-grid-keys" className="sr-only">
        Members grid. Use Up and Down arrows to move between members, Right and Left arrows to reach a member&apos;s role and actions, Escape to
        return to the member row, Tab to leave the grid.
      </p>

      <div className="rounded-lg border">
        <Table role="grid" aria-labelledby="seats-heading" aria-describedby="seats-grid-keys" aria-rowcount={seats.length + 1}>
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
          <TableBody ref={bodyRef} onKeyDown={onGridKeyDown} onFocus={onGridFocus}>
            {seats.map((seat, index) => {
              const removable = seat.role !== "owner" && seat.status !== "deactivated";
              const label = seat.name ?? seat.email;
              const st = seatStatus[seat.status];
              const roleControl =
                seat.role === "owner" || seat.status === "deactivated" ? (
                  <span>{roleLabel[seat.role]}</span>
                ) : (
                  <select
                    tabIndex={-1}
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
                <TableRow
                  key={seat.id}
                  id={`seat-row-${seat.id}`}
                  data-seat-id={seat.id}
                  aria-rowindex={index + 2}
                  aria-label={`${label}, ${roleLabel[seat.role]}, ${st.label}`}
                  tabIndex={seat.id === activeId ? 0 : -1}
                  className={cn(
                    "outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring focus-within:bg-muted/50",
                    seat.status === "deactivated" && "text-muted-foreground"
                  )}
                >
                  <TableCell role="gridcell">
                    <div className="flex min-w-0 flex-col">
                      <span className="truncate font-medium text-foreground">{seat.name ?? <span className="italic text-muted-foreground">Pending invite</span>}</span>
                      <span className="truncate text-xs text-muted-foreground">{seat.email}</span>
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
                  <TableCell role="gridcell" className="hidden md:table-cell">
                    {roleControl}
                  </TableCell>
                  <TableCell role="gridcell" className="hidden sm:table-cell">
                    <StatusBadge tone={st.tone} icon={st.icon}>
                      {st.label}
                    </StatusBadge>
                  </TableCell>
                  <TableCell role="gridcell" className="hidden tabular-nums lg:table-cell">
                    {seat.lastActiveAt ? formatDate(seat.lastActiveAt) : <span className="text-muted-foreground">—</span>}
                  </TableCell>
                  <TableCell role="gridcell" className="text-right">
                    <div className="flex justify-end gap-1 [&>button]:max-sm:size-11 [&>button]:max-sm:px-0">
                      {seat.status === "invited" && (
                        <Button
                          tabIndex={-1}
                          variant="ghost"
                          size="sm"
                          onClick={() => setStatus(`Invite resent to ${seat.email}.`)}
                          aria-label={`Resend invite to ${seat.email}`}
                        >
                          <Mail aria-hidden="true" />
                          <span className="hidden sm:inline">Resend</span>
                        </Button>
                      )}
                      {seat.status === "deactivated" && (
                        <Button tabIndex={-1} variant="ghost" size="sm" onClick={() => reactivate(seat)} aria-label={`Reactivate ${label}`}>
                          <RotateCcw aria-hidden="true" />
                          <span className="hidden sm:inline">Reactivate</span>
                        </Button>
                      )}
                      {removable && (
                        <Button
                          tabIndex={-1}
                          variant="ghost"
                          size="sm"
                          className="text-destructive hover:text-destructive"
                          onClick={(e) => {
                            removeTriggerRef.current = e.currentTarget;
                            removeRowIdRef.current = seat.id;
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
            // Return focus to the row action that opened the dialog (Radix only does this for DialogTrigger);
            // if the action is gone because the member was removed, land on that member's row, then the heading.
            e.preventDefault();
            const t = removeTriggerRef.current;
            const row = removeRowIdRef.current ? document.getElementById(`seat-row-${removeRowIdRef.current}`) : null;
            if (t && document.contains(t)) t.focus();
            else if (row) row.focus();
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
