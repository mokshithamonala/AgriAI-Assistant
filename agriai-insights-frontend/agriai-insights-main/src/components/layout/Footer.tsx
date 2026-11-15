import { Sprout } from "lucide-react";

export function Footer() {
  return (
    <footer className="mt-10 border-t border-border/60 px-4 py-6 text-xs text-muted-foreground sm:px-6 lg:px-8">
      <div className="flex flex-col items-start justify-between gap-2 sm:flex-row sm:items-center">
        <div className="flex items-center gap-2">
          <Sprout className="h-3.5 w-3.5 text-leaf" />
          <span>© {new Date().getFullYear()} AgriAI · Empowering farmers with AI</span>
        </div>
        <div className="flex gap-4">
          <a className="hover:text-foreground" href="#">Privacy</a>
          <a className="hover:text-foreground" href="#">Terms</a>
          <a className="hover:text-foreground" href="#">Support</a>
        </div>
      </div>
    </footer>
  );
}
