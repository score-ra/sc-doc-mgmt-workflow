"""
Tests for YAML frontmatter validator.
"""

import pytest
from pathlib import Path
from src.core.validators.yaml_validator import (
    YAMLValidator,
    ValidationIssue,
    ValidationSeverity
)
from src.utils.config import Config
from src.utils.logger import Logger


class TestYAMLValidator:
    """Tests for YAMLValidator class."""

    @pytest.fixture
    def config(self, tmp_path):
        """Create a test configuration."""
        config_file = tmp_path / "config.yaml"
        config_content = """
processing:
  doc_directories:
    - "."
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"
  include_patterns:
    - "**/*.md"
  exclude_patterns:
    - "_meta/**"

validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - tags
      - status
    allowed_statuses:
      - draft
      - review
      - approved
      - active
      - deprecated
  markdown:
    enabled: false
  naming:
    enabled: false

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"
  verbose: true
  include_suggestions: true
  report_levels:
    - error
    - warning

logging:
  level: "INFO"
  file: "logs/test.log"
  console: true

performance:
  enable_cache: true
  parallel_workers: 0
  processing_timeout: 30
"""
        config_file.write_text(config_content)
        return Config(config_file)

    @pytest.fixture
    def logger(self, tmp_path):
        """Create a test logger."""
        log_file = tmp_path / "test.log"
        return Logger("test", log_file=log_file)

    @pytest.fixture
    def validator(self, config, logger):
        """Create a YAMLValidator instance."""
        return YAMLValidator(config, logger)

    @pytest.fixture
    def fixtures_dir(self):
        """Get path to test fixtures directory."""
        test_dir = Path(__file__).parent.parent.parent
        return test_dir / "fixtures" / "yaml_test_documents"

    def test_validator_initialization(self, validator):
        """Test validator initializes correctly."""
        assert validator.enabled is True
        assert 'title' in validator.required_fields
        assert 'tags' in validator.required_fields
        assert 'status' in validator.required_fields
        assert 'draft' in validator.allowed_statuses

    def test_validate_complete_valid_document(self, validator, fixtures_dir):
        """Test validation passes for document with all required fields."""
        test_file = fixtures_dir / "valid_complete.md"
        issues = validator.validate(test_file)

        assert len(issues) == 0

    def test_validate_missing_frontmatter(self, validator, fixtures_dir):
        """Test YAML-001: Missing frontmatter block."""
        test_file = fixtures_dir / "missing_frontmatter.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-001"
        assert issues[0].severity == ValidationSeverity.ERROR
        assert "missing" in issues[0].message.lower()

    def test_validate_missing_title(self, validator, fixtures_dir):
        """Test YAML-002: Missing required field (title)."""
        test_file = fixtures_dir / "missing_title.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-002"
        assert issues[0].severity == ValidationSeverity.ERROR
        assert "title" in issues[0].message.lower()

    def test_validate_missing_tags(self, validator, fixtures_dir):
        """Test YAML-002: Missing required field (tags)."""
        test_file = fixtures_dir / "missing_tags.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-002"
        assert "tags" in issues[0].message.lower()

    def test_validate_missing_status(self, validator, fixtures_dir):
        """Test YAML-002: Missing required field (status)."""
        test_file = fixtures_dir / "missing_status.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-002"
        assert "status" in issues[0].message.lower()

    def test_validate_invalid_status(self, validator, fixtures_dir):
        """Test YAML-003: Invalid status value."""
        test_file = fixtures_dir / "invalid_status.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-003"
        assert issues[0].severity == ValidationSeverity.ERROR
        assert "invalid" in issues[0].message.lower() or "status" in issues[0].message.lower()

    def test_validate_tags_as_string(self, validator, fixtures_dir):
        """Test YAML-004: Tags must be a list, not a string."""
        test_file = fixtures_dir / "tags_as_string.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].rule_id == "YAML-004"
        assert issues[0].severity == ValidationSeverity.ERROR
        assert "list" in issues[0].message.lower()

    def test_validate_malformed_yaml(self, validator, fixtures_dir):
        """Test malformed YAML handling."""
        test_file = fixtures_dir / "malformed_yaml.md"
        issues = validator.validate(test_file)

        assert len(issues) >= 1
        assert issues[0].rule_id == "YAML-001"
        assert "malformed" in issues[0].message.lower() or "yaml" in issues[0].message.lower()

    def test_validate_multiple_issues(self, validator, fixtures_dir):
        """Test document with multiple validation issues."""
        test_file = fixtures_dir / "multiple_issues.md"
        issues = validator.validate(test_file)

        # Should have: missing title, tags as string, invalid status
        assert len(issues) >= 3

        rule_ids = [issue.rule_id for issue in issues]
        assert "YAML-002" in rule_ids  # Missing title
        assert "YAML-003" in rule_ids  # Invalid status
        assert "YAML-004" in rule_ids  # Tags as string

    def test_validate_all_valid_statuses(self, validator, tmp_path):
        """Test that all allowed statuses are accepted."""
        allowed_statuses = ['draft', 'review', 'approved', 'active', 'deprecated']

        for status in allowed_statuses:
            test_file = tmp_path / f"test_{status}.md"
            test_file.write_text(
                f"---\ntitle: Test\ntags: [test]\nstatus: {status}\n---\n# Content",
                encoding='utf-8'
            )

            issues = validator.validate(test_file)
            assert len(issues) == 0, f"Status '{status}' should be valid"

    def test_validate_nonexistent_file(self, validator, tmp_path):
        """Test validation of non-existent file."""
        test_file = tmp_path / "nonexistent.md"
        issues = validator.validate(test_file)

        assert len(issues) == 1
        assert issues[0].severity == ValidationSeverity.ERROR
        assert "not found" in issues[0].message.lower()

    def test_validation_issue_str_format(self, tmp_path):
        """Test ValidationIssue string representation."""
        issue = ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="Test message",
            file_path=Path("test.md"),
            line_number=5,
            suggestion="Fix it"
        )

        str_repr = str(issue)
        assert "YAML-001" in str_repr
        assert "ERROR" in str_repr
        assert "Test message" in str_repr
        assert "test.md" in str_repr
        assert "Suggestion" in str_repr

    def test_validate_batch(self, validator, fixtures_dir):
        """Test batch validation of multiple files."""
        files = [
            fixtures_dir / "valid_complete.md",
            fixtures_dir / "missing_title.md",
            fixtures_dir / "invalid_status.md",
        ]

        results = validator.validate_batch(files)

        # valid_complete.md should have no issues
        assert fixtures_dir / "valid_complete.md" not in results

        # Other files should have issues
        assert fixtures_dir / "missing_title.md" in results
        assert fixtures_dir / "invalid_status.md" in results

    def test_get_error_count(self, validator):
        """Test error counting in validation issues."""
        issues = [
            ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message="Error 1",
                file_path=Path("test.md")
            ),
            ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.ERROR,
                message="Error 2",
                file_path=Path("test.md")
            ),
            ValidationIssue(
                rule_id="YAML-003",
                severity=ValidationSeverity.WARNING,
                message="Warning",
                file_path=Path("test.md")
            ),
        ]

        error_count = validator.get_error_count(issues)
        assert error_count == 2

    def test_get_warning_count(self, validator):
        """Test warning counting in validation issues."""
        issues = [
            ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message="Error",
                file_path=Path("test.md")
            ),
            ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.WARNING,
                message="Warning 1",
                file_path=Path("test.md")
            ),
            ValidationIssue(
                rule_id="YAML-003",
                severity=ValidationSeverity.WARNING,
                message="Warning 2",
                file_path=Path("test.md")
            ),
        ]

        warning_count = validator.get_warning_count(issues)
        assert warning_count == 2

    def test_validator_disabled(self, tmp_path, logger):
        """Test that validator respects enabled=false config."""
        config_file = tmp_path / "config.yaml"
        config_content = """
processing:
  doc_directories: ["."]
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"

validation:
  yaml:
    enabled: false
    required_fields:
      - title
  markdown:
    enabled: false
  naming:
    enabled: false

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "INFO"
  file: "logs/test.log"
  console: true

performance:
  enable_cache: true
  parallel_workers: 0
  processing_timeout: 30
"""
        config_file.write_text(config_content)
        config = Config(config_file)
        validator = YAMLValidator(config, logger)

        # Create invalid document
        test_file = tmp_path / "test.md"
        test_file.write_text("# No frontmatter", encoding='utf-8')

        # Should return empty list when disabled
        issues = validator.validate(test_file)
        assert len(issues) == 0

    def test_tags_with_non_string_items(self, validator, tmp_path):
        """Test YAML-004: Tags list with non-string items."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test\ntags: [tag1, 123, tag2]\nstatus: draft\n---\n# Content",
            encoding='utf-8'
        )

        issues = validator.validate(test_file)

        # Should have a warning about non-string tags
        warnings = [i for i in issues if i.severity == ValidationSeverity.WARNING]
        assert len(warnings) >= 1
        assert any("string" in w.message.lower() for w in warnings)

    def test_status_as_non_string(self, validator, tmp_path):
        """Test YAML-003: Status as non-string type."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test\ntags: [test]\nstatus: 123\n---\n# Content",
            encoding='utf-8'
        )

        issues = validator.validate(test_file)

        assert len(issues) >= 1
        status_issues = [i for i in issues if i.rule_id == "YAML-003"]
        assert len(status_issues) >= 1
        assert "string" in status_issues[0].message.lower()

    def test_suggestion_provided_for_issues(self, validator, fixtures_dir):
        """Test that validation issues include helpful suggestions."""
        test_file = fixtures_dir / "missing_title.md"
        issues = validator.validate(test_file)

        assert len(issues) >= 1
        assert issues[0].suggestion is not None
        assert len(issues[0].suggestion) > 0


