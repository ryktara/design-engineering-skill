export type ApiKeyStatus = "active" | "revoked";

export interface ApiKey {
  id: string;
  name: string;
  prefix: string; // shown always, e.g. "sk_live_a91f"
  last4: string; // shown always
  secret: string; // full value; masked in the UI until explicitly revealed
  scope: "read" | "read_write";
  createdAt: string; // ISO date
  lastUsedAt: string | null; // ISO date
  status: ApiKeyStatus;
}

export const scopeLabel: Record<ApiKey["scope"], string> = {
  read: "Read",
  read_write: "Read and write",
};

const keys: ApiKey[] = [
  {
    id: "key_01",
    name: "Production server",
    prefix: "nb_demo_a91f",
    last4: "7d2c",
    secret: "nb_demo_a91f0c4e8b1d4a7f9e2c6b3d5a8f7d2c",
    scope: "read_write",
    createdAt: "2026-01-14",
    lastUsedAt: "2026-03-02",
    status: "active",
  },
  {
    id: "key_02",
    name: "Reporting export",
    prefix: "nb_demo_4c77",
    last4: "b019",
    secret: "nb_demo_4c77e2a1d9f04b6c8a35e7d21c94b019",
    scope: "read",
    createdAt: "2025-11-03",
    lastUsedAt: "2026-02-27",
    status: "active",
  },
  {
    id: "key_03",
    name: "Old CI runner",
    prefix: "nb_demo_bd20",
    last4: "5f81",
    secret: "nb_demo_bd2091c3e7a54d8b06f2a9c4d7e15f81",
    scope: "read",
    createdAt: "2025-06-18",
    lastUsedAt: null,
    status: "revoked",
  },
];

export async function getApiKeys(): Promise<ApiKey[]> {
  return keys;
}

// Always-safe display form: the prefix, a fixed run of dots, then the last four characters.
export function maskKey(key: Pick<ApiKey, "prefix" | "last4">) {
  return `${key.prefix}${"·".repeat(8)}${key.last4}`;
}
