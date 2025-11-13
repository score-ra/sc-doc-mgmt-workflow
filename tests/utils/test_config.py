"""
Tests for configuration validation module.
"""

import pytest
import json
from pathlib import Path
from src.utils.config import Config, ConfigurationError


class TestConfigValidation:
    """Tests for Config class validation."""

    @pytest.fixture
    def valid_config_data(self):
        """Return valid configuration data."""
        return {
            "processing": {
                "doc_directories": ["."],
                "cache_file": "_meta/.document-cache.json",
                "backup_dir": "_meta/.backups/",
                "include_patterns": ["**/*.md"],
                "exclude_patterns": ["_meta/**"]
            },
            "validation": {
                "yaml": {
                    "enabled": True,
                    "required_fields": ["title", "tags", "status"],
                    "allowed_statuses": ["draft", "review", "approved"]
                },
                "markdown": {
                    "enabled": True,
                    "enforce_heading_hierarchy": True
                },
                "naming": {
                    "enabled": True,
                    "pattern": "lowercase-with-hyphens",
                    "max_length": 50
                }
            },
            "reporting": {
                "format": "markdown",
                "output_dir": "_meta/reports/",
                "verbose": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/symphony-core.log",
                "console": True
            }
        }

    @pytest.fixture
    def temp_config_file(self, tmp_path, valid_config_data):
        """Create a temporary valid config file."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Also create schema file
        schema_file = config_dir / "config-schema.json"
        schema_content = self._get_test_schema()
        with open(schema_file, 'w') as f:
            json.dump(schema_content, f)

        return config_file

    def _get_test_schema(self):
        """Return a minimal test schema."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["processing", "validation", "reporting", "logging"],
            "properties": {
                "processing": {
                    "type": "object",
                    "required": ["doc_directories", "cache_file"],
                    "properties": {
                        "doc_directories": {
                            "type": "array",
                            "minItems": 1
                        },
                        "cache_file": {
                            "type": "string",
                            "pattern": "\\.json$"
                        }
                    }
                },
                "validation": {
                    "type": "object",
                    "required": ["yaml", "markdown", "naming"]
                },
                "reporting": {
                    "type": "object",
                    "required": ["format", "output_dir"],
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "json", "text", "console"]
                        }
                    }
                },
                "logging": {
                    "type": "object",
                    "required": ["level", "file"],
                    "properties": {
                        "level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                        },
                        "file": {
                            "type": "string"
                        }
                    }
                }
            }
        }

    def test_load_valid_config(self, temp_config_file):
        """Test loading a valid configuration file."""
        config = Config(temp_config_file)

        assert config.config_path == temp_config_file
        assert config.config_data is not None
        assert 'processing' in config.config_data
        assert 'validation' in config.config_data

    def test_missing_config_file(self, tmp_path):
        """Test error when config file doesn't exist."""
        nonexistent = tmp_path / "nonexistent.yaml"

        with pytest.raises(ConfigurationError, match="not found"):
            Config(nonexistent)

    def test_missing_required_section(self, tmp_path, valid_config_data):
        """Test error when required section is missing."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Remove required section
        del valid_config_data['logging']

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Create schema
        schema_file = config_dir / "config-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(self._get_test_schema(), f)

        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        assert "logging" in str(exc_info.value).lower()
        assert "required" in str(exc_info.value).lower()

    def test_invalid_type(self, tmp_path, valid_config_data):
        """Test error when field has wrong type."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Invalid type - should be array
        valid_config_data['processing']['doc_directories'] = "not_an_array"

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Create schema
        schema_file = config_dir / "config-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(self._get_test_schema(), f)

        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        assert "type" in str(exc_info.value).lower()

    def test_invalid_enum_value(self, tmp_path, valid_config_data):
        """Test error when enum value is invalid."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Invalid log level
        valid_config_data['logging']['level'] = "INVALID_LEVEL"

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Create schema
        schema_file = config_dir / "config-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(self._get_test_schema(), f)

        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        error_msg = str(exc_info.value)
        assert "allowed values" in error_msg.lower() or "one of" in error_msg.lower()

    def test_pattern_validation(self, tmp_path, valid_config_data):
        """Test pattern validation for fields."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Invalid cache_file (doesn't end with .json)
        valid_config_data['processing']['cache_file'] = "cache.txt"

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Create schema
        schema_file = config_dir / "config-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(self._get_test_schema(), f)

        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        assert "pattern" in str(exc_info.value).lower()

    def test_helpful_error_message_format(self, tmp_path, valid_config_data):
        """Test that error messages are helpful and well-formatted."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Remove required field
        del valid_config_data['processing']['cache_file']

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Create schema
        schema_file = config_dir / "config-schema.json"
        with open(schema_file, 'w') as f:
            json.dump(self._get_test_schema(), f)

        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        error_msg = str(exc_info.value)

        # Check error message contains helpful information
        assert "How to fix" in error_msg
        assert "cache_file" in error_msg
        assert str(config_file) in error_msg

    def test_fallback_validation_without_schema(self, tmp_path, valid_config_data):
        """Test fallback validation when schema file doesn't exist."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Don't create schema file - should use fallback validation
        config = Config(config_file)

        assert config.config_data is not None

    def test_fallback_validation_error(self, tmp_path, valid_config_data):
        """Test fallback validation error messages."""
        import yaml

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Remove required section
        del valid_config_data['logging']

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(valid_config_data, f)

        # Don't create schema file
        with pytest.raises(ConfigurationError) as exc_info:
            Config(config_file)

        error_msg = str(exc_info.value)
        assert "logging" in error_msg.lower()
        assert "How to fix" in error_msg

    def test_malformed_yaml(self, tmp_path):
        """Test error handling for malformed YAML."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            f.write("invalid: yaml: content:\n  - bad indentation")

        with pytest.raises(ConfigurationError, match="parse"):
            Config(config_file)


class TestConfigGetters:
    """Tests for Config getter methods."""

    @pytest.fixture
    def config(self, tmp_path):
        """Create a config instance for testing."""
        import yaml

        config_data = {
            "processing": {
                "doc_directories": ["."],
                "cache_file": "_meta/.cache.json",
                "backup_dir": "_meta/.backups/"
            },
            "validation": {
                "yaml": {
                    "enabled": True,
                    "required_fields": ["title", "tags", "status"],
                    "allowed_statuses": ["draft", "approved"]
                },
                "markdown": {"enabled": True},
                "naming": {
                    "enabled": True,
                    "pattern": "lowercase-with-hyphens",
                    "max_length": 50
                }
            },
            "reporting": {
                "format": "markdown",
                "output_dir": "_meta/reports/"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/test.log"
            }
        }

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        return Config(config_file)

    def test_get_simple_value(self, config):
        """Test getting a simple configuration value."""
        assert config.get('logging.level') == 'INFO'
        assert config.get('reporting.format') == 'markdown'

    def test_get_nested_value(self, config):
        """Test getting nested configuration values."""
        assert config.get('validation.yaml.enabled') is True
        assert config.get('validation.naming.pattern') == 'lowercase-with-hyphens'

    def test_get_with_default(self, config):
        """Test getting value with default fallback."""
        assert config.get('nonexistent.key', 'default') == 'default'
        assert config.get('also.missing', 42) == 42

    def test_get_doc_directories(self, config):
        """Test getting document directories."""
        dirs = config.get_doc_directories()
        assert len(dirs) == 1
        assert dirs[0] == Path('.')

    def test_get_cache_file_path(self, config):
        """Test getting cache file path."""
        cache_path = config.get_cache_file_path()
        assert cache_path == Path('_meta/.cache.json')

    def test_get_backup_dir(self, config):
        """Test getting backup directory."""
        backup_dir = config.get_backup_dir()
        assert backup_dir == Path('_meta/.backups/')

    def test_get_report_output_dir(self, config):
        """Test getting report output directory."""
        output_dir = config.get_report_output_dir()
        assert output_dir == Path('_meta/reports/')

    def test_is_validation_enabled(self, config):
        """Test checking if validators are enabled."""
        assert config.is_validation_enabled('yaml') is True
        assert config.is_validation_enabled('markdown') is True
        assert config.is_validation_enabled('naming') is True

    def test_get_allowed_statuses(self, config):
        """Test getting allowed statuses."""
        statuses = config.get_allowed_statuses()
        assert 'draft' in statuses
        assert 'approved' in statuses

    def test_get_naming_pattern(self, config):
        """Test getting naming pattern."""
        pattern = config.get_naming_pattern()
        assert pattern == 'lowercase-with-hyphens'

    def test_get_max_filename_length(self, config):
        """Test getting max filename length."""
        max_length = config.get_max_filename_length()
        assert max_length == 50


class TestConfigEnvironmentOverrides:
    """Tests for environment variable overrides."""

    def test_log_level_override(self, tmp_path, monkeypatch):
        """Test log level override from environment."""
        import yaml

        config_data = {
            "processing": {"doc_directories": ["."], "cache_file": "_meta/.cache.json"},
            "validation": {
                "yaml": {"enabled": True, "required_fields": ["title"], "allowed_statuses": ["draft"]},
                "markdown": {"enabled": True},
                "naming": {"enabled": True, "pattern": "lowercase-with-hyphens"}
            },
            "reporting": {"format": "markdown", "output_dir": "_meta/reports/"},
            "logging": {"level": "INFO", "file": "logs/test.log"}
        }

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        config_file = config_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        # Set environment override
        monkeypatch.setenv('SC_LOG_LEVEL', 'DEBUG')

        config = Config(config_file)
        assert config.get('logging.level') == 'DEBUG'
