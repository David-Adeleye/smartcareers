"""FastAPI application entry point."""

from fastapi import FastAPI

from smartcareers_api.api.routes.health import router as health_router
from smartcareers_api.config import get_settings


def create_app() -> FastAPI:
    """Create and configure the SmartCareers API application."""

    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        description="Explainable, evidence-grounded career intelligence API.",
    )

    application.include_router(
        health_router,
        prefix="/api/v1",
    )

    return application


app = create_app()
