"""
Tests for cache management module.
"""

import pytest
from pathlib import Path
from datetime import datetime
from src.utils.cache import DocumentCache, compute_file_hash, CacheError
import tempfile
import json


class TestDocumentCache:
    """Tests for DocumentCache class."""

    @pytest.fixture
    def temp_cache_file(self, tmp_path):
        """Create a temporary cache file."""
        return tmp_path / ".test-cache.json"

    @pytest.fixture
    def cache(self, temp_cache_file):
        """Create a DocumentCache instance."""
        return DocumentCache(temp_cache_file)

    def test_init_creates_new_cache(self, temp_cache_file):
        """Test cache initialization creates new file."""
        cache = DocumentCache(temp_cache_file)

        assert temp_cache_file.exists()
        assert len(cache) == 0
        assert cache.cache_data['version'] == DocumentCache.VERSION

    def test_init_loads_existing_cache(self, temp_cache_file):
        """Test cache loads existing valid cache file."""
        # Create existing cache
        existing_data = {
            "version": DocumentCache.VERSION,
            "last_updated": "2025-11-07T10:00:00",
            "documents": {
                "test.md": {
                    "hash": "abc123",
                    "last_processed": "2025-11-07T09:00:00"
                }
            }
        }

        with open(temp_cache_file, 'w') as f:
            json.dump(existing_data, f)

        # Load cache
        cache = DocumentCache(temp_cache_file)

        assert len(cache) == 1
        assert "test.md" in cache.cache_data['documents']

    def test_update_document(self, cache):
        """Test updating document in cache."""
        doc_path = Path("test.md")
        file_hash = "abc123def456"
        last_modified = datetime.now()

        cache.update_document(
            doc_path=doc_path,
            file_hash=file_hash,
            last_modified=last_modified,
            validation_status="passed",
            error_count=0,
            warning_count=2
        )

        assert len(cache) == 1
        doc_data = cache.get_document(doc_path)
        assert doc_data['hash'] == file_hash
        assert doc_data['validation_status'] == "passed"
        assert doc_data['error_count'] == 0
        assert doc_data['warning_count'] == 2

    def test_get_document_not_found(self, cache):
        """Test getting non-existent document returns None."""
        result = cache.get_document(Path("nonexistent.md"))
        assert result is None

    def test_has_document_changed_new_document(self, cache):
        """Test new document is detected as changed."""
        result = cache.has_document_changed(Path("new.md"), "hash123")
        assert result is True

    def test_has_document_changed_same_hash(self, cache):
        """Test unchanged document is detected correctly."""
        doc_path = Path("test.md")
        file_hash = "hash123"

        cache.update_document(doc_path, file_hash)

        result = cache.has_document_changed(doc_path, file_hash)
        assert result is False

    def test_has_document_changed_different_hash(self, cache):
        """Test modified document is detected."""
        doc_path = Path("test.md")

        cache.update_document(doc_path, "old_hash")

        result = cache.has_document_changed(doc_path, "new_hash")
        assert result is True

    def test_remove_document(self, cache):
        """Test removing document from cache."""
        doc_path = Path("test.md")

        cache.update_document(doc_path, "hash123")
        assert len(cache) == 1

        cache.remove_document(doc_path)
        assert len(cache) == 0

    def test_save_and_reload(self, cache, temp_cache_file):
        """Test saving and reloading cache persists data."""
        doc_path = Path("test.md")
        cache.update_document(doc_path, "hash123")
        cache.save()

        # Create new cache instance from same file
        cache2 = DocumentCache(temp_cache_file)

        assert len(cache2) == 1
        assert doc_path in cache2

    def test_get_all_cached_paths(self, cache):
        """Test getting all cached document paths."""
        cache.update_document(Path("doc1.md"), "hash1")
        cache.update_document(Path("doc2.md"), "hash2")
        cache.update_document(Path("doc3.md"), "hash3")

        paths = cache.get_all_cached_paths()

        assert len(paths) == 3
        assert Path("doc1.md") in paths
        assert Path("doc2.md") in paths
        assert Path("doc3.md") in paths

    def test_get_stats(self, cache):
        """Test getting cache statistics."""
        cache.update_document(
            Path("doc1.md"), "hash1",
            validation_status="passed", error_count=0, warning_count=1
        )
        cache.update_document(
            Path("doc2.md"), "hash2",
            validation_status="failed", error_count=5, warning_count=2
        )

        stats = cache.get_stats()

        assert stats['total_documents'] == 2
        assert stats['passed'] == 1
        assert stats['failed'] == 1
        assert stats['total_errors'] == 5
        assert stats['total_warnings'] == 3

    def test_clear(self, cache):
        """Test clearing all cached documents."""
        cache.update_document(Path("doc1.md"), "hash1")
        cache.update_document(Path("doc2.md"), "hash2")

        assert len(cache) == 2

        cache.clear()

        assert len(cache) == 0

    def test_contains(self, cache):
        """Test __contains__ magic method."""
        doc_path = Path("test.md")

        assert doc_path not in cache

        cache.update_document(doc_path, "hash123")

        assert doc_path in cache


class TestComputeFileHash:
    """Tests for compute_file_hash function."""

    def test_compute_hash_of_file(self, tmp_path):
        """Test computing hash of a real file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, world!")

        hash1 = compute_file_hash(test_file)

        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters

        # Same content should produce same hash
        hash2 = compute_file_hash(test_file)
        assert hash1 == hash2

    def test_compute_hash_different_content(self, tmp_path):
        """Test different content produces different hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Content A")
        file2.write_text("Content B")

        hash1 = compute_file_hash(file1)
        hash2 = compute_file_hash(file2)

        assert hash1 != hash2

    def test_compute_hash_nonexistent_file(self, tmp_path):
        """Test error handling for non-existent file."""
        nonexistent = tmp_path / "nonexistent.txt"

        with pytest.raises(CacheError):
            compute_file_hash(nonexistent)
