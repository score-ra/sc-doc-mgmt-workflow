"""
Tests for YAML frontmatter parsing and manipulation.
"""

import pytest
from pathlib import Path
from src.utils.frontmatter import (
    has_frontmatter,
    parse_frontmatter,
    extract_frontmatter_and_content,
    add_frontmatter,
    update_frontmatter,
    remove_frontmatter,
    FrontmatterError
)


class TestHasFrontmatter:
    """Tests for has_frontmatter function."""

    def test_has_frontmatter_with_valid_frontmatter(self, tmp_path):
        """Test detection of valid frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test\ntags: [test]\n---\n# Content",
            encoding='utf-8'
        )

        assert has_frontmatter(test_file) is True

    def test_has_frontmatter_without_frontmatter(self, tmp_path):
        """Test detection when no frontmatter present."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Just markdown content", encoding='utf-8')

        assert has_frontmatter(test_file) is False

    def test_has_frontmatter_with_incomplete_delimiters(self, tmp_path):
        """Test detection with incomplete frontmatter delimiters."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test\n# Missing closing delimiter",
            encoding='utf-8'
        )

        assert has_frontmatter(test_file) is False

    def test_has_frontmatter_with_empty_file(self, tmp_path):
        """Test detection on empty file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("", encoding='utf-8')

        assert has_frontmatter(test_file) is False

    def test_has_frontmatter_file_not_found(self, tmp_path):
        """Test FileNotFoundError is raised for non-existent file."""
        test_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            has_frontmatter(test_file)

    def test_has_frontmatter_with_frontmatter_in_middle(self, tmp_path):
        """Test that frontmatter must be at start of file."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "# Content first\n---\ntitle: Test\n---",
            encoding='utf-8'
        )

        assert has_frontmatter(test_file) is False


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_parse_valid_frontmatter(self, tmp_path):
        """Test parsing valid YAML frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Test Document\ntags: [test, sample]\nstatus: draft\n---\n# Content",
            encoding='utf-8'
        )

        metadata = parse_frontmatter(test_file)

        assert metadata['title'] == "Test Document"
        assert metadata['tags'] == ['test', 'sample']
        assert metadata['status'] == 'draft'

    def test_parse_frontmatter_no_frontmatter(self, tmp_path):
        """Test parsing file without frontmatter returns empty dict."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Just content", encoding='utf-8')

        metadata = parse_frontmatter(test_file)

        assert metadata == {}

    def test_parse_frontmatter_empty_frontmatter(self, tmp_path):
        """Test parsing empty frontmatter block."""
        test_file = tmp_path / "test.md"
        test_file.write_text("---\n\n---\n# Content", encoding='utf-8')

        metadata = parse_frontmatter(test_file)

        assert metadata == {}

    def test_parse_frontmatter_complex_yaml(self, tmp_path):
        """Test parsing complex YAML structures."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\n"
            "title: Complex Document\n"
            "tags: [pricing, policy]\n"
            "status: review\n"
            "metadata:\n"
            "  author: John Doe\n"
            "  version: 1.2.0\n"
            "  reviewers:\n"
            "    - Alice\n"
            "    - Bob\n"
            "---\n"
            "# Content",
            encoding='utf-8'
        )

        metadata = parse_frontmatter(test_file)

        assert metadata['title'] == "Complex Document"
        assert metadata['metadata']['author'] == "John Doe"
        assert metadata['metadata']['reviewers'] == ['Alice', 'Bob']

    def test_parse_frontmatter_invalid_yaml(self, tmp_path):
        """Test parsing malformed YAML raises FrontmatterError."""
        test_file = tmp_path / "test.md"
        # Use actually invalid YAML syntax (unclosed quote)
        test_file.write_text(
            "---\ntitle: \"Unclosed quote\ntags: [test]\n---\n# Content",
            encoding='utf-8'
        )

        with pytest.raises(FrontmatterError, match="Invalid YAML"):
            parse_frontmatter(test_file)

    def test_parse_frontmatter_non_dict_yaml(self, tmp_path):
        """Test parsing YAML that's not a dictionary raises error."""
        test_file = tmp_path / "test.md"
        test_file.write_text("---\n- item1\n- item2\n---\n# Content", encoding='utf-8')

        with pytest.raises(FrontmatterError, match="must be a YAML dictionary"):
            parse_frontmatter(test_file)

    def test_parse_frontmatter_empty_file(self, tmp_path):
        """Test parsing empty file returns empty dict."""
        test_file = tmp_path / "test.md"
        test_file.write_text("", encoding='utf-8')

        metadata = parse_frontmatter(test_file)

        assert metadata == {}

    def test_parse_frontmatter_file_not_found(self, tmp_path):
        """Test FileNotFoundError for non-existent file."""
        test_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            parse_frontmatter(test_file)

    def test_parse_frontmatter_whitespace_variations(self, tmp_path):
        """Test parsing with various whitespace patterns."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---   \n  title: Test  \n  tags: [sample]  \n---  \n# Content",
            encoding='utf-8'
        )

        metadata = parse_frontmatter(test_file)

        assert metadata['title'] == "Test"
        assert metadata['tags'] == ['sample']


class TestExtractFrontmatterAndContent:
    """Tests for extract_frontmatter_and_content function."""

    def test_extract_with_frontmatter(self, tmp_path):
        """Test extracting both frontmatter and content."""
        test_file = tmp_path / "test.md"
        content = "---\ntitle: Test\ntags: [test]\n---\n# Heading\n\nParagraph"
        test_file.write_text(content, encoding='utf-8')

        metadata, markdown = extract_frontmatter_and_content(test_file)

        assert metadata['title'] == "Test"
        assert metadata['tags'] == ['test']
        assert "# Heading" in markdown
        assert "Paragraph" in markdown

    def test_extract_without_frontmatter(self, tmp_path):
        """Test extracting from file without frontmatter."""
        test_file = tmp_path / "test.md"
        content = "# Heading\n\nParagraph"
        test_file.write_text(content, encoding='utf-8')

        metadata, markdown = extract_frontmatter_and_content(test_file)

        assert metadata == {}
        assert markdown == content

    def test_extract_empty_file(self, tmp_path):
        """Test extracting from empty file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("", encoding='utf-8')

        metadata, markdown = extract_frontmatter_and_content(test_file)

        assert metadata == {}
        assert markdown == ""

    def test_extract_preserves_content_formatting(self, tmp_path):
        """Test that content formatting is preserved."""
        test_file = tmp_path / "test.md"
        markdown_content = "# Heading\n\n- List item 1\n- List item 2\n\n```python\ncode\n```"
        content = f"---\ntitle: Test\n---\n{markdown_content}"
        test_file.write_text(content, encoding='utf-8')

        metadata, markdown = extract_frontmatter_and_content(test_file)

        assert markdown == markdown_content


