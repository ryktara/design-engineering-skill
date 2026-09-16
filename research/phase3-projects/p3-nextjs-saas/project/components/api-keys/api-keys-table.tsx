"use client";

import * as React from "react";
import { CircleCheck, CircleSlash, Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/billing/status-badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatDate } from "@/lib/billing";
import { maskKey, scopeLabel, type ApiKey } from "@/lib/api-keys";

// Same table language as the seat / invoice tables: <th scope>, status as badge + label (never colour alone),
// dates in the shared format, secondary columns folded under the name below md (members-table convention).
// Key values are masked by default and revealed one row at a time on request.
export function ApiKeysTable({ apiKeys }: { apiKeys: ApiKey[] }) {
  const [revealed, setRevealed] = React.useState<string | null>(null);

  return (
    <section aria-labelledby="api-keys-heading" className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-2">
        <div className="space-y-1">
          <h2 id="api-keys-heading" className="text-base font-semibold">
            Keys
          </h2>
          <p className="text-sm text-muted-foreground">
            Keys are shown masked. Reveal a key only where nobody can read your screen.
          </p>
        </div>
        <Button size="sm">Create key</Button>
      </div>

      <div className="rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead scope="col">Name</TableHead>
              <TableHead scope="col">Key</TableHead>
              <TableHead scope="col" className="hidden md:table-cell">
                Access
              </TableHead>
              <TableHead scope="col" className="hidden lg:table-cell">
                Created
              </TableHead>
              <TableHead scope="col" className="hidden lg:table-cell">
                Last used
              </TableHead>
              <TableHead scope="col" className="hidden md:table-cell">
                Status
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {apiKeys.map((key) => {
              const isRevealed = revealed === key.id;
              return (
                <TableRow key={key.id}>
                  <TableCell>
                    <div className="flex min-w-0 flex-col">
                      <span className="font-medium">{key.name}</span>
                      <span className="mt-1 text-xs text-muted-foreground md:hidden">
                        {key.status === "active" ? "Active" : "Revoked"} · {scopeLabel[key.scope]}
                      </span>
                      <span className="mt-0.5 text-xs text-muted-foreground lg:hidden">
                        Created {formatDate(key.createdAt)}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      {/* Reserve the revealed width so the columns do not jump when a key is shown. */}
                      <span className="font-mono text-xs md:min-w-[19.5rem]">
                        {isRevealed ? key.secret : maskKey(key)}
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="-my-1 shrink-0 max-sm:size-11 max-sm:px-0 md:h-8 md:px-2"
                        aria-pressed={isRevealed}
                        onClick={() => setRevealed(isRevealed ? null : key.id)}
                      >
                        {isRevealed ? <EyeOff aria-hidden="true" /> : <Eye aria-hidden="true" />}
                        <span className="sr-only">
                          {isRevealed ? `Hide key ${key.name}` : `Reveal key ${key.name}`}
                        </span>
                      </Button>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">{scopeLabel[key.scope]}</TableCell>
                  <TableCell className="hidden tabular-nums lg:table-cell">{formatDate(key.createdAt)}</TableCell>
                  <TableCell className="hidden tabular-nums text-muted-foreground lg:table-cell">
                    {key.lastUsedAt ? formatDate(key.lastUsedAt) : "Never"}
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    {key.status === "active" ? (
                      <StatusBadge tone="success" icon={CircleCheck}>
                        Active
                      </StatusBadge>
                    ) : (
                      <StatusBadge tone="neutral" icon={CircleSlash}>
                        Revoked
                      </StatusBadge>
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </section>
  );
}
