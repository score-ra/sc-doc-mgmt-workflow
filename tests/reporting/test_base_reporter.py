"""
Tests for base reporter functionality.
"""

import pytest
from pathlib import Path

from src.reporting.base_reporter import BaseReporter, ReportData


class ConcreteReporter(BaseReporter):
    """Concrete implementation for testing abstract base class."""

    def generate(self, data: ReportData) -> str:
        return f"Test report with {data.total_documents} documents"


class TestReportData:
    """Test ReportData dataclass."""

    def test_report_data_creation(self):
        """Test creating ReportData instance."""
        data = ReportData(
            total_documents=100,
            passed_documents=90,
            failed_documents=10,
            total_errors=5,
            total_warnings=10
        )
        assert data.total_documents == 100
        assert data.passed_documents == 90
        assert data.failed_documents == 10

    def test_pass_rate_calculation(self):
        """Test pass rate percentage calculation."""
        data = ReportData(
            total_documents=100,
            passed_documents=75,
            failed_documents=25,
            total_errors=20,
            total_warnings=10
        )
        assert data.pass_rate == 75.0
        assert data.fail_rate == 25.0

    def test_pass_rate_zero_documents(self):
        """Test pass rate with zero documents."""
        data = ReportData(
            total_documents=0,
            passed_documents=0,
            failed_documents=0,
            total_errors=0,
            total_warnings=0
        )
        assert data.pass_rate == 0.0
        assert data.fail_rate == 100.0


class TestBaseReporter:
    """Test BaseReporter functionality."""

    def test_abstract_base_class(self):
        """Test that BaseReporter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseReporter()

    def test_concrete_implementation(self):
        """Test concrete reporter implementation."""
        reporter = ConcreteReporter()
        data = ReportData(
            total_documents=50,
            passed_documents=40,
            failed_documents=10,
            total_errors=5,
            total_warnings=5
        )
        report = reporter.generate(data)
        assert "50 documents" in report

    def test_save_report(self, tmp_path):
        """Test saving report to file."""
        reporter = ConcreteReporter()
        data = ReportData(
            total_documents=50,
            passed_documents=40,
            failed_documents=10,
            total_errors=5,
            total_warnings=5
        )
        report = reporter.generate(data)

        output_file = tmp_path / "test_report.txt"
        reporter.save(report, output_file)

        assert output_file.exists()
        assert "50 documents" in output_file.read_text()

    def test_save_creates_parent_directories(self, tmp_path):
        """Test that save creates parent directories if they don't exist."""
        reporter = ConcreteReporter()
        data = ReportData(
            total_documents=10,
            passed_documents=10,
            failed_documents=0,
            total_errors=0,
            total_warnings=0
        )
        report = reporter.generate(data)

        output_file = tmp_path / "nested" / "dir" / "report.txt"
        reporter.save(report, output_file)

        assert output_file.exists()
        assert output_file.parent.exists()
