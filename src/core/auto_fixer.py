"""
Auto-fix engine for document validation issues.

This module provides safe automatic fixes for common validation issues,
with preview and backup capabilities (ADR-003).
"""

import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.frontmatter import (
    parse_frontmatter,
    add_frontmatter,
    update_frontmatter,
    has_frontmatter
)
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


@dataclass
class AutoFixResult:
    """
    Result of auto-fix operation.

    Attributes:
        file_path: Path to the fixed file
        fixes_applied: List of fixes that were applied
        preview_only: Whether this was a preview (no changes made)
        backup_path: Path to backup file (if created)
        success: Whether all fixes succeeded
        errors: Any errors encountered during fixing
    """
    file_path: Path
    fixes_applied: List[str]
    preview_only: bool = False
    backup_path: Optional[Path] = None
    success: bool = True
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

    def __str__(self) -> str:
        """Format auto-fix result as a readable string."""
        status = "PREVIEW" if self.preview_only else ("SUCCESS" if self.success else "FAILED")
        parts = [f"[{status}] {self.file_path}"]

        if self.fixes_applied:
            parts.append(f"  Fixes applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                parts.append(f"    - {fix}")

        if self.backup_path:
            parts.append(f"  Backup: {self.backup_path}")

        if self.errors:
            parts.append(f"  Errors:")
            for error in self.errors:
                parts.append(f"    - {error}")

        return "\n".join(parts)


class AutoFixer:
    """
    Automatic fixer for common validation issues.

    Provides safe fixes with preview and backup capabilities:
    - Add missing YAML frontmatter
    - Extract title from H1 heading
    - Suggest tags from file path
    - Standardize tag format (string → list)
    - Default status to 'draft'
    """

    def __init__(self, config: Config, logger: Logger):
        """
        Initialize auto-fixer.

        Args:
            config: Configuration object
            logger: Logger for diagnostic messages
        """
        self.config = config
        self.logger = logger

        # Load backup directory from config
        self.backup_dir = Path(config.get('processing.backup_dir', '_meta/.backups/'))

        # Load validation settings
        self.required_fields = config.get(
            'validation.yaml.required_fields',
            ['title', 'tags', 'status']
        )
        self.default_status = 'draft'

    def fix_document(
        self,
        file_path: Path,
        issues: List[ValidationIssue],
        preview: bool = True
    ) -> AutoFixResult:
        """
        Fix validation issues in a document.

        Args:
            file_path: Path to the document to fix
            issues: List of validation issues to fix
            preview: If True, only preview changes without applying them

        Returns:
            AutoFixResult with details of fixes applied
        """
        if not file_path.exists():
            return AutoFixResult(
                file_path=file_path,
                fixes_applied=[],
                success=False,
                errors=[f"File not found: {file_path}"]
            )

        fixes_applied = []
        backup_path = None

        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Determine what fixes are needed
            needs_frontmatter = any(issue.rule_id == "YAML-001" for issue in issues)
            missing_fields_issues = [
                issue for issue in issues if issue.rule_id == "YAML-002"
            ]
            tags_format_issues = [
                issue for issue in issues if issue.rule_id == "YAML-004"
            ]

            # Parse or create frontmatter
            if needs_frontmatter:
                metadata = {}
                fixes_applied.append("Added YAML frontmatter block")
            else:
                metadata = parse_frontmatter(file_path)

            # Fix missing required fields
            if missing_fields_issues:
                missing_fields = self._extract_missing_fields(missing_fields_issues)

                for field in missing_fields:
                    if field == 'title':
                        title = self._extract_title_from_content(original_content)
                        if title:
                            metadata['title'] = title
                            fixes_applied.append(f"Added title from H1 heading: '{title}'")
                        else:
                            metadata['title'] = file_path.stem.replace('-', ' ').replace('_', ' ').title()
                            fixes_applied.append(f"Added title from filename: '{metadata['title']}'")

                    elif field == 'tags':
                        tags = self._suggest_tags_from_path(file_path)
                        metadata['tags'] = tags
                        fixes_applied.append(f"Added suggested tags: {tags}")

                    elif field == 'status':
                        metadata['status'] = self.default_status
                        fixes_applied.append(f"Added default status: '{self.default_status}'")

            # Fix tags format (string → list)
            if tags_format_issues:
                if 'tags' in metadata and isinstance(metadata['tags'], str):
                    # Convert string to single-item list
                    metadata['tags'] = [metadata['tags']]
                    fixes_applied.append("Converted tags from string to list")

            # Apply fixes if not in preview mode
            if not preview and fixes_applied:
                # Create backup
                backup_path = self._create_backup(file_path)
                self.logger.info(f"Created backup: {backup_path}")

                # Write updated frontmatter
                add_frontmatter(file_path, metadata, preserve_content=True)
                self.logger.info(f"Applied {len(fixes_applied)} fix(es) to {file_path}")

            return AutoFixResult(
                file_path=file_path,
                fixes_applied=fixes_applied,
                preview_only=preview,
                backup_path=backup_path,
                success=True
            )

        except Exception as e:
            self.logger.error(f"Error fixing {file_path}: {e}")
            return AutoFixResult(
                file_path=file_path,
                fixes_applied=fixes_applied,
                preview_only=preview,
                success=False,
                errors=[str(e)]
            )

    def _extract_missing_fields(self, issues: List[ValidationIssue]) -> List[str]:
        """Extract list of missing field names from validation issues."""
        missing_fields = []

        for issue in issues:
            # Parse message like "Missing required field(s): title, tags"
            if "Missing required field" in issue.message:
                # Extract field names from message
                parts = issue.message.split(":")
                if len(parts) >= 2:
                    field_str = parts[1].strip()
                    fields = [f.strip() for f in field_str.split(",")]
                    missing_fields.extend(fields)

        return list(set(missing_fields))  # Remove duplicates

    def _extract_title_from_content(self, content: str) -> Optional[str]:
        """
        Extract title from first H1 heading in markdown content.

        Args:
            content: Markdown content to search

        Returns:
            Title text if found, None otherwise
        """
        # Remove frontmatter first
        content_without_frontmatter = re.sub(
            r'^---\s*\n.*?\n---\s*\n',
            '',
            content,
            count=1,
            flags=re.DOTALL
        )

        # Look for H1 heading (# Title)
        h1_match = re.search(r'^#\s+(.+)$', content_without_frontmatter, re.MULTILINE)

        if h1_match:
            title = h1_match.group(1).strip()
            # Remove any markdown formatting
            title = re.sub(r'[*_`]', '', title)
            return title

        return None

    def _suggest_tags_from_path(self, file_path: Path) -> List[str]:
        """
        Suggest tags based on file path structure.

        Args:
            file_path: Path to the document

        Returns:
            List of suggested tags (may be empty)
        """
        tags = []

        # Get parent directory names as potential tags
        parent_parts = file_path.parent.parts

        # Known tag categories from config
        known_tags = ['pricing', 'policy', 'policies', 'product-specs', 'support', 'billing', 'operations', 'sop', 'legal']

        for part in parent_parts:
            part_lower = part.lower()
            # Check if directory name matches known tags
            for known_tag in known_tags:
                if known_tag in part_lower:
                    if known_tag not in tags:
                        tags.append(known_tag)

        # If no tags found from path, use generic tag
        if not tags:
            tags = ['general']

        return tags

    def _create_backup(self, file_path: Path) -> Path:
        """
        Create backup of file before modification.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to backup file

        Raises:
            IOError: If backup cannot be created
        """
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_filename

        # Copy file to backup location
        shutil.copy2(file_path, backup_path)

        return backup_path

    def fix_batch(
        self,
        documents: Dict[Path, List[ValidationIssue]],
        preview: bool = True
    ) -> Dict[Path, AutoFixResult]:
        """
        Fix validation issues in multiple documents.

        Args:
            documents: Dictionary mapping file paths to their validation issues
            preview: If True, only preview changes without applying them

        Returns:
            Dictionary mapping file paths to their auto-fix results
        """
        results = {}

        for file_path, issues in documents.items():
            self.logger.debug(f"Auto-fixing {file_path}")

            # Only attempt to fix if there are fixable issues
            fixable_rules = ["YAML-001", "YAML-002", "YAML-004"]
            fixable_issues = [
                issue for issue in issues
                if issue.rule_id in fixable_rules
            ]

            if fixable_issues:
                result = self.fix_document(file_path, fixable_issues, preview=preview)
                results[file_path] = result
            else:
                self.logger.debug(f"No auto-fixable issues in {file_path}")

        return results

    def can_fix(self, issue: ValidationIssue) -> bool:
        """
        Check if a validation issue can be automatically fixed.

        Args:
            issue: Validation issue to check

        Returns:
            True if the issue can be auto-fixed, False otherwise
        """
        fixable_rules = [
            "YAML-001",  # Missing frontmatter
            "YAML-002",  # Missing required fields
            "YAML-004",  # Tags format (string → list)
        ]

        return issue.rule_id in fixable_rules
