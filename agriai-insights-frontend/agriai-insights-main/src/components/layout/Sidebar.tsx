import { Link, useRouterState } from "@tanstack/react-router";
import {
  LayoutDashboard,
  Sparkles,
  Mic,
  CloudSun,
  TrendingUp,
  Leaf,
  Landmark,
  Settings,
  Sprout,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/ask-ai", label: "Ask AI", icon: Sparkles },
  { to: "/voice", label: "Voice Assistant", icon: Mic },
  { to: "/weather", label: "Weather", icon: CloudSun },
  { to: "/market", label: "Market Prices", icon: TrendingUp },
  { to: "/disease", label: "Crop Disease", icon: Leaf },
  { to: "/schemes", label: "Government Schemes", icon: Landmark },
  { to: "/settings", label: "Settings", icon: Settings },
] as const;

export function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <>
      {open && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-30 bg-black/40 backdrop-blur-sm lg:hidden"
        />
      )}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-72 flex-col bg-sidebar text-sidebar-foreground transition-transform duration-300 lg:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex items-center justify-between px-6 pt-6 pb-4">
          <Link to="/" className="flex items-center gap-2.5" onClick={onClose}>
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-leaf shadow-glow">
              <Sprout className="h-5 w-5 text-leaf-foreground" />
            </div>
            <div className="min-w-0">
              <div className="text-lg font-bold tracking-tight">AgriAI</div>
              <div className="text-[11px] text-sidebar-foreground/60">Smart Farming</div>
            </div>
          </Link>
          <button
            className="grid h-9 w-9 place-items-center rounded-lg hover:bg-sidebar-accent lg:hidden"
            onClick={onClose}
            aria-label="Close menu"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-2">
          {nav.map((item) => {
            const active =
              item.to === "/" ? pathname === "/" : pathname.startsWith(item.to);
            const Icon = item.icon;
            return (
              <Link
                key={item.to}
                to={item.to}
                onClick={onClose}
                className={cn(
                  "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
                  active
                    ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-soft"
                    : "text-sidebar-foreground/75 hover:bg-sidebar-accent/60 hover:text-sidebar-foreground",
                )}
              >
                <Icon className={cn("h-4 w-4 shrink-0", active && "text-leaf-foreground")} />
                <span className="truncate">{item.label}</span>
                {active && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-leaf-foreground" />}
              </Link>
            );
          })}
        </nav>

        <div className="m-3 rounded-2xl bg-sidebar-accent/50 p-4">
          <div className="text-xs font-semibold">Farmer Pro</div>
          <div className="mt-1 text-[11px] text-sidebar-foreground/70">
            Unlock premium crop insights and daily forecasts.
          </div>
          <button className="mt-3 w-full rounded-lg bg-leaf px-3 py-1.5 text-xs font-semibold text-leaf-foreground transition hover:opacity-90">
            Upgrade
          </button>
        </div>
      </aside>
    </>
  );
}
