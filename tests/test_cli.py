"""
Tests for the CLI interface.

Tests command-line interface functionality including command parsing,
validation execution, and report generation.
"""

import pytest
from click.testing import CliRunner
from pathlib import Path
import json
import tempfile
import shutil

from src.cli import cli


class TestCLIBasics:
    """Test basic CLI functionality."""

    def test_cli_help(self):
        """Test --help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Symphony Core Document Management Workflow' in result.output
        assert 'validate' in result.output

    def test_cli_version(self):
        """Test --version output."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'version 1.0.0' in result.output

    def test_validate_help(self):
        """Test validate command --help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ['validate', '--help'])
        assert result.exit_code == 0
        assert 'Validate markdown documents' in result.output
        assert '--path' in result.output
        assert '--tags' in result.output
        assert '--force' in result.output
        assert '--auto-fix' in result.output
        assert '--conflicts' in result.output


class TestCLIValidation:
    """Test validation command."""

    def test_validate_with_fixtures(self):
        """Test validate command on fixtures directory."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'tests/fixtures',
            '--force'
        ])
        # Exit code should be 0 or 1 depending on whether errors found
        assert result.exit_code in [0, 1]
        assert 'VALIDATION REPORT' in result.output
        assert 'Documents Scanned' in result.output

    def test_validate_json_format(self):
        """Test JSON format output."""
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_file = f.name

        try:
            result = runner.invoke(cli, [
                'validate',
                '--path', 'tests/fixtures',
                '--force',
                '--format', 'json',
                '--output', output_file
            ])

            # Check file was created
            assert Path(output_file).exists()

            # Check JSON is valid
            with open(output_file, 'r') as f:
                data = json.load(f)
                assert 'summary' in data
                assert 'violations' in data
                assert 'total' in data['summary']
                assert 'passed' in data['summary']
                assert 'failed' in data['summary']

        finally:
            if Path(output_file).exists():
                Path(output_file).unlink()

    def test_validate_markdown_format(self):
        """Test markdown format output."""
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            output_file = f.name

        try:
            result = runner.invoke(cli, [
                'validate',
                '--path', 'tests/fixtures',
                '--force',
                '--format', 'markdown',
                '--output', output_file
            ])

            # Check file was created
            assert Path(output_file).exists()

            # Check markdown content
            content = Path(output_file).read_text()
            assert '# Symphony Core Validation Report' in content
            assert '## Summary' in content
            assert 'Documents Scanned' in content

        finally:
            if Path(output_file).exists():
                Path(output_file).unlink()

    def test_validate_nonexistent_path(self):
        """Test validation with nonexistent path."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'nonexistent/path'
        ])
        # Click should reject the path before we even get to validation
        assert result.exit_code != 0

    def test_preview_without_autofix(self):
        """Test that --preview requires --auto-fix."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'tests/fixtures',
            '--preview'
        ])
        assert result.exit_code == 1
        assert '--preview requires --auto-fix' in result.output


class TestCLIConflictDetection:
    """Test conflict detection mode."""

    def test_conflicts_flag(self):
        """Test --conflicts flag."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'tests/fixtures',
            '--conflicts'
        ])
        # Should complete (exit code depends on whether conflicts found)
        assert result.exit_code in [0, 1]
        assert 'Mode: Conflict Detection' in result.output


class TestCLIEdgeCases:
    """Test edge cases and error handling."""

    def test_validate_empty_directory(self):
        """Test validation on empty directory."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(cli, [
                'validate',
                '--path', tmpdir,
                '--force'
            ])
            assert result.exit_code == 0
            assert 'No documents to process' in result.output

    def test_force_flag(self):
        """Test --force flag."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'tests/fixtures',
            '--force'
        ])
        assert 'Force: Yes' in result.output

    def test_force_flag_default(self):
        """Test force flag defaults to No."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'validate',
            '--path', 'tests/fixtures'
        ])
        assert 'Force: No' in result.output


class TestCLIRealDocs:
    """Test CLI on real documentation (if available)."""

    @pytest.mark.skipif(
        not Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\09-clients").exists(),
        reason="Real docs not available"
    )
    def test_validate_real_docs(self):
        """Test validation on real 09-clients folder (100% pass rate expected)."""
        runner = CliRunner()
        docs_path = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\09-clients")

        result = runner.invoke(cli, [
            'validate',
            '--path', str(docs_path),
            '--force'
        ])

        # 09-clients folder should have 100% pass rate
        assert result.exit_code == 0
        assert 'VALIDATION REPORT' in result.output
