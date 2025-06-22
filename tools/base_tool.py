"""
Base class for OpenWebUI tools
"""

import requests
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()


class BasePneumaTool:
    """Base class for Pneuma tools"""

    class Valves(BaseModel):
        API_BASE_URL: str = "http://localhost:8000/api/v1"
        REQUEST_TIMEOUT: int = 30
        MAX_RETRIES: int = 3

    def __init__(self):
        self.valves = self.Valves()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to Pneuma API with error handling"""
        url = f"{self.valves.API_BASE_URL}{endpoint}"

        for attempt in range(self.valves.MAX_RETRIES):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    timeout=self.valves.REQUEST_TIMEOUT,
                    **kwargs,
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    error_msg = f"API returned status {response.status_code}"
                    if attempt == self.valves.MAX_RETRIES - 1:
                        return {"error": error_msg}

            except requests.exceptions.RequestException as e:
                if attempt == self.valves.MAX_RETRIES - 1:
                    return {"error": f"Connection failed: {str(e)}"}

        return {"error": "Max retries exceeded"}
