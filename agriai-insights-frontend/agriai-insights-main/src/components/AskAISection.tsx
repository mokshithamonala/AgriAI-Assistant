import { useState } from "react";
import { Bot, Mic, Send, Sparkles, Loader2 } from "lucide-react";
import { DashboardCard, CardHeader } from "./DashboardCard";
import { languages } from "@/data/mock";

export function AskAISection() {
  const [lang, setLang] = useState<string>("English");
  const [q, setQ] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Grab the local backend address from your .env configuration
  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  // Map friendly UI language names to regional locale codes expected by your backend
  const languageMapping: Record<string, string> = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN"
  };

  const submit = async () => {
    if (isLoading) return;
    const queryText = q.trim() || "How to control pests and leaf curl in tomato plants?";
    if (!q.trim()) setQ(queryText);

    setIsLoading(true);
    setResponse(null);

    const selectedLangCode = languageMapping[lang] || "en-IN";

    try {
      // Connect to the exact backend endpoint prefix
      const res = await fetch(`${API_BASE_URL}/api/v1/query/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: "session_web_client",
          text: queryText,
          preferred_language: selectedLangCode
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned status: ${res.status}`);
      }

      const data = await res.json();

      // Extract response based on APIResponseSchema
      const apiResponse = data.translated_response || data.canonical_response || data.response;
      
      if (apiResponse) {
        setResponse(apiResponse);
      } else {
        setResponse("Backend connection was successful, but no message key was returned.");
      }

    } catch (error) {
      console.error("FastAPI Connection Error:", error);
      setResponse(
        "Failed to reach the AI Advisory Server. Please verify that your Python local backend is active on port 8000!"
      );
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <DashboardCard>
      <CardHeader
        icon={<Bot className="h-5 w-5 text-leaf" />}
        title="Ask AI"
        subtitle="Ask anything about crops, diseases, fertilizers, irrigation, or farming."
      />

      <div className="grid gap-3 sm:grid-cols-[180px_1fr]">
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          disabled={isLoading}
          className="h-11 rounded-xl border border-border bg-card px-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 disabled:opacity-50"
        >
          {languages.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>
        <div className="flex items-center gap-2 rounded-xl border border-border bg-muted/40 px-3 text-xs text-muted-foreground">
          <Sparkles className="h-3.5 w-3.5 text-leaf" />
          Powered by multilingual agricultural intelligence
        </div>
      </div>

      <textarea
        value={q}
        onChange={(e) => setQ(e.target.value)}
        rows={4}
        disabled={isLoading}
        placeholder="Ask your farming question..."
        className="mt-3 w-full resize-none rounded-xl border border-border bg-card p-4 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20 disabled:opacity-50"
      />

      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        <button
          onClick={submit}
          disabled={isLoading}
          className="flex h-11 items-center justify-center gap-2 rounded-xl bg-gradient-hero text-sm font-semibold text-primary-foreground shadow-glow transition hover:opacity-95 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Thinking...
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              Ask AI
            </>
          )}
        </button>
        <button 
          disabled={isLoading}
          className="flex h-11 items-center justify-center gap-2 rounded-xl bg-sky text-sm font-semibold text-sky-foreground shadow-soft transition hover:opacity-95 disabled:opacity-50"
        >
          <Mic className="h-4 w-4" />
          Speak
        </button>
      </div>

      <div className="mt-5">
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <Bot className="h-3.5 w-3.5" /> AI Response
        </div>
        <div className="rounded-xl border border-dashed border-border bg-muted/30 p-4 text-sm">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin text-leaf" />
              <span>Consulting the database...</span>
            </div>
          ) : response ? (
            <div className="flex gap-3">
              <div className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-leaf text-leaf-foreground">
                <Bot className="h-4 w-4" />
              </div>
              <p className="leading-relaxed text-foreground/90">{response}</p>
            </div>
          ) : (
            <p className="text-muted-foreground">Waiting for your question...</p>
          )}
        </div>
      </div>
    </DashboardCard>
  );
}