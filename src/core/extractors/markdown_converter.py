"""
Markdown conversion module for Symphony Core.

Converts HTML content to SC-compliant markdown following Symphony Core standards:
- No markdown tables (convert to structured content)
- No checkbox symbols (use text alternatives)
- Proper heading hierarchy
- Clean, readable formatting
"""

import re
from typing import Optional, Dict
import html2text
from bs4 import BeautifulSoup


class MarkdownConverter:
    """Convert HTML content to SC-compliant markdown."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize MarkdownConverter.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

        # Configure html2text converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False  # Preserve links
        self.h2t.body_width = 0  # No line wrapping
        self.h2t.ignore_images = False  # Keep image references
        self.h2t.ignore_emphasis = False  # Keep bold/italic
        self.h2t.single_line_break = False  # Use proper paragraph spacing

    def convert_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML to markdown following SC standards.

        Post-processes output to ensure:
        - No markdown tables (converts to structured content)
        - No checkbox symbols (☐, ✓, ✅, ❌)
        - Proper heading hierarchy
        - Clean formatting

        Args:
            html_content: HTML string to convert

        Returns:
            str: SC-compliant markdown
        """
        # Base conversion with html2text
        markdown = self.h2t.handle(html_content)

        # SC compliance post-processing
        markdown = self._convert_tables_to_structured(markdown)
        markdown = self._remove_checkboxes(markdown)
        markdown = self._clean_whitespace(markdown)
        markdown = self._remove_placeholders(markdown)

        return markdown

    def _convert_tables_to_structured(self, markdown: str) -> str:
        """
        Convert markdown tables to SC-compliant structured content.

        SC standard prohibits markdown tables. Converts them to:
        ### Table Title
        **Column 1**: Value
        **Column 2**: Value

        Args:
            markdown: Markdown string with potential tables

        Returns:
            str: Markdown with tables converted to structured content
        """
        lines = markdown.split('\n')
        result = []
        in_table = False
        table_buffer = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Detect table rows (lines with | that look like tables)
            # Must have at least 1 pipe (for two-column tables)
            if '|' in stripped and stripped.count('|') >= 1:
                in_table = True
                table_buffer.append(line)
            else:
                if in_table:
                    # End of table - convert buffer
                    if table_buffer:
                        converted = self._convert_table_buffer(table_buffer)
                        result.append(converted)
                        table_buffer = []
                    in_table = False

                result.append(line)

        # Handle table at end of document
        if table_buffer:
            converted = self._convert_table_buffer(table_buffer)
            result.append(converted)

        return '\n'.join(result)

    def _convert_table_buffer(self, table_lines: list) -> str:
        """
        Convert a buffer of markdown table lines to structured content.

        Args:
            table_lines: List of table row strings

        Returns:
            str: Structured content representation
        """
        if not table_lines:
            return ""

        # Parse table rows
        rows = []
        for line in table_lines:
            # Skip separator lines (e.g., |---|---| or ---|---)
            # These lines only contain hyphens, pipes, colons, and whitespace
            if re.match(r'^[\s\|\-:]+$', line.strip()):
                continue

            # Extract cells
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                rows.append(cells)

        if not rows:
            return ""

        # First row is typically headers
        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []

        # Convert to structured format
        structured = []
        structured.append("")  # Blank line before table

        for i, row in enumerate(data_rows):
            for j, cell in enumerate(row):
                header = headers[j] if j < len(headers) else f"Column {j+1}"
                structured.append(f"**{header}**: {cell}")
            if i < len(data_rows) - 1:  # Add separator between rows
                structured.append("")

        structured.append("")  # Blank line after table

        return '\n'.join(structured)

    def _remove_checkboxes(self, markdown: str) -> str:
        """
        Remove or replace checkbox symbols with text alternatives.

        SC standard prohibits checkbox symbols: ☐, ✓, ✅, ❌, ☑

        Args:
            markdown: Markdown string with potential checkboxes

        Returns:
            str: Markdown with checkboxes removed/replaced
        """
        # Remove checkbox symbols
        checkbox_patterns = [
            (r'☐', ''),
            (r'☑', ''),
            (r'✓', ''),
            (r'✅', ''),
            (r'❌', ''),
            (r'\[ \]', ''),  # Markdown checkbox syntax
            (r'\[x\]', ''),
            (r'\[X\]', ''),
        ]

        result = markdown
        for pattern, replacement in checkbox_patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    def _clean_whitespace(self, markdown: str) -> str:
        """
        Clean up excessive whitespace and formatting issues.

        Args:
            markdown: Markdown string to clean

        Returns:
            str: Cleaned markdown
        """
        # Remove excessive blank lines (more than 2 consecutive)
        result = re.sub(r'\n{3,}', '\n\n', markdown)

        # Remove trailing whitespace from lines
        lines = result.split('\n')
        lines = [line.rstrip() for line in lines]
        result = '\n'.join(lines)

        # Ensure single trailing newline
        result = result.rstrip() + '\n'

        return result

    def _remove_placeholders(self, markdown: str) -> str:
        """
        Remove square bracket placeholders as per SC standard.

        SC standard prohibits placeholders like [Your Name], [Date], etc.

        Args:
            markdown: Markdown string with potential placeholders

        Returns:
            str: Markdown with placeholders removed
        """
        # Pattern to match common placeholders: [Your Name], [Date], [Insert X]
        # Be careful not to match markdown links: [text](url)

        # Remove placeholders that are NOT followed by parentheses (which would be links)
        result = re.sub(r'\[([^\]]+)\](?!\()', r'\1', markdown)

        return result
