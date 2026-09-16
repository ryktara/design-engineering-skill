import { PrimaryNav } from "@/components/primary-nav";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-50 focus:rounded-md focus:bg-primary focus:px-3 focus:py-2 focus:text-primary-foreground"
      >
        Skip to content
      </a>
      <aside className="hidden w-56 shrink-0 border-r bg-muted/40 md:flex md:flex-col">
        <div className="flex h-14 items-center border-b px-4 text-sm font-semibold">Acme Console</div>
        <PrimaryNav />
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 items-center justify-between border-b px-4 md:px-6">
          <span className="text-sm font-semibold md:hidden">Acme Console</span>
          <span className="text-sm text-muted-foreground">Acme Inc. / Workspace</span>
        </header>
        <main id="main" className="flex-1 p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
