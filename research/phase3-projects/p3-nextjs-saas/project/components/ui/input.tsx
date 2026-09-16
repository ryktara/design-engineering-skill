import * as React from "react";
import { cn } from "@/lib/utils";

// shadcn-style Input; same height, border, radius and focus ring as the role <select> used in tables
// (h-11 on touch widths, h-9 from md up so it matches Button's default size).
const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type = "text", ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        "flex h-11 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors md:h-9",
        "placeholder:text-muted-foreground outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "aria-invalid:border-destructive aria-invalid:focus-visible:ring-destructive disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";

export { Input };
