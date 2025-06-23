"""
Main search tool for Pneuma data discovery
"""

from .base_tool import BasePneumaTool
from typing import Dict, Any
import uuid


class PneumaSearchTool(BasePneumaTool):
    """Tool for searching tables using natural language queries"""

    def search_tables(self, query: str, k: int = 5, session_id: str = None) -> str:
        """
        Search for relevant tables using natural language query.

        Args:
            query: Natural language description of desired data
            k: Number of tables to return (1-20)
            session_id: Optional session ID for context tracking

        Returns:
            Formatted string with search results
        """

        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Validate parameters
        k = max(1, min(20, k))

        # Make API request
        response = self._make_request(
            method="POST",
            endpoint="/query",
            json={"query": query, "k": k, "session_id": session_id},
        )

        if "error" in response:
            return f"❌ Error: {response['error']}"

        return self._format_search_results(response, query)

    def get_query_suggestions(self, context: str = "") -> str:
        """
        Get query suggestions based on available data.

        Args:
            context: Optional context for better suggestions

        Returns:
            List of suggested queries
        """

        suggestions = [
            "Find datasets about traffic patterns",
            "Show me crime data with location information",
            "What weather datasets are available?",
            "Find sales or revenue data",
            "Show me demographic or population data",
            "Find datasets about public transportation",
            "What environmental or pollution data exists?",
            "Show me education or school-related datasets",
        ]

        result = "🔍 **Query Suggestions:**\n\n"
        for i, suggestion in enumerate(suggestions, 1):
            result += f"{i}. {suggestion}\n"

        result += "\n💡 **Tips:**\n"
        result += "- Be specific about the type of data you need\n"
        result += "- Mention location, time period, or domain if relevant\n"
        result += "- Ask follow-up questions to refine your search\n"

        return result

    def _format_search_results(
        self, response: Dict[str, Any], original_query: str
    ) -> str:
        """Format search results for display"""

        if not response.get("results"):
            return f"❌ No relevant tables found for query: '{original_query}'"

        results = response["results"]
        search_time = response.get("search_time_ms", 0)

        result = f"🎯 **Found {len(results)} relevant table(s)** (Search time: {search_time:.0f}ms)\n"
        result += f"📝 Query: *{original_query}*\n\n"

        for i, table in enumerate(results, 1):
            table_name = table.get("table_name", "Unknown Table")
            description = table.get("description", "No description available")
            relevance = table.get("relevance_score", 0)
            row_count = table.get("row_count", "Unknown")
            col_count = table.get("column_count", "Unknown")

            result += f"**{i}. {table_name}**\n"
            result += f"   📊 Relevance: {relevance:.2f} | Rows: {row_count} | Columns: {col_count}\n"
            result += f"   📄 {description}\n"

            # Add schema preview if available
            schema = table.get("schema", [])
            if schema:
                col_names = [col.get("name", "unknown") for col in schema[:5]]
                result += f"   🏗️ Key columns: {', '.join(col_names)}"
                if len(schema) > 5:
                    result += f" (+{len(schema) - 5} more)"
                result += "\n"

            result += "\n"

        # Add session info
        session_id = response.get("session_id")
        if session_id:
            result += f"🔗 Session ID: `{session_id}` (use for follow-up queries)\n"

        return result
