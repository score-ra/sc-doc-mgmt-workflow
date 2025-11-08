"""
Markdown syntax validation for markdown documents.

This module validates markdown structure and formatting against standards
defined in the configuration file.
"""

from pathlib import Path
from typing import List, Optional, Tuple
import re

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


class MarkdownValidator:
    """
    Validates markdown syntax and structure.

    Implements validation rules:
    - MD-001: Heading hierarchy (H1 → H2 → H3, no skipped levels)
    - MD-002: Code blocks must specify language
    - MD-003: Link validation (relative links, check if targets exist)
    - MD-004: No trailing whitespace on lines
    - MD-005: Horizontal rule format consistency
    """

    def __init__(self, config: Config, logger: Logger):
        """
        Initialize markdown validator.

        Args:
            config: Configuration object with validation settings
            logger: Logger for diagnostic messages
        """
        self.config = config
        self.logger = logger

        # Load markdown validation settings from config
        self.enabled = config.get('validation.markdown.enabled', True)
        self.enforce_heading_hierarchy = config.get(
            'validation.markdown.enforce_heading_hierarchy', True
        )
        self.require_language_in_code_blocks = config.get(
            'validation.markdown.require_language_in_code_blocks', True
        )
        self.relative_links_only = config.get(
            'validation.markdown.relative_links_only', True
        )
        self.horizontal_rule_format = config.get(
            'validation.markdown.horizontal_rule_format', '---'
        )
        self.check_trailing_whitespace = config.get(
            'validation.markdown.check_trailing_whitespace', True
        )

    def validate(self, file_path: Path, base_path: Optional[Path] = None) -> List[ValidationIssue]:
        """
        Validate markdown syntax and structure in a file.

        Args:
            file_path: Path to the markdown file to validate
            base_path: Base repository path (for checking relative links)

        Returns:
            List of ValidationIssue objects (empty if no issues found)
        """
        if not self.enabled:
            self.logger.debug(f"Markdown validation disabled, skipping {file_path}")
            return []

        if not file_path.exists():
            return [ValidationIssue(
                rule_id="MD-000",
                severity=ValidationSeverity.ERROR,
                message=f"File not found: {file_path}",
                file_path=file_path
            )]

        issues: List[ValidationIssue] = []

        # Read file content
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return [ValidationIssue(
                rule_id="MD-000",
                severity=ValidationSeverity.ERROR,
                message=f"Error reading file: {str(e)}",
                file_path=file_path
            )]

        # Split into lines for line-by-line validation
        lines = content.splitlines()

        # MD-001: Validate heading hierarchy
        if self.enforce_heading_hierarchy:
            issues.extend(self._validate_heading_hierarchy(file_path, lines))

        # MD-002: Validate code blocks have language specified
        if self.require_language_in_code_blocks:
            issues.extend(self._validate_code_blocks(file_path, lines))

        # MD-003: Validate links
        if base_path:
            issues.extend(self._validate_links(file_path, lines, base_path))

        # MD-004: Check for trailing whitespace
        if self.check_trailing_whitespace:
            issues.extend(self._validate_trailing_whitespace(file_path, lines))

        # MD-005: Validate horizontal rule format
        issues.extend(self._validate_horizontal_rules(file_path, lines))

        return issues

    def _validate_heading_hierarchy(
        self,
        file_path: Path,
        lines: List[str]
    ) -> List[ValidationIssue]:
        """
        Validate heading hierarchy (no skipped levels).

        Implements MD-001: Heading hierarchy validation.
        Checks that headings progress sequentially (H1 → H2 → H3, not H1 → H3).
        """
        issues: List[ValidationIssue] = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)')

        last_level = 0
        last_line_num = 0

        for line_num, line in enumerate(lines, start=1):
            match = heading_pattern.match(line)
            if match:
                current_level = len(match.group(1))  # Number of # symbols
                heading_text = match.group(2).strip()

                # Check for skipped levels (e.g., H1 → H3)
                if last_level > 0:
                    if current_level > last_level + 1:
                        issues.append(ValidationIssue(
                            rule_id="MD-001",
                            severity=ValidationSeverity.WARNING,
                            message=f"Heading hierarchy skips level (H{last_level} → H{current_level}): '{heading_text}'",
                            file_path=file_path,
                            line_number=line_num,
                            suggestion=f"Insert H{last_level + 1} heading before this H{current_level} heading"
                        ))

                last_level = current_level
                last_line_num = line_num

        return issues

    def _validate_code_blocks(
        self,
        file_path: Path,
        lines: List[str]
    ) -> List[ValidationIssue]:
        """
        Validate code blocks have language specified.

        Implements MD-002: Code block language validation.
        Checks that fenced code blocks (```) specify a language.
        """
        issues: List[ValidationIssue] = []
        code_fence_pattern = re.compile(r'^```(\w*)$')

        in_code_block = False
        code_block_start_line = 0

        for line_num, line in enumerate(lines, start=1):
            match = code_fence_pattern.match(line.strip())
            if match:
                if not in_code_block:
                    # Opening fence
                    language = match.group(1)
                    if not language:
                        issues.append(ValidationIssue(
                            rule_id="MD-002",
                            severity=ValidationSeverity.WARNING,
                            message="Code block missing language specification",
                            file_path=file_path,
                            line_number=line_num,
                            suggestion="Add language after opening fence: ```python, ```javascript, ```bash, etc."
                        ))
                    in_code_block = True
                    code_block_start_line = line_num
                else:
                    # Closing fence
                    in_code_block = False

        # Check if file ends with unclosed code block
        if in_code_block:
            issues.append(ValidationIssue(
                rule_id="MD-002",
                severity=ValidationSeverity.ERROR,
                message=f"Unclosed code block starting at line {code_block_start_line}",
                file_path=file_path,
                line_number=code_block_start_line,
                suggestion="Add closing ``` to end code block"
            ))

        return issues

    def _validate_links(
        self,
        file_path: Path,
        lines: List[str],
        base_path: Path
    ) -> List[ValidationIssue]:
        """
        Validate markdown links.

        Implements MD-003: Link validation.
        - Checks for absolute URLs in internal docs (if relative_links_only is True)
        - Validates that relative link targets exist
        """
        issues: List[ValidationIssue] = []

        # Markdown link pattern: [text](url)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for line_num, line in enumerate(lines, start=1):
            for match in link_pattern.finditer(line):
                link_text = match.group(1)
                link_url = match.group(2)

                # Skip anchor links (same page)
                if link_url.startswith('#'):
                    continue

                # Check for absolute URLs
                if link_url.startswith(('http://', 'https://', 'ftp://')):
                    if self.relative_links_only:
                        issues.append(ValidationIssue(
                            rule_id="MD-003",
                            severity=ValidationSeverity.INFO,
                            message=f"Absolute URL in internal doc: {link_url}",
                            file_path=file_path,
                            line_number=line_num,
                            suggestion="Consider using relative path for internal documentation links"
                        ))
                    continue

                # Validate relative link target exists
                # Remove anchor if present (e.g., "file.md#section")
                link_target = link_url.split('#')[0]

                if link_target:
                    # Resolve relative to current file's directory
                    target_path = (file_path.parent / link_target).resolve()

                    # Check if target exists relative to base path
                    if not target_path.exists():
                        issues.append(ValidationIssue(
                            rule_id="MD-003",
                            severity=ValidationSeverity.ERROR,
                            message=f"Broken link: target not found '{link_url}'",
                            file_path=file_path,
                            line_number=line_num,
                            suggestion=f"Check if '{link_target}' exists or fix the link path"
                        ))

        return issues

    def _validate_trailing_whitespace(
        self,
        file_path: Path,
        lines: List[str]
    ) -> List[ValidationIssue]:
        """
        Check for trailing whitespace on lines.

        Implements MD-004: Trailing whitespace validation.
        Trailing whitespace can cause issues with version control and markdown rendering.
        """
        issues: List[ValidationIssue] = []

        for line_num, line in enumerate(lines, start=1):
            if line != line.rstrip():
                issues.append(ValidationIssue(
                    rule_id="MD-004",
                    severity=ValidationSeverity.INFO,
                    message="Line has trailing whitespace",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion="Remove trailing whitespace from end of line"
                ))

        return issues

    def _validate_horizontal_rules(
        self,
        file_path: Path,
        lines: List[str]
    ) -> List[ValidationIssue]:
        """
        Validate horizontal rule format consistency.

        Implements MD-005: Horizontal rule format validation.
        Checks that horizontal rules match the configured format (default: ---).
        """
        issues: List[ValidationIssue] = []

        # Horizontal rules: ---, ***, ___ (3 or more)
        hr_pattern = re.compile(r'^(\*\*\*+|---+|___+)\s*$')

        for line_num, line in enumerate(lines, start=1):
            match = hr_pattern.match(line.strip())
            if match:
                hr_format = match.group(1)
                # Check if it matches configured format
                if not hr_format.startswith(self.horizontal_rule_format):
                    issues.append(ValidationIssue(
                        rule_id="MD-005",
                        severity=ValidationSeverity.INFO,
                        message=f"Horizontal rule format '{hr_format}' doesn't match configured format '{self.horizontal_rule_format}'",
                        file_path=file_path,
                        line_number=line_num,
                        suggestion=f"Use '{self.horizontal_rule_format}' for consistency"
                    ))

        return issues

    def validate_batch(
        self,
        file_paths: List[Path],
        base_path: Optional[Path] = None
    ) -> dict[Path, List[ValidationIssue]]:
        """
        Validate multiple files and return results.

        Args:
            file_paths: List of file paths to validate
            base_path: Base repository path for link validation

        Returns:
            Dictionary mapping file paths to their validation issues
        """
        results = {}

        for file_path in file_paths:
            self.logger.debug(f"Validating markdown in {file_path}")
            issues = self.validate(file_path, base_path)

            if issues:
                results[file_path] = issues
                self.logger.info(
                    f"Found {len(issues)} markdown issue(s) in {file_path}"
                )
            else:
                self.logger.debug(f"No markdown issues found in {file_path}")

        return results

    def get_error_count(self, issues: List[ValidationIssue]) -> int:
        """Count number of errors in validation issues."""
        return sum(
            1 for issue in issues
            if issue.severity == ValidationSeverity.ERROR
        )

    def get_warning_count(self, issues: List[ValidationIssue]) -> int:
        """Count number of warnings in validation issues."""
        return sum(
            1 for issue in issues
            if issue.severity == ValidationSeverity.WARNING
        )
