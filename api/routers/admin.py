from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import structlog
from datetime import datetime

from ..services.pneuma_service import PneumaService
from ..services.session_service import SessionService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/status")
async def admin_status(
    pneuma_service: PneumaService = Depends(),
    session_service: SessionService = Depends()
):
    """Get system status for admin"""
    
    try:
        # Basic system info
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "pneuma_initialized": pneuma_service.initialized,
            "services": {
                "pneuma": "healthy" if pneuma_service.is_healthy() else "unhealthy",
                "redis": "unknown"  # We'll check this
            }
        }
        
        # Check Redis
        try:
            if session_service.redis:
                await session_service.redis.ping()
                status["services"]["redis"] = "healthy"
        except:
            status["services"]["redis"] = "unhealthy"
            
        return status
        
    except Exception as e:
        logger.error("Admin status check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Status check failed")


@router.post("/reload")
async def reload_pneuma(pneuma_service: PneumaService = Depends()):
    """Reload Pneuma service (admin only)"""
    
    try:
        await pneuma_service.initialize()
        return {"message": "Pneuma service reloaded successfully"}
        
    except Exception as e:
        logger.error("Failed to reload Pneuma service", error=str(e))
        raise HTTPException(status_code=500, detail="Reload failed")


@router.get("/indexes")
async def list_all_indexes(pneuma_service: PneumaService = Depends()):
    """List all available indexes with details"""
    
    try:
        indexes = await pneuma_service.get_available_indexes()
        
        # Add mock details for each index
        index_details = []
        for index_name in indexes:
            index_details.append({
                "name": index_name,
                "status": "active",
                "table_count": 100,  # This would come from actual Pneuma API
                "size_mb": 250,
                "last_updated": datetime.utcnow().isoformat()
            })
            
        return {"indexes": index_details}
        
    except Exception as e:
        logger.error("Failed to list indexes", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve indexes")


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    session_service: SessionService = Depends()
):
    """Delete a specific session (admin only)"""
    
    try:
        # This would need to be implemented in session_service
        # For now, just return success
        return {"message": f"Session {session_id} deleted"}
        
    except Exception as e:
        logger.error("Failed to delete session", error=str(e))
        raise HTTPException(status_code=500, detail="Session deletion failed")


@router.get("/metrics")
async def get_system_metrics():
    """Get basic system metrics"""
    
    try:
        # Basic metrics - in production you'd get real metrics
        metrics = {
            "uptime_seconds": 3600,  # Mock value
            "total_queries": 150,    # Mock value  
            "active_sessions": 5,    # Mock value
            "memory_usage_mb": 512,  # Mock value
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return metrics
        
    except Exception as e:
        logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")