class TestYAMLValidatorExclusions:
    """Tests for YAML validator file exclusion patterns (NEW-001)."""

    @pytest.fixture
    def config_with_exclusions(self, tmp_path):
        """Create a test configuration with exclusion patterns."""
        config_file = tmp_path / "config.yaml"
        config_content = """
processing:
  doc_directories:
    - "."
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"
  include_patterns:
    - "**/*.md"
  exclude_patterns:
    - "_meta/**"

validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - tags
      - status
    allowed_statuses:
      - draft
      - review
      - approved
      - active
      - deprecated
    exclude_patterns:
      - "README.md"
      - "**/README.md"
      - "CHANGELOG.md"
      - "CONTRIBUTING.md"
      - "LICENSE.md"
  markdown:
    enabled: false
  naming:
    enabled: false

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"
  verbose: true
  include_suggestions: true
  report_levels:
    - error
    - warning

logging:
  level: "INFO"
  file: "logs/test.log"
  console: true

performance:
  enable_cache: true
  parallel_workers: 0
  processing_timeout: 30
"""
        config_file.write_text(config_content)
        return Config(config_file)

    @pytest.fixture
    def logger(self, tmp_path):
        """Create a test logger."""
        log_file = tmp_path / "test.log"
        return Logger("test", log_file=log_file)

    @pytest.fixture
    def validator_with_exclusions(self, config_with_exclusions, logger):
        """Create a YAMLValidator instance with exclusion patterns."""
        return YAMLValidator(config_with_exclusions, logger)

    def test_exclude_root_readme(self, validator_with_exclusions, tmp_path):
        """Test that README.md at root level is excluded from validation."""
        readme_file = tmp_path / "README.md"
        readme_file.write_text("# Project\n\nNo frontmatter here!", encoding='utf-8')

        issues = validator_with_exclusions.validate(readme_file)

        # Should return empty list (file excluded)
        assert len(issues) == 0

    def test_exclude_nested_readme(self, validator_with_exclusions, tmp_path):
        """Test that README.md in subdirectories is excluded via glob pattern."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        readme_file = docs_dir / "README.md"
        readme_file.write_text("# Docs\n\nNo frontmatter!", encoding='utf-8')

        issues = validator_with_exclusions.validate(readme_file)

        # Should return empty list (file excluded via **/README.md pattern)
        assert len(issues) == 0

    def test_exclude_changelog(self, validator_with_exclusions, tmp_path):
        """Test that CHANGELOG.md is excluded from validation."""
        changelog_file = tmp_path / "CHANGELOG.md"
        changelog_file.write_text("# Changelog\n\n## v1.0\n- Initial release", encoding='utf-8')

        issues = validator_with_exclusions.validate(changelog_file)

        # Should return empty list (file excluded)
        assert len(issues) == 0

    def test_exclude_contributing(self, validator_with_exclusions, tmp_path):
        """Test that CONTRIBUTING.md is excluded from validation."""
        contributing_file = tmp_path / "CONTRIBUTING.md"
        contributing_file.write_text("# Contributing\n\nPlease submit PRs", encoding='utf-8')

        issues = validator_with_exclusions.validate(contributing_file)

        # Should return empty list (file excluded)
        assert len(issues) == 0

    def test_exclude_license(self, validator_with_exclusions, tmp_path):
        """Test that LICENSE.md is excluded from validation."""
        license_file = tmp_path / "LICENSE.md"
        license_file.write_text("# License\n\nMIT License", encoding='utf-8')

        issues = validator_with_exclusions.validate(license_file)

        # Should return empty list (file excluded)
        assert len(issues) == 0

    def test_non_excluded_file_still_validated(self, validator_with_exclusions, tmp_path):
        """Test that non-excluded files are still validated normally."""
        doc_file = tmp_path / "document.md"
        doc_file.write_text("# Document\n\nNo frontmatter here!", encoding='utf-8')

        issues = validator_with_exclusions.validate(doc_file)

        # Should have validation errors (not excluded)
        assert len(issues) > 0
        assert issues[0].rule_id == "YAML-001"

    def test_excluded_file_with_valid_frontmatter(self, validator_with_exclusions, tmp_path):
        """Test that excluded files are skipped even if they have valid frontmatter."""
        readme_file = tmp_path / "README.md"
        readme_file.write_text(
            "---\ntitle: Test\ntags: [test]\nstatus: draft\n---\n# Content",
            encoding='utf-8'
        )

        issues = validator_with_exclusions.validate(readme_file)

        # Should still be excluded (no validation performed)
        assert len(issues) == 0

    def test_batch_validation_with_exclusions(self, validator_with_exclusions, tmp_path):
        """Test batch validation respects exclusion patterns."""
        # Create excluded files
        readme = tmp_path / "README.md"
        readme.write_text("# README\n\nNo frontmatter", encoding='utf-8')

        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("# Changes\n\nNo frontmatter", encoding='utf-8')

        # Create non-excluded file with issues
        doc = tmp_path / "document.md"
        doc.write_text("# Document\n\nNo frontmatter", encoding='utf-8')

        files = [readme, changelog, doc]
        results = validator_with_exclusions.validate_batch(files)

        # Only document.md should have issues
        assert readme not in results
        assert changelog not in results
        assert doc in results

    def test_is_excluded_method(self, validator_with_exclusions, tmp_path):
        """Test the _is_excluded method directly."""
        readme = tmp_path / "README.md"
        doc = tmp_path / "document.md"
        nested_readme = tmp_path / "docs" / "README.md"

        assert validator_with_exclusions._is_excluded(readme) is True
        assert validator_with_exclusions._is_excluded(doc) is False
        assert validator_with_exclusions._is_excluded(nested_readme) is True

    def test_no_exclusion_patterns(self, tmp_path, logger):
        """Test validator works correctly with no exclusion patterns."""
        config_file = tmp_path / "config.yaml"
        config_content = """
