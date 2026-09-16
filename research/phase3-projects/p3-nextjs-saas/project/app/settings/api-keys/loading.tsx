import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
  return (
    <div className="space-y-4" aria-busy="true" aria-label="Loading API keys">
      <div className="flex items-end justify-between gap-2">
        <Skeleton className="h-6 w-24" />
        <Skeleton className="h-8 w-28" />
      </div>
      <Skeleton className="h-[220px]" />
    </div>
  );
}
