import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { DiseaseUpload } from "@/components/DiseaseUpload";

export const Route = createFileRoute("/disease")({
  head: () => ({
    meta: [
      { title: "Crop Disease · AgriAI" },
      { name: "description", content: "Upload a leaf image to diagnose crop disease." },
    ],
  }),
  component: () => (
    <AppShell title="Crop Disease">
      <div className="mx-auto max-w-3xl">
        <DiseaseUpload />
      </div>
    </AppShell>
  ),
});
