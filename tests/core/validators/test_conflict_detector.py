"""
Tests for conflict detector.
"""

import pytest
from pathlib import Path
from src.core.validators.conflict_detector import ConflictDetector
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity
from src.utils.config import Config
from src.utils.logger import Logger


class TestConflictDetector:
    """Tests for ConflictDetector class."""

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
  conflicts:
    enabled: true
    tag_synonyms:
      ghl: gohighlevel
      wp: wordpress

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "INFO"
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
        return Logger("test", log_file=log_file)

    @pytest.fixture
    def detector(self, config, logger):
        """Create a ConflictDetector instance."""
        return ConflictDetector(config, logger)

    @pytest.fixture
    def test_docs_dir(self, tmp_path):
        """Create a temporary directory structure for testing."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        return docs_dir

    def test_detector_initialization(self, detector):
        """Test detector initializes correctly."""
        assert detector.enabled is True
        assert 'draft' in detector.allowed_status_values
        assert 'ghl' in detector.tag_synonyms
        assert detector.tag_synonyms['ghl'] == 'gohighlevel'

    def test_no_conflicts_in_single_doc(self, detector, test_docs_dir):
        """Test no conflicts when analyzing single document."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Test Doc
tags: [pricing]
status: draft
---

# Test Document

Some content.
""")

        conflicts = detector.detect_conflicts([doc1])
        all_issues = sum((len(issues) for issues in conflicts.values()), 0)
        assert all_issues == 0

    def test_status_case_conflict(self, detector, test_docs_dir):
        """Test detection of status value case conflicts."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [test]
status: draft
---
Content
""")

        doc2 = test_docs_dir / "doc2.md"
        doc2.write_text("""---
title: Doc 2
tags: [test]
status: Draft
---
Content
""")

        conflicts = detector.detect_conflicts([doc1, doc2])
        status_conflicts = conflicts['status']

        assert len(status_conflicts) >= 1
        assert any(issue.rule_id == "CONFLICT-001" for issue in status_conflicts)
        assert any("case variations" in issue.message.lower() for issue in status_conflicts)
        # Verify line number is tracked (status is on line 4 in both docs)
        for issue in status_conflicts:
            if "case variations" in issue.message.lower():
                assert issue.line_number == 4, f"Expected line 4, got {issue.line_number}"

    def test_non_standard_status(self, detector, test_docs_dir):
        """Test detection of non-standard status values."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [test]
status: published
---
Content
""")

        doc2 = test_docs_dir / "doc2.md"
        doc2.write_text("""---
title: Doc 2
tags: [test]
status: complete
---
Content
""")

        conflicts = detector.detect_conflicts([doc1, doc2])
        status_conflicts = conflicts['status']

        # Should flag both non-standard values
        non_standard_issues = [i for i in status_conflicts if "non-standard" in i.message.lower()]
        assert len(non_standard_issues) >= 2
        # Verify line numbers are tracked
        for issue in non_standard_issues:
            assert issue.line_number == 4, f"Expected line 4, got {issue.line_number}"

    def test_tag_synonym_conflict(self, detector, test_docs_dir):
        """Test detection of tag synonym conflicts."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [ghl, platform]
status: draft
---
Content about GHL
""")

        doc2 = test_docs_dir / "doc2.md"
        doc2.write_text("""---
title: Doc 2
tags: [gohighlevel, platform]
status: draft
---
Content about GoHighLevel
""")

        conflicts = detector.detect_conflicts([doc1, doc2])
        tag_conflicts = conflicts['tags']

        assert len(tag_conflicts) >= 1
        assert any(issue.rule_id == "CONFLICT-002" for issue in tag_conflicts)
        assert any("synonym conflict" in issue.message.lower() for issue in tag_conflicts)
        # Verify line number is tracked (tags is on line 3 in both docs)
        for issue in tag_conflicts:
            if "synonym conflict" in issue.message.lower():
                assert issue.line_number == 3, f"Expected line 3, got {issue.line_number}"

    def test_pricing_conflict(self, detector, test_docs_dir):
        """Test detection of pricing conflicts."""
        doc1 = test_docs_dir / "pricing1.md"
        doc1.write_text("""---
title: Pricing Page 1
tags: [pricing]
status: draft
---

# Pricing

Basic plan: $99/month
""")

        doc2 = test_docs_dir / "pricing2.md"
        doc2.write_text("""---
