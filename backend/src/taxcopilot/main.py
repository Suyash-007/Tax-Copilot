"""FastAPI application. Run with `make dev`; it binds to 127.0.0.1 only."""

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from taxcopilot import __version__
from taxcopilot.api import health


def create_app() -> FastAPI:
    app = FastAPI(
        title="Tax Copilot",
        version=__version__,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    # Reject requests whose Host is not loopback (guards against DNS-rebinding from a web page).
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])
    app.include_router(health.router, prefix="/api")
    return app


app = create_app()
