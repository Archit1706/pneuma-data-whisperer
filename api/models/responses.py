from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class TableInfo(BaseModel):
    table_id: str
    table_name: str
    description: Optional[str] = None
    relevance_score: Optional[float] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    schema: Optional[List[Dict[str, Any]]] = None
    sample_data: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query: str
    session_id: Optional[str] = None
    results: List[TableInfo]
    total_results: int
    search_time_ms: float
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    pneuma_status: str
    redis_status: str


class IndexInfo(BaseModel):
    name: str
    table_count: int
    created_at: datetime
    last_updated: datetime


class IndexListResponse(BaseModel):
    indexes: List[IndexInfo]
    default_index: str
