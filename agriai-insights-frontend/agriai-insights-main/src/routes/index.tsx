import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { Hero } from "@/components/Hero";
import { StatsRow } from "@/components/StatsRow";
import { AskAISection } from "@/components/AskAISection";
import { VoiceAssistant } from "@/components/VoiceAssistant";
import { WeatherCard } from "@/components/WeatherCard";
import { MarketPriceTable } from "@/components/MarketPriceTable";
import { SchemesGrid } from "@/components/SchemeCard";
import { DiseaseUpload } from "@/components/DiseaseUpload";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "AgriAI · Smart Farmer Assistant" },
      {
        name: "description",
        content:
          "AI-powered multilingual agricultural advisory platform with weather, market prices, disease diagnosis and government schemes.",
      },
      { property: "og:title", content: "AgriAI · Smart Farmer Assistant" },
      {
        property: "og:description",
        content: "Multilingual AI advisory for crops, weather, prices and schemes.",
      },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  return (
    <AppShell title="Dashboard">
      <div className="space-y-6">
        <Hero />
        <StatsRow />
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <AskAISection />
          </div>
          <VoiceAssistant />
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <WeatherCard />
          <MarketPriceTable />
        </div>
        <DiseaseUpload />
        <div>
          <div className="mb-4 flex items-end justify-between">
            <div>
              <h3 className="text-lg font-semibold">Government Schemes</h3>
              <p className="text-sm text-muted-foreground">Programs you may be eligible for.</p>
            </div>
          </div>
          <SchemesGrid />
        </div>
      </div>
    </AppShell>
  );
}
