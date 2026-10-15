from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.core.config import get_settings
from app.core.database import Base, engine
from app.api.v1.router import api_router

# Routers الويب
from app.web.routes import public as web_public
from app.web.routes import auth as web_auth
from app.web.routes import dashboard as web_dashboard
from app.web.routes import menus as web_menus
from app.web.routes import items as web_items

from app.models import Menu, MenuItem, User  # noqa

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
settings.static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# API
app.include_router(api_router)

# Web UI (Jinja2)
app.include_router(web_public.router)
app.include_router(web_auth.router)
app.include_router(web_dashboard.router)
app.include_router(web_menus.router)
app.include_router(web_items.router)


@app.get("/", tags=["Root"])
def root():
    return RedirectResponse(url="/menu")


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}