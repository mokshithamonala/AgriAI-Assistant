import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { MarketPriceTable } from "@/components/MarketPriceTable";

export const Route = createFileRoute("/market")({
  head: () => ({
    meta: [
      { title: "Market Prices · AgriAI" },
      { name: "description", content: "Live mandi rates for major crops across markets." },
    ],
  }),
  component: () => (
    <AppShell title="Market Prices">
      <MarketPriceTable />
    </AppShell>
  ),
});
