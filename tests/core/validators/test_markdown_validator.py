"""
Tests for markdown syntax validator.
"""

import pytest
from pathlib import Path
from src.core.validators.markdown_validator import MarkdownValidator
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity
from src.utils.config import Config
from src.utils.logger import Logger


class TestMarkdownValidator:
    """Tests for MarkdownValidator class."""

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
    enabled: false
  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true
    relative_links_only: true
    horizontal_rule_format: "---"
    check_trailing_whitespace: true
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
        """Create a MarkdownValidator instance."""
        return MarkdownValidator(config, logger)

    @pytest.fixture
    def test_docs_dir(self, tmp_path):
        """Create a temporary directory structure for testing."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        return docs_dir

    def test_validator_initialization(self, validator):
        """Test validator initializes correctly."""
        assert validator.enabled is True
        assert validator.enforce_heading_hierarchy is True
        assert validator.require_language_in_code_blocks is True
        assert validator.relative_links_only is True
        assert validator.horizontal_rule_format == "---"
        assert validator.check_trailing_whitespace is True

    def test_validate_good_markdown(self, validator, test_docs_dir):
        """Test validation passes for well-formatted markdown."""
        content = """# Main Title

This is a paragraph.

## Section 1

Some content here.

### Subsection 1.1

More content.

```python
print("Hello, World!")
```

---

[Link to other doc](./other.md)
"""
        test_file = test_docs_dir / "good-doc.md"
        test_file.write_text(content)

        # Create the linked file so link validation passes
        (test_docs_dir / "other.md").write_text("# Other")

        issues = validator.validate(test_file, base_path=test_docs_dir)
        # Should have no errors or warnings (maybe INFO level for trailing whitespace)
        errors_and_warnings = [
            i for i in issues
            if i.severity in [ValidationSeverity.ERROR, ValidationSeverity.WARNING]
        ]
        assert len(errors_and_warnings) == 0

    def test_heading_hierarchy_violation(self, validator, test_docs_dir):
        """Test detection of skipped heading levels."""
        content = """# Main Title

### Skipped H2

This should be flagged.
"""
        test_file = test_docs_dir / "bad-hierarchy.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        assert any(issue.rule_id == "MD-001" for issue in issues)
        assert any("skips level" in issue.message.lower() for issue in issues)

    def test_multiple_heading_violations(self, validator, test_docs_dir):
        """Test detection of multiple heading hierarchy violations."""
        content = """# Title

### H3 (skipped H2)

##### H5 (skipped H4)

## Back to H2
"""
        test_file = test_docs_dir / "multiple-violations.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_001_issues = [i for i in issues if i.rule_id == "MD-001"]
        assert len(md_001_issues) >= 2  # Should catch both skips

    def test_code_block_without_language(self, validator, test_docs_dir):
        """Test detection of code blocks without language."""
        content = """# Title

```
print("No language specified")
```

This should be flagged.
"""
        test_file = test_docs_dir / "no-lang.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        assert any(issue.rule_id == "MD-002" for issue in issues)
        assert any("language specification" in issue.message.lower() for issue in issues)

    def test_code_block_with_language(self, validator, test_docs_dir):
        """Test code block with language passes validation."""
        content = """# Title

```python
print("Language specified")
```

```javascript
console.log("Also good");
```
"""
        test_file = test_docs_dir / "with-lang.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_002_issues = [i for i in issues if i.rule_id == "MD-002"]
        assert len(md_002_issues) == 0

    def test_unclosed_code_block(self, validator, test_docs_dir):
        """Test detection of unclosed code blocks."""
        content = """# Title

