import type { Metadata } from "next";
import { ApiKeysTable } from "@/components/api-keys/api-keys-table";
import { getApiKeys } from "@/lib/api-keys";

export const metadata: Metadata = { title: "API keys · Settings · Acme Console" };

export default async function ApiKeysSettingsPage() {
  const apiKeys = await getApiKeys();
  return (
    <div className="space-y-8">
      <ApiKeysTable apiKeys={apiKeys} />
    </div>
  );
}
