"""
Tests for auto-fix engine.
"""

import pytest
from pathlib import Path
from src.core.auto_fixer import AutoFixer, AutoFixResult
from src.core.validators.yaml_validator import YAMLValidator, ValidationIssue, ValidationSeverity
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.frontmatter import parse_frontmatter, has_frontmatter


class TestAutoFixer:
    """Tests for AutoFixer class."""

    @pytest.fixture
    def config(self, tmp_path):
        """Create a test configuration."""
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
      - review
      - approved
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
        return Config(config_file)

    @pytest.fixture
    def logger(self, tmp_path):
        """Create a test logger."""
        log_file = tmp_path / "test.log"
        return Logger("test", log_file=log_file)

    @pytest.fixture
    def fixer(self, config, logger):
        """Create an AutoFixer instance."""
        return AutoFixer(config, logger)

    @pytest.fixture
    def validator(self, config, logger):
        """Create a YAMLValidator instance for testing."""
        return YAMLValidator(config, logger)

    def test_fixer_initialization(self, fixer):
        """Test auto-fixer initializes correctly."""
        assert fixer.required_fields == ['title', 'tags', 'status']
        assert fixer.default_status == 'draft'
        assert fixer.backup_dir.name == '.backups'

    def test_fix_missing_frontmatter_preview(self, fixer, validator, tmp_path):
        """Test adding missing frontmatter in preview mode."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nContent here.", encoding='utf-8')

        issues = validator.validate(test_file)
        result = fixer.fix_document(test_file, issues, preview=True)

        assert result.success is True
        assert result.preview_only is True
        assert len(result.fixes_applied) > 0
        assert "frontmatter" in result.fixes_applied[0].lower()

        # File should not be modified in preview mode
        assert not has_frontmatter(test_file)

    def test_fix_missing_frontmatter_apply(self, fixer, tmp_path):
        """Test adding missing frontmatter with actual application."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nContent here.", encoding='utf-8')

        # Create issues for missing frontmatter AND missing fields
        issues = [
            ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message="YAML frontmatter block is missing",
                file_path=test_file
            ),
            ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.ERROR,
                message="Missing required field(s): title, tags, status",
                file_path=test_file
            )
        ]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True
        assert result.preview_only is False
        assert len(result.fixes_applied) > 0
        assert result.backup_path is not None
        assert result.backup_path.exists()

        # File should now have frontmatter
        assert has_frontmatter(test_file)

        # Verify frontmatter has required fields
        metadata = parse_frontmatter(test_file)
        assert 'title' in metadata
        assert 'tags' in metadata
        assert 'status' in metadata

    def test_extract_title_from_h1_heading(self, fixer, tmp_path):
        """Test extracting title from H1 heading."""
        test_file = tmp_path / "test.md"
        content = "# My Awesome Document\n\nSome content"
        test_file.write_text(content, encoding='utf-8')

        title = fixer._extract_title_from_content(content)

        assert title == "My Awesome Document"

    def test_extract_title_from_h1_with_formatting(self, fixer, tmp_path):
        """Test extracting title from H1 with markdown formatting."""
        test_file = tmp_path / "test.md"
        content = "# My **Bold** and *Italic* `Code` Title\n\nContent"
        test_file.write_text(content, encoding='utf-8')

        title = fixer._extract_title_from_content(content)

        assert title == "My Bold and Italic Code Title"

    def test_extract_title_no_h1(self, fixer, tmp_path):
        """Test extracting title when no H1 heading exists."""
        content = "## H2 Heading\n\nContent"

        title = fixer._extract_title_from_content(content)

        assert title is None

    def test_suggest_tags_from_path(self, fixer, tmp_path):
        """Test tag suggestion from file path."""
        # Create file in a pricing directory
        pricing_dir = tmp_path / "pricing"
        pricing_dir.mkdir()
        test_file = pricing_dir / "test.md"
        test_file.write_text("# Test", encoding='utf-8')

        tags = fixer._suggest_tags_from_path(test_file)

        assert 'pricing' in tags

    def test_suggest_tags_from_nested_path(self, fixer, tmp_path):
        """Test tag suggestion from nested path."""
        # Create file in nested directory
        nested_dir = tmp_path / "operations" / "policies"
        nested_dir.mkdir(parents=True)
        test_file = nested_dir / "test.md"
        test_file.write_text("# Test", encoding='utf-8')

        tags = fixer._suggest_tags_from_path(test_file)

        assert len(tags) >= 1
        assert 'operations' in tags or 'policies' in tags or 'policy' in tags

    def test_suggest_tags_default(self, fixer, tmp_path):
        """Test default tag suggestion when no known paths."""
        # Create file in unknown directory
        test_file = tmp_path / "unknown" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("# Test", encoding='utf-8')

        tags = fixer._suggest_tags_from_path(test_file)

        assert 'general' in tags

    def test_fix_missing_title_from_h1(self, fixer, tmp_path):
        """Test fixing missing title by extracting from H1."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntags: [test]\nstatus: draft\n---\n# Amazing Document\n\nContent",
            encoding='utf-8'
        )

        issues = [ValidationIssue(
            rule_id="YAML-002",
            severity=ValidationSeverity.ERROR,
            message="Missing required field(s): title",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True
        metadata = parse_frontmatter(test_file)
        assert metadata['title'] == "Amazing Document"

    def test_fix_missing_title_from_filename(self, fixer, tmp_path):
        """Test fixing missing title from filename when no H1."""
        test_file = tmp_path / "my-test-document.md"
        test_file.write_text(
            "---\ntags: [test]\nstatus: draft\n---\n\nNo H1 heading here.",
            encoding='utf-8'
        )

        issues = [ValidationIssue(
            rule_id="YAML-002",
            severity=ValidationSeverity.ERROR,
            message="Missing required field(s): title",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True
        metadata = parse_frontmatter(test_file)
        assert metadata['title'] == "My Test Document"

    def test_fix_tags_string_to_list(self, fixer, tmp_path):
        """Test converting tags from string to list."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test\ntags: pricing\nstatus: draft\n---\n# Content",
            encoding='utf-8'
        )

        issues = [ValidationIssue(
            rule_id="YAML-004",
            severity=ValidationSeverity.ERROR,
            message="Tags must be a list, got str",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True
        assert any("Converted tags" in fix for fix in result.fixes_applied)

        metadata = parse_frontmatter(test_file)
        assert isinstance(metadata['tags'], list)
        assert metadata['tags'] == ['pricing']

    def test_fix_multiple_issues(self, fixer, tmp_path):
        """Test fixing multiple issues in one document."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nContent", encoding='utf-8')

        issues = [
            ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message="YAML frontmatter block is missing",
                file_path=test_file
            ),
            ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.ERROR,
                message="Missing required field(s): title, tags, status",
                file_path=test_file
            )
        ]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True
        assert len(result.fixes_applied) >= 4  # frontmatter + title + tags + status

        metadata = parse_frontmatter(test_file)
        assert metadata['title'] == "Test Document"
        assert isinstance(metadata['tags'], list)
        assert metadata['status'] == 'draft'

    def test_create_backup(self, fixer, tmp_path):
        """Test backup creation before fixes."""
        test_file = tmp_path / "test.md"
        original_content = "# Test\n\nOriginal content"
        test_file.write_text(original_content, encoding='utf-8')

        backup_path = fixer._create_backup(test_file)

        assert backup_path.exists()
        assert backup_path.parent == fixer.backup_dir
        assert test_file.stem in backup_path.name

        # Verify backup has same content
        assert backup_path.read_text(encoding='utf-8') == original_content

    def test_fix_nonexistent_file(self, fixer, tmp_path):
        """Test fixing non-existent file returns error."""
        test_file = tmp_path / "nonexistent.md"

        issues = [ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="Missing frontmatter",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=True)

        assert result.success is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    def test_fix_batch(self, fixer, validator, tmp_path):
        """Test batch fixing of multiple documents."""
        # Create multiple documents with issues
        file1 = tmp_path / "file1.md"
        file1.write_text("# Doc 1\n\nContent", encoding='utf-8')

        file2 = tmp_path / "file2.md"
        file2.write_text("---\ntags: pricing\nstatus: draft\n---\n# Doc 2", encoding='utf-8')

        # Validate and get issues
        issues1 = validator.validate(file1)
        issues2 = validator.validate(file2)

        documents = {
            file1: issues1,
            file2: issues2
        }

        # Fix in batch (preview)
        results = fixer.fix_batch(documents, preview=True)

        assert len(results) == 2
        assert file1 in results
        assert file2 in results
        assert results[file1].success is True
        assert results[file2].success is True

    def test_can_fix_validation_issue(self, fixer, tmp_path):
        """Test checking if an issue can be auto-fixed."""
        fixable_issue = ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="Missing frontmatter",
            file_path=Path("test.md")
        )

        unfixable_issue = ValidationIssue(
            rule_id="YAML-003",
            severity=ValidationSeverity.ERROR,
            message="Invalid status",
            file_path=Path("test.md")
        )

        assert fixer.can_fix(fixable_issue) is True
        assert fixer.can_fix(unfixable_issue) is False

    def test_auto_fix_result_str_format(self):
        """Test AutoFixResult string representation."""
        result = AutoFixResult(
            file_path=Path("test.md"),
            fixes_applied=["Added frontmatter", "Added title"],
            preview_only=False,
            backup_path=Path("backup/test.md"),
            success=True
        )

        str_repr = str(result)
        assert "test.md" in str_repr
        assert "Added frontmatter" in str_repr
        assert "Added title" in str_repr
        assert "Backup" in str_repr

    def test_preview_mode_doesnt_modify_file(self, fixer, tmp_path):
        """Test that preview mode doesn't modify the file."""
        test_file = tmp_path / "test.md"
        original_content = "# Test\n\nContent"
        test_file.write_text(original_content, encoding='utf-8')

        issues = [ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="Missing frontmatter",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=True)

        assert result.preview_only is True
        assert result.backup_path is None
        assert test_file.read_text(encoding='utf-8') == original_content

    def test_content_preserved_after_fix(self, fixer, tmp_path):
        """Test that markdown content is preserved after fixes."""
        test_file = tmp_path / "test.md"
        markdown_content = "# Test\n\n- List item 1\n- List item 2\n\n```python\ncode\n```"
        test_file.write_text(markdown_content, encoding='utf-8')

        issues = [ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="Missing frontmatter",
            file_path=test_file
        )]

        result = fixer.fix_document(test_file, issues, preview=False)

        assert result.success is True

        # Read file and check content is preserved
        content = test_file.read_text(encoding='utf-8')
        assert "# Test" in content
        assert "List item 1" in content
        assert "```python" in content
        assert "code" in content
