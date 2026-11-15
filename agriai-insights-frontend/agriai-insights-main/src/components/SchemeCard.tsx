import { ArrowRight, Landmark } from "lucide-react";
import { schemes } from "@/data/mock";

export function SchemesGrid() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {schemes.map((s) => (
        <div
          key={s.name}
          className="group flex flex-col rounded-2xl border border-border/60 bg-card p-5 shadow-soft transition hover:-translate-y-0.5 hover:shadow-elevated"
        >
          <div className="mb-3 flex items-center justify-between">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-hero text-primary-foreground shadow-glow">
              <Landmark className="h-5 w-5" />
            </div>
            <span className="rounded-full bg-accent px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-accent-foreground">
              {s.tag}
            </span>
          </div>
          <div className="text-base font-semibold">{s.name}</div>
          <p className="mt-1.5 flex-1 text-sm text-muted-foreground">{s.description}</p>
          <button className="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-leaf transition group-hover:gap-2">
            Read More <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>
      ))}
    </div>
  );
}
