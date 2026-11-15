import { Bell, Menu, Search } from "lucide-react";

export function Header({ onMenu, title }: { onMenu: () => void; title: string }) {
  return (
    <header className="sticky top-0 z-20 border-b border-border/60 bg-background/85 backdrop-blur-xl">
      <div className="flex h-16 items-center gap-3 px-4 sm:px-6 lg:px-8">
        <button
          onClick={onMenu}
          className="grid h-10 w-10 place-items-center rounded-xl border border-border bg-card lg:hidden"
          aria-label="Open menu"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="min-w-0 flex-1">
          <h1 className="truncate text-lg font-semibold tracking-tight sm:text-xl">{title}</h1>
          <p className="hidden text-xs text-muted-foreground sm:block">
            Welcome back, let's help your farm thrive today.
          </p>
        </div>

        <div className="hidden max-w-xs flex-1 md:block">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              placeholder="Search crops, schemes…"
              className="h-10 w-full rounded-xl border border-border bg-card pl-9 pr-3 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>

        <button
          className="relative grid h-10 w-10 place-items-center rounded-xl border border-border bg-card transition hover:bg-accent"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-destructive" />
        </button>

        <div className="flex items-center gap-2 rounded-xl border border-border bg-card px-2 py-1.5">
          <div className="grid h-7 w-7 place-items-center rounded-lg bg-gradient-hero text-xs font-bold text-primary-foreground">
            RK
          </div>
          <div className="hidden sm:block">
            <div className="text-xs font-semibold leading-tight">Ravi Kumar</div>
            <div className="text-[10px] text-muted-foreground">Karnataka, IN</div>
          </div>
        </div>
      </div>
    </header>
  );
}
