import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type StatusTone = "success" | "warning" | "destructive" | "neutral" | "info";

// One status chip for the whole billing page (seat status, invoice status): outline badge,
// tone carried by text + dot, and the label always present so colour is never the only cue.
const tones: Record<StatusTone, { badge: string; dot: string | null }> = {
  success: { badge: "border-success/40 text-success", dot: "bg-success" },
  warning: { badge: "border-warning/40 text-warning", dot: "bg-warning" },
  destructive: { badge: "border-destructive/40 text-destructive", dot: "bg-destructive" },
  info: { badge: "border-transparent bg-secondary text-secondary-foreground", dot: null },
  neutral: { badge: "text-muted-foreground", dot: null },
};

export function StatusBadge({ tone, className, children }: { tone: StatusTone; className?: string; children: React.ReactNode }) {
  const t = tones[tone];
  return (
    <Badge variant="outline" className={cn("gap-1.5", t.badge, className)}>
      {t.dot && <span className={cn("size-1.5 rounded-full", t.dot)} aria-hidden="true" />}
      {children}
    </Badge>
  );
}
