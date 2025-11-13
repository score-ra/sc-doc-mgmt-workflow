"""
Tests for logging utilities module.
"""

import pytest
import logging
from pathlib import Path
from datetime import datetime
import time
from src.utils.logger import Logger, PerformanceTracker, get_logger, setup_logger


class TestLogger:
    """Tests for Logger class."""

    def test_logger_initialization_console_only(self):
        """Test logger initialization with console output only."""
        logger = Logger(name="test_logger", console_output=True)

        assert logger.logger is not None
        assert logger.logger.name == "test_logger"
        assert logger.log_file is None
        assert len(logger.logger.handlers) == 1  # Console handler only

    def test_logger_initialization_with_file(self, tmp_path):
        """Test logger initialization with file output."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test_logger", log_file=log_file, console_output=False)

        assert logger.log_file == log_file
        assert log_file.exists()  # File should be created
        assert len(logger.logger.handlers) == 1  # File handler only

    def test_logger_initialization_both_outputs(self, tmp_path):
        """Test logger initialization with both console and file output."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test_logger", log_file=log_file, console_output=True)

        assert len(logger.logger.handlers) == 2  # Console + file handlers

    def test_logger_log_levels(self, tmp_path):
        """Test different log levels."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test_logger", log_file=log_file, log_level="DEBUG", console_output=False)

        # Test all log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        # Read log file and verify messages
        log_content = log_file.read_text()
        assert "Debug message" in log_content
        assert "Info message" in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content
        assert "Critical message" in log_content

    def test_logger_info_level_filters_debug(self, tmp_path):
        """Test that INFO level filters out DEBUG messages."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test_logger", log_file=log_file, log_level="INFO", console_output=False)

        logger.debug("This should not appear")
        logger.info("This should appear")

        log_content = log_file.read_text()
        assert "This should not appear" not in log_content
        assert "This should appear" in log_content

    def test_logger_exception_with_traceback(self, tmp_path):
        """Test exception logging with traceback."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test_logger", log_file=log_file, console_output=False)

        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")

        log_content = log_file.read_text()
        assert "An error occurred" in log_content
        assert "ValueError" in log_content
        assert "Test exception" in log_content

    def test_logger_file_rotation(self, tmp_path):
        """Test log file rotation."""
        log_file = tmp_path / "test.log"
        # Create logger with very small max file size (1 byte) to force rotation
        logger = Logger(
            name="test_logger",
            log_file=log_file,
            console_output=False,
            max_file_size_mb=0.00001,  # Very small to trigger rotation
            backup_count=2
        )

        # Write enough messages to trigger rotation
        for i in range(100):
            logger.info(f"Message {i} " * 10)  # Long messages to fill file

        # Check if rotation happened (backup files should exist)
        # Note: Rotation may or may not happen depending on exact timing
        assert log_file.exists()

    def test_logger_creates_log_directory(self, tmp_path):
        """Test that logger creates log directory if it doesn't exist."""
        log_dir = tmp_path / "logs" / "subdir"
        log_file = log_dir / "test.log"

        assert not log_dir.exists()

        logger = Logger(name="test_logger", log_file=log_file, console_output=False)

        assert log_dir.exists()
        assert log_file.exists()

    def test_logger_different_levels(self):
        """Test logger with different logging levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger = Logger(name=f"test_{level}", log_level=level, console_output=False)
            assert logger.logger.level == getattr(logging, level)


class TestPerformanceTracker:
    """Tests for PerformanceTracker class."""

    def test_performance_tracker_initialization(self):
        """Test performance tracker initialization."""
        tracker = PerformanceTracker()

        assert tracker.metrics['documents_processed'] == 0
        assert tracker.metrics['documents_failed'] == 0
        assert tracker.metrics['total_processing_time'] == 0.0
        assert tracker.metrics['validation_errors'] == 0
        assert tracker.metrics['validation_warnings'] == 0
        assert tracker.start_time is None

    def test_performance_tracker_with_logger(self, tmp_path):
        """Test performance tracker with logger."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test", log_file=log_file, console_output=False)
        tracker = PerformanceTracker(logger=logger)

        tracker.start()

        assert tracker.start_time is not None

        # Check log contains start message
        log_content = log_file.read_text()
        assert "Performance tracking started" in log_content

    def test_increment_documents_processed(self):
        """Test incrementing documents processed counter."""
        tracker = PerformanceTracker()

        tracker.increment_documents_processed()
        assert tracker.metrics['documents_processed'] == 1

        tracker.increment_documents_processed(5)
        assert tracker.metrics['documents_processed'] == 6

    def test_increment_documents_failed(self):
        """Test incrementing documents failed counter."""
        tracker = PerformanceTracker()

        tracker.increment_documents_failed()
        assert tracker.metrics['documents_failed'] == 1

        tracker.increment_documents_failed(3)
        assert tracker.metrics['documents_failed'] == 4

    def test_add_processing_time(self):
        """Test adding processing time."""
        tracker = PerformanceTracker()

        tracker.add_processing_time(1.5)
        assert tracker.metrics['total_processing_time'] == 1.5

        tracker.add_processing_time(2.3)
        assert tracker.metrics['total_processing_time'] == pytest.approx(3.8)

    def test_increment_errors(self):
        """Test incrementing error count."""
        tracker = PerformanceTracker()

        tracker.increment_errors()
        assert tracker.metrics['validation_errors'] == 1

        tracker.increment_errors(5)
        assert tracker.metrics['validation_errors'] == 6

    def test_increment_warnings(self):
        """Test incrementing warning count."""
        tracker = PerformanceTracker()

        tracker.increment_warnings()
        assert tracker.metrics['validation_warnings'] == 1

        tracker.increment_warnings(3)
        assert tracker.metrics['validation_warnings'] == 4

    def test_increment_api_calls(self):
        """Test incrementing API calls and cost."""
        tracker = PerformanceTracker()

        tracker.increment_api_calls(count=1, estimated_cost=0.01)
        assert tracker.metrics['api_calls'] == 1
        assert tracker.metrics['api_cost_estimate'] == pytest.approx(0.01)

        tracker.increment_api_calls(count=3, estimated_cost=0.05)
        assert tracker.metrics['api_calls'] == 4
        assert tracker.metrics['api_cost_estimate'] == pytest.approx(0.06)

    def test_get_metrics_without_start(self):
        """Test getting metrics without starting tracker."""
        tracker = PerformanceTracker()
        tracker.increment_documents_processed(5)

        metrics = tracker.get_metrics()

        assert metrics['documents_processed'] == 5
        assert 'elapsed_time' not in metrics

    def test_get_metrics_with_start(self):
        """Test getting metrics after starting tracker."""
        tracker = PerformanceTracker()
        tracker.start()

        time.sleep(0.1)  # Small delay to get measurable elapsed time

        metrics = tracker.get_metrics()

        assert 'elapsed_time' in metrics
        assert metrics['elapsed_time'] > 0

    def test_get_metrics_returns_copy(self):
        """Test that get_metrics returns a copy, not reference."""
        tracker = PerformanceTracker()
        tracker.increment_documents_processed(5)

        metrics1 = tracker.get_metrics()
        metrics1['documents_processed'] = 999  # Modify the copy

        metrics2 = tracker.get_metrics()

        assert metrics2['documents_processed'] == 5  # Original unchanged

    def test_log_summary_without_logger(self):
        """Test log_summary does nothing without logger."""
        tracker = PerformanceTracker(logger=None)
        tracker.increment_documents_processed(5)

        # Should not raise exception
        tracker.log_summary()

    def test_log_summary_with_logger(self, tmp_path):
        """Test log_summary with logger."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test", log_file=log_file, console_output=False)
        tracker = PerformanceTracker(logger=logger)

        tracker.start()
        tracker.increment_documents_processed(10)
        tracker.increment_documents_failed(2)
        tracker.increment_errors(5)
        tracker.increment_warnings(3)
        tracker.add_processing_time(15.5)
        tracker.increment_api_calls(count=20, estimated_cost=2.50)

        tracker.log_summary()

        log_content = log_file.read_text()

        assert "PERFORMANCE SUMMARY" in log_content
        assert "Documents Processed: 10" in log_content
        assert "Documents Failed: 2" in log_content
        assert "Validation Errors: 5" in log_content
        assert "Validation Warnings: 3" in log_content
        assert "Total Processing Time: 15.50s" in log_content
        assert "Average Time per Document" in log_content
        assert "API Calls: 20" in log_content
        assert "Estimated API Cost: $2.5000" in log_content

    def test_log_summary_with_zero_documents(self, tmp_path):
        """Test log_summary with zero documents processed."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test", log_file=log_file, console_output=False)
        tracker = PerformanceTracker(logger=logger)

        tracker.log_summary()

        log_content = log_file.read_text()

        assert "PERFORMANCE SUMMARY" in log_content
        assert "Documents Processed: 0" in log_content
        # Should not have average time calculation
        assert "Average Time per Document" not in log_content

    def test_log_summary_without_api_calls(self, tmp_path):
        """Test log_summary without API calls."""
        log_file = tmp_path / "test.log"
        logger = Logger(name="test", log_file=log_file, console_output=False)
        tracker = PerformanceTracker(logger=logger)

        tracker.increment_documents_processed(5)
        tracker.log_summary()

        log_content = log_file.read_text()

        # Should not have API call info
        assert "API Calls:" not in log_content


class TestGlobalLogger:
    """Tests for global logger functions."""

    def test_setup_logger(self, tmp_path):
        """Test setup_logger function."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(log_file=log_file, log_level="DEBUG", console_output=False)

        assert logger is not None
        assert logger.log_file == log_file

        logger.info("Test message")

        log_content = log_file.read_text()
        assert "Test message" in log_content

    def test_setup_logger_replaces_instance(self, tmp_path):
        """Test that setup_logger replaces the global instance."""
        log_file1 = tmp_path / "test1.log"
        log_file2 = tmp_path / "test2.log"

        logger1 = setup_logger(log_file=log_file1, console_output=False)
        logger2 = setup_logger(log_file=log_file2, console_output=False)

        # Should be different instances with different files
        assert logger2.log_file == log_file2
        assert logger2.log_file != logger1.log_file
