"""
Configuration management for Symphony Core Document Management Workflow.

This module handles loading, validating, and accessing configuration settings
from YAML files with support for environment variable overrides.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


class ConfigurationError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""
    pass


class Config:
    """
    Configuration manager for the application.

    Loads configuration from YAML files, validates settings, and provides
    typed access to configuration values.

    Attributes:
        config_path: Path to the configuration YAML file
        config_data: Parsed configuration dictionary
        mode: Current operating mode (symphony-core or business-docs)
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to config.yaml file. If None, uses default location.

        Raises:
            ConfigurationError: If configuration file cannot be loaded or is invalid
        """
        if config_path is None:
            # Default to config/config.yaml in project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.mode: str = "symphony-core"

        self._load_config()
        self._validate_config()

    def _load_config(self) -> None:
        """
        Load configuration from YAML file.

        Raises:
            ConfigurationError: If file cannot be read or parsed
        """
        if not self.config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Failed to parse configuration file: {e}"
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load configuration file: {e}"
            )

        # Get mode from config
        self.mode = self.config_data.get('mode', 'symphony-core')

        # Override with environment variables if present
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        # Mode override
        if os.getenv('SC_MODE'):
            self.mode = os.getenv('SC_MODE')
            self.config_data['mode'] = self.mode

        # API key override (for future use)
        if os.getenv('ANTHROPIC_API_KEY'):
            if 'api' not in self.config_data:
                self.config_data['api'] = {}
            self.config_data['api']['api_key'] = os.getenv('ANTHROPIC_API_KEY')

        # Log level override
        if os.getenv('SC_LOG_LEVEL'):
            self.config_data['logging']['level'] = os.getenv('SC_LOG_LEVEL')

    def _validate_config(self) -> None:
        """
        Validate configuration structure and required fields.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Check required top-level sections
        required_sections = ['processing', 'validation', 'reporting', 'logging']
        for section in required_sections:
            if section not in self.config_data:
                raise ConfigurationError(
                    f"Missing required configuration section: {section}"
                )

        # Validate mode
        valid_modes = ['symphony-core', 'business-docs']
        if self.mode not in valid_modes:
            raise ConfigurationError(
                f"Invalid mode '{self.mode}'. Must be one of: {valid_modes}"
            )

        # Validate processing settings
        if 'doc_directories' not in self.config_data['processing']:
            raise ConfigurationError(
                "Missing 'doc_directories' in processing configuration"
            )

        # Validate cache file path
        if 'cache_file' not in self.config_data['processing']:
            raise ConfigurationError(
                "Missing 'cache_file' in processing configuration"
            )

        # Validate logging level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_level = self.config_data['logging'].get('level', 'INFO')
        if log_level not in valid_log_levels:
            raise ConfigurationError(
                f"Invalid log level '{log_level}'. Must be one of: {valid_log_levels}"
            )

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path to configuration value (e.g., 'logging.level')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get('logging.level')
            'INFO'
            >>> config.get('validation.yaml.enabled')
            True
        """
        keys = key_path.split('.')
        value = self.config_data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_required_yaml_fields(self) -> List[str]:
        """
        Get list of required YAML frontmatter fields for current mode.

        Returns:
            List of required field names
        """
        fields = self.get(f'validation.yaml.required_fields.{self.mode}', [])
        return fields if fields else []

    def get_doc_directories(self) -> List[Path]:
        """
        Get list of document directories to scan.

        Returns:
            List of Path objects for document directories
        """
        dirs = self.get('processing.doc_directories', ['.'])
        return [Path(d) for d in dirs]

    def get_cache_file_path(self) -> Path:
        """
        Get path to cache file for change detection.

        Returns:
            Path object for cache file
        """
        cache_file = self.get('processing.cache_file', '_meta/.document-cache.json')
        return Path(cache_file)

    def get_backup_dir(self) -> Path:
        """
        Get path to backup directory.

        Returns:
            Path object for backup directory
        """
        backup_dir = self.get('processing.backup_dir', '_meta/.backups/')
        return Path(backup_dir)

    def get_report_output_dir(self) -> Path:
        """
        Get path to report output directory.

        Returns:
            Path object for report directory
        """
        output_dir = self.get('reporting.output_dir', '_meta/reports/')
        return Path(output_dir)

    def is_validation_enabled(self, validator_type: str) -> bool:
        """
        Check if a specific validator is enabled.

        Args:
            validator_type: Type of validator ('yaml', 'markdown', 'naming')

        Returns:
            True if validator is enabled, False otherwise
        """
        return self.get(f'validation.{validator_type}.enabled', True)

    def get_allowed_statuses(self) -> List[str]:
        """
        Get list of allowed status values.

        Returns:
            List of allowed status strings
        """
        return self.get('validation.yaml.allowed_statuses', [])

    def get_allowed_categories(self) -> List[str]:
        """
        Get list of allowed category values (Symphony Core mode).

        Returns:
            List of allowed category strings
        """
        return self.get('validation.yaml.allowed_categories', [])

    def get_naming_pattern(self) -> str:
        """
        Get naming pattern requirement.

        Returns:
            Naming pattern string
        """
        return self.get('validation.naming.pattern', 'lowercase-with-hyphens')

    def get_max_filename_length(self) -> int:
        """
        Get maximum allowed filename length.

        Returns:
            Maximum length (excluding extension)
        """
        return self.get('validation.naming.max_length', 50)

    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a feature flag is enabled.

        Args:
            feature_name: Name of the feature

        Returns:
            True if feature is enabled, False otherwise
        """
        return self.get(f'features.{feature_name}', False)

    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config(mode={self.mode}, config_path={self.config_path})"


# Global configuration instance (initialized when first accessed)
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    """
    Get global configuration instance (singleton pattern).

    Args:
        config_path: Optional path to config file (only used on first call)

    Returns:
        Global Config instance
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = Config(config_path)

    return _config_instance


def reload_config(config_path: Optional[Path] = None) -> Config:
    """
    Reload configuration from file.

    Args:
        config_path: Optional path to config file

    Returns:
        New Config instance
    """
    global _config_instance
    _config_instance = Config(config_path)
    return _config_instance
