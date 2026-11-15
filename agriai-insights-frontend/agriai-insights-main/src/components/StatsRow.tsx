import { stats } from "@/data/mock";

export function StatsRow() {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {stats.map((s) => (
        <div
          key={s.label}
          className="rounded-2xl border border-border/60 bg-card p-4 shadow-soft"
        >
          <div className="text-xs font-medium text-muted-foreground">{s.label}</div>
          <div className="mt-1 text-2xl font-bold tracking-tight">{s.value}</div>
          <div className="mt-0.5 text-[11px] text-leaf">{s.hint}</div>
        </div>
      ))}
    </div>
  );
}
