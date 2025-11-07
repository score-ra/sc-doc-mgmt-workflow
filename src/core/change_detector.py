"""
Change detection for markdown documents.

Detects new, modified, and deleted documents using SHA-256 file hashing
and persistent caching for efficient incremental processing.
"""

from pathlib import Path
from typing import List, Set, Dict, Any, Tuple
from datetime import datetime
from ..utils.cache import DocumentCache, compute_file_hash, CacheError
from ..utils.logger import Logger


class ChangeDetectionError(Exception):
    """Raised when change detection fails."""
    pass


class ChangeDetector:
    """
    Detects changes in markdown documents for incremental processing.

    Uses file hashing (SHA-256) and persistent caching to identify:
    - New documents (not in cache)
    - Modified documents (hash changed)
    - Deleted documents (in cache but file missing)
    - Unchanged documents (same hash as cache)

    Attributes:
        cache: DocumentCache instance for persistent storage
        logger: Logger instance for tracking operations
    """

    def __init__(self, cache: DocumentCache, logger: Logger):
        """
        Initialize change detector.

        Args:
            cache: DocumentCache instance
            logger: Logger instance
        """
        self.cache = cache
        self.logger = logger

    def scan_directory(
        self,
        directory: Path,
        include_patterns: List[str] = None,
        exclude_patterns: List[str] = None,
        recursive: bool = True
    ) -> List[Path]:
        """
        Scan directory for markdown files matching patterns.

        Args:
            directory: Directory to scan
            include_patterns: Glob patterns to include (e.g., ["**/*.md"])
            exclude_patterns: Glob patterns to exclude (e.g., ["_meta/**"])
            recursive: Scan subdirectories recursively

        Returns:
            List of Path objects for matching markdown files

        Raises:
            ChangeDetectionError: If directory doesn't exist or cannot be scanned
        """
        if not directory.exists():
            raise ChangeDetectionError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ChangeDetectionError(f"Not a directory: {directory}")

        if include_patterns is None:
            include_patterns = ["**/*.md" if recursive else "*.md"]

        if exclude_patterns is None:
            exclude_patterns = []

        self.logger.debug(f"Scanning directory: {directory}")
        self.logger.debug(f"Include patterns: {include_patterns}")
        self.logger.debug(f"Exclude patterns: {exclude_patterns}")

        found_files: Set[Path] = set()

        # Find files matching include patterns
        for pattern in include_patterns:
            matching_files = directory.glob(pattern)
            found_files.update(matching_files)

        self.logger.debug(f"Found {len(found_files)} files matching include patterns")

        # Filter out files matching exclude patterns
        excluded_files: Set[Path] = set()
        for pattern in exclude_patterns:
            matching_excluded = directory.glob(pattern)
            excluded_files.update(matching_excluded)

        filtered_files = found_files - excluded_files

        self.logger.info(
            f"Scanned {directory}: found {len(filtered_files)} markdown files "
            f"({len(excluded_files)} excluded)"
        )

        return sorted(filtered_files)

    def detect_changes(
        self,
        current_files: List[Path],
        force_reprocess: bool = False
    ) -> Dict[str, List[Path]]:
        """
        Detect changes in documents by comparing with cache.

        Args:
            current_files: List of current document paths
            force_reprocess: If True, treat all files as changed

        Returns:
            Dictionary with keys: 'new', 'modified', 'unchanged', 'deleted'
            Each value is a list of Path objects

        Raises:
            ChangeDetectionError: If change detection fails
        """
        self.logger.info(f"Detecting changes in {len(current_files)} files")

        changes: Dict[str, List[Path]] = {
            'new': [],
            'modified': [],
            'unchanged': [],
            'deleted': []
        }

        # If force reprocess, treat all as modified
        if force_reprocess:
            self.logger.info("Force reprocess enabled - treating all files as changed")
            changes['modified'] = current_files
            return changes

        # Check each current file
        for file_path in current_files:
            try:
                # Compute current hash
                current_hash = compute_file_hash(file_path)

                # Check if file is in cache and compare hash
                if self.cache.has_document_changed(file_path, current_hash):
                    # New or modified
                    if file_path in self.cache:
                        changes['modified'].append(file_path)
                        self.logger.debug(f"Modified: {file_path}")
                    else:
                        changes['new'].append(file_path)
                        self.logger.debug(f"New: {file_path}")
                else:
                    # Unchanged
                    changes['unchanged'].append(file_path)
                    self.logger.debug(f"Unchanged: {file_path}")

            except CacheError as e:
                self.logger.warning(f"Failed to compute hash for {file_path}: {e}")
                # Treat as modified to be safe
                changes['modified'].append(file_path)

        # Check for deleted files (in cache but not in current files)
        current_file_set = set(current_files)
        cached_paths = self.cache.get_all_cached_paths()

        for cached_path in cached_paths:
            if cached_path not in current_file_set:
                changes['deleted'].append(cached_path)
                self.logger.debug(f"Deleted: {cached_path}")

        # Log summary
        self.logger.info(
            f"Changes detected - "
            f"New: {len(changes['new'])}, "
            f"Modified: {len(changes['modified'])}, "
            f"Unchanged: {len(changes['unchanged'])}, "
            f"Deleted: {len(changes['deleted'])}"
        )

        return changes

    def update_cache_for_file(
        self,
        file_path: Path,
        validation_status: str = None,
        error_count: int = 0,
        warning_count: int = 0
    ) -> None:
        """
        Update cache entry for a processed file.

        Args:
            file_path: Path to processed file
            validation_status: 'passed' or 'failed'
            error_count: Number of validation errors
            warning_count: Number of validation warnings

        Raises:
            ChangeDetectionError: If cache update fails
        """
        try:
            # Compute hash and get modification time
            file_hash = compute_file_hash(file_path)
            last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)

            # Update cache
            self.cache.update_document(
                doc_path=file_path,
                file_hash=file_hash,
                last_modified=last_modified,
                validation_status=validation_status,
                error_count=error_count,
                warning_count=warning_count
            )

            self.logger.debug(f"Updated cache for: {file_path}")

        except (CacheError, OSError) as e:
            raise ChangeDetectionError(
                f"Failed to update cache for {file_path}: {e}"
            )

    def remove_deleted_from_cache(self, deleted_files: List[Path]) -> None:
        """
        Remove deleted files from cache.

        Args:
            deleted_files: List of deleted file paths
        """
        for file_path in deleted_files:
            self.cache.remove_document(file_path)
            self.logger.debug(f"Removed from cache: {file_path}")

        if deleted_files:
            self.logger.info(f"Removed {len(deleted_files)} deleted files from cache")

    def get_files_to_process(
        self,
        directory: Path,
        include_patterns: List[str] = None,
        exclude_patterns: List[str] = None,
        force_reprocess: bool = False
    ) -> Tuple[List[Path], Dict[str, Any]]:
        """
        Get list of files that need processing based on changes.

        Convenience method that combines scanning and change detection.

        Args:
            directory: Directory to scan
            include_patterns: Glob patterns to include
            exclude_patterns: Glob patterns to exclude
            force_reprocess: Treat all files as changed

        Returns:
            Tuple of (files_to_process, change_summary)
            files_to_process: List of Path objects needing processing
            change_summary: Dictionary with change statistics

        Raises:
            ChangeDetectionError: If scanning or detection fails
        """
        # Scan directory
        current_files = self.scan_directory(
            directory=directory,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns
        )

        # Detect changes
        changes = self.detect_changes(
            current_files=current_files,
            force_reprocess=force_reprocess
        )

        # Files to process are new + modified
        files_to_process = changes['new'] + changes['modified']

        # Clean up deleted files from cache
        if changes['deleted']:
            self.remove_deleted_from_cache(changes['deleted'])

        # Build summary
        change_summary = {
            'total_files': len(current_files),
            'files_to_process': len(files_to_process),
            'new_files': len(changes['new']),
            'modified_files': len(changes['modified']),
            'unchanged_files': len(changes['unchanged']),
            'deleted_files': len(changes['deleted'])
        }

        return files_to_process, change_summary

    def save_cache(self) -> None:
        """
        Save cache to disk.

        Raises:
            ChangeDetectionError: If save fails
        """
        try:
            self.cache.save()
            self.logger.debug("Cache saved successfully")
        except CacheError as e:
            raise ChangeDetectionError(f"Failed to save cache: {e}")
