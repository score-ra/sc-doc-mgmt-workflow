"""
JSON reporter for validation results.

Generates machine-readable JSON reports for CI/CD integration and automation.
"""

import json
from datetime import datetime
from src.reporting.base_reporter import BaseReporter, ReportData


class JSONReporter(BaseReporter):
    """
    Generate JSON-formatted validation reports.

    Produces structured JSON output suitable for CI/CD systems,
    automation, and programmatic consumption.
    """

    def __init__(self, indent: int = 2, include_timestamp: bool = True):
        """
        Initialize JSON reporter.

        Args:
            indent: JSON indentation level (default: 2)
            include_timestamp: Include timestamp in report (default: True)
        """
        super().__init__()
        self.indent = indent
        self.include_timestamp = include_timestamp

    def generate(self, data: ReportData) -> str:
        """
        Generate JSON-formatted report.

        Args:
            data: Report data containing validation results

        Returns:
            Formatted JSON report
        """
        report_dict = {
            "summary": {
                "total": data.total_documents,
                "passed": data.passed_documents,
                "failed": data.failed_documents,
                "pass_rate": round(data.pass_rate, 2),
                "errors": data.total_errors,
                "warnings": data.total_warnings,
                "missing_frontmatter": data.missing_frontmatter_count,
            },
            "violations": [],
        }

        # Add timestamp if requested
        if self.include_timestamp:
            timestamp = data.timestamp or datetime.now().isoformat()
            report_dict["timestamp"] = timestamp

        # Add scan metadata
        if data.scan_path:
            report_dict["scan_path"] = str(data.scan_path)
        report_dict["scan_mode"] = data.scan_mode

        # Add violations by rule
        if data.rule_counts:
            report_dict["violations_by_rule"] = data.rule_counts

        # Add detailed violations
        for issue in data.all_issues:
            violation = {
                "file": str(issue.file_path),
                "rule_id": issue.rule_id,
                "severity": self._extract_severity(issue),
                "message": issue.message,
                "line": self._extract_line_number(issue),
                "suggestion": issue.suggestion,
            }
            report_dict["violations"].append(violation)

        return json.dumps(report_dict, indent=self.indent, ensure_ascii=False)


class ConflictJSONReporter(BaseReporter):
    """
    Generate JSON-formatted conflict reports.

    Produces structured JSON output for conflict detection results.
    """

    def __init__(self, indent: int = 2, include_timestamp: bool = True):
        """
        Initialize conflict JSON reporter.

        Args:
            indent: JSON indentation level (default: 2)
            include_timestamp: Include timestamp in report (default: True)
        """
        super().__init__()
        self.indent = indent
        self.include_timestamp = include_timestamp

    def generate(self, data: ReportData) -> str:
        """
        Generate JSON-formatted conflict report.

        Args:
            data: Report data containing conflict information

        Returns:
            Formatted JSON conflict report
        """
        report_dict = {
            "summary": {
                "total_conflicts": len(data.all_issues),
                "documents_scanned": data.total_documents,
            },
            "conflicts": [],
        }

        # Add timestamp if requested
        if self.include_timestamp:
            timestamp = data.timestamp or datetime.now().isoformat()
            report_dict["timestamp"] = timestamp

        # Group conflicts by type for summary
        conflicts_by_type = {}
        for conflict in data.all_issues:
            conflict_type = getattr(conflict, "conflict_type", "unknown")
            if conflict_type not in conflicts_by_type:
                conflicts_by_type[conflict_type] = 0
            conflicts_by_type[conflict_type] += 1

        report_dict["summary"]["conflicts_by_type"] = conflicts_by_type

        # Add detailed conflicts
        for conflict in data.all_issues:
            conflict_dict = {
                "type": getattr(conflict, "conflict_type", "unknown"),
                "rule_id": getattr(conflict, "rule_id", "UNKNOWN"),
                "severity": self._extract_severity(conflict),
                "message": getattr(conflict, "message", "No message"),
                "suggestion": getattr(conflict, "suggestion", None),
            }

            # Add file information if available
            if hasattr(conflict, "file_path"):
                conflict_dict["file"] = str(conflict.file_path)

            report_dict["conflicts"].append(conflict_dict)

        return json.dumps(report_dict, indent=self.indent, ensure_ascii=False)
