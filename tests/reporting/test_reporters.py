"""
Tests for console, markdown, and JSON reporters.
"""

import pytest
import json
from pathlib import Path
from dataclasses import dataclass

from src.reporting.base_reporter import ReportData
from src.reporting.console_reporter import ConsoleReporter
from src.reporting.markdown_reporter import MarkdownReporter
from src.reporting.json_reporter import JSONReporter


@dataclass
class MockIssue:
    """Mock validation issue for testing."""
    file_path: Path
    rule_id: str
    severity: str
    message: str
    suggestion: str = None
    line_number: int = None

    @property
    def line(self):
        return self.line_number


class TestConsoleReporter:
    """Test ConsoleReporter."""

    def test_console_reporter_initialization(self):
        """Test ConsoleReporter can be initialized."""
        reporter = ConsoleReporter()
        assert reporter is not None
        assert reporter.use_colors is False

    def test_console_reporter_with_colors(self):
        """Test ConsoleReporter with colors enabled."""
        reporter = ConsoleReporter(use_colors=True)
        assert reporter.use_colors is True

    def test_generate_empty_report(self):
        """Test generating report with no issues."""
        reporter = ConsoleReporter()
        data = ReportData(
            total_documents=10,
            passed_documents=10,
            failed_documents=0,
            total_errors=0,
            total_warnings=0
        )
        report = reporter.generate(data)

        assert "VALIDATION REPORT" in report
        assert "Documents Scanned: 10" in report
        assert "Passed: 10" in report
        assert "100.0%" in report

    def test_generate_report_with_issues(self):
        """Test generating report with validation issues."""
        reporter = ConsoleReporter()

        issue = MockIssue(
            file_path=Path("test.md"),
            rule_id="TEST-001",
            severity="error",
            message="Test error message",
            suggestion="Fix this"
        )

        data = ReportData(
            total_documents=5,
            passed_documents=4,
            failed_documents=1,
            total_errors=1,
            total_warnings=0,
            issues_by_file={"test.md": [issue]},
            all_issues=[issue],
            rule_counts={"TEST-001": 1}
        )

        report = reporter.generate(data)

        assert "Documents Scanned: 5" in report
        assert "Passed: 4" in report
        assert "Failed: 1" in report
        assert "TEST-001" in report
        assert "Test error message" in report
        assert "Fix this" in report


class TestMarkdownReporter:
    """Test MarkdownReporter."""

    def test_markdown_reporter_initialization(self):
        """Test MarkdownReporter can be initialized."""
        reporter = MarkdownReporter()
        assert reporter is not None
        assert reporter.include_timestamp is True

    def test_markdown_reporter_without_timestamp(self):
        """Test MarkdownReporter without timestamp."""
        reporter = MarkdownReporter(include_timestamp=False)
        assert reporter.include_timestamp is False

    def test_generate_markdown_report(self):
        """Test generating markdown report."""
        reporter = MarkdownReporter(include_timestamp=False)

        data = ReportData(
            total_documents=10,
            passed_documents=8,
            failed_documents=2,
            total_errors=2,
            total_warnings=1
        )

        report = reporter.generate(data)

        assert "# Symphony Core Validation Report" in report
        assert "## Summary" in report
        assert "- **Passed**: 8 (80.0%)" in report
        assert "- **Failed**: 2 (20.0%)" in report

    def test_generate_markdown_with_issues(self):
        """Test generating markdown report with issues."""
        reporter = MarkdownReporter(include_timestamp=False)

        issue = MockIssue(
            file_path=Path("doc.md"),
            rule_id="MD-001",
            severity="warning",
            message="Markdown issue",
            suggestion="Fix markdown"
        )

        data = ReportData(
            total_documents=5,
            passed_documents=4,
            failed_documents=1,
            total_errors=0,
            total_warnings=1,
            issues_by_file={"doc.md": [issue]},
            all_issues=[issue],
            rule_counts={"MD-001": 1}
        )

        report = reporter.generate(data)

        assert "## Violations by Rule" in report
        assert "| MD-001 | 1 |" in report
        assert "### doc.md" in report
        assert "Markdown issue" in report

    def test_markdown_includes_timestamp(self):
        """Test that markdown includes timestamp when enabled."""
        reporter = MarkdownReporter(include_timestamp=True)

        data = ReportData(
            total_documents=5,
            passed_documents=5,
            failed_documents=0,
            total_errors=0,
            total_warnings=0,
            timestamp="2025-11-09T10:00:00"
        )

        report = reporter.generate(data)
        assert "**Date**: 2025-11-09T10:00:00" in report