class TestAddFrontmatter:
    """Tests for add_frontmatter function."""

    def test_add_frontmatter_to_file_without_frontmatter(self, tmp_path):
        """Test adding frontmatter to file that doesn't have it."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Content", encoding='utf-8')

        metadata = {'title': 'Test', 'tags': ['test'], 'status': 'draft'}
        add_frontmatter(test_file, metadata)

        # Verify frontmatter was added
        result = parse_frontmatter(test_file)
        assert result['title'] == 'Test'
        assert result['tags'] == ['test']
        assert result['status'] == 'draft'

        # Verify content was preserved
        content = test_file.read_text(encoding='utf-8')
        assert "# Content" in content

    def test_add_frontmatter_replaces_existing(self, tmp_path):
        """Test that adding frontmatter replaces existing frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Old\n---\n# Content",
            encoding='utf-8'
        )

        metadata = {'title': 'New', 'tags': ['updated']}
        add_frontmatter(test_file, metadata)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'New'
        assert result['tags'] == ['updated']

    def test_add_frontmatter_preserves_content(self, tmp_path):
        """Test that markdown content is preserved when adding frontmatter."""
        test_file = tmp_path / "test.md"
        original_content = "# Heading\n\nSome **bold** text\n\n- List item"
        test_file.write_text(original_content, encoding='utf-8')

        metadata = {'title': 'Test', 'status': 'draft'}
        add_frontmatter(test_file, metadata)

        _, content = extract_frontmatter_and_content(test_file)
        assert content == original_content

    def test_add_frontmatter_without_preserving_content(self, tmp_path):
        """Test adding frontmatter without preserving content."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Old content", encoding='utf-8')

        metadata = {'title': 'Test'}
        add_frontmatter(test_file, metadata, preserve_content=False)

        content = test_file.read_text(encoding='utf-8')
        assert "# Old content" not in content
        assert "title: Test" in content

    def test_add_frontmatter_file_not_found(self, tmp_path):
        """Test FileNotFoundError when file doesn't exist."""
        test_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            add_frontmatter(test_file, {'title': 'Test'})

    def test_add_frontmatter_complex_types(self, tmp_path):
        """Test adding frontmatter with complex but serializable types."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Content", encoding='utf-8')

        # PyYAML is very permissive and can serialize most types
        # Test that it handles various types correctly
        metadata = {
            'title': 'Test',
            'tags': ['tag1', 'tag2'],
            'nested': {'key': 'value'},
            'list_of_dicts': [{'a': 1}, {'b': 2}]
        }
        add_frontmatter(test_file, metadata)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'Test'
        assert result['nested']['key'] == 'value'

    def test_add_frontmatter_unicode_content(self, tmp_path):
        """Test adding frontmatter with unicode characters."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Content", encoding='utf-8')

        metadata = {'title': 'Test 测试', 'author': 'José García'}
        add_frontmatter(test_file, metadata)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'Test 测试'
        assert result['author'] == 'José García'


