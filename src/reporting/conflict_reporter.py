"""
Conflict Reporter for Symphony Core Document Management Workflow.

Generates detailed conflict analysis reports with severity levels,
impact assessment, and resolution recommendations.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class ConflictData:
    """
    Data structure for conflict reporting.

    Attributes:
        total_conflicts: Total number of conflicts found
        conflicts_by_type: Conflicts grouped by type
        conflicts_by_severity: Conflicts grouped by severity
        documents_affected: Number of unique documents with conflicts
        impact_assessment: Dictionary with impact metrics
        recommendations: List of recommended actions
    """
    total_conflicts: int
    conflicts_by_type: Dict[str, List[Any]] = field(default_factory=dict)
    conflicts_by_severity: Dict[str, int] = field(default_factory=dict)
    documents_affected: int = 0
    impact_assessment: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ConflictReporter:
    """
    Generate detailed conflict analysis reports.

    Supports multiple output formats:
    - Console: Human-readable terminal output
    - Markdown: Documentation-ready format
    - JSON: Machine-readable for CI/CD
    """

    def __init__(self):
        """Initialize conflict reporter."""
        pass

    def analyze_conflicts(self, conflicts: Dict[str, List[Any]]) -> ConflictData:
        """
        Analyze conflicts and generate impact assessment.

        Args:
            conflicts: Dictionary mapping conflict type to list of issues

        Returns:
            ConflictData with analysis results
        """
        # Count total conflicts
        total = sum(len(issues) for issues in conflicts.values())

        # Extract unique documents affected
        affected_docs = set()
        for issues in conflicts.values():
            for issue in issues:
                if hasattr(issue, 'file_path'):
                    affected_docs.add(str(issue.file_path))

        # Determine severity distribution
        severity_counts = {'error': 0, 'warning': 0, 'info': 0}
        for issues in conflicts.values():
            for issue in issues:
                # Extract severity value (handle both enum and string)
                severity = getattr(issue, 'severity', 'warning')
                if hasattr(severity, 'value'):
                    severity = severity.value
                severity = str(severity).lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1

        # Build impact assessment
        impact = {
            'documents_affected': len(affected_docs),
            'conflict_density': round(total / max(len(affected_docs), 1), 2),
            'severity_distribution': severity_counts,
            'critical_conflicts': severity_counts['error']
        }

        # Generate recommendations
        recommendations = self._generate_recommendations(conflicts, severity_counts)

        return ConflictData(
            total_conflicts=total,
            conflicts_by_type=conflicts,
            conflicts_by_severity=severity_counts,
            documents_affected=len(affected_docs),
            impact_assessment=impact,
            recommendations=recommendations
        )

    def _generate_recommendations(
        self,
        conflicts: Dict[str, List[Any]],
        severity_counts: Dict[str, int]
    ) -> List[str]:
        """
        Generate actionable recommendations based on conflicts found.

        Args:
            conflicts: Conflicts by type
            severity_counts: Count of conflicts by severity

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Critical conflicts
        if severity_counts['error'] > 0:
            recommendations.append(
                f"CRITICAL: {severity_counts['error']} error-level conflicts require immediate attention"
            )

        # Conflict-specific recommendations
        if 'status' in conflicts and conflicts['status']:
            recommendations.append(
                "Review status field consistency across related documents"
            )

        if 'tags' in conflicts and conflicts['tags']:
            recommendations.append(
                "Standardize tag usage to improve discoverability and reduce conflicts"
            )

        if 'pricing' in conflicts and conflicts['pricing']:
            recommendations.append(
                "URGENT: Resolve pricing conflicts to prevent customer confusion"
            )

        if 'cross_references' in conflicts and conflicts['cross_references']:
            recommendations.append(
                "Update or remove references to deprecated documents"
            )

        # General recommendations
        if not recommendations:
            recommendations.append("No critical conflicts found. Consider periodic reviews.")
        else:
            recommendations.append(
                "Run conflict detection after each major documentation update"
            )

        return recommendations

    def generate_console_report(self, data: ConflictData) -> str:
        """
        Generate console-formatted conflict report.

        Args:
            data: Conflict data to report

        Returns:
            Formatted console report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("CONFLICT DETECTION REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Conflicts: {data.total_conflicts}")
        lines.append(f"Documents Affected: {data.documents_affected}")
        lines.append(f"Conflict Density: {data.impact_assessment['conflict_density']} per document")
        lines.append("")

        # Severity distribution
        lines.append("SEVERITY DISTRIBUTION")
        lines.append("-" * 80)
        for severity, count in data.conflicts_by_severity.items():
            if count > 0:
                lines.append(f"  {severity.upper()}: {count}")
        lines.append("")

        # Conflicts by type
        if data.total_conflicts > 0:
            lines.append("CONFLICTS BY TYPE")
            lines.append("-" * 80)
            for conflict_type, issues in data.conflicts_by_type.items():
                if issues:
                    lines.append(f"\n{conflict_type.upper()} ({len(issues)}):")
                    for issue in issues[:5]:  # Show first 5 per type
                        severity = issue.severity.value if hasattr(issue.severity, 'value') else str(issue.severity)
                        lines.append(f"  [{severity.upper()}] {issue.file_path.name}")
                        lines.append(f"    {issue.message}")
                    if len(issues) > 5:
                        lines.append(f"    ... and {len(issues) - 5} more")
            lines.append("")

        # Recommendations
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(data.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def generate_markdown_report(self, data: ConflictData) -> str:
        """
        Generate markdown-formatted conflict report.

        Args:
            data: Conflict data to report

        Returns:
            Formatted markdown report string
        """
        lines = []
        lines.append("# Conflict Detection Report")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Conflicts**: {data.total_conflicts}")
        lines.append(f"- **Documents Affected**: {data.documents_affected}")
        lines.append(f"- **Conflict Density**: {data.impact_assessment['conflict_density']} per document")
        lines.append("")

        # Severity distribution
        lines.append("## Severity Distribution")
        lines.append("")
        lines.append("| Severity | Count |")
        lines.append("|----------|-------|")
        for severity, count in data.conflicts_by_severity.items():
            lines.append(f"| {severity.upper()} | {count} |")
        lines.append("")

        # Conflicts by type
        if data.total_conflicts > 0:
            lines.append("## Conflicts by Type")
            lines.append("")
            for conflict_type, issues in data.conflicts_by_type.items():
                if issues:
                    lines.append(f"### {conflict_type.upper()} ({len(issues)} conflicts)")
                    lines.append("")
                    for issue in issues[:5]:
                        severity = issue.severity.value if hasattr(issue.severity, 'value') else str(issue.severity)
                        lines.append(f"**[{severity.upper()}]** `{issue.file_path.name}`")
                        lines.append(f"- {issue.message}")
                        lines.append("")
                    if len(issues) > 5:
                        lines.append(f"*... and {len(issues) - 5} more*")
                        lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(data.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

        return "\n".join(lines)

    def generate_json_report(self, data: ConflictData) -> str:
        """
        Generate JSON-formatted conflict report.

        Args:
            data: Conflict data to report

        Returns:
            JSON report string
        """
        # Convert conflict issues to serializable format
        conflicts_serialized = {}
        for conflict_type, issues in data.conflicts_by_type.items():
            conflicts_serialized[conflict_type] = [
                {
                    'file': str(issue.file_path),
                    'severity': issue.severity.value if hasattr(issue.severity, 'value') else str(issue.severity),
                    'rule_id': issue.rule_id,
                    'message': issue.message,
                    'suggestion': getattr(issue, 'suggestion', None)
                }
                for issue in issues
            ]

        report = {
            'summary': {
                'total_conflicts': data.total_conflicts,
                'documents_affected': data.documents_affected,
                'conflict_density': data.impact_assessment['conflict_density']
            },
            'severity_distribution': data.conflicts_by_severity,
            'conflicts_by_type': conflicts_serialized,
            'impact_assessment': data.impact_assessment,
            'recommendations': data.recommendations
        }

        return json.dumps(report, indent=2)
