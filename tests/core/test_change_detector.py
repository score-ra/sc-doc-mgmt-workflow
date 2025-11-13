"""
Tests for change detector module.
"""

import pytest
from pathlib import Path
from src.core.change_detector import ChangeDetector, ChangeDetectionError
from src.utils.cache import DocumentCache
from src.utils.logger import Logger


class TestChangeDetector:
    """Tests for ChangeDetector class."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory with test files."""
        test_dir = tmp_path / "docs"
        test_dir.mkdir()

        # Create some test markdown files
        (test_dir / "doc1.md").write_text("# Document 1\nContent")
        (test_dir / "doc2.md").write_text("# Document 2\nContent")

        # Create subdirectory
        sub_dir = test_dir / "subdir"
        sub_dir.mkdir()
        (sub_dir / "doc3.md").write_text("# Document 3\nContent")

        return test_dir

    @pytest.fixture
    def cache(self, tmp_path):
        """Create a DocumentCache instance."""
        cache_file = tmp_path / ".cache.json"
        return DocumentCache(cache_file)

    @pytest.fixture
    def logger(self, tmp_path):
        """Create a Logger instance."""
        log_file = tmp_path / "test.log"
        return Logger(name="test", log_file=log_file, log_level="DEBUG")

    @pytest.fixture
    def detector(self, cache, logger):
        """Create a ChangeDetector instance."""
        return ChangeDetector(cache, logger)

    def test_scan_directory(self, detector, temp_dir):
        """Test scanning directory for markdown files."""
        files = detector.scan_directory(temp_dir)

        assert len(files) == 3
        assert all(f.suffix == ".md" for f in files)

    def test_scan_directory_nonexistent(self, detector, tmp_path):
        """Test error when scanning non-existent directory."""
        nonexistent = tmp_path / "nonexistent"

        with pytest.raises(ChangeDetectionError):
            detector.scan_directory(nonexistent)

    def test_scan_directory_with_exclusions(self, detector, temp_dir):
        """Test scanning with exclusion patterns."""
        files = detector.scan_directory(
            temp_dir,
            include_patterns=["**/*.md"],
            exclude_patterns=["**/subdir/*.md"]  # Fixed: match files in subdir, not just the directory
        )

        assert len(files) == 2
        assert not any("subdir" in str(f) for f in files)

    def test_detect_changes_all_new(self, detector, temp_dir):
        """Test detecting changes when all files are new."""
        files = detector.scan_directory(temp_dir)
        changes = detector.detect_changes(files)

        assert len(changes['new']) == 3
        assert len(changes['modified']) == 0
        assert len(changes['unchanged']) == 0
        assert len(changes['deleted']) == 0

    def test_detect_changes_all_unchanged(self, detector, temp_dir, cache):
        """Test detecting changes when all files are unchanged."""
        files = detector.scan_directory(temp_dir)

        # Process files once to populate cache
        for file in files:
            detector.update_cache_for_file(file, "passed", 0, 0)

        # Detect changes again
        changes = detector.detect_changes(files)

        assert len(changes['new']) == 0
        assert len(changes['modified']) == 0
        assert len(changes['unchanged']) == 3
        assert len(changes['deleted']) == 0

    def test_detect_changes_modified(self, detector, temp_dir, cache):
        """Test detecting modified files."""
        files = detector.scan_directory(temp_dir)

        # Process files once
        for file in files:
            detector.update_cache_for_file(file, "passed", 0, 0)

        # Modify one file
        (temp_dir / "doc1.md").write_text("# Modified Document 1\nNew content")

        # Detect changes
        changes = detector.detect_changes(files)

        assert len(changes['new']) == 0
        assert len(changes['modified']) == 1
        assert len(changes['unchanged']) == 2
        assert len(changes['deleted']) == 0
        assert temp_dir / "doc1.md" in changes['modified']

    def test_detect_changes_deleted(self, detector, temp_dir, cache):
        """Test detecting deleted files."""
        files = detector.scan_directory(temp_dir)

        # Process files once
        for file in files:
            detector.update_cache_for_file(file, "passed", 0, 0)

        # Delete one file
        (temp_dir / "doc1.md").unlink()

        # Scan again
        files = detector.scan_directory(temp_dir)

        # Detect changes
        changes = detector.detect_changes(files)

        assert len(changes['deleted']) == 1
        assert temp_dir / "doc1.md" in changes['deleted']

    def test_detect_changes_force_reprocess(self, detector, temp_dir, cache):
        """Test force reprocess treats all files as modified."""
        files = detector.scan_directory(temp_dir)

        # Process files once
        for file in files:
            detector.update_cache_for_file(file, "passed", 0, 0)

        # Detect changes with force_reprocess
        changes = detector.detect_changes(files, force_reprocess=True)

        assert len(changes['modified']) == 3
        assert len(changes['unchanged']) == 0

    def test_update_cache_for_file(self, detector, temp_dir, cache):
        """Test updating cache for a file."""
        test_file = temp_dir / "doc1.md"

        detector.update_cache_for_file(
            test_file,
            validation_status="passed",
            error_count=0,
            warning_count=2
        )

        doc_data = cache.get_document(test_file)

        assert doc_data is not None
        assert doc_data['validation_status'] == "passed"
        assert doc_data['error_count'] == 0
        assert doc_data['warning_count'] == 2

    def test_remove_deleted_from_cache(self, detector, temp_dir, cache):
        """Test removing deleted files from cache."""
        files = detector.scan_directory(temp_dir)

        # Process files
        for file in files:
            detector.update_cache_for_file(file, "passed", 0, 0)

        assert len(cache) == 3

        # Remove one file from cache
        deleted_files = [temp_dir / "doc1.md"]
        detector.remove_deleted_from_cache(deleted_files)

        assert len(cache) == 2
        assert temp_dir / "doc1.md" not in cache

    def test_get_files_to_process(self, detector, temp_dir):
        """Test getting files to process (integration test)."""
        files_to_process, summary = detector.get_files_to_process(temp_dir)

        assert len(files_to_process) == 3
        assert summary['total_files'] == 3
        assert summary['files_to_process'] == 3
        assert summary['new_files'] == 3
        assert summary['modified_files'] == 0
        assert summary['unchanged_files'] == 0
        assert summary['deleted_files'] == 0

    def test_get_files_to_process_incremental(self, detector, temp_dir, cache):
        """Test incremental processing with some changes."""
        # Initial processing
        files_to_process, _ = detector.get_files_to_process(temp_dir)
        for file in files_to_process:
            detector.update_cache_for_file(file, "passed", 0, 0)
        detector.save_cache()

        # Modify one file
        (temp_dir / "doc1.md").write_text("# Modified content")

        # Next processing run
        files_to_process, summary = detector.get_files_to_process(temp_dir)

        assert len(files_to_process) == 1
        assert summary['files_to_process'] == 1
        assert summary['modified_files'] == 1
        assert summary['unchanged_files'] == 2

    def test_save_cache(self, detector, cache):
        """Test saving cache to disk."""
        # This should not raise an exception
        detector.save_cache()

        # Verify cache file exists
        assert cache.cache_file.exists()


class TestChangeDetectorEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def detector(self, tmp_path):
        """Create detector with temporary cache and logger."""
        cache = DocumentCache(tmp_path / ".cache.json")
        logger = Logger(name="test", log_level="DEBUG", console_output=False)
        return ChangeDetector(cache, logger)

    def test_scan_empty_directory(self, detector, tmp_path):
        """Test scanning empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        files = detector.scan_directory(empty_dir)

        assert len(files) == 0

    def test_scan_directory_no_markdown(self, detector, tmp_path):
        """Test scanning directory with no markdown files."""
        test_dir = tmp_path / "nomd"
        test_dir.mkdir()
        (test_dir / "test.txt").write_text("Not markdown")
        (test_dir / "test.py").write_text("# Python comment")

        files = detector.scan_directory(test_dir)

        assert len(files) == 0

    def test_detect_changes_empty_list(self, detector):
        """Test detecting changes with empty file list."""
        changes = detector.detect_changes([])

        assert len(changes['new']) == 0
        assert len(changes['modified']) == 0
        assert len(changes['unchanged']) == 0
        assert len(changes['deleted']) == 0
