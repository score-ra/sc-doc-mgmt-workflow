"""
Tests for severity filtering functionality in the reporting module.

This module tests the Severity enum and filter_issues_by_severity function
introduced in PB-002 (severity-based filtering feature).
"""

import pytest
from pathlib import Path
from dataclasses import dataclass

from src.reporting import Severity, filter_issues_by_severity
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


class TestSeverity:
    """Test Severity enum functionality."""

    def test_severity_values(self):
        """Test that severity enum has correct values."""
        assert Severity.ERROR.value == "error"
        assert Severity.WARNING.value == "warning"
        assert Severity.INFO.value == "info"

    def test_from_string_uppercase(self):
        """Test from_string with uppercase input."""
        assert Severity.from_string("ERROR") == Severity.ERROR
        assert Severity.from_string("WARNING") == Severity.WARNING
        assert Severity.from_string("INFO") == Severity.INFO

    def test_from_string_lowercase(self):
        """Test from_string with lowercase input."""
        assert Severity.from_string("error") == Severity.ERROR
        assert Severity.from_string("warning") == Severity.WARNING
        assert Severity.from_string("info") == Severity.INFO

    def test_from_string_mixed_case(self):
        """Test from_string with mixed case input."""
        assert Severity.from_string("Error") == Severity.ERROR
        assert Severity.from_string("Warning") == Severity.WARNING
        assert Severity.from_string("Info") == Severity.INFO

    def test_from_string_invalid(self):
        """Test from_string with invalid input."""
        with pytest.raises(ValueError, match="Invalid severity level"):
            Severity.from_string("CRITICAL")
        with pytest.raises(ValueError, match="Invalid severity level"):
            Severity.from_string("debug")
        with pytest.raises(ValueError, match="Invalid severity level"):
            Severity.from_string("")

    def test_includes_error_level(self):
        """Test ERROR severity includes only ERROR."""
        assert Severity.ERROR.includes(Severity.ERROR) is True
        assert Severity.ERROR.includes(Severity.WARNING) is False
        assert Severity.ERROR.includes(Severity.INFO) is False

    def test_includes_warning_level(self):
        """Test WARNING severity includes ERROR and WARNING."""
        assert Severity.WARNING.includes(Severity.ERROR) is True
        assert Severity.WARNING.includes(Severity.WARNING) is True
        assert Severity.WARNING.includes(Severity.INFO) is False

    def test_includes_info_level(self):
        """Test INFO severity includes all levels."""
        assert Severity.INFO.includes(Severity.ERROR) is True
        assert Severity.INFO.includes(Severity.WARNING) is True
        assert Severity.INFO.includes(Severity.INFO) is True


