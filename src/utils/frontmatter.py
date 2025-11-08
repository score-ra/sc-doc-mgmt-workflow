"""
YAML frontmatter parsing and manipulation for markdown documents.

This module provides utilities for reading, writing, and validating YAML frontmatter
in markdown files. Frontmatter is metadata enclosed between --- delimiters at the
start of markdown files.
"""

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import yaml


class FrontmatterError(Exception):
    """Raised when frontmatter cannot be parsed or is malformed."""
    pass


def has_frontmatter(file_path: Path) -> bool:
    """
    Check if a markdown file contains YAML frontmatter.

    Args:
        file_path: Path to the markdown file to check

    Returns:
        True if the file has valid YAML frontmatter, False otherwise

    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for frontmatter delimiters at start of file
        # Pattern: starts with ---, has content, ends with ---
        pattern = r'^---\s*\n.*?\n---\s*\n'
        return bool(re.match(pattern, content, re.DOTALL))

    except Exception:
        return False


def parse_frontmatter(file_path: Path) -> Dict[str, Any]:
    """
    Parse YAML frontmatter from a markdown file.

    Args:
        file_path: Path to the markdown file to parse

    Returns:
        Dictionary containing the parsed YAML frontmatter.
        Returns empty dict if no frontmatter is present.

    Raises:
        FileNotFoundError: If the file does not exist
        FrontmatterError: If frontmatter exists but is malformed or invalid YAML
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle empty files
        if not content.strip():
            return {}

        # Extract frontmatter using regex
        # Pattern: ---\n<yaml content>\n---
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            # No frontmatter found
            return {}

        yaml_content = match.group(1)

        # Handle empty frontmatter block
        if not yaml_content.strip():
            return {}

        # Parse YAML
        try:
            metadata = yaml.safe_load(yaml_content)

            # Handle case where YAML is valid but empty (None)
            if metadata is None:
                return {}

            # Ensure we return a dictionary
            if not isinstance(metadata, dict):
                raise FrontmatterError(
                    f"Frontmatter must be a YAML dictionary, got {type(metadata).__name__}"
                )

            return metadata

        except yaml.YAMLError as e:
            raise FrontmatterError(
                f"Invalid YAML in frontmatter: {str(e)}"
            ) from e

    except FrontmatterError:
        raise
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FrontmatterError(
            f"Error reading file {file_path}: {str(e)}"
        ) from e


def extract_frontmatter_and_content(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """
    Extract both frontmatter and markdown content from a file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Tuple of (metadata_dict, markdown_content)
        If no frontmatter exists, returns (empty_dict, full_content)

    Raises:
        FileNotFoundError: If the file does not exist
        FrontmatterError: If frontmatter is malformed
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle empty files
    if not content.strip():
        return {}, ""

    # Extract frontmatter and content
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        # No frontmatter, return all as content
        return {}, content

    yaml_content = match.group(1)
    markdown_content = match.group(2)

    # Parse YAML frontmatter
    metadata = parse_frontmatter(file_path)

    return metadata, markdown_content


def add_frontmatter(
    file_path: Path,
    metadata: Dict[str, Any],
    preserve_content: bool = True
) -> None:
    """
    Add or replace YAML frontmatter in a markdown file.

    If the file already has frontmatter, it will be replaced.
    If preserve_content is True, existing markdown content is preserved.

    Args:
        file_path: Path to the markdown file
        metadata: Dictionary of metadata to add as frontmatter
        preserve_content: If True, preserves existing markdown content

    Raises:
        FileNotFoundError: If the file does not exist
        FrontmatterError: If metadata cannot be serialized to YAML
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Read existing content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract existing markdown content (without frontmatter)
        if preserve_content:
            pattern = r'^---\s*\n.*?\n---\s*\n(.*)$'
            match = re.match(pattern, content, re.DOTALL)

            if match:
                # File has frontmatter, extract content after it
                markdown_content = match.group(1)
            else:
                # No frontmatter, use full content
                markdown_content = content
        else:
            markdown_content = ""

        # Generate YAML frontmatter
        try:
            yaml_str = yaml.dump(
                metadata,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False
            )
        except Exception as e:
            raise FrontmatterError(
                f"Cannot serialize metadata to YAML: {str(e)}"
            ) from e

        # Construct new file content
        new_content = f"---\n{yaml_str}---\n{markdown_content}"

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    except FrontmatterError:
        raise
    except FileNotFoundError:
        raise
    except Exception as e:
        raise FrontmatterError(
            f"Error writing frontmatter to {file_path}: {str(e)}"
        ) from e


def update_frontmatter(
    file_path: Path,
    updates: Dict[str, Any],
    merge: bool = True
) -> None:
    """
    Update specific fields in existing frontmatter.

    Args:
        file_path: Path to the markdown file
        updates: Dictionary of fields to update
        merge: If True, merges with existing metadata. If False, replaces entirely.

    Raises:
        FileNotFoundError: If the file does not exist
        FrontmatterError: If frontmatter cannot be updated
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if merge:
        # Get existing frontmatter
        existing_metadata = parse_frontmatter(file_path)
        # Merge with updates
        existing_metadata.update(updates)
        metadata = existing_metadata
    else:
        metadata = updates

    # Write updated frontmatter
    add_frontmatter(file_path, metadata, preserve_content=True)


def remove_frontmatter(file_path: Path) -> None:
    """
    Remove YAML frontmatter from a markdown file, preserving content.

    Args:
        file_path: Path to the markdown file

    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract content without frontmatter
    pattern = r'^---\s*\n.*?\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if match:
        # Has frontmatter, extract just the content
        markdown_content = match.group(1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    # If no frontmatter, file remains unchanged
