"""
Configuration management for Symphony Core Document Management Workflow.

This module handles loading, validating, and accessing configuration settings
from YAML files with support for environment variable overrides.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from jsonschema import validate, ValidationError as JSONSchemaValidationError, SchemaError


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
        Validate configuration structure and required fields using JSON Schema.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Load JSON Schema
        schema_path = self.config_path.parent / "config-schema.json"

        if not schema_path.exists():
            # Fallback to basic validation if schema not found
            self._validate_config_basic()
            return

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load configuration schema: {e}"
            )

        # Validate config against schema
        try:
            validate(instance=self.config_data, schema=schema)
        except JSONSchemaValidationError as e:
            # Create helpful error message
            error_path = " → ".join(str(p) for p in e.path) if e.path else "root"
            error_msg = self._format_validation_error(e, error_path)
            raise ConfigurationError(error_msg)
        except SchemaError as e:
            raise ConfigurationError(
                f"Configuration schema is invalid: {e}"
            )

    def _format_validation_error(self, error: JSONSchemaValidationError, path: str) -> str:
        """
        Format JSON Schema validation error into helpful message.

        Args:
            error: The validation error
            path: Path to the invalid field

        Returns:
            Formatted error message with fix suggestions
        """
        message_parts = [
            "Configuration Validation Error",
            "",
            f"Location: {path}",
            f"Issue: {error.message}",
            ""
        ]

        # Add specific guidance based on error type
        if error.validator == "required":
            missing_field = error.message.split("'")[1] if "'" in error.message else "unknown"
            message_parts.extend([
                "How to fix:",
                f"  Add the required field '{missing_field}' to your config.yaml",
                "",
                "Example:",
                f"  {missing_field}: <value>",
            ])
        elif error.validator == "type":
            expected_type = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  The field must be of type: {expected_type}",
                "",
                "Example:",
                f"  {path}: <{expected_type} value>",
            ])
        elif error.validator == "enum":
            allowed_values = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  Use one of the allowed values: {', '.join(map(str, allowed_values))}",
                "",
                "Example:",
                f"  {path}: {allowed_values[0]}",
            ])
        elif error.validator == "minimum":
            min_value = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  Value must be at least: {min_value}",
            ])
        elif error.validator == "maximum":
            max_value = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  Value must be at most: {max_value}",
            ])
        elif error.validator == "minItems":
            min_items = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  Array must contain at least {min_items} item(s)",
            ])
        elif error.validator == "pattern":
            pattern = error.validator_value
            message_parts.extend([
                "How to fix:",
                f"  Value must match pattern: {pattern}",
            ])
        else:
            message_parts.extend([
                "How to fix:",
                "  Review the configuration schema and correct the value",
            ])

        message_parts.extend([
            "",
            "Configuration file:",
            f"  {self.config_path}",
            "",
            "Documentation:",
            "  See config/config.yaml for examples",
        ])

        return "\n".join(message_parts)

    def _validate_config_basic(self) -> None:
        """
        Basic configuration validation (fallback when schema not available).

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Check required top-level sections
        required_sections = ['processing', 'validation', 'reporting', 'logging']
        for section in required_sections:
            if section not in self.config_data:
                raise ConfigurationError(
                    f"Missing required configuration section: {section}\n"
                    f"\nHow to fix:\n"
                    f"  Add the '{section}' section to your config.yaml\n"
                    f"\nConfiguration file: {self.config_path}"
                )

        # Validate processing settings
        if 'doc_directories' not in self.config_data['processing']:
            raise ConfigurationError(
                "Missing 'doc_directories' in processing configuration\n"
                "\nHow to fix:\n"
                "  Add doc_directories to the processing section:\n"
                "\n  processing:\n"
                "    doc_directories:\n"
                "      - '.'\n"
                f"\nConfiguration file: {self.config_path}"
            )

        # Validate cache file path
        if 'cache_file' not in self.config_data['processing']:
            raise ConfigurationError(
                "Missing 'cache_file' in processing configuration\n"
                "\nHow to fix:\n"
                "  Add cache_file to the processing section:\n"
                "\n  processing:\n"
                "    cache_file: '_meta/.document-cache.json'\n"
                f"\nConfiguration file: {self.config_path}"
            )

        # Validate logging level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_level = self.config_data['logging'].get('level', 'INFO')
        if log_level not in valid_log_levels:
            raise ConfigurationError(
                f"Invalid log level '{log_level}'\n"
                f"\nHow to fix:\n"
                f"  Use one of: {', '.join(valid_log_levels)}\n"
                "\nExample:\n"
                "  logging:\n"
                "    level: 'INFO'\n"
                f"\nConfiguration file: {self.config_path}"
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
