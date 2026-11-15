import { useRef, useState } from "react";
import { ImagePlus, Leaf, ScanSearch, Upload, X } from "lucide-react";
import { DashboardCard, CardHeader } from "./DashboardCard";

export function DiseaseUpload() {
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<null | { name: string; conf: number; care: string }>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const onFile = (f?: File | null) => {
    if (!f) return;
    setPreview(URL.createObjectURL(f));
    setResult(null);
  };

  return (
    <DashboardCard>
      <CardHeader
        icon={<Leaf className="h-5 w-5 text-leaf" />}
        title="Crop Disease Diagnosis"
        subtitle="Upload a leaf photo to get an instant AI diagnosis."
      />

      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          onFile(e.dataTransfer.files?.[0]);
        }}
        onClick={() => inputRef.current?.click()}
        className="group relative flex min-h-[220px] cursor-pointer flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed border-border bg-muted/30 p-6 text-center transition hover:border-primary hover:bg-accent/40"
      >
        {preview ? (
          <>
            <img src={preview} alt="Preview" className="max-h-56 rounded-xl object-cover" />
            <button
              onClick={(e) => {
                e.stopPropagation();
                setPreview(null);
                setResult(null);
              }}
              className="absolute right-3 top-3 grid h-8 w-8 place-items-center rounded-full bg-background shadow-soft"
            >
              <X className="h-4 w-4" />
            </button>
          </>
        ) : (
          <>
            <div className="grid h-12 w-12 place-items-center rounded-xl bg-leaf/15 text-leaf">
              <ImagePlus className="h-6 w-6" />
            </div>
            <div className="text-sm font-semibold">Drag & drop a leaf image</div>
            <div className="text-xs text-muted-foreground">or click to browse · PNG, JPG</div>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => onFile(e.target.files?.[0])}
        />
      </div>

      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        <button
          onClick={() => inputRef.current?.click()}
          className="flex h-11 items-center justify-center gap-2 rounded-xl border border-border bg-card text-sm font-semibold transition hover:bg-accent"
        >
          <Upload className="h-4 w-4" /> Upload
        </button>
        <button
          disabled={!preview}
          onClick={() =>
            setResult({
              name: "Leaf Blight (Suspected)",
              conf: 92,
              care: "Apply copper-based fungicide; ensure proper drainage and avoid overhead irrigation.",
            })
          }
          className="flex h-11 items-center justify-center gap-2 rounded-xl bg-gradient-hero text-sm font-semibold text-primary-foreground shadow-glow transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <ScanSearch className="h-4 w-4" /> Analyze
        </button>
      </div>

      {result && (
        <div className="mt-4 rounded-xl border border-leaf/30 bg-leaf/10 p-4">
          <div className="flex items-center justify-between">
            <div className="text-sm font-semibold text-foreground">{result.name}</div>
            <div className="rounded-full bg-leaf px-2 py-0.5 text-xs font-semibold text-leaf-foreground">
              {result.conf}% match
            </div>
          </div>
          <p className="mt-2 text-sm text-foreground/80">{result.care}</p>
        </div>
      )}
    </DashboardCard>
  );
}
