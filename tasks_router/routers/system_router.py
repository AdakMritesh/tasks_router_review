"""
System endpoints for health checks and root welcome message.
"""

import structlog
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from tasks_router.dependencies import database

router: APIRouter = APIRouter(tags=["System"])
logger = structlog.get_logger(__name__)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Endpoint to check the health status of the service."""
    logger.debug("system.health_check")
    return {
        "service": "tasks-api",
        "status": "healthy"
        }

@router.get("/health/db", response_class=JSONResponse)
def health_check_db() -> JSONResponse:
    """Endpoint to check database reachability."""
    logger.debug("system.health_check_db")
    if database.ping_database():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "healthy", "database": "reachable"},
        )
    else:
        logger.error("system.health_check_db.failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "unreachable"},
        )

@router.get("/", status_code=status.HTTP_200_OK)
async def root() -> dict[str, str | dict[str, str]]:
    """Endpoint to provide a welcome message and list available endpoints."""
    logger.debug("system.root")
    return {
        "message": "Welcome to the Tasks API!",
        "endpoints": {
            "/tasks": "Manage tasks (CRUD operations)",
            "/health": "Check the health status of the service",
            "/health/db": "Check database reachability",
            "/docs": "API documentation (Swagger UI)",
            "/redoc": "API documentation (ReDoc)"
        }
    }
