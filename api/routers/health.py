from fastapi import APIRouter, Depends
from datetime import datetime
import structlog

from ..models.responses import HealthResponse
from ..services.pneuma_service import PneumaService
from ..services.session_service import SessionService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(
    pneuma_service: PneumaService = Depends(),
    session_service: SessionService = Depends(),
):
    """Health check endpoint"""

    # Check Pneuma service
    pneuma_status = "healthy" if pneuma_service.is_healthy() else "unhealthy"

    # Check Redis connection
    redis_status = "healthy"
    try:
        if session_service.redis:
            await session_service.redis.ping()
    except:
        redis_status = "unhealthy"

    overall_status = (
        "healthy"
        if all([pneuma_status == "healthy", redis_status == "healthy"])
        else "unhealthy"
    )

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version="0.1.0",
        pneuma_status=pneuma_status,
        redis_status=redis_status,
    )


@router.get("/health/pneuma")
async def pneuma_health(pneuma_service: PneumaService = Depends()):
    """Detailed Pneuma service health"""
    return {
        "status": "healthy" if pneuma_service.is_healthy() else "unhealthy",
        "initialized": pneuma_service.initialized,
        "timestamp": datetime.utcnow(),
    }
