"""
Tests for file and directory naming convention validator.
"""

import pytest
from pathlib import Path
from src.core.validators.naming_validator import NamingValidator
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity
from src.utils.config import Config
from src.utils.logger import Logger


class TestNamingValidator:
    """Tests for NamingValidator class."""

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
    enabled: false
  naming:
    enabled: true
    pattern: "lowercase-with-hyphens"
    max_length: 50
    min_length: 5
    no_version_numbers: true

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
        """Create a NamingValidator instance."""
        return NamingValidator(config, logger)

    @pytest.fixture
    def test_docs_dir(self, tmp_path):
        """Create a temporary directory structure for testing."""
        # Create base directory
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        return docs_dir

    def test_validator_initialization(self, validator):
        """Test validator initializes correctly."""
        assert validator.enabled is True
        assert validator.pattern == "lowercase-with-hyphens"
        assert validator.max_length == 50
        assert validator.min_length == 5
        assert validator.no_version_numbers is True
        assert 'README.md' in validator.allow_uppercase_files
        assert '.csv' in validator.allow_spaces_extensions

    def test_validate_valid_filename(self, validator, test_docs_dir):
        """Test validation passes for correctly named file."""
        # Create valid file
        test_file = test_docs_dir / "pricing-strategy.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) == 0

    def test_validate_uppercase_filename(self, validator, test_docs_dir):
        """Test validation fails for uppercase in filename."""
        # Create file with uppercase
        test_file = test_docs_dir / "PricingStrategy.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-001" for issue in issues)
        assert any("lowercase-with-hyphens" in issue.message for issue in issues)
        assert any("pricing-strategy.md" in issue.suggestion for issue in issues)

    def test_validate_spaces_in_filename(self, validator, test_docs_dir):
        """Test validation fails for spaces in filename."""
        # Create file with spaces
        test_file = test_docs_dir / "pricing strategy.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-002" for issue in issues)
        assert any("spaces" in issue.message.lower() for issue in issues)
        assert any("pricing-strategy.md" in issue.suggestion for issue in issues)

    def test_validate_filename_too_long(self, validator, test_docs_dir):
        """Test validation fails for filename exceeding max length."""
        # Create file with very long name (>50 chars)
        long_name = "a" * 60 + ".md"
        test_file = test_docs_dir / long_name
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-003" for issue in issues)
        assert any("exceeds maximum length" in issue.message for issue in issues)

    def test_validate_filename_too_short(self, validator, test_docs_dir):
        """Test validation fails for filename below min length."""
        # Create file with very short name (<5 chars)
        test_file = test_docs_dir / "abc.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-004" for issue in issues)
        assert any("too short" in issue.message.lower() for issue in issues)

    def test_validate_version_number_in_filename(self, validator, test_docs_dir):
        """Test validation fails for version numbers in filename."""
        test_cases = [
            "pricing-strategy-v1.md",
            "pricing-strategy-v1.0.md",
            "pricing-strategy_v2.md",
            "pricing-v1-strategy.md",
        ]

        for filename in test_cases:
            test_file = test_docs_dir / filename
            test_file.write_text("# Test")

            issues = validator.validate(test_file)
            assert any(issue.rule_id == "NAME-005" for issue in issues), \
                f"Expected NAME-005 for {filename}"
            assert any("version number" in issue.message.lower() for issue in issues)

    def test_readme_exception(self, validator, test_docs_dir):
        """Test README.md is exempt from uppercase check."""
        # Create README.md (uppercase is allowed)
        test_file = test_docs_dir / "README.md"
        test_file.write_text("# README")

        issues = validator.validate(test_file)
        # Should not flag NAME-001 (uppercase) for README.md
        assert not any(issue.rule_id == "NAME-001" for issue in issues)

    def test_csv_exception(self, validator, test_docs_dir):
        """Test .csv files are exempt from space check."""
        # Create .csv file with spaces (allowed)
        test_file = test_docs_dir / "client data.csv"
        test_file.write_text("name,email\n")

        issues = validator.validate(test_file)
        # Should not flag NAME-002 (spaces) for .csv files
        assert not any(issue.rule_id == "NAME-002" for issue in issues)

    def test_validate_uppercase_directory(self, validator, test_docs_dir):
        """Test validation fails for uppercase in directory names."""
        # Create directory structure with uppercase
        subdir = test_docs_dir / "UppercaseDir"
        subdir.mkdir()
        test_file = subdir / "pricing-strategy.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file, base_path=test_docs_dir)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-001" for issue in issues)
        assert any("Directory name must be lowercase" in issue.message for issue in issues)
        assert any("uppercasedir" in issue.suggestion.lower() for issue in issues)

    def test_validate_spaces_in_directory(self, validator, test_docs_dir):
        """Test validation fails for spaces in directory names."""
        # Create directory with spaces
        subdir = test_docs_dir / "pricing strategy"
        subdir.mkdir()
        test_file = subdir / "overview.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file, base_path=test_docs_dir)
        assert len(issues) >= 1
        assert any(issue.rule_id == "NAME-002" for issue in issues)
        assert any("Directory name contains spaces" in issue.message for issue in issues)
        assert any("pricing-strategy" in issue.suggestion for issue in issues)

    def test_validate_nested_directories(self, validator, test_docs_dir):
        """Test validation checks all parent directories."""
        # Create nested structure with violations
        level1 = test_docs_dir / "GoodDir"
        level1.mkdir()
        level2 = level1 / "bad dir"
        level2.mkdir()
        test_file = level2 / "document.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file, base_path=test_docs_dir)
        # Should find both uppercase and space violations
        name_001_issues = [i for i in issues if i.rule_id == "NAME-001"]
        name_002_issues = [i for i in issues if i.rule_id == "NAME-002"]

        assert len(name_001_issues) >= 1  # GoodDir
        assert len(name_002_issues) >= 1  # "bad dir"

    def test_convert_to_lowercase_with_hyphens(self, validator):
        """Test filename conversion helper."""
        test_cases = [
            ("PricingStrategy", "pricing-strategy"),
            ("pricing_strategy", "pricing-strategy"),
            ("Pricing Strategy", "pricing-strategy"),
            ("PricingStrategyV2", "pricing-strategy-v2"),
            ("PRICING-STRATEGY", "pricing-strategy"),
            ("pricing--strategy", "pricing-strategy"),  # Multiple hyphens
            ("-pricing-strategy-", "pricing-strategy"),  # Leading/trailing hyphens
        ]

        for input_text, expected_output in test_cases:
            result = validator._convert_to_lowercase_with_hyphens(input_text)
            assert result == expected_output, \
                f"Expected '{expected_output}', got '{result}' for '{input_text}'"

    def test_get_rename_suggestions(self, validator, test_docs_dir):
        """Test rename suggestion generation."""
        # Create file with violation
        test_file = test_docs_dir / "Pricing Strategy.md"
        test_file.write_text("# Test")

        suggestions = validator.get_rename_suggestions(test_file)
        assert 'filename' in suggestions
        assert suggestions['filename'] == 'pricing-strategy.md'

    def test_validate_batch(self, validator, test_docs_dir):
        """Test batch validation of multiple files."""
        # Create multiple test files with various issues
        files = {
            "valid-filename.md": [],  # No issues
            "InvalidFilename.md": ["NAME-001"],  # Uppercase
            "file name.md": ["NAME-002"],  # Spaces
            "a.md": ["NAME-004"],  # Too short
        }

        file_paths = []
        for filename, expected_rules in files.items():
            test_file = test_docs_dir / filename
            test_file.write_text("# Test")
            file_paths.append(test_file)

        results = validator.validate_batch(file_paths)

        # Check that files with issues are in results
        assert (test_docs_dir / "InvalidFilename.md") in results
        assert (test_docs_dir / "file name.md") in results
        assert (test_docs_dir / "a.md") in results

        # Valid file should not be in results
        assert (test_docs_dir / "valid-filename.md") not in results

    def test_validator_disabled(self, config, logger, test_docs_dir):
        """Test validator can be disabled via configuration."""
        # Modify config to disable naming validation
        config.config_data['validation']['naming']['enabled'] = False
        validator = NamingValidator(config, logger)

        # Create file with violations
        test_file = test_docs_dir / "Invalid Filename.md"
        test_file.write_text("# Test")

        issues = validator.validate(test_file)
        assert len(issues) == 0  # Should skip validation when disabled

    def test_nonexistent_file(self, validator):
        """Test validation handles nonexistent files gracefully."""
        nonexistent = Path("/nonexistent/file.md")
        issues = validator.validate(nonexistent)

        assert len(issues) == 1
        assert issues[0].rule_id == "NAME-000"
        assert "not found" in issues[0].message.lower()


