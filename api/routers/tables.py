from fastapi import APIRouter, HTTPException, Depends
from typing import List
import structlog

from ..models.requests import TableDetailsRequest
from ..models.responses import IndexListResponse
from ..services.pneuma_service import PneumaService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/indexes", response_model=IndexListResponse)
async def list_indexes(pneuma_service: PneumaService = Depends()):
    """List available Pneuma indexes"""
    try:
        indexes = await pneuma_service.get_available_indexes()

        # Mock index info (implement based on actual Pneuma API)
        index_list = []
        for index_name in indexes:
            index_list.append(
                {
                    "name": index_name,
                    "table_count": 100 if index_name == "default" else 50,
                    "created_at": "2024-01-01T00:00:00Z",
                    "last_updated": "2024-01-15T00:00:00Z",
                }
            )

        return IndexListResponse(indexes=index_list, default_index="default")

    except Exception as e:
        logger.error("Failed to list indexes", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve indexes")


@router.get("/table/{table_id}")
async def get_table_details(
    table_id: str,
    include_sample_data: bool = True,
    sample_size: int = 10,
    pneuma_service: PneumaService = Depends(),
):
    """Get detailed information about a specific table"""
    try:
        table_info = await pneuma_service.get_table_details(table_id)

        if not table_info:
            raise HTTPException(status_code=404, detail="Table not found")

        return table_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get table details", error=str(e), table_id=table_id)
        raise HTTPException(status_code=500, detail="Failed to retrieve table details")
