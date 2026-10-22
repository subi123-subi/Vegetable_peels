import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.api import api_router
import app.db.base  # noqa: F401 - Register all SQLAlchemy mappers

# Configure structured logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("smart_peel_ai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up %s v%s in %s mode...", settings.PROJECT_NAME, settings.VERSION, settings.ENVIRONMENT)
    yield
    logger.info("Shutting down %s...", settings.PROJECT_NAME)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Vegetable Peel Nutrient Identification and Food Waste Valorization System API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://.*$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled Exception: %s for request %s %s", str(exc), request.method, request.url, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please contact system administrator if this persists.",
            "path": str(request.url.path),
        },
    )


import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Locate web directory (HTML, CSS, JS, Images)
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web"))

if os.path.exists(web_dir):
    css_dir = os.path.join(web_dir, "css")
    js_dir = os.path.join(web_dir, "js")
    img_dir = os.path.join(web_dir, "images")

    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="web_css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="web_js")
    if os.path.exists(img_dir):
        app.mount("/images", StaticFiles(directory=img_dir), name="web_images")
    app.mount("/static", StaticFiles(directory=web_dir), name="web_static")

    @app.get("/", summary="Smart Peel Analyzer Professional Web Application")
    async def serve_index(request: Request):
        index_file = os.path.join(web_dir, "index.html")
        accept = request.headers.get("accept", "")
        if "application/json" in accept and "text/html" not in accept:
            return {
                "message": f"Welcome to {settings.PROJECT_NAME} API",
                "version": settings.VERSION,
                "docs_url": f"{settings.API_V1_STR}/docs",
                "health_check": f"{settings.API_V1_STR}/health",
            }
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"error": "index.html not found"}

    @app.get("/kiosk", summary="Direct Kiosk HTML Endpoint")
    async def serve_kiosk():
        index_file = os.path.join(web_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Kiosk file not found"}
else:
    @app.get("/", summary="Root Endpoint")
    async def root():
        return {
            "message": f"Welcome to {settings.PROJECT_NAME} API",
            "version": settings.VERSION,
            "docs_url": f"{settings.API_V1_STR}/docs",
            "health_check": f"{settings.API_V1_STR}/health",
        }


# API Info endpoint
@app.get("/api", summary="API Overview")
async def api_info():
    return {
        "message": f"{settings.PROJECT_NAME} REST API",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_check": f"{settings.API_V1_STR}/health",
    }


# Health check alias at root level
@app.get("/health", summary="Root Health Check Alias")
async def root_health():
    from app.api.v1.endpoints.health import health_check
    return await health_check()

