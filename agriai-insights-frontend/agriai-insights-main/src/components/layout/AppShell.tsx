import { useState, type ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { Footer } from "./Footer";

export function AppShell({ title, children }: { title: string; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="min-h-screen bg-background">
      <Sidebar open={open} onClose={() => setOpen(false)} />
      <div className="lg:pl-72">
        <Header onMenu={() => setOpen(true)} title={title} />
        <main className="px-4 py-6 sm:px-6 lg:px-8">{children}</main>
        <Footer />
      </div>
    </div>
  );
}