class TestNamingValidatorRealDocs:
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
  include_patterns:
    - "**/*.md"
  exclude_patterns:
    - "_meta/**"

validation:
  yaml:
    enabled: false
  markdown:
    enabled: false
  naming:
    enabled: true
    pattern: "lowercase-with-hyphens"
    max_length: 50
    min_length: 5
    no_version_numbers: true

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
        """Create a NamingValidator instance."""
        return NamingValidator(config, logger)

    def test_detect_uppercase_directories(self, validator, real_docs_path):
        """Test detection of uppercase directories in real documentation."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Known violations from DOCUMENTATION_REVIEW_REPORT.md:
        # 08-reference/platforms/Extendly/
        # 08-reference/platforms/GHL/
        known_violations = [
            real_docs_path / "08-reference" / "platforms" / "Extendly" / "training-docs" / "automation ecosystem map.md",
            real_docs_path / "08-reference" / "platforms" / "GHL" / "user-training-ghl-info.md",
        ]

        violations_found = 0
        for doc_path in known_violations:
            if doc_path.exists():
                issues = validator.validate(doc_path, base_path=real_docs_path)
                # Should find NAME-001 (uppercase directory)
                name_001_issues = [i for i in issues if i.rule_id == "NAME-001"]
                if len(name_001_issues) > 0:
                    violations_found += 1

        # Should find at least some of the known violations
        assert violations_found > 0, "Expected to find uppercase directory violations"

    def test_detect_spaces_in_filenames(self, validator, real_docs_path):
        """Test detection of spaces in filenames in real documentation."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Known violations from review:
        # "steps to fix domain issue.md"
        # "automation ecosystem map.md"
        known_violations = [
            real_docs_path / "02-marketing-brand" / "website" / "issues-to-fix" / "steps to fix domain issue.md",
            real_docs_path / "08-reference" / "platforms" / "Extendly" / "training-docs" / "automation ecosystem map.md",
        ]

        violations_found = 0
        for doc_path in known_violations:
            if doc_path.exists():
                issues = validator.validate(doc_path, base_path=real_docs_path)
                # Should find NAME-002 (spaces in filename)
                name_002_issues = [i for i in issues if i.rule_id == "NAME-002"]
                if len(name_002_issues) > 0:
                    violations_found += 1

        # Should find at least some of the known violations
        assert violations_found > 0, "Expected to find space-in-filename violations"

    def test_scan_entire_repository(self, validator, real_docs_path):
        """Test scanning entire repository for naming violations."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Find all markdown files
        all_docs = list(real_docs_path.glob("**/*.md"))
        # Exclude READMEs
        all_docs = [d for d in all_docs if d.name != "README.md"]

        # Should have 150+ documents
        assert len(all_docs) > 150, f"Expected >150 docs, found {len(all_docs)}"

        # Validate all and collect statistics
        results = validator.validate_batch(all_docs[:50], base_path=real_docs_path)  # Test first 50

        # Should find at least some violations (44 known from review)
        total_violations = sum(len(issues) for issues in results.values())
        assert total_violations > 0, "Expected to find naming violations in real docs"

        # Count by rule
        rule_counts = {}
        for issues in results.values():
            for issue in issues:
                rule_counts[issue.rule_id] = rule_counts.get(issue.rule_id, 0) + 1

        print(f"\nNaming violations found (first 50 docs):")
        for rule_id, count in sorted(rule_counts.items()):
            print(f"  {rule_id}: {count}")
