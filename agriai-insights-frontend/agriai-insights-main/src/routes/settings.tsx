import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Bell, Moon, Sun, User, Volume2 } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { DashboardCard, CardHeader } from "@/components/DashboardCard";
import { languages } from "@/data/mock";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title: "Settings · AgriAI" },
      { name: "description", content: "Manage your AgriAI preferences." },
    ],
  }),
  component: Settings,
});

function Toggle({ on, onChange }: { on: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange(!on)}
      className={cn(
        "relative h-6 w-11 rounded-full transition",
        on ? "bg-leaf" : "bg-muted",
      )}
    >
      <span
        className={cn(
          "absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition",
          on ? "left-5" : "left-0.5",
        )}
      />
    </button>
  );
}

function Row({
  icon,
  title,
  desc,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  desc: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-4 py-3">
      <div className="flex min-w-0 items-center gap-3">
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-accent text-accent-foreground">
          {icon}
        </div>
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold">{title}</div>
          <div className="text-xs text-muted-foreground">{desc}</div>
        </div>
      </div>
      <div className="shrink-0">{children}</div>
    </div>
  );
}

function Settings() {
  const [dark, setDark] = useState(false);
  const [voice, setVoice] = useState(true);
  const [notify, setNotify] = useState(true);
  const [lang, setLang] = useState("English");

  const toggleDark = (v: boolean) => {
    setDark(v);
    document.documentElement.classList.toggle("dark", v);
  };

  return (
    <AppShell title="Settings">
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <DashboardCard>
            <CardHeader title="Preferences" subtitle="Personalise how AgriAI works for you." />
            <div className="divide-y divide-border">
              <Row
                icon={dark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
                title="Dark theme"
                desc="Reduce glare in low light."
              >
                <Toggle on={dark} onChange={toggleDark} />
              </Row>
              <Row
                icon={<Volume2 className="h-4 w-4" />}
                title="Voice output"
                desc="Read AI answers aloud."
              >
                <Toggle on={voice} onChange={setVoice} />
              </Row>
              <Row
                icon={<Bell className="h-4 w-4" />}
                title="Notifications"
                desc="Alerts for weather and prices."
              >
                <Toggle on={notify} onChange={setNotify} />
              </Row>
              <Row
                icon={<span className="text-xs font-bold">Aa</span>}
                title="Language"
                desc="Assistant response language."
              >
                <select
                  value={lang}
                  onChange={(e) => setLang(e.target.value)}
                  className="h-9 rounded-lg border border-border bg-card px-2 text-sm"
                >
                  {languages.map((l) => (
                    <option key={l}>{l}</option>
                  ))}
                </select>
              </Row>
            </div>
          </DashboardCard>
        </div>

        <DashboardCard>
          <CardHeader title="Profile" subtitle="Your account information." />
          <div className="flex flex-col items-center gap-3 py-2">
            <div className="grid h-20 w-20 place-items-center rounded-2xl bg-gradient-hero text-2xl font-bold text-primary-foreground shadow-glow">
              RK
            </div>
            <div className="text-center">
              <div className="text-base font-semibold">Ravi Kumar</div>
              <div className="text-xs text-muted-foreground">Mysuru, Karnataka</div>
            </div>
            <div className="mt-2 grid w-full grid-cols-2 gap-3 text-center">
              <div className="rounded-xl border border-border p-3">
                <div className="text-lg font-bold">4</div>
                <div className="text-[11px] text-muted-foreground">Crops</div>
              </div>
              <div className="rounded-xl border border-border p-3">
                <div className="text-lg font-bold">12</div>
                <div className="text-[11px] text-muted-foreground">Queries</div>
              </div>
            </div>
            <button className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-border bg-card py-2 text-sm font-semibold hover:bg-accent">
              <User className="h-4 w-4" /> Edit profile
            </button>
          </div>
        </DashboardCard>
      </div>
    </AppShell>
  );
}
