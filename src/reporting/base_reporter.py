"""
Base reporter class for validation and conflict reports.

Defines the interface that all reporters must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class ReportData:
    """
    Container for validation report data.

    This data structure is passed to reporters to generate reports in
    various formats.
    """

    # Summary statistics
    total_documents: int
    passed_documents: int
    failed_documents: int
    total_errors: int
    total_warnings: int

    # Validation issues grouped by file
    issues_by_file: Dict[str, List[Any]] = field(default_factory=dict)

    # All issues (flat list)
    all_issues: List[Any] = field(default_factory=list)

    # Violation counts by rule
    rule_counts: Dict[str, int] = field(default_factory=dict)

    # Frontmatter completeness tracking (PB-003)
    missing_frontmatter_count: int = 0

    # Additional metadata
    scan_path: Optional[Path] = None
    scan_mode: str = "validation"  # "validation", "auto-fix", "conflicts"
    timestamp: Optional[str] = None

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate percentage."""
        if self.total_documents == 0:
            return 0.0
        return (self.passed_documents / self.total_documents) * 100

    @property
    def fail_rate(self) -> float:
        """Calculate fail rate percentage."""
        return 100.0 - self.pass_rate


class BaseReporter(ABC):
    """
    Abstract base class for all reporters.

    Reporters take validation data and generate reports in various formats
    (console, markdown, JSON, etc.).
    """

    def __init__(self):
        """Initialize the reporter."""
        pass

    @abstractmethod
    def generate(self, data: ReportData) -> str:
        """
        Generate a report from the given data.

        Args:
            data: Report data containing validation results

        Returns:
            Formatted report as a string
        """
        pass

    def save(self, report: str, output_path: Path) -> None:
        """
        Save report to a file.

        Args:
            report: Generated report string
            output_path: Path to save the report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")

    def _extract_severity(self, issue: Any) -> str:
        """
        Extract severity from validation issue.

        Handles both enum and string severity values.

        Args:
            issue: Validation issue object

        Returns:
            Severity as string (error, warning, info)
        """
        severity = issue.severity
        if hasattr(severity, "value"):
            return severity.value
        return str(severity)

    def _extract_line_number(self, issue: Any) -> Optional[int]:
        """
        Extract line number from validation issue.

        Handles different attribute names (line, line_number).

        Args:
            issue: Validation issue object

        Returns:
            Line number or None
        """
        return getattr(issue, "line", None) or getattr(issue, "line_number", None)