class TestUpdateFrontmatter:
    """Tests for update_frontmatter function."""

    def test_update_frontmatter_merges_with_existing(self, tmp_path):
        """Test updating frontmatter merges with existing fields."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Original\ntags: [test]\n---\n# Content",
            encoding='utf-8'
        )

        update_frontmatter(test_file, {'status': 'draft'}, merge=True)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'Original'  # Preserved
        assert result['tags'] == ['test']  # Preserved
        assert result['status'] == 'draft'  # Added

    def test_update_frontmatter_overwrites_field(self, tmp_path):
        """Test updating frontmatter overwrites existing field."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Old\ntags: [old]\n---\n# Content",
            encoding='utf-8'
        )

        update_frontmatter(test_file, {'title': 'New'}, merge=True)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'New'
        assert result['tags'] == ['old']  # Preserved

    def test_update_frontmatter_no_merge(self, tmp_path):
        """Test updating without merge replaces all frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            "---\ntitle: Old\ntags: [old]\nstatus: draft\n---\n# Content",
            encoding='utf-8'
        )

        update_frontmatter(test_file, {'title': 'New'}, merge=False)

        result = parse_frontmatter(test_file)
        assert result['title'] == 'New'
        assert 'tags' not in result  # Removed
        assert 'status' not in result  # Removed

    def test_update_frontmatter_preserves_content(self, tmp_path):
        """Test that updating frontmatter preserves markdown content."""
        test_file = tmp_path / "test.md"
        content = "# Heading\n\nParagraph"
        test_file.write_text(f"---\ntitle: Test\n---\n{content}", encoding='utf-8')

        update_frontmatter(test_file, {'status': 'draft'})

        _, markdown = extract_frontmatter_and_content(test_file)
        assert markdown == content


class TestRemoveFrontmatter:
    """Tests for remove_frontmatter function."""

    def test_remove_frontmatter_preserves_content(self, tmp_path):
        """Test removing frontmatter preserves markdown content."""
        test_file = tmp_path / "test.md"
        content = "# Heading\n\nParagraph text"
        test_file.write_text(
            f"---\ntitle: Test\ntags: [test]\n---\n{content}",
            encoding='utf-8'
        )

        remove_frontmatter(test_file)

        result_content = test_file.read_text(encoding='utf-8')
        assert result_content == content
        assert not has_frontmatter(test_file)

    def test_remove_frontmatter_no_frontmatter(self, tmp_path):
        """Test removing frontmatter from file without it is a no-op."""
        test_file = tmp_path / "test.md"
        original_content = "# Just content"
        test_file.write_text(original_content, encoding='utf-8')

        remove_frontmatter(test_file)

        result_content = test_file.read_text(encoding='utf-8')
        assert result_content == original_content

    def test_remove_frontmatter_file_not_found(self, tmp_path):
        """Test FileNotFoundError when file doesn't exist."""
        test_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            remove_frontmatter(test_file)
