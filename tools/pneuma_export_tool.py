"""
Tool for exporting table data and metadata
"""

from .base_tool import BasePneumaTool
from typing import Dict, Any, List


class PneumaExportTool(BasePneumaTool):
    """Tool for exporting table data and metadata"""

    def export_table_metadata(self, table_ids: List[str], format: str = "json") -> str:
        """
        Export metadata for one or more tables.

        Args:
            table_ids: List of table identifiers
            format: Export format (json, csv, markdown)

        Returns:
            Export information and download instructions
        """

        if not table_ids:
            return "❌ Please provide at least one table ID"

        if format not in ["json", "csv", "markdown"]:
            return "❌ Supported formats: json, csv, markdown"

        response = self._make_request(
            method="POST",
            endpoint="/export/metadata",
            json={"table_ids": table_ids, "format": format, "include_metadata": True},
        )

        if "error" in response:
            return f"❌ Export failed: {response['error']}"

        return self._format_export_response(response, "metadata")

    def export_search_results(self, session_id: str, format: str = "json") -> str:
        """
        Export search results from a session.

        Args:
            session_id: Session identifier
            format: Export format

        Returns:
            Export information
        """

        response = self._make_request(
            method="POST",
            endpoint="/export/session",
            json={"session_id": session_id, "format": format},
        )

        if "error" in response:
            return f"❌ Export failed: {response['error']}"

        return self._format_export_response(response, "search results")

    def generate_data_report(self, table_ids: List[str]) -> str:
        """
        Generate a comprehensive data report for selected tables.

        Args:
            table_ids: List of table identifiers

        Returns:
            Formatted data report
        """

        if not table_ids:
            return "❌ Please provide at least one table ID"

        response = self._make_request(
            method="POST", endpoint="/export/report", json={"table_ids": table_ids}
        )

        if "error" in response:
            return f"❌ Report generation failed: {response['error']}"

        return self._format_data_report(response)

    def _format_export_response(
        self, response: Dict[str, Any], export_type: str
    ) -> str:
        """Format export response"""

        result = f"✅ **{export_type.title()} Export Completed**\n\n"

        download_url = response.get("download_url")
        file_size = response.get("file_size", "Unknown")
        expires_at = response.get("expires_at")

        if download_url:
            result += f"📥 **Download URL:** {download_url}\n"
            result += f"📁 **File Size:** {file_size}\n"
            if expires_at:
                result += f"⏰ **Expires:** {expires_at}\n"

        tables_exported = response.get("tables_exported", [])
        if tables_exported:
            result += f"\n📊 **Tables Exported:** {len(tables_exported)}\n"
            for table in tables_exported[:5]:  # Show first 5
                result += f"   • {table}\n"
            if len(tables_exported) > 5:
                result += f"   ... and {len(tables_exported) - 5} more\n"

        return result

    def _format_data_report(self, report_data: Dict[str, Any]) -> str:
        """Format comprehensive data report"""

        result = "📈 **Data Discovery Report**\n\n"

        summary = report_data.get("summary", {})
        result += "📊 **Summary:**\n"
        result += f"   • Total Tables: {summary.get('total_tables', 0)}\n"
        result += f"   • Total Rows: {summary.get('total_rows', 0):,}\n"
        result += f"   • Total Columns: {summary.get('total_columns', 0)}\n"
        result += (
            f"   • Data Quality Score: {summary.get('avg_quality_score', 'N/A')}\n\n"
        )

        recommendations = report_data.get("recommendations", [])
        if recommendations:
            result += "💡 **Recommendations:**\n"
            for rec in recommendations:
                result += f"   • {rec}\n"
            result += "\n"

        download_url = report_data.get("report_url")
        if download_url:
            result += f"📥 **Full Report:** {download_url}\n"

        return result


# Tool registration for OpenWebUI
tools = [PneumaSearchTool(), PneumaAnalysisTool(), PneumaExportTool()]