class TestJSONReporter:
    """Test JSONReporter."""

    def test_json_reporter_initialization(self):
        """Test JSONReporter can be initialized."""
        reporter = JSONReporter()
        assert reporter is not None
        assert reporter.indent == 2
        assert reporter.include_timestamp is True

    def test_json_reporter_custom_indent(self):
        """Test JSONReporter with custom indent."""
        reporter = JSONReporter(indent=4)
        assert reporter.indent == 4

    def test_generate_json_report(self):
        """Test generating JSON report."""
        reporter = JSONReporter(include_timestamp=False)

        data = ReportData(
            total_documents=20,
            passed_documents=18,
            failed_documents=2,
            total_errors=2,
            total_warnings=0
        )

        report = reporter.generate(data)
        report_dict = json.loads(report)

        assert report_dict['summary']['total'] == 20
        assert report_dict['summary']['passed'] == 18
        assert report_dict['summary']['failed'] == 2
        assert report_dict['summary']['pass_rate'] == 90.0
        assert report_dict['summary']['errors'] == 2

    def test_generate_json_with_violations(self):
        """Test generating JSON report with violations."""
        reporter = JSONReporter(include_timestamp=False)

        issue = MockIssue(
            file_path=Path("file.md"),
            rule_id="YAML-001",
            severity="error",
            message="Missing frontmatter",
            suggestion="Add YAML frontmatter",
            line_number=1
        )

        data = ReportData(
            total_documents=10,
            passed_documents=9,
            failed_documents=1,
            total_errors=1,
            total_warnings=0,
            all_issues=[issue],
            rule_counts={"YAML-001": 1}
        )

        report = reporter.generate(data)
        report_dict = json.loads(report)

        assert 'violations' in report_dict
        assert len(report_dict['violations']) == 1
        assert report_dict['violations'][0]['rule_id'] == "YAML-001"
        assert report_dict['violations'][0]['severity'] == "error"
        assert report_dict['violations'][0]['line'] == 1

    def test_json_includes_timestamp(self):
        """Test that JSON includes timestamp when enabled."""
        reporter = JSONReporter(include_timestamp=True)

        data = ReportData(
            total_documents=5,
            passed_documents=5,
            failed_documents=0,
            total_errors=0,
            total_warnings=0,
            timestamp="2025-11-09T10:00:00"
        )

        report = reporter.generate(data)
        report_dict = json.loads(report)

        assert 'timestamp' in report_dict
        assert report_dict['timestamp'] == "2025-11-09T10:00:00"

    def test_json_valid_structure(self):
        """Test that generated JSON has valid structure."""
        reporter = JSONReporter()

        data = ReportData(
            total_documents=1,
            passed_documents=1,
            failed_documents=0,
            total_errors=0,
            total_warnings=0
        )

        report = reporter.generate(data)

        # Should not raise exception
        report_dict = json.loads(report)

        # Check required fields exist
        assert 'summary' in report_dict
        assert 'violations' in report_dict
        assert 'scan_mode' in report_dict


class TestReporterIntegration:
    """Integration tests for reporters."""

    def test_all_reporters_work_with_same_data(self):
        """Test that all reporters can process the same data."""
        data = ReportData(
            total_documents=10,
            passed_documents=7,
            failed_documents=3,
            total_errors=3,
            total_warnings=2
        )

        console_reporter = ConsoleReporter()
        markdown_reporter = MarkdownReporter()
        json_reporter = JSONReporter()

        console_report = console_reporter.generate(data)
        markdown_report = markdown_reporter.generate(data)
        json_report = json_reporter.generate(data)

        assert "Documents Scanned: 10" in console_report
        assert "- **Passed**: 7 (70.0%)" in markdown_report

        json_dict = json.loads(json_report)
        assert json_dict['summary']['total'] == 10

    def test_save_functionality(self, tmp_path):
        """Test that all reporters can save to files."""
        data = ReportData(
            total_documents=5,
            passed_documents=5,
            failed_documents=0,
            total_errors=0,
            total_warnings=0
        )

        reporters = [
            (ConsoleReporter(), "console.txt"),
            (MarkdownReporter(), "report.md"),
            (JSONReporter(), "report.json")
        ]

        for reporter, filename in reporters:
            output_path = tmp_path / filename
            report = reporter.generate(data)
            reporter.save(report, output_path)

            assert output_path.exists()
            assert output_path.stat().st_size > 0
