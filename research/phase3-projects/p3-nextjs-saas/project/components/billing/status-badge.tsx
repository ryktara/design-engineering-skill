import type { LucideIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type StatusTone = "success" | "warning" | "destructive" | "neutral" | "info";

// One status chip for the whole billing page (seat status, invoice status): outline badge,
// tone carried by colour, meaning carried by the label and an icon whose shape differs per status,
// so colour is never the only cue (WCAG 1.4.1). Icons are decorative; the label is the name.
const tones: Record<StatusTone, string> = {
  success: "border-success/40 text-success",
  warning: "border-warning/40 text-warning",
  destructive: "border-destructive/40 text-destructive",
  info: "border-transparent bg-secondary text-secondary-foreground",
  neutral: "text-muted-foreground",
};

export function StatusBadge({
  tone,
  icon: Icon,
  className,
  children,
}: {
  tone: StatusTone;
  icon?: LucideIcon;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <Badge variant="outline" className={cn("gap-1", tones[tone], className)}>
      {Icon && <Icon className="size-3.5 shrink-0" strokeWidth={2.25} aria-hidden="true" />}
      {children}
    </Badge>
  );
}
