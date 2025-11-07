"""
Cache management for document processing state.

Handles persistent storage of document hashes and processing state
to enable incremental processing and change detection.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime
import fcntl
import os


class CacheError(Exception):
    """Raised when cache operations fail."""
    pass


class DocumentCache:
    """
    Persistent cache for document processing state.

    Stores document hashes, timestamps, and validation results to enable
    efficient incremental processing.

    Cache structure:
    {
        "version": "1.0.0",
        "last_updated": "2025-11-07T10:30:00",
        "documents": {
            "path/to/doc.md": {
                "hash": "sha256_hash",
                "last_processed": "2025-11-07T10:30:00",
                "last_modified": "2025-11-07T09:15:00",
                "validation_status": "passed"|"failed",
                "error_count": 0,
                "warning_count": 0
            }
        }
    }
    """

    VERSION = "1.0.0"

    def __init__(self, cache_file: Path):
        """
        Initialize document cache.

        Args:
            cache_file: Path to cache file (JSON format)
        """
        self.cache_file = Path(cache_file)
        self.cache_data: Dict[str, Any] = {
            "version": self.VERSION,
            "last_updated": None,
            "documents": {}
        }

        self._load()

    def _load(self) -> None:
        """
        Load cache from file.

        Creates new cache if file doesn't exist or is invalid.
        """
        if not self.cache_file.exists():
            self._initialize_new_cache()
            return

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                # Acquire shared lock for reading
                if os.name != 'nt':  # Unix-like systems
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)

                loaded_data = json.load(f)

                if os.name != 'nt':
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            # Validate cache version
            if loaded_data.get('version') != self.VERSION:
                # Version mismatch - reinitialize
                self._initialize_new_cache()
                return

            self.cache_data = loaded_data

        except (json.JSONDecodeError, OSError, IOError) as e:
            raise CacheError(f"Failed to load cache from {self.cache_file}: {e}")

    def _initialize_new_cache(self) -> None:
        """Initialize a new empty cache."""
        self.cache_data = {
            "version": self.VERSION,
            "last_updated": self._current_timestamp(),
            "documents": {}
        }
        self.save()

    def _current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def save(self) -> None:
        """
        Save cache to file atomically.

        Uses atomic write pattern to prevent corruption.

        Raises:
            CacheError: If save fails
        """
        # Ensure cache directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Update last_updated timestamp
        self.cache_data['last_updated'] = self._current_timestamp()

        # Write to temporary file first (atomic write pattern)
        temp_file = self.cache_file.with_suffix('.tmp')

        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                # Acquire exclusive lock for writing
                if os.name != 'nt':  # Unix-like systems
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)

                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

                if os.name != 'nt':
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            # Atomic rename
            temp_file.replace(self.cache_file)

        except (OSError, IOError) as e:
            if temp_file.exists():
                temp_file.unlink()
            raise CacheError(f"Failed to save cache to {self.cache_file}: {e}")

    def get_document(self, doc_path: Path) -> Optional[Dict[str, Any]]:
        """
        Get cached data for a document.

        Args:
            doc_path: Path to document

        Returns:
            Cached document data or None if not found
        """
        doc_key = str(doc_path)
        return self.cache_data['documents'].get(doc_key)

    def update_document(
        self,
        doc_path: Path,
        file_hash: str,
        last_modified: Optional[datetime] = None,
        validation_status: Optional[str] = None,
        error_count: int = 0,
        warning_count: int = 0
    ) -> None:
        """
        Update cache entry for a document.

        Args:
            doc_path: Path to document
            file_hash: SHA-256 hash of file content
            last_modified: File modification timestamp
            validation_status: 'passed' or 'failed'
            error_count: Number of validation errors
            warning_count: Number of validation warnings
        """
        doc_key = str(doc_path)

        doc_data = {
            "hash": file_hash,
            "last_processed": self._current_timestamp(),
            "last_modified": last_modified.isoformat() if last_modified else None,
            "validation_status": validation_status,
            "error_count": error_count,
            "warning_count": warning_count
        }

        self.cache_data['documents'][doc_key] = doc_data

    def remove_document(self, doc_path: Path) -> None:
        """
        Remove document from cache.

        Args:
            doc_path: Path to document
        """
        doc_key = str(doc_path)
        if doc_key in self.cache_data['documents']:
            del self.cache_data['documents'][doc_key]

    def has_document_changed(
        self,
        doc_path: Path,
        current_hash: str
    ) -> bool:
        """
        Check if document has changed since last processing.

        Args:
            doc_path: Path to document
            current_hash: Current SHA-256 hash of file

        Returns:
            True if document changed or not in cache, False if unchanged
        """
        cached_doc = self.get_document(doc_path)

        if cached_doc is None:
            return True  # New document

        return cached_doc.get('hash') != current_hash

    def get_all_cached_paths(self) -> list:
        """
        Get list of all document paths in cache.

        Returns:
            List of Path objects for cached documents
        """
        return [Path(path) for path in self.cache_data['documents'].keys()]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        documents = self.cache_data['documents']

        passed = sum(1 for d in documents.values()
                    if d.get('validation_status') == 'passed')
        failed = sum(1 for d in documents.values()
                    if d.get('validation_status') == 'failed')
        total_errors = sum(d.get('error_count', 0) for d in documents.values())
        total_warnings = sum(d.get('warning_count', 0) for d in documents.values())

        return {
            'total_documents': len(documents),
            'passed': passed,
            'failed': failed,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'last_updated': self.cache_data.get('last_updated')
        }

    def clear(self) -> None:
        """Clear all cached documents."""
        self.cache_data['documents'] = {}
        self.cache_data['last_updated'] = self._current_timestamp()

    def __len__(self) -> int:
        """Return number of cached documents."""
        return len(self.cache_data['documents'])

    def __contains__(self, doc_path: Path) -> bool:
        """Check if document is in cache."""
        return str(doc_path) in self.cache_data['documents']

    def __repr__(self) -> str:
        """String representation of cache."""
        return (
            f"DocumentCache(file={self.cache_file}, "
            f"documents={len(self)}, "
            f"version={self.VERSION})"
        )


def compute_file_hash(file_path: Path) -> str:
    """
    Compute SHA-256 hash of file content.

    Args:
        file_path: Path to file

    Returns:
        Hexadecimal string of SHA-256 hash

    Raises:
        CacheError: If file cannot be read
    """
    try:
        sha256_hash = hashlib.sha256()

        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    except (OSError, IOError) as e:
        raise CacheError(f"Failed to compute hash for {file_path}: {e}")
