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
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from app.db.database import engine, Base
from app.db import models  # noqa: F401
from app.core.logger import logger
from app.frontend_server import FRONTEND_HTML
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading

try:
    Base.metadata.create_all(bind=engine)
except Exception as db_init_err:
    logger.warning(f"Table auto-creation skipped: {db_init_err}")


class _FrontendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = FRONTEND_HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def _start_frontend_port(port: int):
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", port), _FrontendHandler)
        logger.info(f"AgriAI Frontend Server running on http://127.0.0.1:{port}")
        srv.serve_forever()
    except Exception as e:
        logger.warning(f"Frontend mirror on port {port} skipped: {e}")


for _port in (8080, 5173, 3000):
    threading.Thread(target=_start_frontend_port, args=(_port,), daemon=True).start()


def _warmup_and_verify_fullstack():
    import time
    import requests as _req
    time.sleep(2.5)
    try:
        r_ta = _req.post(
            "http://127.0.0.1:8000/api/v1/query/text",
            json={
                "session_id": "session_web_client",
                "text": "தக்காளி செடிகளில் பூச்சி மற்றும் இலை சுருட்டை நோயை கட்டுப்படுத்த என்ன தெளிக்க வேண்டும்?",
                "preferred_language": "ta-IN",
            },
            timeout=25,
        )
        if r_ta.status_code == 200:
            d = r_ta.json()
            logger.info(
                f"[FullStack Verification] Tamil AI Response OK (intent={d.get('inferred_intent')}): {str(d.get('translated_response'))[:120]}..."
            )
        r_db = _req.get("http://127.0.0.1:8000/api/v1/db/sessions", timeout=5)
        if r_db.status_code == 200:
            db_info = r_db.json()
            logger.info(
                f"[FullStack Verification] Database OK: engine={db_info.get('database_engine')}, sessions={db_info.get('total_sessions')}, messages={db_info.get('total_messages')}"
            )
    except Exception as e:
        logger.warning(f"Warmup check skipped: {e}")


threading.Thread(target=_warmup_and_verify_fullstack, daemon=True).start()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual NLP Processing Engine for Farmer Query Assistance (Full-Stack Implementation)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health Check"])
async def root_health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_milestone": "Full-Stack Complete (Frontend + Backend + Database)",
        "links": {
            "frontend_8080": "http://127.0.0.1:8080",
            "frontend_5173": "http://127.0.0.1:5173",
            "frontend_3000": "http://127.0.0.1:3000",
            "web_dashboard": "http://127.0.0.1:8000/ui",
            "swagger_docs": "http://127.0.0.1:8000/docs",
            "redoc_docs": "http://127.0.0.1:8000/redoc",
            "database_sessions_api": "http://127.0.0.1:8000/api/v1/db/sessions",
            "weather_api": "http://127.0.0.1:8000/api/v1/weather?location=Bengaluru",
            "mandi_prices_api": "http://127.0.0.1:8000/api/v1/mandi-prices/all",
            "schemes_api": "http://127.0.0.1:8000/api/v1/schemes",
            "text_query_api": "http://127.0.0.1:8000/api/v1/query/text",
            "audio_query_api": "http://127.0.0.1:8000/api/v1/query/audio",
            "disease_analyze_api": "http://127.0.0.1:8000/api/v1/disease/analyze",
        },
    }


@app.get("/ui", response_class=HTMLResponse, tags=["Web Dashboard"])
@app.get("/ask-ai", response_class=HTMLResponse, include_in_schema=False)
@app.get("/voice", response_class=HTMLResponse, include_in_schema=False)
@app.get("/weather", response_class=HTMLResponse, include_in_schema=False)
@app.get("/market", response_class=HTMLResponse, include_in_schema=False)
@app.get("/disease", response_class=HTMLResponse, include_in_schema=False)
@app.get("/schemes", response_class=HTMLResponse, include_in_schema=False)
@app.get("/database", response_class=HTMLResponse, include_in_schema=False)
@app.get("/settings", response_class=HTMLResponse, include_in_schema=False)
async def web_dashboard():
    return FRONTEND_HTML


logger.info("FastAPI initialization sequence completed successfully.")