processing:
  doc_directories: ["."]
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"

validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - tags
      - status
    allowed_statuses:
      - draft
  markdown:
    enabled: false
  naming:
    enabled: false

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "INFO"
  file: "logs/test.log"
  console: true

performance:
  enable_cache: true
  parallel_workers: 0
  processing_timeout: 30
"""
        config_file.write_text(config_content)
        config = Config(config_file)
        validator = YAMLValidator(config, logger)

        # README should be validated when no exclusion patterns
        readme = tmp_path / "README.md"
        readme.write_text("# README\n\nNo frontmatter", encoding='utf-8')

        issues = validator.validate(readme)

        # Should have validation errors (not excluded)
        assert len(issues) > 0

    def test_empty_exclusion_patterns(self, tmp_path, logger):
        """Test validator with explicitly empty exclusion patterns."""
        config_file = tmp_path / "config.yaml"
        config_content = """
processing:
  doc_directories: ["."]
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"

validation:
  yaml:
    enabled: true
    required_fields:
      - title
    allowed_statuses:
      - draft
    exclude_patterns: []
  markdown:
    enabled: false
  naming:
    enabled: false

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "INFO"
  file: "logs/test.log"
  console: true

performance:
  enable_cache: true
  parallel_workers: 0
  processing_timeout: 30
"""
        config_file.write_text(config_content)
        config = Config(config_file)
        validator = YAMLValidator(config, logger)

        readme = tmp_path / "README.md"
        readme.write_text("# README", encoding='utf-8')

        issues = validator.validate(readme)

        # Should have validation errors (empty exclusion list)
        assert len(issues) > 0

    def test_case_sensitive_pattern_matching(self, validator_with_exclusions, tmp_path):
        """Test that pattern matching is case-sensitive."""
        # README.md is excluded, but readme.md should not be (case-sensitive)
        readme_lower = tmp_path / "readme.md"
        readme_lower.write_text("# readme\n\nNo frontmatter", encoding='utf-8')

        issues = validator_with_exclusions.validate(readme_lower)

        # Should have validation errors (case-sensitive, not excluded)
        assert len(issues) > 0
