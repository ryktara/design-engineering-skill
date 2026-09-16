import type { Metadata } from "next";
import { MembersTable } from "@/components/members/members-table";
import { getSubscription } from "@/lib/billing";
import { getMembers } from "@/lib/members";

export const metadata: Metadata = { title: "Members · Settings · Acme Console" };

export default async function MembersSettingsPage() {
  const [members, subscription] = await Promise.all([getMembers(), getSubscription()]);
  return (
    <div className="space-y-8">
      <MembersTable members={members} seatsPurchased={subscription.seatsPurchased} />
    </div>
  );
}
