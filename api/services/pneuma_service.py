import asyncio
import json
import time
from typing import Dict, Any, List, Optional
import structlog

from ..config import settings
from ..models.requests import QueryRequest
from ..models.responses import QueryResponse, TableInfo

logger = structlog.get_logger()


class PneumaService:
    """Service for interacting with Pneuma core functionality"""

    def __init__(self):
        self.pneuma = None
        self.initialized = False

    async def initialize(self):
        """Initialize Pneuma instance"""
        try:
            logger.info("Initializing Pneuma service...")

            # Import Pneuma here to avoid import issues during module load
            from src.pneuma import Pneuma

            self.pneuma = Pneuma(
                out_path=settings.pneuma_storage_path,
                llm_path=settings.pneuma_llm_path,
                embed_path=settings.pneuma_embed_path,
            )

            # Run setup in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.pneuma.setup)

            self.initialized = True
            logger.info("Pneuma service initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize Pneuma service", error=str(e))
            raise

    async def query_tables(self, request: QueryRequest) -> QueryResponse:
        """Query tables using Pneuma"""
        if not self.initialized:
            raise RuntimeError("Pneuma service not initialized")

        start_time = time.time()

        try:
            logger.info("Executing Pneuma query", query=request.query, k=request.k)

            # Run Pneuma query in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response_str = await loop.run_in_executor(
                None,
                self.pneuma.query_index,
                request.index_name,
                request.query,
                request.k,
                request.n,
                request.alpha,
            )

            # Parse Pneuma response
            response_data = json.loads(response_str)
            search_time = (time.time() - start_time) * 1000  # Convert to ms

            # Convert to our response format
            tables = self._convert_pneuma_response(response_data)

            return QueryResponse(
                query=request.query,
                session_id=request.session_id,
                results=tables,
                total_results=len(tables),
                search_time_ms=search_time,
                timestamp=time.time(),
            )

        except Exception as e:
            logger.error("Pneuma query failed", error=str(e), query=request.query)
            raise

    def _convert_pneuma_response(
        self, response_data: Dict[str, Any]
    ) -> List[TableInfo]:
        """Convert Pneuma response to our TableInfo format"""
        tables = []

        if "data" in response_data and "response" in response_data["data"]:
            for table_data in response_data["data"]["response"]:
                table_info = TableInfo(
                    table_id=table_data.get("table_id", "unknown"),
                    table_name=table_data.get("table_name", "Unknown Table"),
                    description=table_data.get("description"),
                    relevance_score=table_data.get("relevance_score"),
                    row_count=table_data.get("row_count"),
                    column_count=table_data.get("column_count"),
                    schema=table_data.get("schema", []),
                    sample_data=table_data.get("sample_data", []),
                    metadata=table_data.get("metadata", {}),
                )
                tables.append(table_info)

        return tables

    async def get_available_indexes(self) -> List[str]:
        """Get list of available indexes"""
        # This would need to be implemented based on Pneuma's actual API
        return ["default", "chicago_data", "demo_index"]

    async def get_table_details(self, table_id: str) -> Optional[TableInfo]:
        """Get detailed information about a specific table"""
        # This would need to be implemented based on Pneuma's actual API
        return None

    def is_healthy(self) -> bool:
        """Check if Pneuma service is healthy"""
        return self.initialized and self.pneuma is not None
