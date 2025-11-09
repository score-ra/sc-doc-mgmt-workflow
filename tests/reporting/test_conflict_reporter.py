"""
Tests for ConflictReporter.

Tests conflict analysis reporting with severity levels, impact assessment,
and multiple output formats.
"""

import pytest
import json
from pathlib import Path
from src.reporting.conflict_reporter import ConflictReporter, ConflictData
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


class TestConflictData:
    """Test ConflictData dataclass."""

    def test_conflict_data_creation(self):
        """Test creating ConflictData with default values."""
        data = ConflictData(total_conflicts=5)
        assert data.total_conflicts == 5
        assert data.documents_affected == 0
        assert data.conflicts_by_type == {}
        assert data.conflicts_by_severity == {}
        assert data.impact_assessment == {}
        assert data.recommendations == []


class TestConflictReporter:
    """Test ConflictReporter."""

    @pytest.fixture
    def reporter(self):
        """Create a ConflictReporter instance."""
        return ConflictReporter()

    @pytest.fixture
    def sample_conflicts(self, tmp_path):
        """Create sample conflict issues for testing."""
        conflicts = {
            'status': [
                ValidationIssue(
                    rule_id='CONFLICT-001',
                    severity=ValidationSeverity.ERROR,
                    message='Status mismatch: draft vs approved',
                    file_path=tmp_path / 'doc1.md',
                    line_number=1,
                    suggestion='Standardize status field'
                ),
                ValidationIssue(
                    rule_id='CONFLICT-001',
                    severity=ValidationSeverity.WARNING,
                    message='Status case mismatch',
                    file_path=tmp_path / 'doc2.md',
                    line_number=1,
                    suggestion='Use consistent casing'
                )
            ],
            'pricing': [
                ValidationIssue(
                    rule_id='CONFLICT-003',
                    severity=ValidationSeverity.ERROR,
                    message='Pricing conflict: $100 vs $150',
                    file_path=tmp_path / 'pricing1.md',
                    line_number=10,
                    suggestion='Verify correct price'
                )
            ]
        }
        return conflicts

    def test_reporter_initialization(self, reporter):
        """Test ConflictReporter initialization."""
        assert isinstance(reporter, ConflictReporter)

    def test_analyze_conflicts_empty(self, reporter):
        """Test analyzing empty conflicts."""
        conflicts = {}
        data = reporter.analyze_conflicts(conflicts)

        assert data.total_conflicts == 0
        assert data.documents_affected == 0
        assert data.conflicts_by_severity == {'error': 0, 'warning': 0, 'info': 0}

    def test_analyze_conflicts_with_data(self, reporter, sample_conflicts):
        """Test analyzing conflicts with sample data."""
        data = reporter.analyze_conflicts(sample_conflicts)

        assert data.total_conflicts == 3
        assert data.documents_affected == 3
        assert data.conflicts_by_severity['error'] == 2
        assert data.conflicts_by_severity['warning'] == 1
        assert data.impact_assessment['documents_affected'] == 3
        assert data.impact_assessment['critical_conflicts'] == 2

    def test_analyze_conflicts_density(self, reporter, sample_conflicts):
        """Test conflict density calculation."""
        data = reporter.analyze_conflicts(sample_conflicts)

        # 3 conflicts across 3 documents = 1.0 conflicts/doc
        assert data.impact_assessment['conflict_density'] == 1.0

    def test_generate_recommendations_critical(self, reporter, sample_conflicts):
        """Test recommendations generation with critical conflicts."""
        data = reporter.analyze_conflicts(sample_conflicts)

        recommendations = data.recommendations
        assert len(recommendations) > 0

        # Should have critical recommendation
        critical_rec = [r for r in recommendations if 'CRITICAL' in r or 'error' in r.lower()]
        assert len(critical_rec) > 0

    def test_generate_recommendations_pricing(self, reporter, sample_conflicts):
        """Test pricing-specific recommendations."""
        data = reporter.analyze_conflicts(sample_conflicts)

        recommendations = data.recommendations
        pricing_rec = [r for r in recommendations if 'pricing' in r.lower() or 'URGENT' in r]
        assert len(pricing_rec) > 0

    def test_generate_console_report(self, reporter, sample_conflicts):
        """Test console report generation."""
        data = reporter.analyze_conflicts(sample_conflicts)
        report = reporter.generate_console_report(data)

        assert 'CONFLICT DETECTION REPORT' in report
        assert 'Total Conflicts: 3' in report
        assert 'Documents Affected: 3' in report
        assert 'STATUS' in report
        assert 'PRICING' in report
        assert 'RECOMMENDATIONS' in report

    def test_generate_console_report_empty(self, reporter):
        """Test console report with no conflicts."""
        data = reporter.analyze_conflicts({})
        report = reporter.generate_console_report(data)

        assert 'CONFLICT DETECTION REPORT' in report
        assert 'Total Conflicts: 0' in report
        assert 'RECOMMENDATIONS' in report

    def test_generate_markdown_report(self, reporter, sample_conflicts):
        """Test markdown report generation."""
        data = reporter.analyze_conflicts(sample_conflicts)
        report = reporter.generate_markdown_report(data)

        assert '# Conflict Detection Report' in report
        assert '## Summary' in report
        assert '**Total Conflicts**: 3' in report
        assert '**Documents Affected**: 3' in report
        assert '## Severity Distribution' in report
        assert '## Conflicts by Type' in report
        assert '### STATUS' in report
        assert '### PRICING' in report
        assert '## Recommendations' in report

    def test_generate_markdown_report_tables(self, reporter, sample_conflicts):
        """Test markdown report has proper table formatting."""
        data = reporter.analyze_conflicts(sample_conflicts)
        report = reporter.generate_markdown_report(data)

        # Check for markdown table
        assert '| Severity | Count |' in report
        assert '|----------|-------|' in report

    def test_generate_json_report(self, reporter, sample_conflicts):
        """Test JSON report generation."""
        data = reporter.analyze_conflicts(sample_conflicts)
        report = reporter.generate_json_report(data)

        # Parse JSON
        parsed = json.loads(report)

        assert 'summary' in parsed
        assert parsed['summary']['total_conflicts'] == 3
        assert parsed['summary']['documents_affected'] == 3
        assert 'severity_distribution' in parsed
        assert 'conflicts_by_type' in parsed
        assert 'recommendations' in parsed

    def test_generate_json_report_structure(self, reporter, sample_conflicts):
        """Test JSON report has correct structure."""
        data = reporter.analyze_conflicts(sample_conflicts)
        report = reporter.generate_json_report(data)

        parsed = json.loads(report)

        # Verify conflict structure
        assert 'status' in parsed['conflicts_by_type']
        assert 'pricing' in parsed['conflicts_by_type']

        # Each conflict should have required fields
        for conflict in parsed['conflicts_by_type']['status']:
            assert 'file' in conflict
            assert 'severity' in conflict
            assert 'rule_id' in conflict
            assert 'message' in conflict

    def test_recommendations_no_conflicts(self, reporter):
        """Test recommendations when no conflicts found."""
        data = reporter.analyze_conflicts({})
        recommendations = data.recommendations

        assert len(recommendations) > 0
        assert any('No critical conflicts' in r for r in recommendations)

    def test_impact_assessment_multiple_docs_one_file(self, reporter, tmp_path):
        """Test impact assessment with multiple conflicts in one file."""
        conflicts = {
            'status': [
                ValidationIssue(
                    rule_id='CONFLICT-001',
                    severity=ValidationSeverity.ERROR,
                    message='Conflict 1',
                    file_path=tmp_path / 'doc1.md',
                    line_number=1
                ),
                ValidationIssue(
                    rule_id='CONFLICT-001',
                    severity=ValidationSeverity.ERROR,
                    message='Conflict 2',
                    file_path=tmp_path / 'doc1.md',
                    line_number=5
                )
            ]
        }

        data = reporter.analyze_conflicts(conflicts)

        # 2 conflicts in 1 document
        assert data.total_conflicts == 2
        assert data.documents_affected == 1
        assert data.impact_assessment['conflict_density'] == 2.0


