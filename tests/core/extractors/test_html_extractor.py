"""Tests for HTMLExtractor class."""

import pytest
from pathlib import Path
from src.core.extractors.html_extractor import HTMLExtractor


class TestHTMLExtractor:
    """Test suite for HTMLExtractor."""

    def test_extract_title_from_h1(self, tmp_path):
        """Test extracting title from H1 tag."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <head><title>Page Title</title></head>
            <body><h1>Main Heading</h1><p>Content</p></body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['title'] == "Main Heading"

    def test_extract_title_from_title_tag(self, tmp_path):
        """Test extracting title from <title> tag when no H1."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <head><title>Page Title</title></head>
            <body><p>Content without heading</p></body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['title'] == "Page Title"

    def test_extract_title_fallback(self, tmp_path):
        """Test fallback title when no title found."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html><body><p>Content</p></body></html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['title'] == "Untitled Document"

    def test_remove_navigation(self, tmp_path):
        """Test that navigation elements are removed."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <body>
                <nav><a href="/">Home</a></nav>
                <main><h1>Content</h1></main>
            </body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert '<nav>' not in result['html_content']
        assert '<h1>Content</h1>' in result['html_content']

    def test_remove_footer(self, tmp_path):
        """Test that footer elements are removed."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <body>
                <main><h1>Content</h1></main>
                <footer>Copyright 2025</footer>
            </body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert '<footer>' not in result['html_content']
        assert 'Copyright' not in result['html_content']

    def test_remove_scripts_and_styles(self, tmp_path):
        """Test that scripts and styles are removed."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <head>
                <style>.class { color: red; }</style>
                <script>alert('test');</script>
            </head>
            <body><h1>Content</h1></body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert '<script>' not in result['html_content']
        assert '<style>' not in result['html_content']
        assert 'alert' not in result['html_content']

    def test_find_main_tag(self, tmp_path):
        """Test finding <main> tag as main content."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <body>
                <nav>Nav content</nav>
                <main><h1>Main Content</h1></main>
                <footer>Footer</footer>
            </body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert 'Main Content' in result['html_content']

    def test_find_article_tag(self, tmp_path):
        """Test finding <article> tag as main content."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <body>
                <article><h1>Article Content</h1></article>
            </body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert 'Article Content' in result['html_content']

    def test_extract_metadata(self, tmp_path):
        """Test extracting metadata from head section."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html>
            <head>
                <meta name="description" content="Test description">
                <meta name="keywords" content="test,sample">
                <meta property="og:url" content="https://example.com">
            </head>
            <body><h1>Content</h1></body>
        </html>
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['metadata']['description'] == "Test description"
        assert result['metadata']['keywords'] == "test,sample"
        assert result['metadata']['url'] == "https://example.com"

    def test_file_not_found(self):
        """Test handling of missing file."""
        extractor = HTMLExtractor()

        with pytest.raises(FileNotFoundError):
            extractor.extract_main_content(Path("/nonexistent/file.html"))

    def test_malformed_html(self, tmp_path):
        """Test handling of malformed HTML."""
        html_file = tmp_path / "test.html"
        html_file.write_text("""
        <html><body><h1>Unclosed tag<p>Content
        """)

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        # Should still extract content even with malformed HTML
        assert result['title'] == "Unclosed tag"
        assert 'html_content' in result

    def test_empty_file(self, tmp_path):
        """Test handling of empty HTML file."""
        html_file = tmp_path / "test.html"
        html_file.write_text("")

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['title'] == "Untitled Document"
        assert 'html_content' in result
