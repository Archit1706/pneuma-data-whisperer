from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import structlog

from ..models.requests import QueryRequest
from ..models.responses import QueryResponse
from ..services.pneuma_service import PneumaService
from ..services.session_service import SessionService

logger = structlog.get_logger()
router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_tables(
    request: QueryRequest,
    pneuma_service: PneumaService = Depends(),
    session_service: SessionService = Depends()
):
    """Query Pneuma for relevant tables based on natural language"""
    
    try:
        # Execute query
        response = await pneuma_service.query_tables(request)
        
        # Store in session if session_id provided
        if request.session_id:
            await session_service.add_query_to_session(
                request.session_id,
                request.query,
                response
            )
        
        logger.info(
            "Query executed successfully",
            query=request.query,
            results_count=len(response.results),
            search_time=response.search_time_ms
        )
        
        return response
        
    except Exception as e:
        logger.error("Query execution failed", error=str(e), query=request.query)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@router.get("/query/session/{session_id}")
async def get_session_queries(
    session_id: str,
    session_service: SessionService = Depends()
):
    """Get query history for a session"""
    
    try:
        history = await session_service.get_session_history(session_id)
        return {"session_id": session_id, "queries": history}
        
    except Exception as e:
        logger.error("Failed to retrieve session history", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve session history")