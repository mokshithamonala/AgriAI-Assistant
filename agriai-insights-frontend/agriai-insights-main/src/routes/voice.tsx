import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { VoiceAssistant } from "@/components/VoiceAssistant";

export const Route = createFileRoute("/voice")({
  head: () => ({
    meta: [
      { title: "Voice Assistant · AgriAI" },
      { name: "description", content: "Speak to AgriAI in your language." },
    ],
  }),
  component: () => (
    <AppShell title="Voice Assistant">
      <div className="mx-auto max-w-2xl">
        <VoiceAssistant />
      </div>
    </AppShell>
  ),
});
