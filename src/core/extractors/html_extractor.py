"""
HTML content extraction module for Symphony Core.

This module provides functionality to extract structured content from HTML files,
intelligently identifying main content areas and removing navigation, footers, and ads.
"""

from pathlib import Path
from typing import Optional, Dict
import logging
from bs4 import BeautifulSoup, Tag


class HTMLExtractor:
    """Extract structured content from HTML files."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize HTMLExtractor.

        Args:
            logger: Optional logger instance for logging extraction operations
        """
        self.logger = logger or logging.getLogger(__name__)

    def extract_main_content(self, html_path: Path) -> Dict:
        """
        Extract main content from HTML file.

        Args:
            html_path: Path to HTML file

        Returns:
            dict: {
                'title': str,           # Extracted title from H1 or <title>
                'html_content': str,    # Clean HTML content for conversion
                'metadata': dict        # Extracted metadata (description, etc.)
            }

        Raises:
            FileNotFoundError: If HTML file doesn't exist
            Exception: If parsing fails
        """
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_path}")

        try:
            self.logger.info(f"Extracting content from: {html_path}")

            # Read HTML file
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'lxml')

            # Remove unwanted elements
            self._remove_unwanted_elements(soup)

            # Extract title
            title = self._extract_title(soup)
            self.logger.debug(f"Extracted title: {title}")

            # Find and extract main content
            main_content = self._find_main_content(soup)
            html_content = str(main_content) if main_content else str(soup.body or soup)

            # Extract metadata
            metadata = self._extract_metadata(soup)

            return {
                'title': title,
                'html_content': html_content,
                'metadata': metadata
            }

        except Exception as e:
            self.logger.error(f"Failed to extract content: {e}")
            raise

    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        """
        Remove navigation, footer, scripts, and other unwanted elements.

        Args:
            soup: BeautifulSoup object to clean (modified in-place)
        """
        # Remove scripts, styles, and other non-content elements
        unwanted_tags = ['script', 'style', 'iframe', 'noscript']
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove common navigation and footer elements
        unwanted_elements = [
            {'name': 'nav'},
            {'name': 'footer'},
            {'class_': lambda x: x and any(
                nav_class in ' '.join(x) if isinstance(x, list) else nav_class in x
                for nav_class in ['nav', 'navigation', 'navbar', 'menu', 'footer', 'sidebar']
            )},
            {'id': lambda x: x and any(
                nav_id in x.lower()
                for nav_id in ['nav', 'navigation', 'navbar', 'menu', 'footer', 'sidebar']
            )}
        ]

        for selector in unwanted_elements:
            for element in soup.find_all(**selector):
                element.decompose()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract title from H1 or <title> tag.

        Args:
            soup: BeautifulSoup object

        Returns:
            str: Extracted title or 'Untitled Document' if not found
        """
        # Try H1 first (most common for main content title)
        h1 = soup.find('h1')
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)

        # Fallback to <title> tag
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text(strip=True):
            return title_tag.get_text(strip=True)

        # Last resort
        return 'Untitled Document'

    def _find_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """
        Intelligently find main content area.

        Looks for semantic HTML5 tags first (<main>, <article>),
        then falls back to finding the largest content block.

        Args:
            soup: BeautifulSoup object

        Returns:
            Tag: Main content element, or None if not found
        """
        # Try semantic HTML5 tags first
        main_tag = soup.find('main')
        if main_tag:
            self.logger.debug("Found <main> tag")
            return main_tag

        article_tag = soup.find('article')
        if article_tag:
            self.logger.debug("Found <article> tag")
            return article_tag

        # Look for common content container classes/ids
        content_selectors = [
            {'class_': lambda x: x and 'content' in ' '.join(x) if isinstance(x, list) else 'content' in x},
            {'id': lambda x: x and 'content' in x.lower()},
            {'class_': lambda x: x and 'main' in ' '.join(x) if isinstance(x, list) else 'main' in x},
            {'id': lambda x: x and 'main' in x.lower()}
        ]

        for selector in content_selectors:
            content_div = soup.find('div', **selector)
            if content_div:
                self.logger.debug(f"Found content container: {selector}")
                return content_div

        # Fallback to body
        self.logger.debug("Using <body> as main content")
        return soup.body

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """
        Extract metadata from HTML head section.

        Args:
            soup: BeautifulSoup object

        Returns:
            dict: Metadata including description, keywords, etc.
        """
        metadata = {}

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            metadata['description'] = meta_desc['content']

        # Extract meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            metadata['keywords'] = meta_keywords['content']

        # Extract Open Graph URL (if available)
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        if og_url and og_url.get('content'):
            metadata['url'] = og_url['content']

        return metadata
