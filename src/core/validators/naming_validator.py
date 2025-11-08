"""
File and directory naming convention validation for markdown documents.

This module validates file and directory names against naming standards
defined in the configuration file (lowercase-with-hyphens pattern).
"""

from pathlib import Path
from typing import List, Optional
import re

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


class NamingValidator:
    """
    Validates file and directory naming conventions.

    Implements validation rules:
    - NAME-001: Directory names must be lowercase-with-hyphens
    - NAME-002: Filenames must not contain spaces
    - NAME-003: Filenames must not exceed maximum length
    - NAME-004: Filenames must meet minimum length
    - NAME-005: Filenames must use valid characters only
    """

    def __init__(self, config: Config, logger: Logger):
        """
        Initialize naming validator.

        Args:
            config: Configuration object with validation settings
            logger: Logger for diagnostic messages
        """
        self.config = config
        self.logger = logger

        # Load naming validation settings from config
        self.enabled = config.get('validation.naming.enabled', True)
        self.pattern = config.get('validation.naming.pattern', 'lowercase-with-hyphens')
        self.max_length = config.get('validation.naming.max_length', 50)
        self.min_length = config.get('validation.naming.min_length', 5)
        self.no_version_numbers = config.get('validation.naming.no_version_numbers', True)

        # Exceptions (from START_HERE.md guidance)
        self.allow_uppercase_files = ['README.md', 'LICENSE', 'CHANGELOG.md', 'CLAUDE.md']
        self.allow_spaces_extensions = ['.csv']

    def validate(self, file_path: Path, base_path: Optional[Path] = None) -> List[ValidationIssue]:
        """
        Validate naming conventions for a file and its parent directories.

        Args:
            file_path: Path to the file to validate
            base_path: Base repository path (to check relative directories)

        Returns:
            List of ValidationIssue objects (empty if no issues found)
        """
        if not self.enabled:
            self.logger.debug(f"Naming validation disabled, skipping {file_path}")
            return []

        if not file_path.exists():
            return [ValidationIssue(
                rule_id="NAME-000",
                severity=ValidationSeverity.ERROR,
                message=f"File not found: {file_path}",
                file_path=file_path
            )]

        issues: List[ValidationIssue] = []

        # Validate filename
        issues.extend(self._validate_filename(file_path))

        # Validate directory names (if base_path provided)
        if base_path:
            issues.extend(self._validate_directories(file_path, base_path))

        return issues

    def _validate_filename(self, file_path: Path) -> List[ValidationIssue]:
        """
        Validate filename against naming conventions.

        Checks for:
        - Spaces in filename
        - Uppercase letters (except for exceptions)
        - Length limits
        - Version numbers (if disallowed)
        """
        issues: List[ValidationIssue] = []
        filename = file_path.name
        stem = file_path.stem  # Filename without extension
        extension = file_path.suffix

        # Skip validation for exception files
        if filename in self.allow_uppercase_files:
            self.logger.debug(f"Skipping naming validation for exception file: {filename}")
            return []

        # Skip space check for exception extensions
        if extension in self.allow_spaces_extensions:
            self.logger.debug(f"Skipping space check for {extension} file: {filename}")
        else:
            # NAME-002: Check for spaces in filename
            if ' ' in filename:
                # Convert spaces to hyphens AND lowercase for consistency
                suggested_name = self._convert_to_lowercase_with_hyphens(stem) + extension
                issues.append(ValidationIssue(
                    rule_id="NAME-002",
                    severity=ValidationSeverity.ERROR,
                    message=f"Filename contains spaces: '{filename}'",
                    file_path=file_path,
                    suggestion=f"Rename to: '{suggested_name}'"
                ))

        # NAME-001: Check for uppercase letters in filename (lowercase-with-hyphens pattern)
        if self.pattern == 'lowercase-with-hyphens':
            # Allow uppercase in extension (e.g., .MD is okay)
            if stem != stem.lower():
                suggested_name = self._convert_to_lowercase_with_hyphens(stem) + extension
                issues.append(ValidationIssue(
                    rule_id="NAME-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Filename must be lowercase-with-hyphens: '{filename}'",
                    file_path=file_path,
                    suggestion=f"Rename to: '{suggested_name}'"
                ))

        # NAME-003: Check maximum length (excluding extension)
        if len(stem) > self.max_length:
            issues.append(ValidationIssue(
                rule_id="NAME-003",
                severity=ValidationSeverity.WARNING,
                message=f"Filename exceeds maximum length ({len(stem)} > {self.max_length}): '{filename}'",
                file_path=file_path,
                suggestion=f"Consider shortening filename to under {self.max_length} characters"
            ))

        # NAME-004: Check minimum length (excluding extension)
        if len(stem) < self.min_length:
            issues.append(ValidationIssue(
                rule_id="NAME-004",
                severity=ValidationSeverity.WARNING,
                message=f"Filename too short ({len(stem)} < {self.min_length}): '{filename}'",
                file_path=file_path,
                suggestion=f"Use more descriptive filename (min {self.min_length} characters)"
            ))

        # NAME-005: Check for version numbers in filename (if disallowed)
        if self.no_version_numbers:
            # Match explicit version patterns with "v" prefix: -v1, _v2.0, -v1.2.3, -version1, etc.
            # Require "v" or "ver" or "version" prefix to avoid false positives with KB numbers
            version_pattern = r'[-_](v|ver|version)\d+(\.\d+)*($|[-_])'
            if re.search(version_pattern, stem, re.IGNORECASE):
                issues.append(ValidationIssue(
                    rule_id="NAME-005",
                    severity=ValidationSeverity.WARNING,
                    message=f"Filename contains version number: '{filename}'",
                    file_path=file_path,
                    suggestion="Use frontmatter 'version' field instead of versioning in filename"
                ))

        return issues

    def _validate_directories(
        self,
        file_path: Path,
        base_path: Path
    ) -> List[ValidationIssue]:
        """
        Validate directory names in the path (relative to base_path).

        Checks for:
        - Uppercase letters in directory names
        - Spaces in directory names
        """
        issues: List[ValidationIssue] = []

        try:
            relative_path = file_path.relative_to(base_path)
        except ValueError:
            self.logger.warning(f"File {file_path} is not relative to base {base_path}")
            return issues

        # Check each directory component
        for i, part in enumerate(relative_path.parts[:-1]):  # Exclude filename
            # NAME-001: Check for uppercase in directory names
            if part != part.lower():
                suggested_name = part.lower()
                issues.append(ValidationIssue(
                    rule_id="NAME-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Directory name must be lowercase: '{part}'",
                    file_path=file_path,
                    suggestion=f"Rename directory '{part}' to '{suggested_name}'"
                ))

            # NAME-002: Check for spaces in directory names
            if ' ' in part:
                suggested_name = part.replace(' ', '-')
                issues.append(ValidationIssue(
                    rule_id="NAME-002",
                    severity=ValidationSeverity.ERROR,
                    message=f"Directory name contains spaces: '{part}'",
                    file_path=file_path,
                    suggestion=f"Rename directory '{part}' to '{suggested_name}'"
                ))

        return issues

    def _convert_to_lowercase_with_hyphens(self, text: str) -> str:
        """
        Convert text to lowercase-with-hyphens format.

        Handles:
        - Spaces → hyphens
        - Underscores → hyphens
        - CamelCase → lowercase-with-hyphens
        - Multiple consecutive hyphens → single hyphen
        """
        # Replace underscores and spaces with hyphens
        text = text.replace('_', '-').replace(' ', '-')

        # Insert hyphen before uppercase letters (for CamelCase)
        text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)

        # Convert to lowercase
        text = text.lower()

        # Replace multiple consecutive hyphens with single hyphen
        text = re.sub(r'-+', '-', text)

        # Remove leading/trailing hyphens
        text = text.strip('-')

        return text

    def validate_batch(
        self,
        file_paths: List[Path],
        base_path: Optional[Path] = None
    ) -> dict[Path, List[ValidationIssue]]:
        """
        Validate multiple files and return results.

        Args:
            file_paths: List of file paths to validate
            base_path: Base repository path for directory validation

        Returns:
            Dictionary mapping file paths to their validation issues
        """
        results = {}

        for file_path in file_paths:
            self.logger.debug(f"Validating naming for {file_path}")
            issues = self.validate(file_path, base_path)

            if issues:
                results[file_path] = issues
                self.logger.info(
                    f"Found {len(issues)} naming issue(s) in {file_path}"
                )
            else:
                self.logger.debug(f"No naming issues found in {file_path}")

        return results

    def get_rename_suggestions(self, file_path: Path) -> dict[str, str]:
        """
        Generate rename suggestions for a file with naming violations.

        Returns:
            Dictionary with 'filename' and/or 'directories' suggestions
        """
        suggestions = {}
        issues = self._validate_filename(file_path)

        # Extract suggestions from issues
        for issue in issues:
            if issue.suggestion and 'Rename to:' in issue.suggestion:
                # Extract suggested name from suggestion text
                match = re.search(r"Rename to: '([^']+)'", issue.suggestion)
                if match:
                    suggestions['filename'] = match.group(1)
                    break

        return suggestions
