import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { AskAISection } from "@/components/AskAISection";

export const Route = createFileRoute("/ask-ai")({
  head: () => ({
    meta: [
      { title: "Ask AI · AgriAI" },
      { name: "description", content: "Ask the AgriAI assistant anything about farming." },
    ],
  }),
  component: () => (
    <AppShell title="Ask AI">
      <AskAISection />
    </AppShell>
  ),
});
