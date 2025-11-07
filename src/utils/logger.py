"""
Logging utilities for Symphony Core Document Management Workflow.

Provides structured logging with file and console output, log rotation,
and performance tracking capabilities.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
from datetime import datetime


class Logger:
    """
    Centralized logging manager for the application.

    Provides both file and console logging with appropriate formatting,
    log rotation, and performance metrics tracking.

    Attributes:
        logger: Python logging.Logger instance
        log_file: Path to log file
    """

    def __init__(
        self,
        name: str = "symphony_core",
        log_file: Optional[Path] = None,
        log_level: str = "INFO",
        console_output: bool = True,
        max_file_size_mb: int = 10,
        backup_count: int = 5
    ):
        """
        Initialize logger with file and console handlers.

        Args:
            name: Logger name
            log_file: Path to log file. If None, logs only to console
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Enable console output
            max_file_size_mb: Maximum log file size before rotation (MB)
            backup_count: Number of backup log files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.log_file = log_file

        # Clear any existing handlers
        self.logger.handlers = []

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level.upper()))
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler with rotation
        if log_file:
            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_file_size_mb * 1024 * 1024,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)

    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, extra=kwargs)


class PerformanceTracker:
    """
    Track performance metrics for document processing.

    Provides timing and statistics collection for performance monitoring.
    """

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize performance tracker.

        Args:
            logger: Logger instance for outputting metrics
        """
        self.logger = logger
        self.metrics: dict = {
            'documents_processed': 0,
            'documents_failed': 0,
            'total_processing_time': 0.0,
            'validation_errors': 0,
            'validation_warnings': 0,
            'api_calls': 0,
            'api_cost_estimate': 0.0
        }
        self.start_time: Optional[datetime] = None

    def start(self) -> None:
        """Start tracking a processing run."""
        self.start_time = datetime.now()
        if self.logger:
            self.logger.info("Performance tracking started")

    def increment_documents_processed(self, count: int = 1) -> None:
        """Increment count of successfully processed documents."""
        self.metrics['documents_processed'] += count

    def increment_documents_failed(self, count: int = 1) -> None:
        """Increment count of failed documents."""
        self.metrics['documents_failed'] += count

    def add_processing_time(self, seconds: float) -> None:
        """Add processing time to total."""
        self.metrics['total_processing_time'] += seconds

    def increment_errors(self, count: int = 1) -> None:
        """Increment validation error count."""
        self.metrics['validation_errors'] += count

    def increment_warnings(self, count: int = 1) -> None:
        """Increment validation warning count."""
        self.metrics['validation_warnings'] += count

    def increment_api_calls(self, count: int = 1, estimated_cost: float = 0.0) -> None:
        """
        Increment API call count and track cost.

        Args:
            count: Number of API calls made
            estimated_cost: Estimated cost in USD
        """
        self.metrics['api_calls'] += count
        self.metrics['api_cost_estimate'] += estimated_cost

    def get_metrics(self) -> dict:
        """
        Get current performance metrics.

        Returns:
            Dictionary of metrics
        """
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.metrics['elapsed_time'] = elapsed

        return self.metrics.copy()

    def log_summary(self) -> None:
        """Log summary of performance metrics."""
        if not self.logger:
            return

        metrics = self.get_metrics()

        self.logger.info("=" * 60)
        self.logger.info("PERFORMANCE SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Documents Processed: {metrics['documents_processed']}")
        self.logger.info(f"Documents Failed: {metrics['documents_failed']}")
        self.logger.info(f"Validation Errors: {metrics['validation_errors']}")
        self.logger.info(f"Validation Warnings: {metrics['validation_warnings']}")
        self.logger.info(
            f"Total Processing Time: {metrics['total_processing_time']:.2f}s"
        )

        if metrics['documents_processed'] > 0:
            avg_time = metrics['total_processing_time'] / metrics['documents_processed']
            self.logger.info(f"Average Time per Document: {avg_time:.2f}s")

        if 'elapsed_time' in metrics:
            self.logger.info(f"Total Elapsed Time: {metrics['elapsed_time']:.2f}s")

        if metrics['api_calls'] > 0:
            self.logger.info(f"API Calls: {metrics['api_calls']}")
            self.logger.info(
                f"Estimated API Cost: ${metrics['api_cost_estimate']:.4f}"
            )

        self.logger.info("=" * 60)


# Global logger instance
_logger_instance: Optional[Logger] = None


def get_logger() -> Logger:
    """
    Get global logger instance (singleton pattern).

    Returns:
        Global Logger instance
    """
    global _logger_instance

    if _logger_instance is None:
        from .config import get_config

        config = get_config()

        log_file_path = Path(config.get('logging.file', 'logs/symphony-core.log'))
        log_level = config.get('logging.level', 'INFO')
        console_output = config.get('logging.console', True)
        max_file_size = config.get('logging.max_file_size_mb', 10)
        backup_count = config.get('logging.backup_count', 5)

        _logger_instance = Logger(
            name='symphony_core',
            log_file=log_file_path,
            log_level=log_level,
            console_output=console_output,
            max_file_size_mb=max_file_size,
            backup_count=backup_count
        )

    return _logger_instance


def setup_logger(
    log_file: Optional[Path] = None,
    log_level: str = "INFO",
    console_output: bool = True
) -> Logger:
    """
    Set up and configure logger.

    Args:
        log_file: Path to log file
        log_level: Logging level
        console_output: Enable console output

    Returns:
        Configured Logger instance
    """
    global _logger_instance

    _logger_instance = Logger(
        name='symphony_core',
        log_file=log_file,
        log_level=log_level,
        console_output=console_output
    )

    return _logger_instance
