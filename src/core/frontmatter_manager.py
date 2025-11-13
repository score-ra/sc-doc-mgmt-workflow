"""
Bulk frontmatter field management for markdown documents.

This module provides functionality for adding, updating, or removing frontmatter
fields across multiple markdown documents in bulk operations. It builds on top
of the lower-level frontmatter utilities to provide batch processing capabilities.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from src.utils.frontmatter import (
    has_frontmatter,
    parse_frontmatter,
    update_frontmatter,
    add_frontmatter,
    FrontmatterError
)
from src.utils.logger import Logger


@dataclass
class FrontmatterOperationResult:
    """Result of a frontmatter operation on a single file."""
    file_path: Path
    success: bool
    message: str
    field_name: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None


class FrontmatterManager:
    """
    Manages bulk frontmatter operations across multiple markdown documents.

    This class provides high-level methods for adding, updating, or removing
    frontmatter fields across multiple files, with support for filtering,
    validation, and detailed reporting.
    """

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize the FrontmatterManager.

        Args:
            logger: Optional logger instance for operation logging
        """
        self.logger = logger or Logger("frontmatter_manager")

    def add_field_to_documents(
        self,
        documents: List[Path],
        field_name: str,
        field_value: Any,
        overwrite: bool = False,
        only_if_missing: bool = True
    ) -> List[FrontmatterOperationResult]:
        """
        Add a field to multiple markdown documents.

        Args:
            documents: List of Path objects for markdown files
            field_name: Name of the field to add
            field_value: Value to set for the field
            overwrite: If True, overwrite existing field values
            only_if_missing: If True, only add to documents that don't have the field

        Returns:
            List of FrontmatterOperationResult objects with operation results
        """
        results = []

        for doc_path in documents:
            try:
                result = self._add_field_to_document(
                    doc_path,
                    field_name,
                    field_value,
                    overwrite,
                    only_if_missing
                )
                results.append(result)

                if result.success:
                    self.logger.info(f"Added field '{field_name}' to {doc_path}")
                else:
                    self.logger.warning(f"Skipped {doc_path}: {result.message}")

            except Exception as e:
                error_msg = f"Error processing {doc_path}: {str(e)}"
                self.logger.error(error_msg)
                results.append(FrontmatterOperationResult(
                    file_path=doc_path,
                    success=False,
                    message=error_msg,
                    field_name=field_name
                ))

        return results

    def _add_field_to_document(
        self,
        doc_path: Path,
        field_name: str,
        field_value: Any,
        overwrite: bool,
        only_if_missing: bool
    ) -> FrontmatterOperationResult:
        """
        Add a field to a single document.

        Args:
            doc_path: Path to the markdown file
            field_name: Name of the field to add
            field_value: Value to set for the field
            overwrite: If True, overwrite existing field values
            only_if_missing: If True, only add if field doesn't exist

        Returns:
            FrontmatterOperationResult with operation details
        """
        # Validate file exists and is a markdown file
        if not doc_path.exists():
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message="File not found",
                field_name=field_name
            )

        if doc_path.suffix.lower() != '.md':
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message="Not a markdown file",
                field_name=field_name
            )

        # Check if document has frontmatter, create if missing
        if not has_frontmatter(doc_path):
            # Create new frontmatter with the field
            metadata = {field_name: field_value}
            add_frontmatter(doc_path, metadata, preserve_content=True)
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=True,
                message="Created frontmatter and added field",
                field_name=field_name,
                old_value=None,
                new_value=field_value
            )

        # Parse existing frontmatter
        try:
            metadata = parse_frontmatter(doc_path)
        except FrontmatterError as e:
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message=f"Failed to parse frontmatter: {str(e)}",
                field_name=field_name
            )

        # Check if field already exists
        old_value = metadata.get(field_name)
        field_exists = field_name in metadata

        if field_exists and only_if_missing:
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message=f"Field '{field_name}' already exists (use --overwrite to replace)",
                field_name=field_name,
                old_value=old_value,
                new_value=None
            )

        if field_exists and not overwrite:
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message=f"Field '{field_name}' already exists (use --overwrite to replace)",
                field_name=field_name,
                old_value=old_value,
                new_value=None
            )

        # Add or update the field
        update_frontmatter(doc_path, {field_name: field_value}, merge=True)

        action = "Updated" if field_exists else "Added"
        return FrontmatterOperationResult(
            file_path=doc_path,
            success=True,
            message=f"{action} field '{field_name}'",
            field_name=field_name,
            old_value=old_value,
            new_value=field_value
        )

    def remove_field_from_documents(
        self,
        documents: List[Path],
        field_name: str,
        ignore_missing: bool = True
    ) -> List[FrontmatterOperationResult]:
        """
        Remove a field from multiple markdown documents.

        Args:
            documents: List of Path objects for markdown files
            field_name: Name of the field to remove
            ignore_missing: If True, don't report error if field doesn't exist

        Returns:
            List of FrontmatterOperationResult objects with operation results
        """
        results = []

        for doc_path in documents:
            try:
                result = self._remove_field_from_document(
                    doc_path,
                    field_name,
                    ignore_missing
                )
                results.append(result)

                if result.success:
                    self.logger.info(f"Removed field '{field_name}' from {doc_path}")
                else:
                    self.logger.warning(f"Skipped {doc_path}: {result.message}")

            except Exception as e:
                error_msg = f"Error processing {doc_path}: {str(e)}"
                self.logger.error(error_msg)
                results.append(FrontmatterOperationResult(
                    file_path=doc_path,
                    success=False,
                    message=error_msg,
                    field_name=field_name
                ))

        return results

    def _remove_field_from_document(
        self,
        doc_path: Path,
        field_name: str,
        ignore_missing: bool
    ) -> FrontmatterOperationResult:
        """
        Remove a field from a single document.

        Args:
            doc_path: Path to the markdown file
            field_name: Name of the field to remove
            ignore_missing: If True, don't report error if field doesn't exist

        Returns:
            FrontmatterOperationResult with operation details
        """
        # Validate file
        if not doc_path.exists():
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message="File not found",
                field_name=field_name
            )

        if not has_frontmatter(doc_path):
            message = "No frontmatter found"
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=ignore_missing,
                message=message,
                field_name=field_name
            )

        # Parse frontmatter
        try:
            metadata = parse_frontmatter(doc_path)
        except FrontmatterError as e:
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=False,
                message=f"Failed to parse frontmatter: {str(e)}",
                field_name=field_name
            )

        # Check if field exists
        if field_name not in metadata:
            message = f"Field '{field_name}' not found"
            return FrontmatterOperationResult(
                file_path=doc_path,
                success=ignore_missing,
                message=message,
                field_name=field_name
            )

        # Remove the field
        old_value = metadata[field_name]
        del metadata[field_name]

        # Update frontmatter without the field
        add_frontmatter(doc_path, metadata, preserve_content=True)

        return FrontmatterOperationResult(
            file_path=doc_path,
            success=True,
            message=f"Removed field '{field_name}'",
            field_name=field_name,
            old_value=old_value,
            new_value=None
        )

    def find_documents_with_field(
        self,
        documents: List[Path],
        field_name: str,
        field_value: Optional[Any] = None
    ) -> List[Tuple[Path, Any]]:
        """
        Find documents that have a specific field (optionally with a specific value).

        Args:
            documents: List of Path objects for markdown files
            field_name: Name of the field to search for
            field_value: Optional specific value to match (None = any value)

        Returns:
            List of tuples (file_path, field_value) for matching documents
        """
        matching_docs = []

        for doc_path in documents:
            try:
                if not has_frontmatter(doc_path):
                    continue

                metadata = parse_frontmatter(doc_path)

                if field_name in metadata:
                    doc_value = metadata[field_name]

                    # If specific value requested, check for match
                    if field_value is not None:
                        if doc_value == field_value:
                            matching_docs.append((doc_path, doc_value))
                    else:
                        # No specific value, include any document with the field
                        matching_docs.append((doc_path, doc_value))

            except Exception as e:
                self.logger.warning(f"Error processing {doc_path}: {str(e)}")
                continue

        return matching_docs

    def find_documents_without_field(
        self,
        documents: List[Path],
        field_name: str
    ) -> List[Path]:
        """
        Find documents that are missing a specific field.

        Args:
            documents: List of Path objects for markdown files
            field_name: Name of the field to check for

        Returns:
            List of Path objects for documents missing the field
        """
        missing_docs = []

        for doc_path in documents:
            try:
                if not has_frontmatter(doc_path):
                    missing_docs.append(doc_path)
                    continue

                metadata = parse_frontmatter(doc_path)

                if field_name not in metadata:
                    missing_docs.append(doc_path)

            except Exception as e:
                self.logger.warning(f"Error processing {doc_path}: {str(e)}")
                continue

        return missing_docs

    def generate_summary_report(
        self,
        results: List[FrontmatterOperationResult]
    ) -> Dict[str, Any]:
        """
        Generate a summary report from operation results.

        Args:
            results: List of FrontmatterOperationResult objects

        Returns:
            Dictionary containing summary statistics and details
        """
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful

        # Group by message for failure analysis
        failure_reasons = {}
        for result in results:
            if not result.success:
                reason = result.message
                if reason not in failure_reasons:
                    failure_reasons[reason] = []
                failure_reasons[reason].append(str(result.file_path))

        return {
            'total_documents': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'failure_reasons': failure_reasons,
            'results': results
        }
