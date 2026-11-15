import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function DashboardCard({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-border/60 bg-card p-5 shadow-soft transition hover:shadow-elevated sm:p-6",
        className,
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  icon,
  title,
  subtitle,
  action,
}: {
  icon?: ReactNode;
  title: string;
  subtitle?: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="mb-4 flex items-start justify-between gap-3">
      <div className="flex min-w-0 items-start gap-3">
        {icon && (
          <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-accent text-accent-foreground">
            {icon}
          </div>
        )}
        <div className="min-w-0">
          <h3 className="truncate text-base font-semibold sm:text-lg">{title}</h3>
          {subtitle && <p className="mt-0.5 text-sm text-muted-foreground">{subtitle}</p>}
        </div>
      </div>
      {action}
    </div>
  );
}
