"""
Markdown reporter for validation results.

Generates markdown-formatted reports suitable for documentation and sharing.
"""

from datetime import datetime
from src.reporting.base_reporter import BaseReporter, ReportData


class MarkdownReporter(BaseReporter):
    """
    Generate markdown-formatted validation reports.

    Produces structured markdown output suitable for documentation,
    sharing, and archiving.
    """

    def __init__(self, include_timestamp: bool = True):
        """
        Initialize markdown reporter.

        Args:
            include_timestamp: Include timestamp in report (default: True)
        """
        super().__init__()
        self.include_timestamp = include_timestamp

    def generate(self, data: ReportData) -> str:
        """
        Generate markdown-formatted report.

        Args:
            data: Report data containing validation results

        Returns:
            Formatted markdown report
        """
        lines = [
            "# Symphony Core Validation Report",
            "",
        ]

        # Timestamp
        if self.include_timestamp:
            timestamp = data.timestamp or datetime.now().isoformat()
            lines.append(f"**Date**: {timestamp}")
            lines.append("")

        # Scan metadata
        if data.scan_path:
            lines.append(f"**Path**: {data.scan_path}")
        lines.append(f"**Mode**: {data.scan_mode}")
        lines.append(f"**Documents**: {data.total_documents} scanned")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Passed**: {data.passed_documents} ({data.pass_rate:.1f}%)")
        lines.append(f"- **Failed**: {data.failed_documents} ({data.fail_rate:.1f}%)")
        lines.append(f"- **Total Errors**: {data.total_errors}")
        lines.append(f"- **Total Warnings**: {data.total_warnings}")
        lines.append("")

        # Violations by rule
        if data.rule_counts:
            lines.append("## Violations by Rule")
            lines.append("")
            lines.append("| Rule ID | Count |")
            lines.append("|---------|-------|")

            for rule_id, count in sorted(data.rule_counts.items()):
                lines.append(f"| {rule_id} | {count} |")

            lines.append("")

        # Failed documents
        if data.issues_by_file:
            lines.append("## Failed Documents")
            lines.append("")

            for file_path, file_issues in sorted(data.issues_by_file.items()):
                lines.append(f"### {file_path}")
                lines.append("")

                for issue in file_issues:
                    severity_label = self._extract_severity(issue).upper()
                    lines.append(
                        f"- **[{severity_label}]** {issue.rule_id}: {issue.message}"
                    )
                    if issue.suggestion:
                        lines.append(f"  - Suggestion: {issue.suggestion}")

                lines.append("")

        return '\n'.join(lines)


class ConflictMarkdownReporter(BaseReporter):
    """
    Generate markdown-formatted conflict reports.

    Produces structured markdown output for conflict detection results.
    """

    def __init__(self, include_timestamp: bool = True):
        """
        Initialize conflict markdown reporter.

        Args:
            include_timestamp: Include timestamp in report (default: True)
        """
        super().__init__()
        self.include_timestamp = include_timestamp

    def generate(self, data: ReportData) -> str:
        """
        Generate markdown-formatted conflict report.

        Args:
            data: Report data containing conflict information

        Returns:
            Formatted markdown conflict report
        """
        lines = [
            "# Symphony Core Conflict Detection Report",
            "",
        ]

        # Timestamp
        if self.include_timestamp:
            timestamp = data.timestamp or datetime.now().isoformat()
            lines.append(f"**Date**: {timestamp}")
            lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Conflicts**: {len(data.all_issues)}")
        lines.append(f"- **Documents Scanned**: {data.total_documents}")
        lines.append("")

        # Group conflicts by type
        conflicts_by_type = {}
        for conflict in data.all_issues:
            conflict_type = getattr(conflict, 'conflict_type', 'unknown')
            if conflict_type not in conflicts_by_type:
                conflicts_by_type[conflict_type] = []
            conflicts_by_type[conflict_type].append(conflict)

        # Display conflicts by type
        type_labels = {
            'status': 'Status Conflicts',
            'tag_synonym': 'Tag Synonym Conflicts',
            'pricing': 'Pricing Conflicts',
            'cross_reference': 'Cross-Reference Conflicts'
        }

        for conflict_type, conflicts in sorted(conflicts_by_type.items()):
            type_label = type_labels.get(conflict_type, conflict_type.title())
            lines.append(f"## {type_label}")
            lines.append("")
            lines.append(f"**Count**: {len(conflicts)}")
            lines.append("")

            for conflict in conflicts:
                rule_id = getattr(conflict, 'rule_id', 'UNKNOWN')
                message = getattr(conflict, 'message', 'No message')
                lines.append(f"### [{rule_id}]")
                lines.append("")
                lines.append(message)
                lines.append("")

                if hasattr(conflict, 'suggestion') and conflict.suggestion:
                    lines.append(f"**Suggestion**: {conflict.suggestion}")
                    lines.append("")

        return '\n'.join(lines)
