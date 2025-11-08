#!/usr/bin/env python3
"""
Fill empty frontmatter blocks ({}) with proper metadata

Quick fix for documents that got empty frontmatter from buggy auto-fixer
"""
import re
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.auto_fixer import AutoFixer
from src.utils.config import Config
from src.utils.logger import Logger


def has_empty_frontmatter(file_path: Path) -> bool:
    """Check if file has empty {} frontmatter"""
    content = file_path.read_text(encoding='utf-8')
    # Match: ---\n{}\n---
    pattern = r'^---\s*\{\s*\}\s*---'
    return bool(re.match(pattern, content, re.MULTILINE))


def fill_empty_frontmatter(file_path: Path, fixer: AutoFixer):
    """Fill empty frontmatter with proper metadata"""
    content = file_path.read_text(encoding='utf-8')

    # Extract title from H1
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace('-', ' ').replace('_', ' ').title()

    # Suggest tags from path
    tags = fixer._suggest_tags_from_path(file_path)

    # Create proper frontmatter
    frontmatter = f"""---
title: {title}
tags: {tags}
status: draft
---"""

    # Replace empty frontmatter
    new_content = re.sub(r'^---\s*\{\s*\}\s*---', frontmatter, content, count=1, flags=re.MULTILINE)

    # Write back
    file_path.write_text(new_content, encoding='utf-8')
    print(f"[OK] {file_path.name}: title='{title}', tags={tags}")


def main():
    docs_path = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\03-sales")

    config = Config()
    logger = Logger("empty-fixer", console_output=False)
    fixer = AutoFixer(config, logger)

    files_fixed = 0
    for md_file in docs_path.glob("**/*.md"):
        if md_file.name == "README.md":
            continue

        if has_empty_frontmatter(md_file):
            fill_empty_frontmatter(md_file, fixer)
            files_fixed += 1

    print(f"\n[DONE] Fixed {files_fixed} files with empty frontmatter")


if __name__ == '__main__':
    main()
