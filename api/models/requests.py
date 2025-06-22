from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    index_name: str = Field(default="default", description="Index to search in")
    k: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    n: int = Field(default=5, ge=1, le=20, description="Multiplier for candidate generation")
    alpha: float = Field(default=0.5, ge=0.0, le=1.0, description="Hybrid search weight")
    session_id: Optional[str] = Field(default=None, description="Session ID for context")

class TableDetailsRequest(BaseModel):
    table_id: str = Field(..., description="Table identifier")
    include_sample_data: bool = Field(default=True, description="Include sample rows")
    sample_size: int = Field(default=10, ge=1, le=100, description="Number of sample rows")

class ExportRequest(BaseModel):
    table_ids: List[str] = Field(..., description="List of table IDs to export")
    format: str = Field(default="json", description="Export format (json, csv)")
    include_metadata: bool = Field(default=True, description="Include table metadata")