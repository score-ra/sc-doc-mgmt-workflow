"""
Console reporter for validation results.

Generates human-readable console output with formatting and colors.
"""

from src.reporting.base_reporter import BaseReporter, ReportData


class ConsoleReporter(BaseReporter):
    """
    Generate console-formatted validation reports.

    Produces human-readable output suitable for terminal display with
    optional color support.
    """

    def __init__(self, use_colors: bool = False):
        """
        Initialize console reporter.

        Args:
            use_colors: Enable ANSI color codes (default: False)
        """
        super().__init__()
        self.use_colors = use_colors

    def generate(self, data: ReportData) -> str:
        """
        Generate console-formatted report.

        Args:
            data: Report data containing validation results

        Returns:
            Formatted console report
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Summary statistics
        lines.append(f"Documents Scanned: {data.total_documents}")
        lines.append(f"Passed: {data.passed_documents} " f"({data.pass_rate:.1f}%)")
        lines.append(f"Failed: {data.failed_documents} " f"({data.fail_rate:.1f}%)")
        lines.append("")
        lines.append(f"Total Errors: {data.total_errors}")
        lines.append(f"Total Warnings: {data.total_warnings}")
        lines.append("")

        # Frontmatter completeness (PB-003)
        if data.missing_frontmatter_count > 0:
            lines.append(
                f"Documents Missing Frontmatter: {data.missing_frontmatter_count}"
            )
            lines.append("")

        # Violations by rule
        if data.rule_counts:
            lines.append("VIOLATIONS BY RULE:")
            for rule_id, count in sorted(data.rule_counts.items()):
                lines.append(f"  {rule_id}: {count}")
            lines.append("")

        # Failed documents with details
        if data.issues_by_file:
            lines.append("FAILED DOCUMENTS:")
            for file_path, file_issues in sorted(data.issues_by_file.items()):
                lines.append(f"\n  {file_path}")
                for issue in file_issues:
                    severity_label = self._extract_severity(issue).upper()
                    lines.append(
                        f"    [{severity_label}] {issue.rule_id}: {issue.message}"
                    )
                    if issue.suggestion:
                        lines.append(f"    Suggestion: {issue.suggestion}")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)


class ConflictConsoleReporter(BaseReporter):
    """
    Generate console-formatted conflict reports.

    Produces human-readable conflict detection output for terminal display.
    """

    def __init__(self, use_colors: bool = False):
        """
        Initialize conflict console reporter.

        Args:
            use_colors: Enable ANSI color codes (default: False)
        """
        super().__init__()
        self.use_colors = use_colors

    def generate(self, data: ReportData) -> str:
        """
        Generate console-formatted conflict report.

        Args:
            data: Report data containing conflict information

        Returns:
            Formatted console conflict report
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("CONFLICT DETECTION REPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Total Conflicts Found: {len(data.all_issues)}")
        lines.append("")

        # Group conflicts by type
        conflicts_by_type = {}
        for conflict in data.all_issues:
            conflict_type = getattr(conflict, "conflict_type", "UNKNOWN")
            if conflict_type not in conflicts_by_type:
                conflicts_by_type[conflict_type] = []
            conflicts_by_type[conflict_type].append(conflict)

        # Display conflicts by type
        type_labels = {
            "status": "STATUS CONFLICTS",
            "tag_synonym": "TAG SYNONYM CONFLICTS",
            "pricing": "PRICING CONFLICTS",
            "cross_reference": "CROSS-REFERENCE CONFLICTS",
        }

        for conflict_type, conflicts in sorted(conflicts_by_type.items()):
            type_label = type_labels.get(conflict_type, conflict_type.upper())
            lines.append(f"\n{type_label} ({len(conflicts)}):")
            lines.append("-" * 80)
            lines.append("")

            for conflict in conflicts:
                rule_id = getattr(conflict, "rule_id", "UNKNOWN")
                message = getattr(conflict, "message", "No message")
                lines.append(f"[{rule_id}] {message}")

                if hasattr(conflict, "suggestion") and conflict.suggestion:
                    lines.append(f"  Suggestion: {conflict.suggestion}")
                lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)
