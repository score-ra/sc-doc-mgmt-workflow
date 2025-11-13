---
title: Symphony Core - User Guide
tags: [user-guide, documentation, validation, cli]
version: 1.2.0
last_updated: 2025-11-13
status: active
audience: end-users
---

# Symphony Core: User Guide
## Document Validation & Management System

**Version**: 1.2.0 (Enhanced Foundation)
**Status**: Production ready with 83.29% test coverage

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Command-Line Interface](#command-line-interface)
4. [Validation Features](#validation-features)
5. [Auto-Fix Capabilities](#auto-fix-capabilities)
6. [Conflict Detection](#conflict-detection)
7. [Reports & Formats](#reports--formats)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#frequently-asked-questions)

---

## Overview

Symphony Core is an automated document validation system for business operations documentation. It ensures markdown documents meet quality standards by validating YAML frontmatter, markdown syntax, naming conventions, and detecting conflicts across documents.

### What Symphony Core Does

**Core Features** (v1.2 Complete):
- ✅ **YAML Frontmatter Validation** - Ensures required fields (title, tags, status)
- ✅ **Markdown Syntax Validation** - Checks headings, code blocks, links, formatting
- ✅ **Naming Convention Validation** - Enforces lowercase-with-hyphens standard
- ✅ **Conflict Detection** - Identifies pricing conflicts, status mismatches, tag issues
- ✅ **Auto-Fix Engine** - Automatically fixes common issues with preview and backup
- ✅ **Incremental Processing** - Only validates changed documents (5-10x faster)
- ✅ **CLI Interface** - Practical command-line tools for validation
- ✅ **Multiple Report Formats** - Console, JSON, and Markdown outputs
- ✅ **Enhanced Conflict Reporting** - Severity levels, impact assessment, recommendations
- ✅ **URL Content Extraction** - Convert HTML to SC-compliant markdown (v1.1)
- ✅ **Configuration Validation** - JSON Schema validation with helpful errors (v1.2)
- ✅ **Professional Architecture** - 304 tests, 83.29% coverage (v1.2)

**Benefits**:
- Reduce document review time from 4 hours/week to 30 minutes/week
- Ensure 100% standards compliance automatically
- Process 50+ documents in < 10 minutes
- Incremental processing (only check what changed)
- CI/CD integration ready

---

## Getting Started

### Prerequisites

- **Python 3.11 or higher** (required)
- Basic command-line knowledge
- Git (optional, for version control)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sc-doc-mgmt-workflow
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   pytest
   ```
   You should see 304 tests passing. ✅

5. **Test the CLI:**
   ```bash
   python main.py --help
   ```

### Quick Start

This tool validates **external document repositories**. Point it to any folder containing markdown documents:

```bash
# Validate external document repository
python main.py validate --path /path/to/your/documentation

# Validate current directory (if you're in a docs folder)
python main.py validate

# Validate specific external folder (Windows example)
python main.py validate --path C:\Users\YourName\Documents\your-docs

# Force full validation (ignore cache)
python main.py validate --force

# Auto-fix issues with preview
python main.py validate --auto-fix --preview

# Run conflict detection
python main.py validate --conflicts
```

---

## Command-Line Interface

Symphony Core provides a comprehensive CLI built with Click framework.

### Main Commands

#### Help and Version

```bash
# Show main help
python main.py --help

# Show version
python main.py --version

# Show help for validate command
python main.py validate --help
```

#### Basic Validation

```bash
# Validate external document repository (full path)
python main.py validate --path /path/to/your/docs

# Validate all documents in current directory (if you're already in docs folder)
python main.py validate

# Validate specific external folder
python main.py validate --path C:\workspace\project-docs\operations

# Force full validation (ignore cache)
python main.py validate --force
```

#### Tag Filtering

```bash
# Validate only pricing documents
python main.py validate --tags pricing

# Validate multiple tags
python main.py validate --tags pricing,policies
```

#### Auto-Fix Operations

```bash
# Preview auto-fixes (shows what will change)
python main.py validate --auto-fix --preview

# Apply auto-fixes
python main.py validate --auto-fix

# Auto-fix specific external folder
python main.py validate --path /path/to/your/docs --auto-fix
```

#### Conflict Detection

```bash
# Run conflict detection only
python main.py validate --conflicts

# Conflict detection with JSON output
python main.py validate --conflicts --format json --output conflicts.json

# Force conflict detection (reprocess all)
python main.py validate --conflicts --force
```

#### Report Generation

```bash
# Console output (default)
python main.py validate --format console

# JSON output for CI/CD
python main.py validate --format json --output report.json

# Markdown output for documentation
python main.py validate --format markdown --output report.md

# Save JSON report
python main.py validate --conflicts --format json --output conflicts.json
```

### Command Options Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--path PATH` | `-p` | Validate specific folder |
| `--tags TAGS` | `-t` | Filter by comma-separated tags |
| `--force` | `-f` | Ignore cache, revalidate all |
| `--auto-fix` | `-a` | Apply automatic fixes |
| `--preview` | | Preview fixes without applying |
| `--conflicts` | `-c` | Run conflict detection mode |
| `--format FORMAT` | | Output format (console/json/markdown) |
| `--output FILE` | `-o` | Save report to file |

### URL Content Extraction (v1.1+)

Extract HTML files and convert to SC-compliant markdown.

**Basic Usage:**
```bash
# Extract HTML to markdown
python main.py extract-url --source page.html

# With output directory
python main.py extract-url --source page.html --output docs/extracted/

# With custom metadata
python main.py extract-url --source page.html --title "SEO Guide" --tags "seo,marketing"
```

**Extract-URL Options:**

| Option | Description |
|--------|-------------|
| `--source PATH` | HTML file to extract (required) |
| `--output PATH` | Output directory (default: `_output/`) |
| `--title TEXT` | Custom title (default: from HTML) |
| `--tags TEXT` | Comma-separated tags |
| `--category TEXT` | Document category |

**Features:**
- Extracts main content from HTML
- Converts to SC-compliant markdown
- No markdown tables (converted to structured content)
- Automatic YAML frontmatter generation
- Preserves links and formatting

### Exit Codes

Symphony Core returns standard exit codes for CI/CD integration:

```
0: Success - all validations passed
1: Failure - validation errors found
```

Use in CI/CD:
```bash
# Will fail build if validation errors exist
python main.py validate || exit 1
```

---

## Validation Features

### 1. YAML Frontmatter Validation

**What it checks:**
- YAML block present at start of file
- Required fields: `title`, `tags`, `status`
- Status from allowed list
- Tags is a list format (not string)
- Optional fields: `version`, `date`, `author`, `audience`

**Valid Example:**
```yaml
---
title: Pricing Information for Product X
tags: [pricing, product-x, operations]
status: approved
version: 2.0
date: 2025-11-09
---
```

**Allowed Status Values:**
- `draft` - Document in progress
- `review` - Ready for review
- `approved` - Approved and ready for use
- `active` - Currently in use
- `deprecated` - No longer current but preserved
- `complete` - Finished and final

**Common Issues:**
```yaml
# ❌ Missing required fields
---
title: My Document
---

# ❌ Tags as string instead of list
---
title: My Document
tags: pricing, operations
status: draft
---

# ✅ Correct format
---
title: My Document
tags: [pricing, operations]
status: draft
---
```

### 2. Markdown Syntax Validation

**What it checks:**
- Heading hierarchy (no skipped levels: H1→H2→H3)
- Code blocks have language specification
- Links properly formatted
- No trailing whitespace
- Consistent list formatting

**Good Example:**
```markdown
# Main Title (H1)

## Section (H2)

### Subsection (H3)

Code with language:
\```python
print("Hello, world!")
\```

Relative link: [See guide](./guide.md)
```

**Bad Example:**
```markdown
# Main Title (H1)

### Subsection (H3)  ❌ Skipped H2!

Code without language:
\```  ❌ No language
print("Hello")
\```
```

**Supported Code Languages:**
- `python`, `javascript`, `bash`, `json`, `yaml`, `markdown`
- `sql`, `java`, `go`, `rust`, `typescript`
- And many more...

### 3. Naming Convention Validation

**Rules:**
- Lowercase with hyphens only
- Maximum 50 characters
- Minimum 5 characters (descriptive names)
- No version numbers in filename
- No spaces or underscores

**Good Names:**
- ✅ `user-guide.md`
- ✅ `getting-started.md`
- ✅ `api-reference.md`
- ✅ `pricing-policy.md`

**Bad Names:**
- ❌ `UserGuide.md` (uppercase)
- ❌ `user_guide.md` (underscores)
- ❌ `guide-v2.md` (version number)
- ❌ `ug.md` (too short)
- ❌ `user guide.md` (spaces)

**Exceptions:**
- `README.md` - Allowed in uppercase
- `*.csv` files - Not validated

### Validation Severity Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **ERROR** | Critical issue | Must fix (build fails) |
| **WARNING** | Best practice violation | Should fix (build passes) |
| **INFO** | Optional improvement | Nice to fix (cosmetic) |

---

## Auto-Fix Capabilities

Symphony Core can automatically fix common YAML frontmatter issues with safety features.

### What Auto-Fix Can Do

✅ **Add Missing Frontmatter**
- Detects documents without YAML block
- Creates complete frontmatter structure

✅ **Extract Title from H1**
- Finds first H1 heading (e.g., `# My Document`)
- Sets as `title: My Document`

✅ **Suggest Tags from Path**
- Analyzes file path
- Suggests relevant tags (e.g., `pricing/` → `[pricing]`)

✅ **Set Default Status**
- Adds `status: draft` if missing

✅ **Convert Tags Format**
- Changes string tags to list format
- `tags: pricing` → `tags: [pricing]`

### Safety Features

**Preview Mode:**
```bash
# Shows what will change without modifying files
python main.py validate --auto-fix --preview
```

**Automatic Backups:**
- Creates timestamped backup before any changes
- Stored in `_meta/.backups/`
- Format: `filename_YYYYMMDD_HHMMSS.md`

**Validation After Fix:**
- Re-validates after applying fixes
- Ensures fixes are correct

### Auto-Fix Usage Examples

```bash
# Preview all fixes
python main.py validate --auto-fix --preview

# Apply fixes to all documents
python main.py validate --auto-fix

# Fix specific folder
python main.py validate --path docs/pricing/ --auto-fix

# Preview fixes for specific folder
python main.py validate --path docs/ --auto-fix --preview
```

**Example Output:**
```
✓ Auto-fixed: docs/my-document.md
  - Added YAML frontmatter
  - Set title from H1: "My Document"
  - Added tags: [documentation]
  - Set status: draft
  - Backup created: _meta/.backups/my-document_20251109_103045.md
```

### What Auto-Fix Cannot Do

Auto-fix only handles YAML frontmatter issues. It does **not** fix:
- Markdown syntax errors (heading hierarchy, code blocks)
- Naming convention violations (must rename manually)
- Conflicts between documents
- Broken links or references

For these issues, manual intervention is required.

---

## Conflict Detection

Symphony Core detects conflicts across multiple documents to ensure consistency.

### Types of Conflicts Detected

#### 1. Status Conflicts
- Detects inconsistent status casing (`draft` vs `Draft`)
- Identifies non-standard status values
- Suggests standardization

#### 2. Tag Synonym Conflicts
- Finds similar tags that should be unified
- Example: `product-specs` vs `product-specifications`
- Recommends standard tag usage

#### 3. Pricing Conflicts
- Detects different prices for same product
- Normalizes to monthly rates for comparison
- Highlights critical pricing discrepancies

#### 4. Cross-Reference Conflicts
- Finds links to deprecated documents
- Identifies broken internal references
- Suggests updates or removals

### Running Conflict Detection

```bash
# Basic conflict detection
python main.py validate --conflicts

# With JSON output
python main.py validate --conflicts --format json --output conflicts.json

# With markdown report
python main.py validate --conflicts --format markdown --output conflicts.md
```

### Conflict Report Features

**Severity Distribution:**
- Counts errors, warnings, info by type
- Highlights critical conflicts

**Impact Assessment:**
- Documents affected count
- Conflict density (conflicts per document)
- Critical conflict count

**Recommendations:**
- Actionable steps to resolve conflicts
- Prioritized by severity
- Context-aware suggestions

**Example Console Output:**
```
================================================================================
CONFLICT DETECTION REPORT
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Total Conflicts: 8
Documents Affected: 5
Conflict Density: 1.6 per document

SEVERITY DISTRIBUTION
--------------------------------------------------------------------------------
  ERROR: 3
  WARNING: 5

CONFLICTS BY TYPE
--------------------------------------------------------------------------------

STATUS (3):
  [ERROR] pricing-policy.md
    Status mismatch: 'Draft' should be 'draft'
  ...

PRICING (2):
  [ERROR] product-pricing.md
    Pricing conflict: Product X listed as $100 and $150

RECOMMENDATIONS
--------------------------------------------------------------------------------
1. CRITICAL: 3 error-level conflicts require immediate attention
2. URGENT: Resolve pricing conflicts to prevent customer confusion
3. Review status field consistency across related documents
4. Run conflict detection after each major documentation update
```

---

## Reports & Formats

Symphony Core supports three report formats for different use cases.

### Console Format (Default)

Human-readable terminal output with colors and formatting.

**Best for:**
- Interactive development
- Quick validation checks
- Local development

**Example:**
```bash
python main.py validate
```

**Output:**
```
================================================================================
SYMPHONY CORE - DOCUMENT VALIDATION
================================================================================

Mode: Validation
Path: ./docs
Force: No (incremental)

Documents to process: 12

================================================================================
VALIDATION REPORT
================================================================================

Documents Scanned: 12
Passed: 10 (83.3%)
Failed: 2 (16.7%)

Total Errors: 3
Total Warnings: 5

VIOLATIONS BY RULE:
  YAML-001: 2
  MD-002: 5
  NAME-001: 1

FAILED DOCUMENTS:

  docs/my-doc.md
    [ERROR] YAML-001: YAML frontmatter block is missing
    ...
```

### JSON Format

Machine-readable structured output for CI/CD and automation.

**Best for:**
- CI/CD pipelines
- Automated processing
- Integration with other tools
- Programmatic analysis

**Example:**
```bash
python main.py validate --format json --output report.json
```

**Output Structure:**
```json
{
  "summary": {
    "total": 12,
    "passed": 10,
    "failed": 2,
    "pass_rate": 83.33,
    "errors": 3,
    "warnings": 5
  },
  "violations": [
    {
      "file": "docs/my-doc.md",
      "rule_id": "YAML-001",
      "severity": "error",
      "message": "YAML frontmatter block is missing",
      "line": 1,
      "suggestion": "Add YAML frontmatter..."
    }
  ],
  "timestamp": "2025-11-09T12:00:00",
  "scan_mode": "validation",
  "violations_by_rule": {
    "YAML-001": 2,
    "MD-002": 5
  }
}
```

### Markdown Format

Documentation-ready formatted reports with tables.

**Best for:**
- Documentation archives
- Sharing with team
- Historical records
- GitHub/GitLab integration

**Example:**
```bash
python main.py validate --format markdown --output report.md
```

**Output:**
```markdown
# Symphony Core Validation Report

**Date**: 2025-11-09
**Documents**: 12 scanned

## Summary

- **Total**: 12 documents
- **Passed**: 10 (83.3%)
- **Failed**: 2 (16.7%)
- **Errors**: 3
- **Warnings**: 5

## Violations by Rule

| Rule ID | Count | Description |
|---------|-------|-------------|
| YAML-001 | 2 | YAML frontmatter missing |
| MD-002 | 5 | Code block missing language |
...
```

### Choosing the Right Format

| Format | Use Case | Command Flag |
|--------|----------|--------------|
| Console | Interactive development | `--format console` (default) |
| JSON | CI/CD, automation | `--format json` |
| Markdown | Documentation | `--format markdown` |

---

## Configuration

Symphony Core is configured through `config/config.yaml`.

### Main Configuration Sections

#### Processing Settings

```yaml
processing:
  doc_directories:
    - "."  # Directories to scan
  exclude_patterns:
    - "_meta/**"
    - ".*/**"
    - "node_modules/**"
```

#### Validation Rules

```yaml
validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - tags
      - status
    allowed_statuses:
      - draft
      - review
      - approved
      - active
      - deprecated
      - complete

  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true

  naming:
    enabled: true
    pattern: "lowercase-with-hyphens"
    max_length: 50
    min_length: 5

  conflicts:
    enabled: true
    detect_pricing_conflicts: true
    detect_status_conflicts: true
```

#### Paths Configuration

```yaml
paths:
  cache_file: "_meta/.document-cache.json"
  logs_dir: "logs"
  backups_dir: "_meta/.backups"
  reports_dir: "_meta/reports"
```

#### Logging

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file_rotation: true
  max_bytes: 10485760  # 10 MB
  backup_count: 5
```

### Enabling/Disabling Rules

To disable a specific validator:

```yaml
validation:
  yaml:
    enabled: false  # Disable YAML validation
```

To disable specific checks:

```yaml
validation:
  markdown:
    enforce_heading_hierarchy: false
    require_language_in_code_blocks: true
```

### Custom Status Values

Add your own status values:

```yaml
validation:
  yaml:
    allowed_statuses:
      - draft
      - review
      - approved
      - active
      - deprecated
      - complete
      - archived      # Custom
      - in-progress   # Custom
```

---

## Best Practices

### Document Organization

1. **Use clear folder structure:**
   ```
   docs/
   ├── pricing/
   ├── policies/
   ├── product-specs/
   ├── support/
   └── operations/
   ```

2. **Name files descriptively:**
   - ✅ `product-x-pricing-policy.md`
   - ❌ `policy.md`

3. **Apply consistent tags:**
   - Use same tags for similar documents
   - Create tag taxonomy
   - Document tag meanings

### YAML Frontmatter Best Practices

```yaml
---
# Always include required fields
title: Clear, Descriptive Title
tags: [primary-tag, secondary-tag, category]
status: approved

# Include helpful optional fields
version: 1.0
date: 2025-11-09
author: Team Name
audience: internal

# Link related documents
related_docs:
  - pricing-overview.md
  - product-catalog.md
---
```

### Workflow Integration

**Daily Workflow:**
```bash
# 1. Before committing changes
python main.py validate

# 2. If issues found, preview fixes
python main.py validate --auto-fix --preview

# 3. Apply safe fixes
python main.py validate --auto-fix

# 4. Manually fix remaining issues

# 5. Re-validate
python main.py validate

# 6. Commit when clean
git commit -m "docs: update pricing policy"
```

**Weekly Workflow:**
```bash
# Run conflict detection
python main.py validate --conflicts --format markdown --output weekly-conflicts.md

# Review and resolve conflicts

# Run full validation
python main.py validate --force
```

### CI/CD Integration

**GitHub Actions Example:**
```yaml
name: Validate Docs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Validate documents
        run: |
          python main.py validate --format json --output validation.json
      - name: Upload report
        uses: actions/upload-artifact@v2
        if: always()
        with:
          name: validation-report
          path: validation.json
```

### Performance Tips

1. **Use incremental validation:**
   ```bash
   # Fast - only changed files
   python main.py validate
   ```

2. **Force only when needed:**
   ```bash
   # Slower - all files
   python main.py validate --force
   ```

3. **Filter by path for large repos:**
   ```bash
   # Validate only specific area
   python main.py validate --path docs/pricing/
   ```

4. **Use tags for organization:**
   ```bash
   # Validate specific document type
   python main.py validate --tags pricing
   ```

---

## Troubleshooting

### Common Issues

#### 1. Module Not Found Errors

**Problem:** `ModuleNotFoundError` when running commands

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import click; import yaml; print('OK')"
```

#### 2. Configuration Errors

**Problem:** "Configuration file not found" or "Invalid configuration"

**Solution:**
- Verify `config/config.yaml` exists
- Check YAML syntax with online validator
- Ensure all required sections present
- Check file permissions

#### 3. Permission Errors

**Problem:** Cannot write to cache or reports directory

**Solution:**
```bash
# Create directories
mkdir -p _meta logs

# Set permissions (Unix/Mac)
chmod 755 _meta logs

# Windows - check folder properties
```

#### 4. Incremental Mode Not Working

**Problem:** All files validated every time

**Solution:**
```bash
# Check if cache file exists
ls _meta/.document-cache.json

# If missing, will be created on first run
python main.py validate

# If still issues, force rebuild cache
rm _meta/.document-cache.json
python main.py validate
```

#### 5. Unicode Encoding Errors (Windows)

**Problem:** `'charmap' codec can't encode character` errors

**Solution:**
```bash
# Use JSON or Markdown output instead of console
python main.py validate --format json --output report.json

# Or set environment variable
set PYTHONIOENCODING=utf-8
python main.py validate
```

#### 6. Test Failures

**Problem:** Tests failing after installation

**Solution:**
```bash
# Run tests in verbose mode
pytest -v

# Check specific failing test
pytest tests/path/to/test.py::test_name -v

# Check Python version
python --version  # Should be 3.11+
```

### Debug Mode

Enable debug logging for troubleshooting:

```yaml
# config/config.yaml
logging:
  level: "DEBUG"
```

Check logs:
```bash
tail -f logs/validation.log
```

### Getting Help

1. **Check this guide** - Most questions answered here
2. **Review configuration** - Verify `config/config.yaml`
3. **Check logs** - Look in `logs/validation.log`
4. **Run tests** - Ensure system is working: `pytest`
5. **GitHub Issues** - Report bugs with error details

---

## Frequently Asked Questions

### General Usage

**Q: Do I need to run validation every time I edit?**
A: No. Run after significant changes or before committing. Use incremental mode for fast checks.

**Q: Can I disable specific validation rules?**
A: Yes! Edit `config/config.yaml` and set `enabled: false` for any validator.

**Q: How does incremental processing work?**
A: Uses SHA-256 file hashing to detect changes. Only changed files are revalidated. 5-10x faster than full validation.

**Q: Where is the cache stored?**
A: In `_meta/.document-cache.json` (gitignored by default).

**Q: How do I reset the cache?**
A: Delete `_meta/.document-cache.json` or run with `--force` flag.

**Q: Does validation modify my documents?**
A: No, unless you use `--auto-fix`. Preview mode (`--auto-fix --preview`) shows changes first.

### Technical

**Q: What Python version is required?**
A: Python 3.11 or higher.

**Q: Does it work on Windows?**
A: Yes! Works on Windows, macOS, and Linux.

**Q: Can I integrate with CI/CD?**
A: Yes! Returns proper exit codes and supports JSON output. See CI/CD section.

**Q: Can I validate non-markdown files?**
A: No, only markdown (.md) files are supported.

**Q: How fast is validation?**
A: < 5 seconds per document. ~10 minutes for 50 documents (full scan). Incremental mode much faster.

### Features

**Q: What can auto-fix handle?**
A: YAML frontmatter issues only (missing blocks, fields, format). See Auto-Fix section.

**Q: What conflicts can be detected?**
A: Status inconsistencies, tag synonyms, pricing discrepancies, deprecated document references.

**Q: Can I have different rules for different folders?**
A: Not in v1.0. Use `--path` to validate specific folders. v1.1 will support per-directory configs.

**Q: How accurate is conflict detection?**
A: Very accurate for status/pricing. Tag synonym detection uses heuristics (may have false positives).

### Configuration

**Q: Can I use multiple configuration files?**
A: v1.0 uses single config. You can maintain multiple configs and swap them as needed.

**Q: How do I add custom status values?**
A: Add to `validation.yaml.allowed_statuses` in `config/config.yaml`.

**Q: Can I customize report output location?**
A: Yes, set `paths.reports_dir` in config or use `--output` flag.

---

## Quick Reference

### Essential Commands

```bash
# Basic validation
python main.py validate

# Validation with options
python main.py validate --path docs/ --force
python main.py validate --tags pricing
python main.py validate --auto-fix --preview

# Conflict detection
python main.py validate --conflicts

# Generate reports
python main.py validate --format json --output report.json
python main.py validate --format markdown --output report.md

# Help
python main.py --help
python main.py validate --help
```

### File Locations

```
_meta/
├── .document-cache.json       # Cache (gitignored)
├── .backups/                  # Auto-fix backups (gitignored)
└── reports/                   # Generated reports (gitignored)

config/
└── config.yaml                # Configuration

logs/
└── validation.log             # Application logs (gitignored)
```

### Common Fixes

| Issue | Fix |
|-------|-----|
| Missing YAML | Use auto-fix or add manually |
| Wrong status value | Use allowed values (draft, review, approved, etc.) |
| Tags as string | Convert to list: `tags: [tag1, tag2]` |
| Uppercase filename | Rename to lowercase-with-hyphens |
| Code block no language | Add language after \`\`\` |
| Skipped heading level | Add missing heading level |
| Trailing whitespace | Remove spaces at end of lines |

### Validation Rules Quick Reference

| Rule ID | Description | Severity |
|---------|-------------|----------|
| YAML-001 | YAML frontmatter missing | ERROR |
| YAML-002 | Required field missing | ERROR |
| YAML-003 | Invalid status value | ERROR |
| YAML-004 | Tags not in list format | WARNING |
| MD-001 | Heading hierarchy violation | WARNING |
| MD-002 | Code block missing language | WARNING |
| MD-003 | Broken link | ERROR |
| MD-004 | Trailing whitespace | INFO |
| NAME-001 | Uppercase in filename | ERROR |
| NAME-002 | Spaces in filename | ERROR |
| NAME-003 | Version in filename | WARNING |
| CONFLICT-001 | Status conflict | ERROR |
| CONFLICT-002 | Tag synonym | WARNING |
| CONFLICT-003 | Pricing conflict | ERROR |
| CONFLICT-004 | Deprecated reference | WARNING |

---

## What's Next

### Current Version: v1.0.0

All core features complete and production-ready:
- ✅ Full validation suite
- ✅ Auto-fix capabilities
- ✅ Conflict detection
- ✅ CLI interface
- ✅ Multiple report formats

### Coming in v1.1

- Intelligent document routing
- Enhanced automated tagging
- Semantic conflict detection with LLM
- FAQ generation from corpus
- Per-directory configuration
- Advanced reporting dashboard

See `BACKLOG_FEATURES.md` for complete roadmap.

---

**Version**: 1.0.0 - Production Ready
**Last Updated**: 2025-11-09
**Tests**: 215 passing, 82% coverage
**Status**: All features complete

For technical details, see [README.md](../README.md) and [CLAUDE.md](../CLAUDE.md).
