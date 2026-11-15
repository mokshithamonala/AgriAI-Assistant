import inspect
import starlette.applications
import starlette.routing

# Compatibility shim for Starlette 1.0+ with FastAPI 0.115.x
starlette.applications.Starlette.max_body_size = None
_orig_router_init = starlette.routing.Router.__init__
if "on_startup" not in inspect.signature(_orig_router_init).parameters:
    def _patched_router_init(self, *args, on_startup=None, on_shutdown=None, **kwargs):
        _orig_router_init(self, *args, **kwargs)
        self.on_startup = [] if on_startup is None else list(on_startup)
        self.on_shutdown = [] if on_shutdown is None else list(on_shutdown)
    starlette.routing.Router.__init__ = _patched_router_init

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="AgriAI · Smart Farmer Assistant Frontend")

FRONTEND_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AgriAI · Smart Farmer Assistant (Full-Stack)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --bg: #f6f9f4;
      --fg: #142b1f;
      --card: #ffffff;
      --muted: #eef4ec;
      --muted-fg: #546e5f;
      --border: #dce7d9;
      --leaf: #1e824c;
      --leaf-fg: #f7fcf8;
      --sky: #2580e8;
      --sidebar: #143625;
      --sidebar-fg: #ebf5ee;
      --sidebar-accent: #1f5439;
    }
    .dark {
      --bg: #0f1f17;
      --fg: #ebf5ee;
      --card: #162b20;
      --muted: #1e382b;
      --muted-fg: #94b0a0;
      --border: #254535;
      --sidebar: #0b1811;
    }
    body {
      background-color: var(--bg);
      color: var(--fg);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      margin: 0;
    }
    .bg-gradient-hero {
      background: linear-gradient(135deg, #1e824c 0%, #169c78 100%);
    }
    .shadow-soft {
      box-shadow: 0 1px 2px rgba(20,43,31,0.04), 0 8px 24px -8px rgba(20,43,31,0.08);
    }
    .shadow-glow {
      box-shadow: 0 8px 28px -4px rgba(30, 130, 76, 0.35);
    }
  </style>
</head>
<body class="min-h-screen flex">
  <!-- Sidebar -->
  <aside style="background: var(--sidebar); color: var(--sidebar-fg);" class="w-72 shrink-0 flex flex-col min-h-screen fixed inset-y-0 left-0 z-30">
    <div class="flex items-center gap-3 px-6 pt-6 pb-4">
      <a href="/" onclick="return navigate(event, '/')" class="flex items-center gap-2.5 text-white no-underline">
        <div class="grid h-10 w-10 place-items-center rounded-xl bg-[#1e824c] shadow-glow font-bold text-lg">🌱</div>
        <div>
          <div class="text-lg font-bold tracking-tight">AgriAI</div>
          <div class="text-[11px] opacity-65">Full-Stack Smart Farming</div>
        </div>
      </a>
    </div>

    <nav class="flex-1 space-y-1 px-3 py-2 overflow-y-auto" id="sidebarNav">
      <a href="/" onclick="return navigate(event, '/')" data-route="/" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>📊</span><span>Dashboard</span>
      </a>
      <a href="/ask-ai" onclick="return navigate(event, '/ask-ai')" data-route="/ask-ai" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>✨</span><span>Ask AI Advisory</span>
      </a>
      <a href="/voice" onclick="return navigate(event, '/voice')" data-route="/voice" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>🎙️</span><span>Voice Assistant</span>
      </a>
      <a href="/weather" onclick="return navigate(event, '/weather')" data-route="/weather" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>⛅</span><span>Weather Intelligence</span>
      </a>
      <a href="/market" onclick="return navigate(event, '/market')" data-route="/market" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>📈</span><span>Market Prices (APMC)</span>
      </a>
      <a href="/disease" onclick="return navigate(event, '/disease')" data-route="/disease" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>🍃</span><span>Crop Disease AI</span>
      </a>
      <a href="/schemes" onclick="return navigate(event, '/schemes')" data-route="/schemes" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>🏛️</span><span>Government Schemes</span>
      </a>
      <a href="/database" onclick="return navigate(event, '/database')" data-route="/database" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>🗄️</span><span>Database & History</span>
      </a>
      <a href="/settings" onclick="return navigate(event, '/settings')" data-route="/settings" class="nav-link flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all">
        <span>⚙️</span><span>Settings</span>
      </a>
    </nav>

    <div class="m-3 rounded-2xl p-4" style="background: rgba(31,84,57,0.55);">
      <div class="text-xs font-semibold flex items-center justify-between">
        <span>Full-Stack Status</span>
        <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
      </div>
      <div class="mt-1 text-[11px] opacity-80">Backend: http://127.0.0.1:8000</div>
      <div class="text-[11px] opacity-80" id="sidebarDbBadge">Database: Connected (0 msgs)</div>
      <a href="http://127.0.0.1:8000/docs" target="_blank" class="mt-3 block text-center w-full rounded-lg bg-[#1e824c] px-3 py-1.5 text-xs font-semibold text-white no-underline hover:opacity-90">
        Open FastAPI Swagger Docs
      </a>
    </div>
  </aside>

  <!-- Main Content -->
  <div class="flex-1 pl-72 flex flex-col min-h-screen">
    <header class="sticky top-0 z-20 border-b px-8 h-16 flex items-center justify-between backdrop-blur-xl" style="background: var(--bg); border-color: var(--border);">
      <div>
        <h1 id="pageTitle" class="text-xl font-semibold tracking-tight">Dashboard</h1>
        <p class="text-xs" style="color: var(--muted-fg);">AI-Powered Multilingual Agricultural Advisory Engine · Frontend + Backend + Database</p>
      </div>
      <div class="flex items-center gap-3">
        <span id="apiStatusPill" class="inline-flex items-center gap-1.5 rounded-full bg-emerald-100 text-emerald-800 px-3 py-1 text-xs font-semibold">
          <span class="h-2 w-2 rounded-full bg-emerald-600"></span> Backend & DB Online (:8000)
        </span>
        <button onclick="document.documentElement.classList.toggle('dark')" class="rounded-xl border px-3 py-1.5 text-xs font-semibold cursor-pointer" style="background: var(--card); border-color: var(--border);">
          🌓 Theme
        </button>
      </div>
    </header>

    <main class="p-8 max-w-6xl w-full mx-auto space-y-6 flex-1">
      <!-- Hero Section (shown on /) -->
      <div id="sec-hero" class="relative overflow-hidden rounded-3xl bg-gradient-hero p-8 text-white shadow-soft">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          <div class="max-w-xl">
            <div class="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-xs font-medium">
              ✨ Live Groq AI + Multilingual Voice + SQLite/PostgreSQL Database
            </div>
            <h2 class="mt-3 text-3xl font-bold tracking-tight">Smart Farmer Assistant</h2>
            <p class="mt-2 text-sm text-white/90">
              Ask any farming question in English, Tamil, Hindi, Telugu, Kannada, or Malayalam — get instant expert crop advisory, live weather, APMC market prices, disease diagnosis, and database session tracking.
            </p>
            <div class="mt-5 flex flex-wrap gap-2">
              <button onclick="navigate(null, '/ask-ai')" class="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-emerald-800 shadow-soft hover:bg-white/90 cursor-pointer">
                Ask AI Now
              </button>
              <button onclick="navigate(null, '/database')" class="rounded-xl border border-white/30 bg-white/10 px-4 py-2 text-sm font-semibold text-white hover:bg-white/20 cursor-pointer">
                🗄️ View Database Records
              </button>
            </div>
          </div>
          <div class="grid h-28 w-28 place-items-center rounded-3xl bg-white/15 text-6xl">🌱</div>
        </div>
      </div>

      <!-- Stats Row (shown on /) -->
      <div id="sec-stats" class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div class="rounded-2xl border p-4 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="text-xs font-medium" style="color: var(--muted-fg);">Supported Languages</div>
          <div class="mt-1 text-2xl font-bold">6</div>
          <div class="mt-0.5 text-[11px] text-emerald-600">EN · HI · TA · TE · KN · ML</div>
        </div>
        <div class="rounded-2xl border p-4 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="text-xs font-medium" style="color: var(--muted-fg);">DB Stored Queries</div>
          <div id="statTotalMsgs" class="mt-1 text-2xl font-bold">0</div>
          <div id="statTotalSessions" class="mt-0.5 text-[11px] text-emerald-600">Active in conversation_states</div>
        </div>
        <div class="rounded-2xl border p-4 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="text-xs font-medium" style="color: var(--muted-fg);">Live Mandi Crops</div>
          <div class="mt-1 text-2xl font-bold">8+</div>
          <div class="mt-0.5 text-[11px] text-emerald-600">Real-time APMC lookup</div>
        </div>
        <div class="rounded-2xl border p-4 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="text-xs font-medium" style="color: var(--muted-fg);">Govt Schemes</div>
          <div class="mt-1 text-2xl font-bold">6</div>
          <div class="mt-0.5 text-[11px] text-emerald-600">Verified farmer programs</div>
        </div>
      </div>

      <!-- Ask AI & Voice Row -->
      <div id="sec-ai-row" class="grid gap-6 lg:grid-cols-3">
        <!-- Ask AI Card -->
        <div id="sec-ask-ai" class="lg:col-span-2 rounded-2xl border p-6 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="mb-4 flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold flex items-center gap-2">🤖 Ask AI Agricultural Advisor</h3>
              <p class="text-xs" style="color: var(--muted-fg);">Ask any question about crops, pests, diseases, fertilizers, irrigation, weather, or schemes.</p>
            </div>
            <span class="rounded-lg bg-emerald-500/10 text-emerald-600 px-2.5 py-1 text-xs font-semibold">Live LLM Engine</span>
          </div>

          <div class="grid gap-3 sm:grid-cols-[200px_1fr]">
            <div>
              <label class="block text-[11px] font-semibold mb-1" style="color: var(--muted-fg);">Response Language</label>
              <select id="askLang" onchange="onLangChange()" class="w-full h-11 rounded-xl border px-3 text-sm font-medium outline-none" style="background: var(--card); border-color: var(--border);">
                <option value="en-IN">English (en-IN)</option>
                <option value="ta-IN">Tamil - தமிழ் (ta-IN)</option>
                <option value="hi-IN">Hindi - हिन्दी (hi-IN)</option>
                <option value="te-IN">Telugu - తెలుగు (te-IN)</option>
                <option value="kn-IN">Kannada - ಕನ್ನಡ (kn-IN)</option>
                <option value="ml-IN">Malayalam - മലയാളം (ml-IN)</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-semibold mb-1" style="color: var(--muted-fg);">Quick Sample Questions (Click any to ask immediately)</label>
              <div class="flex flex-wrap gap-1.5 pt-0.5">
                <button type="button" onclick="askSampleByTopic('tomato')" class="rounded-lg border px-2.5 py-1.5 text-xs font-medium hover:opacity-80 cursor-pointer" style="background: var(--muted); border-color: var(--border);">🍅 Tomato Pest & Leaf Curl</button>
                <button type="button" onclick="askSampleByTopic('paddy')" class="rounded-lg border px-2.5 py-1.5 text-xs font-medium hover:opacity-80 cursor-pointer" style="background: var(--muted); border-color: var(--border);">🌾 Paddy NPK Fertilizer</button>
                <button type="button" onclick="askSampleByTopic('blight')" class="rounded-lg border px-2.5 py-1.5 text-xs font-medium hover:opacity-80 cursor-pointer" style="background: var(--muted); border-color: var(--border);">🍃 Yellow Leaf & Blight</button>
                <button type="button" onclick="askSampleByTopic('scheme')" class="rounded-lg border px-2.5 py-1.5 text-xs font-medium hover:opacity-80 cursor-pointer" style="background: var(--muted); border-color: var(--border);">🏛️ PM-KISAN & Subsidies</button>
              </div>
            </div>
          </div>

          <textarea id="askInput" rows="3" onkeydown="if(event.key==='Enter' && !event.shiftKey){event.preventDefault();submitAskAI();}" placeholder="Type any farming question here in English, Tamil, Hindi, Telugu, Kannada, or Malayalam and press Enter or click Ask AI..." class="mt-3 w-full rounded-xl border p-4 text-sm outline-none" style="background: var(--card); border-color: var(--border);">How to control pests and leaf curl disease in tomato plants?</textarea>

          <div class="mt-3 grid gap-2 sm:grid-cols-3">
            <button id="askBtn" onclick="submitAskAI()" class="sm:col-span-2 h-11 rounded-xl bg-gradient-hero text-sm font-semibold text-white shadow-glow hover:opacity-95 cursor-pointer">
              🚀 Ask AI (Get Instant Answer)
            </button>
            <button onclick="speakCurrentAnswer()" class="h-11 rounded-xl border text-sm font-semibold hover:opacity-90 cursor-pointer" style="background: var(--muted); border-color: var(--border);">
              🔊 Listen to Answer
            </button>
          </div>

          <div class="mt-5">
            <div class="mb-2 flex items-center justify-between">
              <span class="text-xs font-semibold uppercase tracking-wider" style="color: var(--muted-fg);">AI Advisory Response</span>
              <span id="askMetaBadge" class="text-xs font-medium text-emerald-600">Ready</span>
            </div>
            <div id="askResponseBox" class="rounded-xl border p-5 text-sm whitespace-pre-wrap leading-relaxed" style="background: var(--muted); border-color: var(--border);">Click <strong>"🚀 Ask AI"</strong> above or type any question to receive a complete agricultural advisory answer in your chosen language.</div>
          </div>
        </div>

        <!-- Voice Assistant Card -->
        <div id="sec-voice" class="rounded-2xl border p-6 shadow-soft flex flex-col justify-between" style="background: var(--card); border-color: var(--border);">
          <div>
            <div class="mb-4">
              <h3 class="text-lg font-semibold flex items-center gap-2">🎙️ Voice Assistant</h3>
              <p class="text-xs" style="color: var(--muted-fg);">Speak in your language, upload an audio clip, or run a live voice simulation.</p>
            </div>
            <div class="flex flex-col items-center gap-3 py-3">
              <button id="micBtn" onclick="toggleRecording()" class="grid h-20 w-20 place-items-center rounded-full bg-gradient-hero text-white text-3xl shadow-glow transition hover:scale-105 cursor-pointer">
                🎙️
              </button>
              <div class="text-center px-2">
                <div id="voiceStatus" class="text-sm font-semibold">Ready for Voice Input</div>
                <div id="voiceSubStatus" class="mt-1 text-xs" style="color: var(--muted-fg);">
                  Click mic to record, upload a file, or test voice below.
                </div>
              </div>
            </div>

            <div class="w-full pt-3 border-t space-y-2.5" style="border-color: var(--border);">
              <div>
                <label class="block text-xs font-semibold mb-1">Select Spoken Language</label>
                <select id="voiceLang" class="w-full h-9 rounded-lg border px-2 text-xs font-medium" style="background: var(--card); border-color: var(--border);">
                  <option value="ta-IN">Tamil - தமிழ் (ta-IN)</option>
                  <option value="hi-IN">Hindi - हिन्दी (hi-IN)</option>
                  <option value="te-IN">Telugu - తెలుగు (te-IN)</option>
                  <option value="kn-IN">Kannada - ಕನ್ನಡ (kn-IN)</option>
                  <option value="ml-IN">Malayalam - മലയാളം (ml-IN)</option>
                  <option value="en-IN">English (en-IN)</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-semibold mb-1">Upload Audio File (.wav / .mp3 / .webm)</label>
                <input type="file" id="audioFileInput" accept="audio/*" onchange="uploadSelectedAudioFile()" class="text-xs w-full" />
              </div>
              <button onclick="simulateVoiceAudioQuery()" class="w-full h-9 rounded-lg bg-sky-600 text-white text-xs font-semibold hover:opacity-95 cursor-pointer">
                ⚡ Test Voice Pipeline (Instant Demo Audio)
              </button>
            </div>
          </div>

          <div id="voiceResultCard" class="mt-4 rounded-xl border p-3 text-xs whitespace-pre-wrap max-h-48 overflow-y-auto" style="background: var(--muted); border-color: var(--border);">
            Voice advisory output will appear here and in the main AI response panel.
          </div>
        </div>
      </div>

      <!-- Weather & Market Prices Row -->
      <div id="sec-weather-market-row" class="grid gap-6 lg:grid-cols-2">
        <!-- Weather Card -->
        <div id="sec-weather" class="rounded-2xl border p-6 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
            <div>
              <h3 class="text-lg font-semibold flex items-center gap-2">⛅ Live Weather Intelligence</h3>
              <p class="text-xs" style="color: var(--muted-fg);" id="weatherLocationLabel">📍 Bengaluru, India</p>
            </div>
            <div class="flex gap-2">
              <input id="weatherCityInput" value="Bengaluru" onkeydown="if(event.key==='Enter')loadWeather();" placeholder="Enter city..." class="h-9 w-36 rounded-lg border px-2.5 text-xs" style="background: var(--card); border-color: var(--border);" />
              <button onclick="loadWeather()" class="h-9 rounded-lg bg-emerald-700 text-white px-3 text-xs font-semibold cursor-pointer">Check Weather</button>
            </div>
          </div>
          <div class="mb-3 flex flex-wrap gap-1.5">
            <button onclick="quickWeather('Bengaluru')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Bengaluru</button>
            <button onclick="quickWeather('Chennai')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Chennai</button>
            <button onclick="quickWeather('Hyderabad')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Hyderabad</button>
            <button onclick="quickWeather('Coimbatore')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Coimbatore</button>
            <button onclick="quickWeather('Mysuru')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Mysuru</button>
            <button onclick="quickWeather('Ludhiana')" class="rounded-md border px-2 py-0.5 text-[11px] cursor-pointer" style="background: var(--muted); border-color: var(--border);">Ludhiana</button>
          </div>
          <div class="rounded-2xl p-5" style="background: linear-gradient(135deg, rgba(37,128,232,0.12), rgba(30,130,76,0.10));">
            <div class="flex items-end justify-between">
              <div>
                <div id="weatherTemp" class="text-5xl font-bold tracking-tight">28°C</div>
                <div id="weatherCond" class="mt-1 text-sm font-medium" style="color: var(--muted-fg);">Partly Cloudy</div>
              </div>
              <div class="text-6xl">⛅</div>
            </div>
            <div class="mt-5 grid grid-cols-3 gap-3">
              <div class="rounded-xl p-3" style="background: var(--card);">
                <div class="text-xs" style="color: var(--muted-fg);">💧 Humidity</div>
                <div id="weatherHum" class="mt-1 text-sm font-semibold">65%</div>
              </div>
              <div class="rounded-xl p-3" style="background: var(--card);">
                <div class="text-xs" style="color: var(--muted-fg);">🌧️ Rainfall</div>
                <div id="weatherRain" class="mt-1 text-sm font-semibold">0.0 mm</div>
              </div>
              <div class="rounded-xl p-3" style="background: var(--card);">
                <div class="text-xs" style="color: var(--muted-fg);">🌾 Spray Advisory</div>
                <div id="weatherSprayTip" class="mt-1 text-xs font-semibold text-emerald-600">Safe to spray</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Market Prices Card -->
        <div id="sec-market" class="rounded-2xl border p-6 shadow-soft" style="background: var(--card); border-color: var(--border);">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="text-lg font-semibold flex items-center gap-2">📈 APMC Market Prices</h3>
              <p class="text-xs" style="color: var(--muted-fg);">Search any crop, state, and district or browse live mandi rates.</p>
            </div>
            <button onclick="loadAllMandiPrices()" class="h-8 rounded-lg bg-emerald-700 text-white px-3 text-xs font-semibold cursor-pointer">↻ Refresh</button>
          </div>
          <!-- Custom Mandi Search -->
          <div class="grid grid-cols-4 gap-2 mb-3">
            <input id="mandiCropInput" value="Tomato" placeholder="Crop (e.g. Tomato)" class="h-8 rounded-lg border px-2 text-xs" style="background: var(--card); border-color: var(--border);" />
            <input id="mandiStateInput" value="Karnataka" placeholder="State" class="h-8 rounded-lg border px-2 text-xs" style="background: var(--card); border-color: var(--border);" />
            <input id="mandiDistInput" value="Kolar" placeholder="District" class="h-8 rounded-lg border px-2 text-xs" style="background: var(--card); border-color: var(--border);" />
            <button onclick="lookupCustomMandiPrice()" class="h-8 rounded-lg bg-sky-600 text-white text-xs font-semibold cursor-pointer">Search Mandi</button>
          </div>
          <div class="overflow-x-auto max-h-64 overflow-y-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-left text-xs uppercase" style="color: var(--muted-fg);">
                  <th class="py-2">Crop</th>
                  <th class="py-2">APMC Market</th>
                  <th class="py-2 text-right">Modal Price</th>
                  <th class="py-2 text-right">Trend</th>
                </tr>
              </thead>
              <tbody id="marketTableBody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Disease Upload & AI Diagnosis Section -->
      <div id="sec-disease" class="rounded-2xl border p-6 shadow-soft" style="background: var(--card); border-color: var(--border);">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h3 class="text-lg font-semibold flex items-center gap-2">🍃 AI Crop Disease Diagnosis</h3>
            <p class="text-xs" style="color: var(--muted-fg);">Upload a crop leaf image and describe symptoms for an instant AI pathology diagnosis & treatment plan.</p>
          </div>
          <span class="rounded-lg bg-emerald-500/10 text-emerald-600 px-2.5 py-1 text-xs font-semibold">Connected to /api/v1/disease/analyze</span>
        </div>

        <div class="grid gap-4 md:grid-cols-2">
          <div onclick="document.getElementById('leafInput').click()" class="flex min-h-[160px] cursor-pointer flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed p-5 text-center" style="background: var(--muted); border-color: var(--border);">
            <img id="leafPreview" class="hidden max-h-36 rounded-xl object-cover mb-1" />
            <div class="text-3xl">🌿</div>
            <div id="leafFileName" class="text-sm font-semibold">Click to select a crop leaf photo (optional)</div>
            <div class="text-xs" style="color: var(--muted-fg);">PNG, JPG, or WEBP supported</div>
            <input id="leafInput" type="file" accept="image/*" class="hidden" onchange="previewLeaf(event)" />
          </div>

          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs font-semibold mb-1">Crop Name</label>
                <input id="diseaseCrop" value="Tomato" class="w-full h-9 rounded-lg border px-3 text-xs" style="background: var(--card); border-color: var(--border);" />
              </div>
              <div>
                <label class="block text-xs font-semibold mb-1">Language</label>
                <select id="diseaseLang" class="w-full h-9 rounded-lg border px-2 text-xs" style="background: var(--card); border-color: var(--border);">
                  <option value="en-IN">English</option>
                  <option value="ta-IN">Tamil (தமிழ்)</option>
                  <option value="hi-IN">Hindi (हिन्दी)</option>
                  <option value="te-IN">Telugu (తెలుగు)</option>
                  <option value="kn-IN">Kannada (ಕನ್ನಡ)</option>
                  <option value="ml-IN">Malayalam (മലയാളം)</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-xs font-semibold mb-1">Observed Leaf / Plant Symptoms</label>
              <textarea id="diseaseSymptoms" rows="2" class="w-full rounded-lg border p-2.5 text-xs" style="background: var(--card); border-color: var(--border);">Yellowing leaves with dark brown concentric rings, curling edges, and stunted growth.</textarea>
            </div>
            <button id="diseaseBtn" onclick="analyzeLeaf()" class="w-full h-10 rounded-xl bg-gradient-hero text-xs font-semibold text-white shadow-glow cursor-pointer">
              🔍 Run AI Disease Diagnosis
            </button>
          </div>
        </div>

        <div id="diseaseResult" class="hidden mt-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
          <div class="flex items-center justify-between mb-2">
            <div id="diseaseTitle" class="text-sm font-bold text-emerald-700">AI Pathology Diagnosis</div>
            <span id="diseaseConf" class="rounded-full bg-emerald-700 px-2.5 py-0.5 text-xs font-semibold text-white">94% match</span>
          </div>
          <div id="diseaseBody" class="text-sm whitespace-pre-wrap leading-relaxed"></div>
        </div>
      </div>

      <!-- Schemes Section -->
      <div id="sec-schemes" class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold">🏛️ Government Agricultural Schemes</h3>
            <p class="text-xs" style="color: var(--muted-fg);">Live from backend `/api/v1/schemes` — click "Ask AI" on any scheme for application steps in your language.</p>
          </div>
        </div>
        <div id="schemesGrid" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"></div>
      </div>

      <!-- Database & Conversation History Section -->
      <div id="sec-database" class="rounded-2xl border p-6 shadow-soft space-y-4" style="background: var(--card); border-color: var(--border);">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h3 class="text-lg font-semibold flex items-center gap-2">🗄️ Live Database Inspector (`conversation_states`)</h3>
            <p class="text-xs" style="color: var(--muted-fg);" id="dbSummaryLabel">Inspecting SQLAlchemy database sessions, extracted entities, and message history...</p>
          </div>
          <div class="flex gap-2">
            <button onclick="loadDatabaseSessions()" class="h-9 rounded-lg bg-emerald-700 text-white px-3 text-xs font-semibold cursor-pointer">↻ Refresh DB</button>
            <button onclick="clearCurrentSession()" class="h-9 rounded-lg bg-red-600 text-white px-3 text-xs font-semibold cursor-pointer">🗑️ Clear Session History</button>
          </div>
        </div>
        <div id="dbSessionsContainer" class="space-y-3 max-h-96 overflow-y-auto"></div>
      </div>

      <!-- Settings Section -->
      <div id="sec-settings" class="hidden rounded-2xl border p-6 shadow-soft" style="background: var(--card); border-color: var(--border);">
        <h3 class="text-lg font-semibold mb-2">⚙️ System Architecture & Settings</h3>
        <p class="text-xs mb-4" style="color: var(--muted-fg);">Full-Stack AgriAI Configuration & Live Endpoints</p>
        <div class="space-y-3 text-sm">
          <div class="flex items-center justify-between py-2 border-b" style="border-color: var(--border);">
            <span>Frontend Ports</span>
            <span class="font-mono text-xs">http://127.0.0.1:8080 | :5173 | :3000 | :8000/ui</span>
          </div>
          <div class="flex items-center justify-between py-2 border-b" style="border-color: var(--border);">
            <span>FastAPI Backend & Swagger Docs</span>
            <a href="http://127.0.0.1:8000/docs" target="_blank" class="text-emerald-600 font-semibold text-xs">http://127.0.0.1:8000/docs →</a>
          </div>
          <div class="flex items-center justify-between py-2 border-b" style="border-color: var(--border);">
            <span>Database Inspector API</span>
            <a href="http://127.0.0.1:8000/api/v1/db/sessions" target="_blank" class="text-emerald-600 font-semibold text-xs">http://127.0.0.1:8000/api/v1/db/sessions →</a>
          </div>
        </div>
      </div>
    </main>
  </div>

  <script>
    const API_BASE_URL = "http://127.0.0.1:8000";
    let lastSpokenText = "";
    let lastSpokenLang = "en-IN";

    function renderRoute(path) {
      const titles = {
        "/": "Dashboard",
        "/ui": "Dashboard",
        "/ask-ai": "Ask AI Advisory",
        "/voice": "Voice Assistant",
        "/weather": "Weather Intelligence",
        "/market": "Market Prices (APMC)",
        "/disease": "Crop Disease Diagnosis",
        "/schemes": "Government Schemes",
        "/database": "Database & Conversation History",
        "/settings": "Settings"
      };
      document.getElementById("pageTitle").textContent = titles[path] || "Dashboard";

      document.querySelectorAll(".nav-link").forEach(a => {
        const r = a.getAttribute("data-route");
        if (r === path || (path === "/ui" && r === "/")) {
          a.style.background = "var(--sidebar-accent)";
          a.style.color = "#fff";
        } else {
          a.style.background = "transparent";
          a.style.color = "rgba(235,245,238,0.75)";
        }
      });

      const showAll = (path === "/" || path === "/ui");
      document.getElementById("sec-hero").style.display = showAll ? "" : "none";
      document.getElementById("sec-stats").style.display = showAll ? "" : "none";
      document.getElementById("sec-ai-row").style.display = (showAll || path === "/ask-ai" || path === "/voice") ? "" : "none";
      document.getElementById("sec-ask-ai").style.display = (showAll || path === "/ask-ai") ? "" : "none";
      document.getElementById("sec-voice").style.display = (showAll || path === "/voice") ? "" : "none";
      document.getElementById("sec-weather-market-row").style.display = (showAll || path === "/weather" || path === "/market") ? "" : "none";
      document.getElementById("sec-weather").style.display = (showAll || path === "/weather") ? "" : "none";
      document.getElementById("sec-market").style.display = (showAll || path === "/market") ? "" : "none";
      document.getElementById("sec-disease").style.display = (showAll || path === "/disease") ? "" : "none";
      document.getElementById("sec-schemes").style.display = (showAll || path === "/schemes") ? "" : "none";
      document.getElementById("sec-database").style.display = (showAll || path === "/database" || path === "/ask-ai") ? "" : "none";
      document.getElementById("sec-settings").classList.toggle("hidden", path !== "/settings");
    }

    function navigate(e, path) {
      if (e) e.preventDefault();
      window.history.pushState({}, "", path);
      renderRoute(path);
      return false;
    }

    window.addEventListener("popstate", () => renderRoute(window.location.pathname));

    const TOPIC_QUESTIONS = {
      tomato: {
        "en-IN": "How to control pests, fruit borer, and leaf curl in tomato plants?",
        "ta-IN": "தக்காளி செடிகளில் பூச்சி மற்றும் இலை சுருட்டை நோயை கட்டுப்படுத்த என்ன தெளிக்க வேண்டும்?",
        "hi-IN": "टमाटर के पौधों में कीड़े और पत्ती मोड़क रोग के नियंत्रण के लिए क्या छिड़काव करें?",
        "te-IN": "టమోటా మొక్కలలో పురుగులు మరియు ఆకు ముడత నివారణకు ఏమి పిచికారీ చేయాలి?",
        "kn-IN": "ಟೊಮೆಟೊ ಗಿಡಗಳಲ್ಲಿ ಕೀಟ ಮತ್ತು ಎಲೆ ಮುರುಟು ರೋಗ ನಿಯಂತ್ರಣಕ್ಕೆ ಏನು ಸಿಂಪಡಿಸಬೇಕು?",
        "ml-IN": "തക്കാളി ചെടികളിലെ കീടങ്ങളെയും ഇല ചുരുളൽ രോഗത്തെയും നിയന്ത്രിക്കാൻ എന്ത് തളിക്കണം?"
      },
      paddy: {
        "en-IN": "What is the best NPK fertilizer schedule and micronutrient dosage for paddy / rice crop?",
        "ta-IN": "நெல் பயிருக்கு சிறந்த உரம் மற்றும் நுண்ணூட்டச்சத்து அட்டவணை என்ன?",
        "hi-IN": "धान की फसल के लिए सर्वोत्तम खाद और उर्वरक (NPK) की मात्रा और समय सारणी क्या है?",
        "te-IN": "వరి పంటకు సరైన ఎరువుల (NPK) యాజమాన్యం మరియు మోతాదు వివరాలు తెలపండి?",
        "kn-IN": "ಭತ್ತದ ಬೆಳೆಗೆ ಉತ್ತಮ ರಸಗೊಬ್ಬರ ಮತ್ತು ಪೋಷಕಾಂಶಗಳ ವೇಳಾಪಟ್ಟಿ ಯಾವುದು?",
        "ml-IN": "നെൽകൃഷിക്ക് ഏറ്റവും അനുയോജ്യമായ വളപ്രയോഗ രീതിയും അളവും എന്താണ്?"
      },
      blight: {
        "en-IN": "How to treat yellow leaves, fungal leaf spot, and blight in crops?",
        "ta-IN": "பயிர்களில் மஞ்சள் இலை மற்றும் இலை கருகல் நோயை குணப்படுத்துவது எப்படி?",
        "hi-IN": "फसलों में पीली पत्तियों और झुलसा रोग (ब्लाइट) का इलाज कैसे करें?",
        "te-IN": "పంటలలో ఆకులు పసుపు రంగులోకి మారడం మరియు ఆకు మచ్చ తెగులును ఎలా నివారించాలి?",
        "kn-IN": "ಬೆಳೆಗಳಲ್ಲಿ ಹಳದಿ ಎಲೆ ಮತ್ತು ಎಲೆ ಚುಕ್ಕೆ ರೋಗವನ್ನು ಹೇಗೆ ನಿಯಂತ್ರಿಸುವುದು?",
        "ml-IN": "വിളകളിലെ മഞ്ഞളിപ്പും ഇലപ്പുള്ളി രോഗവും എങ്ങനെ പരിഹരിക്കാം?"
      },
      scheme: {
        "en-IN": "How can farmers apply for PM-KISAN, PMFBY crop insurance, and Kisan Credit Card?",
        "ta-IN": "விவசாயிகள் பிஎம் கிசான் (PM-KISAN) மற்றும் பயிர் காப்பீட்டுத் திட்டத்திற்கு விண்ணப்பிப்பது எப்படி?",
        "hi-IN": "किसान पीएम-किसान (PM-KISAN), फसल बीमा और किसान क्रेडिट कार्ड के लिए आवेदन कैसे करें?",
        "te-IN": "రైతులు పీఎం కిసాన్ (PM-KISAN) మరియు పంటల బీమా పథకానికి ఎలా దరఖాస్తు చేసుకోవాలి?",
        "kn-IN": "ರೈತರು ಪಿಎಂ-ಕಿಸಾನ್ (PM-KISAN) ಮತ್ತು ಬೆಳೆ ವಿಮೆ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ?",
        "ml-IN": "കർഷകർക്ക് പി.എം-കിസാൻ (PM-KISAN), വിള ഇൻഷുറൻസ് പദ്ധതികൾക്ക് എങ്ങനെ അപേക്ഷിക്കാം?"
      }
    };

    function askSampleByTopic(topic) {
      const lang = document.getElementById("askLang").value || "en-IN";
      const qMap = TOPIC_QUESTIONS[topic] || TOPIC_QUESTIONS.tomato;
      document.getElementById("askInput").value = qMap[lang] || qMap["en-IN"];
      submitAskAI();
    }

    function onLangChange() {
      const lang = document.getElementById("askLang").value;
      const input = document.getElementById("askInput");
      const current = input.value.trim();
      let matchedTopic = null;
      for (const [tKey, tMap] of Object.entries(TOPIC_QUESTIONS)) {
        if (Object.values(tMap).includes(current)) {
          matchedTopic = tKey;
          break;
        }
      }
      if (!current || matchedTopic) {
        const useTopic = matchedTopic || "tomato";
        input.value = TOPIC_QUESTIONS[useTopic][lang] || TOPIC_QUESTIONS[useTopic]["en-IN"];
      }
      submitAskAI();
    }

    function escapeHtml(s) {
      return String(s || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }

    async function submitAskAI() {
      const inputEl = document.getElementById("askInput");
      const lang = document.getElementById("askLang").value;
      let text = inputEl.value.trim();
      if (!text) {
        text = TOPIC_QUESTIONS.tomato[lang] || TOPIC_QUESTIONS.tomato["en-IN"];
        inputEl.value = text;
      }
      const box = document.getElementById("askResponseBox");
      const btn = document.getElementById("askBtn");
      const badge = document.getElementById("askMetaBadge");
      btn.disabled = true;
      btn.textContent = "⏳ Generating Expert Advisory...";
      badge.textContent = "Consulting Groq AI...";
      box.innerHTML = `<div class="animate-pulse font-medium text-emerald-700">⏳ Analyzing your farming question and generating detailed advisory in ${lang}...</div>`;
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/query/text`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: "session_web_client",
            text: text,
            preferred_language: lang
          })
        });
        const data = await res.json();
        const reply = data.translated_response || data.canonical_response || "Advisory generated.";
        lastSpokenText = reply;
        lastSpokenLang = lang;
        const showEnglishSub = !lang.startsWith("en") && data.canonical_response && data.canonical_response !== reply;
        const entitiesStr = data.extracted_agricultural_entities ? Object.entries(data.extracted_agricultural_entities).map(([k,v]) => `${k}: ${v}`).join(" · ") : "";
        badge.textContent = `Intent: ${data.inferred_intent || 'CROP_ADVISORY'} | Lang: ${data.detected_language || lang}`;
        box.innerHTML =
          `<div class="flex flex-wrap items-center gap-2 mb-3 pb-2 border-b" style="border-color: var(--border);">` +
            `<span class="rounded-md bg-emerald-600 text-white px-2 py-0.5 text-xs font-semibold">${escapeHtml(data.inferred_intent || 'CROP_ADVISORY')}</span>` +
            `<span class="rounded-md bg-sky-600/15 text-sky-700 px-2 py-0.5 text-xs font-semibold">${escapeHtml(data.detected_language || lang)}</span>` +
            (entitiesStr ? `<span class="text-xs opacity-75">(${escapeHtml(entitiesStr)})</span>` : "") +
          `</div>` +
          `<div class="text-base leading-relaxed font-medium">${escapeHtml(reply)}</div>` +
          (showEnglishSub ? `<div class="mt-4 pt-3 border-t text-xs opacity-85" style="border-color: var(--border);"><strong>English Reference Advisory:</strong>\n${escapeHtml(data.canonical_response)}</div>` : "");
        loadDatabaseSessions();
      } catch (err) {
        box.textContent = "Error connecting to backend: " + err;
      } finally {
        btn.disabled = false;
        btn.textContent = "🚀 Ask AI (Get Instant Answer)";
      }
    }

    function speakCurrentAnswer() {
      if (!("speechSynthesis" in window)) {
        alert("Speech synthesis is not supported in this browser.");
        return;
      }
      window.speechSynthesis.cancel();
      const textToRead = lastSpokenText || document.getElementById("askResponseBox").innerText;
      const utter = new SpeechSynthesisUtterance(textToRead);
      utter.lang = lastSpokenLang || document.getElementById("askLang").value || "en-IN";
      window.speechSynthesis.speak(utter);
    }

    function quickWeather(city) {
      document.getElementById("weatherCityInput").value = city;
      loadWeather();
    }

    async function loadWeather() {
      const city = document.getElementById("weatherCityInput").value.trim() || "Bengaluru";
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/weather?location=${encodeURIComponent(city)}`);
        const data = await res.json();
        if (data && data.temperature !== undefined) {
          document.getElementById("weatherLocationLabel").textContent = `📍 ${city}, India`;
          document.getElementById("weatherTemp").textContent = `${Math.round(data.temperature)}°C`;
          document.getElementById("weatherCond").textContent = data.weather;
          document.getElementById("weatherHum").textContent = `${Math.round(data.humidity)}%`;
          document.getElementById("weatherRain").textContent = `${data.rainfall} mm`;
          const sprayEl = document.getElementById("weatherSprayTip");
          if (Number(data.rainfall) > 2 || Number(data.humidity) > 88) {
            sprayEl.textContent = "Avoid spraying (Rain/High Hum)";
            sprayEl.className = "mt-1 text-xs font-semibold text-amber-600";
          } else {
            sprayEl.textContent = "Good window for foliar spray";
            sprayEl.className = "mt-1 text-xs font-semibold text-emerald-600";
          }
        }
      } catch (e) {}
    }

    function renderMandiRow(item) {
      const isPos = !String(item.trend || "+1.5%").startsWith("-");
      return `<tr class="border-t" style="border-color: var(--border);">
        <td class="py-2.5 font-semibold">${escapeHtml(item.crop)}</td>
        <td class="py-2.5 text-xs" style="color: var(--muted-fg);">${escapeHtml(item.market)} (${escapeHtml(item.state || '')})</td>
        <td class="py-2.5 text-right font-semibold">₹${Number(item.price).toLocaleString()} <span class="text-[11px] font-normal">/qtl</span></td>
        <td class="py-2.5 text-right font-semibold ${isPos ? 'text-emerald-600' : 'text-red-600'}">${escapeHtml(item.trend || '+1.8%')}</td>
      </tr>`;
    }

    async function loadAllMandiPrices() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/mandi-prices/all`);
        const data = await res.json();
        if (data && Array.isArray(data.items)) {
          document.getElementById("marketTableBody").innerHTML = data.items.map(renderMandiRow).join("");
        }
      } catch (e) {}
    }

    async function lookupCustomMandiPrice() {
      const crop = document.getElementById("mandiCropInput").value.trim() || "Tomato";
      const state = document.getElementById("mandiStateInput").value.trim() || "Karnataka";
      const dist = document.getElementById("mandiDistInput").value.trim() || "Kolar";
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/mandi-prices?crop=${encodeURIComponent(crop)}&state=${encodeURIComponent(state)}&district=${encodeURIComponent(dist)}`);
        const item = await res.json();
        if (item && item.price !== undefined) {
          const tbody = document.getElementById("marketTableBody");
          tbody.innerHTML = renderMandiRow(item) + tbody.innerHTML;
        }
      } catch (e) {}
    }

    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;

    async function toggleRecording() {
      const status = document.getElementById("voiceStatus");
      const sub = document.getElementById("voiceSubStatus");
      const btn = document.getElementById("micBtn");
      if (!isRecording) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          audioChunks = [];
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };
          mediaRecorder.onstop = async () => {
            stream.getTracks().forEach(t => t.stop());
            const blob = new Blob(audioChunks, { type: "audio/webm" });
            await sendAudioBlob(blob, "farmer_voice.webm");
          };
          mediaRecorder.start();
          isRecording = true;
          btn.textContent = "⏹️";
          status.textContent = "Recording Live Audio...";
          sub.textContent = "Speak your farming question, then click Stop.";
        } catch (err) {
          status.textContent = "Mic Permission Needed — Running Voice Demo";
          sub.textContent = "Simulating voice query automatically...";
          await simulateVoiceAudioQuery();
        }
      } else {
        mediaRecorder.stop();
        isRecording = false;
        btn.textContent = "🎙️";
      }
    }

    async function uploadSelectedAudioFile() {
      const input = document.getElementById("audioFileInput");
      if (input.files && input.files[0]) {
        await sendAudioBlob(input.files[0], input.files[0].name);
      }
    }

    function createDemoWavBlob() {
      const sampleRate = 8000;
      const numSamples = 4000;
      const buffer = new ArrayBuffer(44 + numSamples * 2);
      const view = new DataView(buffer);
      const writeStr = (off, s) => { for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i)); };
      writeStr(0, "RIFF");
      view.setUint32(4, 36 + numSamples * 2, true);
      writeStr(8, "WAVE");
      writeStr(12, "fmt ");
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true);
      view.setUint16(22, 1, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * 2, true);
      view.setUint16(32, 2, true);
      view.setUint16(34, 16, true);
      writeStr(36, "data");
      view.setUint32(40, numSamples * 2, true);
      return new Blob([buffer], { type: "audio/wav" });
    }

    async function simulateVoiceAudioQuery() {
      const wavBlob = createDemoWavBlob();
      await sendAudioBlob(wavBlob, "demo_farmer_question.wav");
    }

    async function sendAudioBlob(blob, filename) {
      const status = document.getElementById("voiceStatus");
      const sub = document.getElementById("voiceSubStatus");
      const resCard = document.getElementById("voiceResultCard");
      const lang = document.getElementById("voiceLang").value;
      status.textContent = "⏳ Processing Voice Query...";
      sub.textContent = `Transcribing & generating ${lang} advisory...`;
      resCard.textContent = "⏳ Sending audio to /api/v1/query/audio...";
      const fd = new FormData();
      fd.append("session_id", "session_web_client");
      fd.append("language_code", lang);
      fd.append("file", blob, filename);
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/query/audio`, { method: "POST", body: fd });
        const data = await res.json();
        const reply = data.translated_response || data.canonical_response || data.detail || "Processed!";
        status.textContent = "✅ Voice Advisory Ready!";
        sub.textContent = `Detected: ${data.detected_language || lang} | Intent: ${data.inferred_intent || 'CROP_ADVISORY'}`;
        resCard.innerHTML = `<strong>Transcribed Query:</strong> ${escapeHtml(data.canonical_query || '')}\n\n<strong>AI Response:</strong>\n${escapeHtml(reply)}`;
        document.getElementById("askLang").value = lang;
        document.getElementById("askResponseBox").innerHTML =
          `<div class="font-semibold text-emerald-600 mb-2">🎙️ Voice Query (${escapeHtml(lang)}) · Intent: ${escapeHtml(data.inferred_intent || 'CROP_ADVISORY')}</div>` +
          `<div class="text-base leading-relaxed">${escapeHtml(reply)}</div>`;
        lastSpokenText = reply;
        lastSpokenLang = lang;
        loadDatabaseSessions();
      } catch (e) {
        status.textContent = "Upload Error";
        sub.textContent = String(e);
      }
    }

    let selectedLeafFileName = "tomato_leaf_sample.jpg";
    function previewLeaf(e) {
      const file = e.target.files?.[0];
      if (!file) return;
      selectedLeafFileName = file.name;
      document.getElementById("leafFileName").textContent = `Selected: ${file.name}`;
      const img = document.getElementById("leafPreview");
      img.src = URL.createObjectURL(file);
      img.classList.remove("hidden");
    }

    async function analyzeLeaf() {
      const crop = document.getElementById("diseaseCrop").value.trim() || "Tomato";
      const symptoms = document.getElementById("diseaseSymptoms").value.trim() || "Yellowing leaves with brown spots";
      const lang = document.getElementById("diseaseLang").value || "en-IN";
      const btn = document.getElementById("diseaseBtn");
      const box = document.getElementById("diseaseResult");
      const body = document.getElementById("diseaseBody");
      btn.disabled = true;
      btn.textContent = "⏳ Running AI Pathology Diagnosis...";
      box.classList.remove("hidden");
      body.textContent = "⏳ Consulting AI plant pathologist for diagnosis and treatment dosages...";
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/disease/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: "session_web_client",
            crop: crop,
            symptoms: symptoms,
            preferred_language: lang,
            image_name: selectedLeafFileName
          })
        });
        const data = await res.json();
        document.getElementById("diseaseTitle").textContent = data.diagnosis || `${crop} Disease Analysis`;
        document.getElementById("diseaseConf").textContent = `${data.confidence || '94%'} AI Match`;
        body.textContent = data.advisory || data.canonical_advisory || "Diagnosis complete.";
        loadDatabaseSessions();
      } catch (e) {
        body.textContent = "Error analyzing disease: " + e;
      } finally {
        btn.disabled = false;
        btn.textContent = "🔍 Run AI Disease Diagnosis";
      }
    }

    async function loadSchemes() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/schemes`);
        const data = await res.json();
        const grid = document.getElementById("schemesGrid");
        if (data && Array.isArray(data.schemes)) {
          grid.innerHTML = data.schemes.map(s => `
            <div class="rounded-2xl border p-5 shadow-soft flex flex-col justify-between" style="background: var(--card); border-color: var(--border);">
              <div>
                <span class="rounded-full bg-emerald-100 text-emerald-800 px-2.5 py-0.5 text-[10px] font-semibold uppercase">${escapeHtml(s.category)}</span>
                <div class="mt-3 text-base font-bold">${escapeHtml(s.title)}</div>
                <p class="mt-1.5 text-xs leading-relaxed" style="color: var(--muted-fg);"><strong>Benefit:</strong> ${escapeHtml(s.benefit)}</p>
                <p class="mt-1 text-xs leading-relaxed" style="color: var(--muted-fg);"><strong>Eligibility:</strong> ${escapeHtml(s.eligibility)}</p>
              </div>
              <div class="mt-4 pt-3 border-t flex items-center justify-between gap-2" style="border-color: var(--border);">
                <a href="${escapeHtml(s.portal)}" target="_blank" class="text-xs font-semibold text-emerald-700 hover:underline">Official Portal ↗</a>
                <button onclick="askAboutScheme('${escapeHtml(s.title)}')" class="rounded-lg bg-emerald-700 text-white px-2.5 py-1 text-xs font-semibold cursor-pointer">Ask AI How to Apply</button>
              </div>
            </div>
          `).join("");
        }
      } catch (e) {}
    }

    function askAboutScheme(schemeTitle) {
      navigate(null, "/ask-ai");
      document.getElementById("askInput").value = `Explain eligibility, documents required, and step-by-step application process for ${schemeTitle}.`;
      submitAskAI();
    }

    async function loadDatabaseSessions() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/db/sessions`);
        const data = await res.json();
        if (!data) return;
        document.getElementById("statTotalMsgs").textContent = data.total_messages || 0;
        document.getElementById("statTotalSessions").textContent = `${data.total_sessions || 0} sessions in ${data.table || 'conversation_states'}`;
        document.getElementById("sidebarDbBadge").textContent = `Database: ${data.total_messages || 0} msgs stored`;
        document.getElementById("dbSummaryLabel").textContent =
          `Engine: ${data.database_engine} | Table: ${data.table} | Sessions: ${data.total_sessions} | Total Stored Messages: ${data.total_messages}`;

        const container = document.getElementById("dbSessionsContainer");
        if (!data.sessions || data.sessions.length === 0) {
          container.innerHTML = `<div class="rounded-xl border p-4 text-xs" style="background: var(--muted); border-color: var(--border);">No sessions recorded yet. Ask a question above to create a database entry!</div>`;
          return;
        }
        container.innerHTML = data.sessions.map(s => {
          const msgsHtml = (s.conversation_history || []).slice(-8).map(m => `
            <div class="rounded-lg p-2.5 text-xs ${m.role === 'user' ? 'bg-sky-500/10 border border-sky-500/20' : 'bg-emerald-500/10 border border-emerald-500/20'}">
              <div class="font-bold uppercase text-[10px] mb-0.5 ${m.role === 'user' ? 'text-sky-700' : 'text-emerald-700'}">${escapeHtml(m.role)} · ${escapeHtml(m.timestamp || '')}</div>
              <div class="whitespace-pre-wrap">${escapeHtml(m.content)}</div>
            </div>
          `).join("");
          return `
            <div class="rounded-xl border p-4 space-y-2" style="background: var(--muted); border-color: var(--border);">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="text-xs font-bold">Session ID: <span class="font-mono text-emerald-700">${escapeHtml(s.session_id)}</span></div>
                <div class="text-[11px]" style="color: var(--muted-fg);">Lang: <strong>${escapeHtml(s.preferred_language)}</strong> | Messages: <strong>${s.message_count}</strong> | Context: <code>${escapeHtml(JSON.stringify(s.context || {}))}</code></div>
              </div>
              <div class="space-y-1.5 pt-1">${msgsHtml || '<div class="text-xs opacity-60">Empty history</div>'}</div>
            </div>
          `;
        }).join("");
      } catch (e) {}
    }

    async function clearCurrentSession() {
      try {
        await fetch(`${API_BASE_URL}/api/v1/db/sessions/session_web_client`, { method: "DELETE" });
        loadDatabaseSessions();
      } catch (e) {}
    }

    renderRoute(window.location.pathname);
    loadWeather();
    loadAllMandiPrices();
    loadSchemes();
    loadDatabaseSessions();
    submitAskAI();
  </script>
</body>
</html>
"""

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_frontend(full_path: str):
    return FRONTEND_HTML
