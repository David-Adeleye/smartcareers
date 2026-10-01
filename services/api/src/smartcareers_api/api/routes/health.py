"""Operational health endpoint."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from smartcareers_api.config import Settings, get_settings

router = APIRouter(tags=["operations"])

SettingsDependency = Annotated[Settings, Depends(get_settings)]


class HealthResponse(BaseModel):
    """Response returned when the API is healthy."""

    status: Literal["ok"]
    service: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
def health(settings: SettingsDependency) -> HealthResponse:
    """Confirm that the API is available to receive requests."""

    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.api_version,
        environment=settings.environment,
    )