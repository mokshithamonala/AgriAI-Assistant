import { useState, useRef } from "react";
import { Mic, Square, Loader2 } from "lucide-react";
import { DashboardCard, CardHeader } from "./DashboardCard";
import { cn } from "@/lib/utils";

export function VoiceAssistant() {
  const [recording, setRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusText, setStatusText] = useState("Ready");
  const [subStatusText, setSubStatusText] = useState("Click the microphone to begin speaking.");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Grab the local backend address from your .env configuration
  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const startRecording = async () => {
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
        await uploadAudio(audioBlob);
      };

      mediaRecorder.start();
      setRecording(true);
      setStatusText("Listening...");
      setSubStatusText("Speak clearly into the microphone.");
    } catch (error) {
      console.error("Microphone Access Error:", error);
      setStatusText("Error");
      setSubStatusText("Microphone access was denied or is not supported.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const uploadAudio = async (audioBlob: Blob) => {
    setIsProcessing(true);
    setStatusText("Processing...");
    setSubStatusText("Converting speech to text...");

    const formData = new FormData();
    formData.append("session_id", "session_web_client");
    formData.append("language_code", "en-IN"); 
    formData.append("file", audioBlob, "farmer_voice.wav");

    try {
      // Connect directly to the correct /api/v1 voice endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/query/audio`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned error status: ${response.status}`);
      }

      const data = await response.json();
      
      setStatusText("Success!");
      // Displays the translated advisory response returned from the audio processing chain
      setSubStatusText(data.translated_response || data.canonical_response || "Audio sent successfully!");
    } catch (error) {
      console.error("Audio Upload Connection Error:", error);
      setStatusText("Connection Failed");
      setSubStatusText("Could not send voice data to the local FastAPI backend.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleMicClick = () => {
    if (isProcessing) return;
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <DashboardCard>
      <CardHeader
        icon={<Mic className="h-5 w-5 text-sky" />}
        title="Voice Assistant"
        subtitle="Speak in your language, we'll do the rest."
      />

      <div className="flex flex-col items-center gap-4 py-4">
        <button
          onClick={handleMicClick}
          disabled={isProcessing}
          className={cn(
            "relative grid h-24 w-24 place-items-center rounded-full text-primary-foreground transition-all disabled:opacity-50 disabled:cursor-not-allowed",
            recording
              ? "bg-destructive shadow-[0_0_0_10px_oklch(0.58_0.22_25/0.15)]"
              : "bg-gradient-hero shadow-glow hover:scale-105",
          )}
        >
          {isProcessing ? (
            <Loader2 className="h-8 w-8 animate-spin" />
          ) : recording ? (
            <Square className="h-8 w-8" />
          ) : (
            <Mic className="h-8 w-8" />
          )}
          {recording && (
            <span className="absolute inset-0 animate-ping rounded-full bg-destructive/30" />
          )}
        </button>

        <div className="flex h-10 items-end gap-1">
          {Array.from({ length: 24 }).map((_, i) => (
            <span
              key={i}
              className={cn(
                "w-1.5 rounded-full bg-leaf",
                recording ? "animate-wave" : "h-1 opacity-30",
              )}
              style={
                recording
                  ? {
                      height: `${20 + (i % 5) * 8}px`,
                      animationDelay: `${(i % 8) * 0.08}s`,
                    }
                  : undefined
              }
            />
          ))}
        </div>

        <div className="text-center px-4">
          <div className="text-sm font-semibold">
            {statusText}
          </div>
          <div className="mt-1 text-xs text-muted-foreground line-clamp-3 max-w-[250px]">
            {subStatusText}
          </div>
        </div>
      </div>
    </DashboardCard>
  );
}