class TestConflictReporterIntegration:
    """Integration tests for ConflictReporter."""

    def test_full_workflow(self, tmp_path):
        """Test complete workflow from conflicts to report."""
        reporter = ConflictReporter()

        # Create conflicts
        conflicts = {
            'tags': [
                ValidationIssue(
                    rule_id='CONFLICT-002',
                    severity=ValidationSeverity.WARNING,
                    message='Tag mismatch',
                    file_path=tmp_path / 'doc1.md',
                    line_number=3,
                    suggestion='Use consistent tags'
                )
            ]
        }

        # Analyze
        data = reporter.analyze_conflicts(conflicts)

        # Generate all formats
        console_report = reporter.generate_console_report(data)
        markdown_report = reporter.generate_markdown_report(data)
        json_report = reporter.generate_json_report(data)

        # Verify all formats generated
        assert len(console_report) > 0
        assert len(markdown_report) > 0
        assert len(json_report) > 0

        # Verify JSON is valid
        json.loads(json_report)

    def test_all_conflict_types(self, tmp_path):
        """Test with all conflict types."""
        reporter = ConflictReporter()

        conflicts = {
            'status': [ValidationIssue('C-001', ValidationSeverity.ERROR, 'msg', tmp_path / 'd1.md', 1)],
            'tags': [ValidationIssue('C-002', ValidationSeverity.WARNING, 'msg', tmp_path / 'd2.md', 1)],
            'pricing': [ValidationIssue('C-003', ValidationSeverity.ERROR, 'msg', tmp_path / 'd3.md', 1)],
            'cross_references': [ValidationIssue('C-004', ValidationSeverity.WARNING, 'msg', tmp_path / 'd4.md', 1)]
        }

        data = reporter.analyze_conflicts(conflicts)

        assert data.total_conflicts == 4
        assert data.documents_affected == 4

        # Verify all types in recommendations
        recs = ' '.join(data.recommendations)
        assert 'status' in recs.lower() or 'pricing' in recs.lower() or 'tag' in recs.lower()
