"use client";

import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function UsageError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div role="alert" className="flex flex-col items-start gap-3 rounded-lg border border-destructive/40 p-6">
      <div className="flex items-center gap-2">
        <AlertTriangle className="size-5 text-destructive" aria-hidden="true" />
        <h2 className="text-base font-semibold">Usage figures could not be loaded</h2>
      </div>
      <p className="text-sm text-muted-foreground">
        The metering service did not respond. Your API keys keep working and calls are still counted. Try again, or contact
        support if this keeps happening.
      </p>
      <Button onClick={reset} variant="outline" size="sm">
        Try again
      </Button>
    </div>
  );
}
