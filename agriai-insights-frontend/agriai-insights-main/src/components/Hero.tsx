import { Sprout, Sparkles } from "lucide-react";

export function Hero() {
  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-hero p-6 text-primary-foreground shadow-elevated sm:p-8">
      <div className="absolute -right-10 -top-10 h-48 w-48 rounded-full bg-white/10 blur-2xl" />
      <div className="absolute -bottom-16 -left-10 h-56 w-56 rounded-full bg-white/5 blur-3xl" />
      <div className="relative flex flex-col-reverse gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="max-w-xl">
          <div className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-xs font-medium backdrop-blur">
            <Sparkles className="h-3 w-3" /> AI Advisory · Live
          </div>
          <h2 className="mt-3 text-2xl font-bold leading-tight tracking-tight sm:text-3xl lg:text-4xl">
            Smart Farmer Assistant
          </h2>
          <p className="mt-2 max-w-md text-sm text-primary-foreground/85 sm:text-base">
            AI-powered multilingual agricultural advisory platform — crops, weather,
            markets, and schemes in one place.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <button className="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-primary shadow-soft transition hover:bg-white/90">
              Ask AI now
            </button>
            <button className="rounded-xl border border-white/30 bg-white/10 px-4 py-2 text-sm font-semibold backdrop-blur transition hover:bg-white/20">
              View weather
            </button>
          </div>
        </div>
        <div className="grid h-28 w-28 shrink-0 place-items-center rounded-3xl bg-white/15 backdrop-blur sm:h-36 sm:w-36">
          <Sprout className="h-16 w-16 sm:h-20 sm:w-20" />
        </div>
      </div>
    </div>
  );
}
