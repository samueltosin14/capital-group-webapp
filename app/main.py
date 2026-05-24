from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.seed import seed_data
from app.db.session import Base, SessionLocal, engine
from app.routers import admin, api, public


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)

    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, https_only=settings.session_cookie_secure, same_site="lax")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

    app.include_router(public.router)
    app.include_router(api.router, prefix="/api")
    app.include_router(admin.router, prefix="/admin")

    @app.middleware("http")
    async def secure_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

    @app.on_event("startup")
    def startup() -> None:
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            seed_data(db)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    def ready() -> JSONResponse:
        try:
            with engine.connect() as connection:
                connection.exec_driver_sql("SELECT 1")
            return JSONResponse({"status": "ready"})
        except Exception as exc:
            return JSONResponse({"status": "not_ready", "detail": str(exc)}, status_code=503)

    return app


app = create_app()
