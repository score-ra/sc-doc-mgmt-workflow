"""
YAML frontmatter validation for markdown documents.

This module validates YAML frontmatter against required fields and standards
defined in the configuration file (ADR-001: 3 required fields).
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.frontmatter import parse_frontmatter, has_frontmatter, FrontmatterError


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """
    Represents a validation issue found in a document.

    Attributes:
        rule_id: Unique identifier for the validation rule (e.g., 'YAML-001')
        severity: Severity level of the issue
        message: Human-readable description of the issue
        file_path: Path to the file with the issue
        line_number: Optional line number where issue occurs
        suggestion: Optional suggestion for fixing the issue
    """
    rule_id: str
    severity: ValidationSeverity
    message: str
    file_path: Path
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        """Format validation issue as a readable string."""
        location = f"{self.file_path}"
        if self.line_number:
            location += f":{self.line_number}"

        parts = [f"[{self.severity.value.upper()}] {location}"]
        parts.append(f"  {self.rule_id}: {self.message}")
        if self.suggestion:
            parts.append(f"  Suggestion: {self.suggestion}")

        return "\n".join(parts)


class YAMLValidator:
    """
    Validates YAML frontmatter in markdown documents.

    Implements validation rules:
    - YAML-001: YAML frontmatter block present
    - YAML-002: Required fields present (title, tags, status)
    - YAML-003: Status value in allowed list
    - YAML-004: Tags field is a list
    """

    def __init__(self, config: Config, logger: Logger):
        """
        Initialize YAML validator.

        Args:
            config: Configuration object with validation settings
            logger: Logger for diagnostic messages
        """
        self.config = config
        self.logger = logger

        # Load validation settings from config
        self.enabled = config.get('validation.yaml.enabled', True)
        self.required_fields = config.get(
            'validation.yaml.required_fields',
            ['title', 'tags', 'status']
        )
        self.allowed_statuses = config.get(
            'validation.yaml.allowed_statuses',
            ['draft', 'review', 'approved', 'active', 'deprecated']
        )

    def validate(self, file_path: Path) -> List[ValidationIssue]:
        """
        Validate YAML frontmatter in a markdown file.

        Args:
            file_path: Path to the markdown file to validate

        Returns:
            List of ValidationIssue objects (empty if no issues found)
        """
        if not self.enabled:
            self.logger.debug(f"YAML validation disabled, skipping {file_path}")
            return []

        if not file_path.exists():
            return [ValidationIssue(
                rule_id="YAML-000",
                severity=ValidationSeverity.ERROR,
                message=f"File not found: {file_path}",
                file_path=file_path
            )]

        issues: List[ValidationIssue] = []

        # YAML-001: Check if YAML frontmatter block is present
        try:
            has_yaml = has_frontmatter(file_path)
        except Exception as e:
            self.logger.error(f"Error checking frontmatter in {file_path}: {e}")
            return [ValidationIssue(
                rule_id="YAML-000",
                severity=ValidationSeverity.ERROR,
                message=f"Error reading file: {str(e)}",
                file_path=file_path
            )]

        if not has_yaml:
            issues.append(self._create_missing_frontmatter_issue(file_path))
            # If no frontmatter, no point checking other rules
            return issues

        # Parse frontmatter
        try:
            metadata = parse_frontmatter(file_path)
        except FrontmatterError as e:
            issues.append(ValidationIssue(
                rule_id="YAML-001",
                severity=ValidationSeverity.ERROR,
                message=f"Malformed YAML frontmatter: {str(e)}",
                file_path=file_path,
                suggestion="Fix YAML syntax errors in frontmatter"
            ))
            # Can't validate further if YAML is malformed
            return issues

        # YAML-002: Check required fields are present
        issues.extend(self._validate_required_fields(file_path, metadata))

        # YAML-003: Validate status field value (if present)
        if 'status' in metadata:
            issues.extend(self._validate_status(file_path, metadata))

        # YAML-004: Validate tags field is a list (if present)
        if 'tags' in metadata:
            issues.extend(self._validate_tags_format(file_path, metadata))

        return issues

    def _create_missing_frontmatter_issue(self, file_path: Path) -> ValidationIssue:
        """Create validation issue for missing frontmatter."""
        return ValidationIssue(
            rule_id="YAML-001",
            severity=ValidationSeverity.ERROR,
            message="YAML frontmatter block is missing",
            file_path=file_path,
            line_number=1,
            suggestion=(
                "Add YAML frontmatter at the start of the file:\n"
                "---\n"
                "title: Your Document Title\n"
                f"tags: [tag1, tag2]\n"
                "status: draft\n"
                "---"
            )
        )

    def _validate_required_fields(
        self,
        file_path: Path,
        metadata: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """
        Validate that all required fields are present.

        Implements YAML-002: Required fields validation.
        """
        issues: List[ValidationIssue] = []
        missing_fields = []

        for field in self.required_fields:
            if field not in metadata:
                missing_fields.append(field)

        if missing_fields:
            field_list = ", ".join(missing_fields)
            issues.append(ValidationIssue(
                rule_id="YAML-002",
                severity=ValidationSeverity.ERROR,
                message=f"Missing required field(s): {field_list}",
                file_path=file_path,
                suggestion=f"Add the following field(s) to frontmatter: {field_list}"
            ))

        return issues

    def _validate_status(
        self,
        file_path: Path,
        metadata: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """
        Validate status field value is in allowed list.

        Implements YAML-003: Status value validation.
        """
        issues: List[ValidationIssue] = []
        status = metadata.get('status')

        # Check if status is a string
        if not isinstance(status, str):
            issues.append(ValidationIssue(
                rule_id="YAML-003",
                severity=ValidationSeverity.ERROR,
                message=f"Status must be a string, got {type(status).__name__}",
                file_path=file_path,
                suggestion=f"Change status to one of: {', '.join(self.allowed_statuses)}"
            ))
            return issues

        # Check if status is in allowed list
        if status not in self.allowed_statuses:
            issues.append(ValidationIssue(
                rule_id="YAML-003",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid status value: '{status}'",
                file_path=file_path,
                suggestion=f"Use one of the allowed values: {', '.join(self.allowed_statuses)}"
            ))

        return issues

    def _validate_tags_format(
        self,
        file_path: Path,
        metadata: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """
        Validate tags field is a list, not a string.

        Implements YAML-004: Tags format validation.
        """
        issues: List[ValidationIssue] = []
        tags = metadata.get('tags')

        # Check if tags is a list
        if not isinstance(tags, list):
            issues.append(ValidationIssue(
                rule_id="YAML-004",
                severity=ValidationSeverity.ERROR,
                message=f"Tags must be a list, got {type(tags).__name__}",
                file_path=file_path,
                suggestion=(
                    "Change tags format from string to list. "
                    "Example: tags: [pricing, policy] or tags:\n  - pricing\n  - policy"
                )
            ))
            return issues

        # Additional validation: check that all tag items are strings
        non_string_tags = [
            tag for tag in tags if not isinstance(tag, str)
        ]

        if non_string_tags:
            issues.append(ValidationIssue(
                rule_id="YAML-004",
                severity=ValidationSeverity.WARNING,
                message="All tags should be strings",
                file_path=file_path,
                suggestion="Ensure all items in the tags list are strings"
            ))

        return issues

    def validate_batch(self, file_paths: List[Path]) -> Dict[Path, List[ValidationIssue]]:
        """
        Validate multiple files and return results.

        Args:
            file_paths: List of file paths to validate

        Returns:
            Dictionary mapping file paths to their validation issues
        """
        results = {}

        for file_path in file_paths:
            self.logger.debug(f"Validating YAML in {file_path}")
            issues = self.validate(file_path)

            if issues:
                results[file_path] = issues
                self.logger.info(
                    f"Found {len(issues)} issue(s) in {file_path}"
                )
            else:
                self.logger.debug(f"No issues found in {file_path}")

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
