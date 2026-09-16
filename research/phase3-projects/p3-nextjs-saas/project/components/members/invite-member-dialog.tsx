"use client";

import * as React from "react";
import { UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { INVITE_EXPIRY_DAYS, invitableRoles, validateInviteEmail, type Member, type MemberRole } from "@/lib/members";

interface Props {
  members: Pick<Member, "email" | "status">[];
  seatsAvailable: number;
  onInvite: (email: string, role: Exclude<MemberRole, "owner">) => void;
}

// Single-step invite in the same Dialog primitive the billing page uses for confirmations.
// Radix moves focus to the first field on open and back to the trigger on close; validation is inline,
// linked with aria-describedby / aria-invalid, and the field is refocused when submit fails.
export function InviteMemberDialog({ members, seatsAvailable, onInvite }: Props) {
  const [open, setOpen] = React.useState(false);
  const [email, setEmail] = React.useState("");
  const [role, setRole] = React.useState<Exclude<MemberRole, "owner">>("member");
  const [error, setError] = React.useState<string | null>(null);
  const emailRef = React.useRef<HTMLInputElement | null>(null);
  const noSeats = seatsAvailable <= 0;
  const roleInfo = invitableRoles.find((r) => r.value === role)!;

  function reset() {
    setEmail("");
    setRole("member");
    setError(null);
  }

  function onOpenChange(next: boolean) {
    setOpen(next);
    if (!next) reset();
  }

  function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const problem = validateInviteEmail(email, members);
    if (problem) {
      setError(problem);
      // Defer past the tap/click event sequence: on touch, Chromium focuses the submit button after
      // the click handler runs, which would otherwise steal focus back from the field.
      requestAnimationFrame(() => emailRef.current?.focus());
      return;
    }
    onInvite(email.trim(), role);
    onOpenChange(false);
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogTrigger asChild>
        <Button size="sm">
          <UserPlus aria-hidden="true" />
          Invite member
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={submit} noValidate className="grid gap-4">
          <DialogHeader>
            <DialogTitle>Invite a member</DialogTitle>
            <DialogDescription>
              They get an email with a link that works for {INVITE_EXPIRY_DAYS} days.{" "}
              {noSeats ? (
                <span className="text-warning">All purchased seats are in use; add seats on the Billing page first.</span>
              ) : (
                <>
                  <span className="tabular-nums">{seatsAvailable}</span> {seatsAvailable === 1 ? "seat is" : "seats are"} available.
                </>
              )}
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-2">
            <Label htmlFor="invite-email">
              Email address <span className="font-normal text-muted-foreground">(required)</span>
            </Label>
            <Input
              ref={emailRef}
              id="invite-email"
              name="email"
              type="email"
              inputMode="email"
              autoComplete="email"
              autoCapitalize="none"
              spellCheck={false}
              placeholder="name@company.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (error) setError(null);
              }}
              onBlur={() => {
                // Validate on blur only once something was typed; an untouched field is not an error yet.
                if (email.trim()) setError(validateInviteEmail(email, members));
              }}
              aria-required="true"
              aria-invalid={error ? "true" : undefined}
              aria-describedby={error ? "invite-email-error" : undefined}
            />
            {/* Reserved slot: the message must not push the footer down, or a tap on "Send invite" that blurs
                the field lands on the moved layout instead of the button (no submit on touch). */}
            <div className="min-h-5">
              {error && (
                <p id="invite-email-error" role="alert" className="text-sm leading-5 text-destructive">
                  {error}
                </p>
              )}
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="invite-role">Role</Label>
            <select
              id="invite-role"
              name="role"
              value={role}
              onChange={(e) => setRole(e.target.value as Exclude<MemberRole, "owner">)}
              aria-describedby="invite-role-help"
              className="flex h-11 w-full rounded-md border border-input bg-background px-3 text-sm shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-ring md:h-9"
            >
              {invitableRoles.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
            <p id="invite-role-help" className="text-xs text-muted-foreground">
              {roleInfo.description} You can change it later.
            </p>
          </div>

          <DialogFooter>
            <DialogClose asChild>
              <Button type="button" variant="outline">
                Cancel
              </Button>
            </DialogClose>
            <Button type="submit" disabled={noSeats}>
              Send invite
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