title: Pricing Page 2
tags: [pricing]
status: draft
---

# Pricing

Basic plan costs $149 per month
""")

        conflicts = detector.detect_conflicts([doc1, doc2])
        pricing_conflicts = conflicts['pricing']

        # Should detect price conflict for "basic" plan
        assert len(pricing_conflicts) >= 1
        assert any(issue.rule_id == "CONFLICT-003" for issue in pricing_conflicts)
        assert any("pricing conflict" in issue.message.lower() for issue in pricing_conflicts)
        # Verify line number is tracked (first price is on line 9 in doc1)
        for issue in pricing_conflicts:
            if "pricing conflict" in issue.message.lower():
                assert issue.line_number is not None, "Line number should be tracked for pricing conflicts"
                assert issue.line_number == 9, f"Expected line 9, got {issue.line_number}"

    def test_pricing_no_conflict_same_price(self, detector, test_docs_dir):
        """Test no conflict when pricing is consistent."""
        doc1 = test_docs_dir / "pricing1.md"
        doc1.write_text("""---
title: Pricing Page 1
tags: [pricing]
status: draft
---

Basic plan: $99/month
""")

        doc2 = test_docs_dir / "pricing2.md"
        doc2.write_text("""---
title: Pricing Page 2
tags: [pricing]
status: draft
---

Basic plan: $99/month
""")

        conflicts = detector.detect_conflicts([doc1, doc2])
        pricing_conflicts = conflicts['pricing']

        # Should have no conflicts (same price)
        assert len(pricing_conflicts) == 0

    def test_cross_reference_to_deprecated_doc(self, detector, test_docs_dir):
        """Test detection of links to deprecated documents."""
        deprecated_doc = test_docs_dir / "old-guide.md"
        deprecated_doc.write_text("""---
title: Old Guide
tags: [guide]
status: deprecated
---

This is deprecated.
""")

        active_doc = test_docs_dir / "current-doc.md"
        active_doc.write_text("""---
title: Current Doc
tags: [guide]
status: active
---

See [old guide](./old-guide.md) for more info.
""")

        conflicts = detector.detect_conflicts([deprecated_doc, active_doc], base_path=test_docs_dir)
        cross_ref_conflicts = conflicts['cross_references']

        assert len(cross_ref_conflicts) >= 1
        assert any(issue.rule_id == "CONFLICT-004" for issue in cross_ref_conflicts)
        assert any("deprecated document" in issue.message.lower() for issue in cross_ref_conflicts)
        # Verify line number is tracked (link is on line 7 in active_doc)
        for issue in cross_ref_conflicts:
            if "deprecated document" in issue.message.lower():
                assert issue.line_number == 7, f"Expected line 7, got {issue.line_number}"

    def test_no_conflict_for_external_links(self, detector, test_docs_dir):
        """Test external links are not flagged as cross-reference conflicts."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [test]
status: draft
---

