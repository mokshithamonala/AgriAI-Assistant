import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { WeatherCard } from "@/components/WeatherCard";

export const Route = createFileRoute("/weather")({
  head: () => ({
    meta: [
      { title: "Weather · AgriAI" },
      { name: "description", content: "Local weather and 5-day forecast for your farm." },
    ],
  }),
  component: () => (
    <AppShell title="Weather">
      <div className="mx-auto max-w-2xl">
        <WeatherCard />
      </div>
    </AppShell>
  ),
});
