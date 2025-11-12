"""
YAML frontmatter generation module for Symphony Core.

Generates SC-compliant YAML frontmatter with all required fields
and optional metadata for extracted documents.
"""

from datetime import datetime
from typing import Optional, List, Dict
import yaml


class FrontmatterGenerator:
    """Generate YAML frontmatter for extracted documents."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize FrontmatterGenerator.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

    def generate(
        self,
        title: str,
        tags: Optional[List[str]] = None,
        status: str = "draft",
        category: str = "KB Article",
        author: str = "Web Content Extractor",
        version: str = "1.0",
        source_url: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate SC-compliant YAML frontmatter.

        Required fields per SC standard:
        - title: Document title
        - version: Semantic version (default: 1.0)
        - author: Document author
        - last_updated: ISO date (YYYY-MM-DD)
        - category: Document category
        - tags: List of tags
        - status: Document status (draft, review, approved, deprecated, active)

        Optional fields:
        - source_url: Original URL of content
        - extracted_date: Timestamp of extraction
        - extraction_method: How content was extracted

        Args:
            title: Document title (required)
            tags: List of tags (default: ['web-content', 'extracted'])
            status: Document status (default: 'draft')
            category: Document category (default: 'KB Article')
            author: Document author (default: 'Web Content Extractor')
            version: Document version (default: '1.0')
            source_url: Original URL (optional)
            **kwargs: Additional optional fields

        Returns:
            str: YAML frontmatter block with --- delimiters

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate required fields
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        if status not in ['draft', 'review', 'approved', 'deprecated', 'active']:
            raise ValueError(f"Invalid status: {status}. Must be one of: draft, review, approved, deprecated, active")

        # Build frontmatter dictionary
        frontmatter = {
            'title': title.strip(),
            'version': version,
            'author': author,
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'category': category,
            'tags': tags or ['web-content', 'extracted'],
            'status': status
        }

        # Add optional fields
        if source_url:
            frontmatter['source_url'] = source_url

        # Add extraction metadata
        frontmatter['extracted_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        frontmatter['extraction_method'] = kwargs.get('extraction_method', 'html_file')

        # Add any additional kwargs
        for key, value in kwargs.items():
            if key not in frontmatter and key != 'extraction_method':
                frontmatter[key] = value

        # Convert to YAML
        yaml_str = self._format_yaml(frontmatter)

        # Return with delimiters (NO language identifier as per SC standard)
        return f"---\n{yaml_str}---\n"

    def _format_yaml(self, data: Dict) -> str:
        """
        Format dictionary as YAML string.

        Args:
            data: Dictionary to convert to YAML

        Returns:
            str: Formatted YAML string
        """
        # Use yaml.dump with specific formatting options
        yaml_str = yaml.dump(
            data,
            default_flow_style=False,  # Use block style
            sort_keys=False,  # Preserve insertion order
            allow_unicode=True,  # Support Unicode characters
            width=80  # Line width for wrapping
        )

        return yaml_str

    def generate_with_defaults(self, title: str, **kwargs) -> str:
        """
        Generate frontmatter with all default values.

        Convenience method that uses default config values for all fields.

        Args:
            title: Document title (required)
            **kwargs: Optional overrides for any field

        Returns:
            str: YAML frontmatter block
        """
        # Get defaults from config or use hardcoded defaults
        defaults = {
            'status': self.config.get('default_status', 'draft'),
            'category': self.config.get('default_category', 'KB Article'),
            'author': self.config.get('default_author', 'Web Content Extractor'),
            'tags': self.config.get('default_tags', ['web-content', 'extracted']),
        }

        # Merge with provided kwargs (kwargs take precedence)
        merged = {**defaults, **kwargs}

        return self.generate(title=title, **merged)

    def validate_frontmatter(self, frontmatter_str: str) -> bool:
        """
        Validate that a frontmatter string has all required fields.

        Args:
            frontmatter_str: YAML frontmatter string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Remove delimiters
            yaml_content = frontmatter_str.strip()
            if yaml_content.startswith('---'):
                yaml_content = yaml_content[3:]
            if yaml_content.endswith('---'):
                yaml_content = yaml_content[:-3]

            # Parse YAML
            data = yaml.safe_load(yaml_content)

            # Check required fields
            required_fields = ['title', 'version', 'author', 'last_updated', 'category', 'tags', 'status']
            for field in required_fields:
                if field not in data:
                    return False

            # Validate status
            if data['status'] not in ['draft', 'review', 'approved', 'deprecated', 'active']:
                return False

            # Validate tags is a list
            if not isinstance(data['tags'], list):
                return False

            return True

        except Exception:
            return False