[External link](https://example.com)
[Another external](http://test.com)
""")

        conflicts = detector.detect_conflicts([doc1], base_path=test_docs_dir)
        cross_ref_conflicts = conflicts['cross_references']

        # Should not flag external links
        assert len(cross_ref_conflicts) == 0

    def test_documents_without_frontmatter(self, detector, test_docs_dir):
        """Test detector handles documents without frontmatter gracefully."""
        doc1 = test_docs_dir / "no-frontmatter.md"
        doc1.write_text("""# Title

Content without frontmatter.
""")

        doc2 = test_docs_dir / "with-frontmatter.md"
        doc2.write_text("""---
title: With Frontmatter
tags: [test]
status: draft
---

Content
""")

        # Should not crash
        conflicts = detector.detect_conflicts([doc1, doc2])
        assert isinstance(conflicts, dict)

    def test_detector_disabled(self, config, logger, test_docs_dir):
        """Test detector can be disabled via configuration."""
        config.config_data['validation']['conflicts']['enabled'] = False
        detector = ConflictDetector(config, logger)

        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [test]
status: published
---
""")

        conflicts = detector.detect_conflicts([doc1])
        # Should return empty dict when disabled
        assert len(conflicts) == 0 or all(len(issues) == 0 for issues in conflicts.values())

    def test_generate_conflict_report(self, detector, test_docs_dir):
        """Test conflict report generation."""
        doc1 = test_docs_dir / "doc1.md"
        doc1.write_text("""---
title: Doc 1
tags: [test]
status: published
---
Content
""")

        conflicts = detector.detect_conflicts([doc1])
        report = detector.generate_conflict_report(conflicts)

        assert isinstance(report, str)
        assert "CONFLICT DETECTION REPORT" in report
        assert "Total Conflicts Found" in report

    def test_normalize_to_monthly(self, detector):
        """Test price normalization to monthly rate."""
        assert detector._normalize_to_monthly(99.0, 'month') == 99.0
        assert detector._normalize_to_monthly(99.0, 'mo') == 99.0
        assert detector._normalize_to_monthly(1200.0, 'year') == 100.0
        assert detector._normalize_to_monthly(600.0, 'yr') == 50.0


class TestConflictDetectorRealDocs:
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
  conflicts:
    enabled: true

reporting:
  format: "markdown"
  output_dir: "_meta/reports/"

logging:
  level: "WARNING"
  file: "logs/test.log"
  console: false

performance:
  enable_cache: true
"""
        config_file.write_text(config_content)
        return Config(config_file)

    @pytest.fixture
    def logger(self, tmp_path):
        """Create a test logger."""
        log_file = tmp_path / "test.log"
        return Logger("test", log_file=log_file, log_level="WARNING")

    @pytest.fixture
    def detector(self, config, logger):
        """Create a ConflictDetector instance."""
        return ConflictDetector(config, logger)

    def test_detect_real_status_conflicts(self, detector, real_docs_path):
        """Test detection of status conflicts in real documentation."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Sample some documents
        all_docs = list(real_docs_path.glob("**/*.md"))
        all_docs = [d for d in all_docs if d.name != "README.md"]

        if len(all_docs) < 10:
            pytest.skip("Not enough documents for testing")

        # Analyze first 30 docs
        sample_docs = all_docs[:30]
        conflicts = detector.detect_conflicts(sample_docs, base_path=real_docs_path)

        # Should complete without crashing
        print(f"\nAnalyzed {len(sample_docs)} documents for conflicts")

        status_conflicts = conflicts.get('status', [])
        print(f"Status conflicts found: {len(status_conflicts)}")

        # Based on documentation review, we know there are status conflicts
        # (draft vs Draft, published, complete, etc.)
        if status_conflicts:
            for conflict in status_conflicts[:3]:
                print(f"  {conflict.rule_id}: {conflict.message}")

    def test_detect_real_tag_conflicts(self, detector, real_docs_path):
        """Test detection of tag conflicts in real documentation."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Focus on platform docs (likely to have ghl/gohighlevel)
        platform_docs = list((real_docs_path / "08-reference" / "platforms").glob("**/*.md"))

        if len(platform_docs) < 5:
            pytest.skip("Not enough platform documents")

        conflicts = detector.detect_conflicts(platform_docs, base_path=real_docs_path)
        tag_conflicts = conflicts.get('tags', [])

        print(f"\nAnalyzed {len(platform_docs)} platform documents")
        print(f"Tag synonym conflicts found: {len(tag_conflicts)}")

        if tag_conflicts:
            for conflict in tag_conflicts[:3]:
                print(f"  {conflict.rule_id}: {conflict.message}")

    def test_detect_real_pricing_conflicts(self, detector, real_docs_path):
        """Test detection of pricing conflicts in real documentation."""
        if not real_docs_path.exists():
            pytest.skip("Real documentation not available")

        # Focus on pricing and sales docs
        pricing_docs = []
        for pattern in ["03-sales/**/*.md", "02-marketing-brand/**/*.md"]:
            pricing_docs.extend(real_docs_path.glob(pattern))

        pricing_docs = [d for d in pricing_docs if d.name != "README.md"]

        if len(pricing_docs) < 5:
            pytest.skip("Not enough pricing documents")

        conflicts = detector.detect_conflicts(pricing_docs[:20], base_path=real_docs_path)
        pricing_conflicts = conflicts.get('pricing', [])

        print(f"\nAnalyzed {len(pricing_docs[:20])} pricing/sales documents")
        print(f"Pricing conflicts found: {len(pricing_conflicts)}")

        # May or may not find conflicts (depends on current state of docs)
        if pricing_conflicts:
            for conflict in pricing_conflicts[:3]:
                print(f"  {conflict.rule_id}: {conflict.message}")
