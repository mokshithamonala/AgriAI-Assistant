import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { SchemesGrid } from "@/components/SchemeCard";

export const Route = createFileRoute("/schemes")({
  head: () => ({
    meta: [
      { title: "Government Schemes · AgriAI" },
      { name: "description", content: "Discover farmer welfare schemes and subsidies." },
    ],
  }),
  component: () => (
    <AppShell title="Government Schemes">
      <SchemesGrid />
    </AppShell>
  ),
});
