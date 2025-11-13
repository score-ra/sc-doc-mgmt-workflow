"""
Reporting module for Symphony Core Document Management Workflow.

Provides various report formats (console, markdown, JSON) for validation
results and conflict detection.
"""

from enum import Enum
from typing import List, Any

from src.reporting.base_reporter import BaseReporter, ReportData
from src.reporting.console_reporter import ConsoleReporter
from src.reporting.markdown_reporter import MarkdownReporter
from src.reporting.json_reporter import JSONReporter
from src.reporting.conflict_reporter import ConflictReporter, ConflictData


class Severity(Enum):
    """Severity levels for filtering validation reports."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    @classmethod
    def from_string(cls, value: str) -> 'Severity':
        """
        Convert string to Severity enum.

        Args:
            value: Severity level as string (case-insensitive)

        Returns:
            Severity enum value

        Raises:
            ValueError: If value is not a valid severity level
        """
        value_upper = value.upper()
        if value_upper == "ERROR":
            return cls.ERROR
        elif value_upper == "WARNING":
            return cls.WARNING
        elif value_upper == "INFO":
            return cls.INFO
        else:
            raise ValueError(f"Invalid severity level: {value}")

    def includes(self, other: 'Severity') -> bool:
        """
        Check if this severity level includes another severity level.

        Hierarchy: ERROR > WARNING > INFO
        - ERROR includes only ERROR
        - WARNING includes ERROR and WARNING
        - INFO includes ERROR, WARNING, and INFO

        Args:
            other: Severity level to check

        Returns:
            True if other severity should be included
        """
        severity_order = {
            Severity.ERROR: 0,
            Severity.WARNING: 1,
            Severity.INFO: 2
        }
        return severity_order[other] <= severity_order[self]


def filter_issues_by_severity(issues: List[Any], min_severity: Severity) -> List[Any]:
    """
    Filter validation issues by minimum severity level.

    Args:
        issues: List of validation issues
        min_severity: Minimum severity level to include

    Returns:
        Filtered list of issues matching the severity criteria
    """
    filtered = []
    for issue in issues:
        # Extract severity from issue (handles both enum and string)
        issue_severity_str = None
        if hasattr(issue, 'severity'):
            if hasattr(issue.severity, 'value'):
                issue_severity_str = issue.severity.value
            else:
                issue_severity_str = str(issue.severity)

        if issue_severity_str:
            try:
                issue_severity = Severity.from_string(issue_severity_str)
                if min_severity.includes(issue_severity):
                    filtered.append(issue)
            except ValueError:
                # If severity is unknown, include it to be safe
                filtered.append(issue)

    return filtered


__all__ = [
    'BaseReporter',
    'ReportData',
    'ConsoleReporter',
    'MarkdownReporter',
    'JSONReporter',
    'ConflictReporter',
    'ConflictData',
    'Severity',
    'filter_issues_by_severity',
]