class TestFilterIssuesBySeverity:
    """Test filter_issues_by_severity function."""

    @pytest.fixture
    def sample_issues(self):
        """Create sample validation issues for testing."""
        return [
            ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message="Missing required field",
                file_path=Path("test1.md")
            ),
            ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.WARNING,
                message="Optional field missing",
                file_path=Path("test2.md")
            ),
            ValidationIssue(
                rule_id="YAML-003",
                severity=ValidationSeverity.INFO,
                message="Informational message",
                file_path=Path("test3.md")
            ),
            ValidationIssue(
                rule_id="YAML-004",
                severity=ValidationSeverity.ERROR,
                message="Another error",
                file_path=Path("test4.md")
            ),
            ValidationIssue(
                rule_id="YAML-005",
                severity=ValidationSeverity.WARNING,
                message="Another warning",
                file_path=Path("test5.md")
            ),
        ]

    def test_filter_by_error_only(self, sample_issues):
        """Test filtering to show only ERROR level issues."""
        filtered = filter_issues_by_severity(sample_issues, Severity.ERROR)
        assert len(filtered) == 2
        assert all(issue.severity == ValidationSeverity.ERROR for issue in filtered)
        assert filtered[0].rule_id == "YAML-001"
        assert filtered[1].rule_id == "YAML-004"

    def test_filter_by_warning(self, sample_issues):
        """Test filtering to show ERROR and WARNING level issues."""
        filtered = filter_issues_by_severity(sample_issues, Severity.WARNING)
        assert len(filtered) == 4
        # Should include 2 errors + 2 warnings
        error_count = sum(1 for issue in filtered if issue.severity == ValidationSeverity.ERROR)
        warning_count = sum(1 for issue in filtered if issue.severity == ValidationSeverity.WARNING)
        assert error_count == 2
        assert warning_count == 2

    def test_filter_by_info(self, sample_issues):
        """Test filtering to show all issues (ERROR, WARNING, INFO)."""
        filtered = filter_issues_by_severity(sample_issues, Severity.INFO)
        assert len(filtered) == 5
        # Should include all issues
        assert filtered == sample_issues

    def test_filter_empty_list(self):
        """Test filtering an empty list of issues."""
        filtered = filter_issues_by_severity([], Severity.ERROR)
        assert filtered == []

    def test_filter_preserves_order(self, sample_issues):
        """Test that filtering preserves the original order of issues."""
        filtered = filter_issues_by_severity(sample_issues, Severity.WARNING)
        # Check that ERROR issues appear before WARNING issues if they did originally
        rule_ids = [issue.rule_id for issue in filtered]
        assert rule_ids == ["YAML-001", "YAML-002", "YAML-004", "YAML-005"]

    def test_filter_with_string_severity(self):
        """Test filtering with issues that have string severity (edge case)."""
        @dataclass
        class MockIssue:
            rule_id: str
            severity: str
            message: str
            file_path: Path

        issues = [
            MockIssue("TEST-001", "error", "Error message", Path("test1.md")),
            MockIssue("TEST-002", "warning", "Warning message", Path("test2.md")),
            MockIssue("TEST-003", "info", "Info message", Path("test3.md")),
        ]

        filtered = filter_issues_by_severity(issues, Severity.WARNING)
        assert len(filtered) == 2
        assert filtered[0].rule_id == "TEST-001"
        assert filtered[1].rule_id == "TEST-002"

    def test_filter_handles_unknown_severity(self):
        """Test that filtering includes issues with unknown severity (safety measure)."""
        @dataclass
        class MockIssue:
            rule_id: str
            severity: str
            message: str
            file_path: Path

        issues = [
            MockIssue("TEST-001", "error", "Error message", Path("test1.md")),
            MockIssue("TEST-002", "unknown", "Unknown severity", Path("test2.md")),
            MockIssue("TEST-003", "info", "Info message", Path("test3.md")),
        ]

        # Unknown severity issues should be included to be safe
        filtered = filter_issues_by_severity(issues, Severity.ERROR)
        # Should include the error and the unknown severity issue
        assert len(filtered) == 2

    def test_filter_handles_missing_severity_attribute(self):
        """Test filtering with issues missing severity attribute."""
        @dataclass
        class MockIssueNoSeverity:
            rule_id: str
            message: str
            file_path: Path

        issues = [
            MockIssueNoSeverity("TEST-001", "Message", Path("test1.md")),
        ]

        # Issues without severity attribute should not be included
        filtered = filter_issues_by_severity(issues, Severity.INFO)
        assert len(filtered) == 0


class TestSeverityIntegration:
    """Integration tests for severity filtering with config."""

    def test_config_min_severity_getter(self):
        """Test that config can retrieve min_severity setting."""
        from src.utils.config import Config

        config = Config()
        min_severity = config.get_min_severity()

        # Should return a valid severity level
        assert min_severity in ["ERROR", "WARNING", "INFO"]

    def test_severity_filter_end_to_end(self):
        """Test complete severity filtering workflow."""
        # Create sample issues
        issues = [
            ValidationIssue(
                rule_id="TEST-001",
                severity=ValidationSeverity.ERROR,
                message="Error",
                file_path=Path("test1.md")
            ),
            ValidationIssue(
                rule_id="TEST-002",
                severity=ValidationSeverity.WARNING,
                message="Warning",
                file_path=Path("test2.md")
            ),
            ValidationIssue(
                rule_id="TEST-003",
                severity=ValidationSeverity.INFO,
                message="Info",
                file_path=Path("test3.md")
            ),
        ]

        # Test filtering with each severity level
        error_only = filter_issues_by_severity(issues, Severity.ERROR)
        warning_and_up = filter_issues_by_severity(issues, Severity.WARNING)
        all_issues = filter_issues_by_severity(issues, Severity.INFO)

        assert len(error_only) == 1
        assert len(warning_and_up) == 2
        assert len(all_issues) == 3

        # Verify correct issues are included
        assert error_only[0].rule_id == "TEST-001"
        assert warning_and_up[0].rule_id == "TEST-001"
        assert warning_and_up[1].rule_id == "TEST-002"
        assert all_issues[0].rule_id == "TEST-001"
        assert all_issues[1].rule_id == "TEST-002"
        assert all_issues[2].rule_id == "TEST-003"