```python
print("No closing fence")
"""
        test_file = test_docs_dir / "unclosed.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        assert any(issue.rule_id == "MD-002" for issue in issues)
        assert any(issue.severity == ValidationSeverity.ERROR for issue in issues)
        assert any("unclosed" in issue.message.lower() for issue in issues)

    def test_broken_relative_link(self, validator, test_docs_dir):
        """Test detection of broken relative links."""
        content = """# Title

[Link to nonexistent file](./does-not-exist.md)
"""
        test_file = test_docs_dir / "broken-link.md"
        test_file.write_text(content)

        issues = validator.validate(test_file, base_path=test_docs_dir)
        assert any(issue.rule_id == "MD-003" for issue in issues)
        assert any("broken link" in issue.message.lower() for issue in issues)

    def test_valid_relative_link(self, validator, test_docs_dir):
        """Test valid relative links pass validation."""
        content = """# Title

[Link to existing file](./exists.md)
"""
        test_file = test_docs_dir / "good-link.md"
        test_file.write_text(content)

        # Create the target file
        (test_docs_dir / "exists.md").write_text("# Exists")

        issues = validator.validate(test_file, base_path=test_docs_dir)
        md_003_errors = [
            i for i in issues
            if i.rule_id == "MD-003" and i.severity == ValidationSeverity.ERROR
        ]
        assert len(md_003_errors) == 0

    def test_absolute_url_in_internal_doc(self, validator, test_docs_dir):
        """Test detection of absolute URLs when relative_links_only is True."""
        content = """# Title

[External link](https://example.com)
"""
        test_file = test_docs_dir / "absolute-url.md"
        test_file.write_text(content)

        issues = validator.validate(test_file, base_path=test_docs_dir)
        md_003_issues = [i for i in issues if i.rule_id == "MD-003"]
        # Should flag as INFO (not ERROR)
        assert any(
            i.severity == ValidationSeverity.INFO and "absolute url" in i.message.lower()
            for i in md_003_issues
        )

    def test_anchor_links_ignored(self, validator, test_docs_dir):
        """Test that anchor links (same page) are not flagged."""
        content = """# Title

[Link to section](#section-1)

## Section 1
"""
        test_file = test_docs_dir / "anchor-link.md"
        test_file.write_text(content)

        issues = validator.validate(test_file, base_path=test_docs_dir)
        md_003_issues = [i for i in issues if i.rule_id == "MD-003"]
        assert len(md_003_issues) == 0

    def test_trailing_whitespace(self, validator, test_docs_dir):
        """Test detection of trailing whitespace."""
        content = "# Title   \n\nSome content here.   \n"
        test_file = test_docs_dir / "trailing-ws.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_004_issues = [i for i in issues if i.rule_id == "MD-004"]
        assert len(md_004_issues) >= 1  # At least one line with trailing whitespace

    def test_no_trailing_whitespace(self, validator, test_docs_dir):
        """Test no false positives for trailing whitespace."""
        content = "# Title\n\nSome content here.\n"
        test_file = test_docs_dir / "no-trailing-ws.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_004_issues = [i for i in issues if i.rule_id == "MD-004"]
        assert len(md_004_issues) == 0

    def test_horizontal_rule_format_mismatch(self, validator, test_docs_dir):
        """Test detection of non-standard horizontal rule format."""
        content = """# Title

***

Content after rule.
"""
        test_file = test_docs_dir / "hr-mismatch.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_005_issues = [i for i in issues if i.rule_id == "MD-005"]
        assert len(md_005_issues) >= 1
        assert any("horizontal rule" in i.message.lower() for i in md_005_issues)

    def test_horizontal_rule_format_match(self, validator, test_docs_dir):
        """Test correct horizontal rule format passes."""
        content = """# Title

---

Content after rule.
"""
        test_file = test_docs_dir / "hr-match.md"
        test_file.write_text(content)

        issues = validator.validate(test_file)
        md_005_issues = [i for i in issues if i.rule_id == "MD-005"]
        assert len(md_005_issues) == 0

    def test_validate_batch(self, validator, test_docs_dir):
        """Test batch validation of multiple files."""
        # Create test files
        good_file = test_docs_dir / "good.md"
        good_file.write_text("# Title\n\n## Section\n")

        bad_hierarchy = test_docs_dir / "bad-hierarchy.md"
        bad_hierarchy.write_text("# Title\n\n### Skipped\n")

        bad_code = test_docs_dir / "bad-code.md"
        bad_code.write_text("# Title\n\n```\nno lang\n```\n")

        files = [good_file, bad_hierarchy, bad_code]
        results = validator.validate_batch(files)

        # Good file should not be in results (or have no errors/warnings)
        if good_file in results:
            errors_warnings = [
                i for i in results[good_file]
                if i.severity in [ValidationSeverity.ERROR, ValidationSeverity.WARNING]
            ]
            assert len(errors_warnings) == 0

        # Bad files should be in results
        assert bad_hierarchy in results
        assert bad_code in results

    def test_validator_disabled(self, config, logger, test_docs_dir):
        """Test validator can be disabled via configuration."""
        config.config_data['validation']['markdown']['enabled'] = False
        validator = MarkdownValidator(config, logger)

        # Create file with violations
        test_file = test_docs_dir / "bad.md"
        test_file.write_text("# Title\n\n### Skipped\n\n```\nno lang\n```\n")

        issues = validator.validate(test_file)
        assert len(issues) == 0  # Should skip validation when disabled

    def test_nonexistent_file(self, validator):
        """Test validation handles nonexistent files gracefully."""
        nonexistent = Path("/nonexistent/file.md")
        issues = validator.validate(nonexistent)

        assert len(issues) == 1
        assert issues[0].rule_id == "MD-000"
        assert "not found" in issues[0].message.lower()


class TestMarkdownValidatorRealDocs:
    """Tests with real Symphony Core documentation (if available)."""

    @pytest.fixture
    def real_docs_path(self):
        """Path to real Symphony Core documentation repository."""
        return Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")

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

validation:
  yaml:
    enabled: false
  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true
    relative_links_only: true
    horizontal_rule_format: "---"
    check_trailing_whitespace: false  # Too noisy for real docs

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "WARNING"
  file: "logs/test.log"
  console: false

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
        return Logger("test", log_file=log_file, log_level="WARNING")

    @pytest.fixture
    def validator(self, config, logger):
        """Create a MarkdownValidator instance."""
        return MarkdownValidator(config, logger)

    def test_validate_strategy_docs(self, validator, real_docs_path):
        """Test validation on real strategy documents."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        strategy_dir = real_docs_path / "01-strategy"
        if not strategy_dir.exists():
            pytest.skip("Strategy directory not found")

        strategy_docs = list(strategy_dir.glob("**/*.md"))
        strategy_docs = [d for d in strategy_docs if d.name != "README.md"]

        # Should have some docs
        assert len(strategy_docs) > 0

        # Validate all without crashing
        results = validator.validate_batch(strategy_docs[:5], base_path=real_docs_path)

        # Should complete without exceptions (some docs may have issues)
        print(f"\nValidated {len(strategy_docs[:5])} strategy docs")
        if results:
            print(f"Found issues in {len(results)} docs")

    def test_scan_all_docs_without_crashing(self, validator, real_docs_path):
        """Test that validator can process all docs without crashing."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        all_docs = list(real_docs_path.glob("**/*.md"))
        all_docs = [d for d in all_docs if d.name != "README.md"]

        # Should have 150+ documents
        assert len(all_docs) > 150

        # Validate first 20 to keep test fast
        sample_docs = all_docs[:20]
        results = validator.validate_batch(sample_docs, base_path=real_docs_path)

        # Main goal: don't crash! (SUCCESS is completing without exception)
        print(f"\nValidated {len(sample_docs)} documents without crashing")
        print(f"Found issues in {len(results)} docs")

        # Count issues by rule
        rule_counts = {}
        for issues in results.values():
            for issue in issues:
                rule_counts[issue.rule_id] = rule_counts.get(issue.rule_id, 0) + 1

        if rule_counts:
            print("Issues found:")
            for rule_id, count in sorted(rule_counts.items()):
                print(f"  {rule_id}: {count}")
