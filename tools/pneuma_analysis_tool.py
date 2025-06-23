"""
Tool for analyzing table details and data quality
"""

from .base_tool import BasePneumaTool
from typing import Dict, Any


class PneumaAnalysisTool(BasePneumaTool):
    """Tool for analyzing table details and data quality"""

    def get_table_details(self, table_id: str, include_sample: bool = True) -> str:
        """
        Get detailed information about a specific table.

        Args:
            table_id: Unique identifier for the table
            include_sample: Whether to include sample data

        Returns:
            Detailed table information
        """

        response = self._make_request(
            method="GET",
            endpoint=f"/tables/{table_id}",
            params={"include_sample_data": include_sample},
        )

        if "error" in response:
            return f"❌ Error retrieving table details: {response['error']}"

        return self._format_table_details(response)

    def analyze_data_quality(self, table_id: str) -> str:
        """
        Analyze data quality metrics for a table.

        Args:
            table_id: Table identifier

        Returns:
            Data quality analysis
        """

        # This would call a specific data quality endpoint
        response = self._make_request(
            method="GET", endpoint=f"/tables/{table_id}/quality"
        )

        if "error" in response:
            return f"❌ Error analyzing data quality: {response['error']}"

        return self._format_quality_analysis(response)

    def compare_tables(self, table_ids: list) -> str:
        """
        Compare multiple tables side by side.

        Args:
            table_ids: List of table identifiers

        Returns:
            Comparison analysis
        """

        if len(table_ids) < 2:
            return "❌ Please provide at least 2 table IDs for comparison"

        if len(table_ids) > 5:
            return "❌ Maximum 5 tables can be compared at once"

        response = self._make_request(
            method="POST", endpoint="/tables/compare", json={"table_ids": table_ids}
        )

        if "error" in response:
            return f"❌ Error comparing tables: {response['error']}"

        return self._format_table_comparison(response)

    def _format_table_details(self, table_data: Dict[str, Any]) -> str:
        """Format detailed table information"""

        name = table_data.get("table_name", "Unknown")
        description = table_data.get("description", "No description")
        row_count = table_data.get("row_count", "Unknown")
        col_count = table_data.get("column_count", "Unknown")

        result = f"📋 **Table Details: {name}**\n\n"
        result += f"📄 **Description:** {description}\n"
        result += f"📊 **Size:** {row_count} rows × {col_count} columns\n\n"

        # Schema information
        schema = table_data.get("schema", [])
        if schema:
            result += "🏗️ **Schema:**\n"
            for col in schema:
                col_name = col.get("name", "unknown")
                col_type = col.get("type", "unknown")
                col_desc = col.get("description", "")
                result += f"   • **{col_name}** ({col_type})"
                if col_desc:
                    result += f": {col_desc}"
                result += "\n"
            result += "\n"

        # Sample data
        sample_data = table_data.get("sample_data", [])
        if sample_data:
            result += "📝 **Sample Data:**\n"
            result += "```\n"
            # Create a simple table format
            if sample_data:
                headers = list(sample_data[0].keys()) if sample_data else []
                result += " | ".join(headers) + "\n"
                result += "-" * (len(" | ".join(headers))) + "\n"

                for row in sample_data[:3]:  # Show first 3 rows
                    values = [str(row.get(h, "")) for h in headers]
                    result += " | ".join(values) + "\n"

                if len(sample_data) > 3:
                    result += f"... ({len(sample_data) - 3} more rows)\n"
            result += "```\n"

        return result

    def _format_quality_analysis(self, quality_data: Dict[str, Any]) -> str:
        """Format data quality analysis"""

        result = "🔍 **Data Quality Analysis**\n\n"

        # Mock quality metrics (implement based on actual Pneuma API)
        metrics = quality_data.get("metrics", {})

        result += "📊 **Quality Metrics:**\n"
        result += f"   • Completeness: {metrics.get('completeness', 'N/A')}%\n"
        result += f"   • Accuracy: {metrics.get('accuracy', 'N/A')}%\n"
        result += f"   • Consistency: {metrics.get('consistency', 'N/A')}%\n"
        result += f"   • Freshness: {metrics.get('freshness', 'N/A')}\n\n"

        issues = quality_data.get("issues", [])
        if issues:
            result += "⚠️ **Potential Issues:**\n"
            for issue in issues:
                result += f"   • {issue}\n"

        return result

    def _format_table_comparison(self, comparison_data: Dict[str, Any]) -> str:
        """Format table comparison results"""

        result = "🔄 **Table Comparison**\n\n"

        tables = comparison_data.get("tables", [])

        result += "📊 **Overview:**\n"
        for table in tables:
            name = table.get("name", "Unknown")
            rows = table.get("row_count", "Unknown")
            cols = table.get("column_count", "Unknown")
            result += f"   • **{name}**: {rows} rows × {cols} columns\n"

        result += "\n🏗️ **Schema Comparison:**\n"
        # Add schema comparison logic here

        return result
