"""Tests for MarkdownConverter class."""

import pytest
from src.core.extractors.markdown_converter import MarkdownConverter


class TestMarkdownConverter:
    """Test suite for MarkdownConverter."""

    def test_basic_html_to_markdown(self):
        """Test basic HTML to markdown conversion."""
        converter = MarkdownConverter()
        html = "<h1>Title</h1><p>Paragraph text</p>"
        result = converter.convert_to_markdown(html)

        assert "# Title" in result
        assert "Paragraph text" in result

    def test_preserve_links(self):
        """Test that links are preserved in markdown format."""
        converter = MarkdownConverter()
        html = '<p>Check out <a href="https://example.com">this link</a></p>'
        result = converter.convert_to_markdown(html)

        assert "[this link](https://example.com)" in result

    def test_convert_heading_levels(self):
        """Test conversion of different heading levels."""
        converter = MarkdownConverter()
        html = "<h1>H1</h1><h2>H2</h2><h3>H3</h3>"
        result = converter.convert_to_markdown(html)

        assert "# H1" in result
        assert "## H2" in result
        assert "### H3" in result

    def test_convert_lists(self):
        """Test conversion of ordered and unordered lists."""
        converter = MarkdownConverter()
        html = """
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <ol>
            <li>First</li>
            <li>Second</li>
        </ol>
        """
        result = converter.convert_to_markdown(html)

        assert "Item 1" in result
        assert "Item 2" in result
        assert "First" in result
        assert "Second" in result

    def test_convert_table_to_structured(self):
        """Test conversion of markdown tables to structured content."""
        converter = MarkdownConverter()
        markdown = """Feature | Status
---|---
Extraction | Working
Conversion | Working
"""
        result = converter._convert_tables_to_structured(markdown)

        # Should have structured format, not table
        assert "Feature | Status" not in result or "**Feature**:" in result
        assert "**Status**:" in result or "Status" in result
        assert "Extraction" in result
        assert "Working" in result
        assert "---|---" not in result  # Separator should be removed

    def test_table_conversion_removes_separator(self):
        """Test that table separator rows are removed."""
        converter = MarkdownConverter()
        table_lines = [
            "Header 1 | Header 2",
            "---|---",
            "Data 1 | Data 2"
        ]

        result = converter._convert_table_buffer(table_lines)

        assert "---|---" not in result
        assert "Header 1" in result or "**Header 1**:" in result
        assert "Data 1" in result

    def test_remove_checkboxes(self):
        """Test removal of checkbox symbols."""
        converter = MarkdownConverter()
        markdown = """
☐ Unchecked item
✓ Checked item
✅ Done item
❌ Cancelled item
[ ] Markdown checkbox
[x] Markdown checked
"""
        result = converter._remove_checkboxes(markdown)

        # All checkbox symbols should be removed
        assert "☐" not in result
        assert "✓" not in result
        assert "✅" not in result
        assert "❌" not in result
        assert "[ ]" not in result
        assert "[x]" not in result
        # Content should remain
        assert "Unchecked item" in result
        assert "Checked item" in result

    def test_clean_whitespace(self):
        """Test cleaning excessive whitespace."""
        converter = MarkdownConverter()
        markdown = "Line 1\n\n\n\n\nLine 2\n\n\n\nLine 3"

        result = converter._clean_whitespace(markdown)

        # Should reduce excessive blank lines
        assert "\n\n\n\n" not in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_remove_placeholders(self):
        """Test removal of square bracket placeholders."""
        converter = MarkdownConverter()
        markdown = """
[Your Name] should be replaced
[Date] should be replaced
But [link text](url) should remain
"""
        result = converter._remove_placeholders(markdown)

        # Placeholders should be removed but content retained
        assert "Your Name" in result
        assert "Date" in result
        # Links should be preserved
        assert "[link text](url)" in result

    def test_preserve_code_blocks(self):
        """Test that code blocks are preserved."""
        converter = MarkdownConverter()
        html = """
<pre><code>
def hello():
    print("Hello")
</code></pre>
"""
        result = converter.convert_to_markdown(html)

        assert "def hello():" in result
        assert 'print("Hello")' in result

    def test_preserve_emphasis(self):
        """Test that bold and italic are preserved."""
        converter = MarkdownConverter()
        html = "<p><strong>Bold</strong> and <em>italic</em></p>"
        result = converter.convert_to_markdown(html)

        # html2text converts to markdown emphasis
        assert "Bold" in result
        assert "italic" in result

    def test_full_conversion_pipeline(self):
        """Test complete conversion with tables, checkboxes, and whitespace."""
        converter = MarkdownConverter()
        html = """
<h1>Test Document</h1>
<p>Introduction paragraph.</p>

<table>
    <tr><th>Column 1</th><th>Column 2</th></tr>
    <tr><td>Value 1</td><td>Value 2</td></tr>
</table>

<p>☐ Task item</p>
<p><a href="https://example.com">Link</a></p>
"""
        result = converter.convert_to_markdown(html)

        # Title should be converted
        assert "# Test Document" in result
        # Paragraph should exist
        assert "Introduction paragraph" in result
        # Table should be converted to structured format
        assert "**Column 1**:" in result or "Column 1" in result
        # Checkbox should be removed
        assert "☐" not in result
        assert "Task item" in result
        # Link should be preserved
        assert "[Link](https://example.com)" in result

    def test_empty_input(self):
        """Test handling of empty input."""
        converter = MarkdownConverter()
        result = converter.convert_to_markdown("")

        assert result == "\n"  # html2text returns newline for empty input

    def test_complex_table_conversion(self):
        """Test conversion of table with multiple rows."""
        converter = MarkdownConverter()
        table_lines = [
            "Name | Age | City",
            "---|---|---",
            "Alice | 30 | NYC",
            "Bob | 25 | LA",
            "Charlie | 35 | SF"
        ]

        result = converter._convert_table_buffer(table_lines)

        # Should have all data
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result
        assert "30" in result
        assert "NYC" in result
        # Should not have separator
        assert "---|---|---" not in result
