"""Tests for FrontmatterGenerator class."""

import pytest
from datetime import datetime
from src.core.extractors.frontmatter_generator import FrontmatterGenerator


class TestFrontmatterGenerator:
    """Test suite for FrontmatterGenerator."""

    def test_generate_with_required_fields(self):
        """Test generation with all required fields."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test Document")

        assert result.startswith("---\n")
        assert result.endswith("---\n")
        assert "title: Test Document" in result
        assert "version:" in result
        assert "author:" in result
        assert "last_updated:" in result
        assert "category:" in result
        assert "tags:" in result
        assert "status:" in result

    def test_generate_with_custom_tags(self):
        """Test generation with custom tags."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            tags=["custom", "test", "sample"]
        )

        assert "- custom" in result
        assert "- test" in result
        assert "- sample" in result

    def test_generate_with_custom_status(self):
        """Test generation with custom status."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            status="review"
        )

        assert "status: review" in result

    def test_generate_with_source_url(self):
        """Test generation with source URL."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            source_url="https://example.com/page"
        )

        assert "source_url: https://example.com/page" in result

    def test_generate_includes_extraction_metadata(self):
        """Test that extraction metadata is included."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test")

        assert "extracted_date:" in result
        assert "extraction_method:" in result

    def test_generate_with_custom_category(self):
        """Test generation with custom category."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            category="Guide"
        )

        assert "category: Guide" in result

    def test_generate_with_custom_author(self):
        """Test generation with custom author."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            author="Custom Author"
        )

        assert "author: Custom Author" in result

    def test_generate_with_custom_version(self):
        """Test generation with custom version."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            version="2.0"
        )

        assert "version: '2.0'" in result

    def test_date_format(self):
        """Test that date is in correct format."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test")

        # Should have date in YYYY-MM-DD format
        today = datetime.now().strftime('%Y-%m-%d')
        assert f"last_updated: '{today}'" in result

    def test_default_tags(self):
        """Test default tags when none provided."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test")

        assert "- web-content" in result
        assert "- extracted" in result

    def test_default_status(self):
        """Test default status is draft."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test")

        assert "status: draft" in result

    def test_invalid_status_raises_error(self):
        """Test that invalid status raises ValueError."""
        generator = FrontmatterGenerator()

        with pytest.raises(ValueError, match="Invalid status"):
            generator.generate(title="Test", status="invalid")

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        generator = FrontmatterGenerator()

        with pytest.raises(ValueError, match="Title is required"):
            generator.generate(title="")

    def test_none_title_raises_error(self):
        """Test that None title raises ValueError."""
        generator = FrontmatterGenerator()

        with pytest.raises(ValueError, match="Title is required"):
            generator.generate(title=None)

    def test_title_whitespace_stripped(self):
        """Test that title whitespace is stripped."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="  Test Document  ")

        assert "title: Test Document" in result
        assert "title:   Test Document  " not in result

    def test_valid_statuses(self):
        """Test all valid status values."""
        generator = FrontmatterGenerator()
        valid_statuses = ['draft', 'review', 'approved', 'deprecated', 'active']

        for status in valid_statuses:
            result = generator.generate(title="Test", status=status)
            assert f"status: {status}" in result

    def test_generate_with_defaults_method(self):
        """Test generate_with_defaults convenience method."""
        generator = FrontmatterGenerator()
        result = generator.generate_with_defaults(title="Test")

        assert result.startswith("---\n")
        assert "title: Test" in result

    def test_generate_with_defaults_custom_config(self):
        """Test generate_with_defaults with custom config."""
        config = {
            'default_status': 'active',
            'default_category': 'Documentation',
            'default_tags': ['docs', 'guide']
        }
        generator = FrontmatterGenerator(config=config)
        result = generator.generate_with_defaults(title="Test")

        assert "status: active" in result
        assert "category: Documentation" in result
        assert "- docs" in result
        assert "- guide" in result

    def test_validate_frontmatter_valid(self):
        """Test validation of valid frontmatter."""
        generator = FrontmatterGenerator()
        frontmatter = generator.generate(title="Test")

        assert generator.validate_frontmatter(frontmatter) is True

    def test_validate_frontmatter_missing_required_field(self):
        """Test validation fails with missing required field."""
        generator = FrontmatterGenerator()
        invalid = """---
title: Test
version: '1.0'
---
"""
        assert generator.validate_frontmatter(invalid) is False

    def test_validate_frontmatter_invalid_status(self):
        """Test validation fails with invalid status."""
        generator = FrontmatterGenerator()
        invalid = """---
title: Test
version: '1.0'
author: Test
last_updated: '2025-01-01'
category: Test
tags: [test]
status: invalid
---
"""
        assert generator.validate_frontmatter(invalid) is False

    def test_validate_frontmatter_tags_not_list(self):
        """Test validation fails when tags is not a list."""
        generator = FrontmatterGenerator()
        invalid = """---
title: Test
version: '1.0'
author: Test
last_updated: '2025-01-01'
category: Test
tags: test
status: draft
---
"""
        assert generator.validate_frontmatter(invalid) is False

    def test_no_language_identifier_in_frontmatter(self):
        """Test that frontmatter doesn't have yaml language identifier."""
        generator = FrontmatterGenerator()
        result = generator.generate(title="Test")

        # Should not have ```yaml or similar
        assert "```" not in result
        assert result.startswith("---\n")

    def test_additional_kwargs(self):
        """Test that additional kwargs are added to frontmatter."""
        generator = FrontmatterGenerator()
        result = generator.generate(
            title="Test",
            custom_field="custom_value",
            another_field=123
        )

        assert "custom_field: custom_value" in result
        assert "another_field: 123" in result
