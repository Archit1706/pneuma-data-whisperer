import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import aioredis
import structlog

from ..config import settings

logger = structlog.get_logger()


class SessionService:
    """Service for managing user sessions and conversation context"""

    def __init__(self):
        self.redis = None

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis = aioredis.from_url(
                f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
                password=settings.redis_password,
                encoding="utf-8",
                decode_responses=True,
            )

            # Test connection
            await self.redis.ping()
            logger.info("Redis connection established")

        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise

    async def cleanup(self):
        """Cleanup Redis connection"""
        if self.redis:
            await self.redis.close()

    async def add_query_to_session(self, session_id: str, query: str, response: Any):
        """Add a query and response to session history"""
        try:
            session_key = f"session:{session_id}"

            # Get existing session data
            session_data = await self.get_session_data(session_id)

            # Add new query
            query_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "query": query,
                "response_summary": {
                    "results_count": len(response.results) if response.results else 0,
                    "search_time_ms": response.search_time_ms,
                    "table_names": [
                        r.table_name for r in response.results[:5]
                    ],  # First 5 tables
                },
            }

            session_data["queries"].append(query_entry)
            session_data["last_activity"] = datetime.utcnow().isoformat()
            session_data["query_count"] = len(session_data["queries"])

            # Store updated session
            await self.redis.setex(
                session_key,
                timedelta(hours=settings.session_expire_hours).total_seconds(),
                json.dumps(session_data),
            )

        except Exception as e:
            logger.error("Failed to store session data", error=str(e))

    async def get_session_data(self, session_id: str) -> Dict[str, Any]:
        """Get session data"""
        try:
            session_key = f"session:{session_id}"
            data = await self.redis.get(session_key)

            if data:
                return json.loads(data)
            else:
                # Create new session
                return {
                    "session_id": session_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "last_activity": datetime.utcnow().isoformat(),
                    "queries": [],
                    "query_count": 0,
                    "bookmarked_tables": [],
                }

        except Exception as e:
            logger.error("Failed to retrieve session data", error=str(e))
            return {"session_id": session_id, "queries": [], "query_count": 0}

    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get query history for a session"""
        session_data = await self.get_session_data(session_id)
        return session_data.get("queries", [])
