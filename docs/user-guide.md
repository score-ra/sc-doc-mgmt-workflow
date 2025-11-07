---
title: Symphony Core - User Guide
version: 1.0-dev
last_updated: 2025-11-07
status: in-progress
audience: end-users
---

# Symphony Core: User Guide
## Document Validation System

**Version**: 1.0-dev (MVP in development)
**Status**: Sprint 1 complete, Sprint 2-4 upcoming

---

## Overview

Symphony Core is an automated document validation system that ensures your markdown documentation meets quality standards. It validates YAML frontmatter, markdown syntax, and naming conventions across both Symphony Core technical documentation and business operation documents.

### What Symphony Core Does

**Current (Sprint 1 Complete):**
- ✅ Detects which documents changed (incremental processing)
- ✅ Caches results for fast re-runs
- ✅ Configurable for different document types

**Coming Soon (Sprint 2-4):**
- ⏳ Validates YAML frontmatter (fields, dates, status values)
- ⏳ Validates markdown syntax (headings, links, code blocks)
- ⏳ Validates file naming conventions
- ⏳ Generates detailed validation reports
- ⏳ Command-line interface (CLI)

**Future (v1.1+):**
- 📋 Intelligent document routing
- 📋 Automated tagging
- 📋 Conflict detection
- 📋 FAQ generation

---

## Getting Started

### Prerequisites

- **Python 3.11 or higher** (required)
- Basic command-line knowledge
- Git (optional, for version control)

### Installation

1. **Download or clone the repository:**
   ```bash
   git clone <repository-url>
   cd sc-doc-mgmt-workflow
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation:**
   ```bash
   pytest
   ```

   You should see all tests passing. ✅

---

## Configuration

Symphony Core is configured through `config/config.yaml`. The system supports two modes:

### Modes

**1. Symphony Core Mode** (Technical Documentation)
- Strict standards for internal technical docs
- Required fields: title, version, author, last_updated, category, tags, status, audience
- Used for Symphony Core repository documentation

**2. Business Docs Mode** (Business Operations)
- More flexible for business documents
- Required fields: title, version, date, tags, status
- Used for pricing, policies, product specs, support docs

### Editing Configuration

Open `config/config.yaml` and customize:

```yaml
# Select your mode
mode: "symphony-core"  # or "business-docs"

# Document directories to scan
processing:
  doc_directories:
    - "."  # Current directory

# Validation rules (can be enabled/disabled)
validation:
  yaml:
    enabled: true
  markdown:
    enabled: true
  naming:
    enabled: true

# Where to save reports
reporting:
  output_dir: "_meta/reports/"
```

See the comments in `config.yaml` for all available options.

---

## Usage (When Complete)

### Basic Commands

> **Note**: CLI commands will be available after Sprint 4. Currently, the foundation is in place.

```bash
# Validate all documents
python main.py validate

# Validate specific file
python main.py validate --file docs/my-document.md

# Force revalidate everything (ignore cache)
python main.py validate --force

# Show help
python main.py --help
```

### Typical Workflow

1. **Initial Setup**: Configure `config.yaml` for your document type
2. **First Run**: System validates all documents, creates cache
3. **Edit Documents**: Make changes to your markdown files
4. **Incremental Run**: System only validates changed documents
5. **Review Report**: Check validation report in `_meta/reports/`
6. **Fix Issues**: Address any errors or warnings
7. **Re-run**: Verify all issues resolved

---

## Understanding Validation

### What Gets Validated?

#### 1. YAML Frontmatter ⏳ (Sprint 2)

**Checks:**
- YAML block present at start of file
- Required fields included (depends on mode)
- Date format correct (YYYY-MM-DD)
- Status from allowed list
- Tags is a list (not a string)

**Example Valid Frontmatter (Symphony Core mode):**
```yaml
---
title: My Document
version: 1.0
author: John Doe
last_updated: 2025-11-07
category: Guide
tags: [documentation, howto]
status: approved
audience: internal-technical
---
```

**Example Valid Frontmatter (Business Docs mode):**
```yaml
---
title: Pricing Information
version: 2.0
date: 2025-11-07
tags: [pricing, product-x]
status: approved
---
```

#### 2. Markdown Syntax ⏳ (Sprint 3)

**Checks:**
- Heading hierarchy correct (H1 → H2 → H3, no skips)
- Code blocks have language specified
- Links use relative paths (internal docs)
- Horizontal rules use `---` format
- No trailing whitespace
- Lists formatted consistently

**Good Example:**
```markdown
# Main Title (H1)

## Section (H2)

### Subsection (H3)

Code with language:
\```python
print("Hello, world!")
\```

Relative link: [See other doc](./other-doc.md)
```

**Bad Example:**
```markdown
# Main Title (H1)

### Subsection (H3) ❌ Skipped H2!

Code without language:
\``` ❌ No language specified
print("Hello")
\```

Absolute link: https://example.com/doc.md ❌ Should be relative
```

#### 3. File Naming ⏳ (Sprint 3)

**Checks:**
- Lowercase with hyphens only
- Maximum 50 characters
- No version numbers in filename
- Descriptive name (minimum 5 characters)

**Good Names:**
- `user-guide.md` ✅
- `getting-started-guide.md` ✅
- `api-reference.md` ✅

**Bad Names:**
- `UserGuide.md` ❌ (uppercase)
- `user_guide.md` ❌ (underscores)
- `guide-v2.md` ❌ (version number)
- `ug.md` ❌ (too short)
- `this-is-a-very-long-filename-that-exceeds-fifty-characters.md` ❌ (too long)

---

## Validation Reports

### Report Structure ⏳ (Sprint 4)

Validation reports will be generated in markdown format at `_meta/reports/`:

```markdown
# Document Validation Report

**Generated**: 2025-11-07 10:30:00
**Mode**: Symphony Core
**Files Processed**: 10
**Passed**: 8
**Failed**: 2

## Summary
- ✅ 8 files passed all checks
- ❌ 2 files failed with issues

## Failed Files

### ❌ docs/my-doc.md
#### YAML Frontmatter (2 errors)
- **Error**: Date format incorrect (line 5)
  - Current: `11/07/2025`
  - Expected: `2025-11-07`
  - Fix: Change date format to YYYY-MM-DD

#### Naming Convention (1 error)
- **Error**: Uppercase letters in filename
  - Current: `My-Doc.md`
  - Expected: `my-doc.md`
  - Fix: Rename file to lowercase

## Passed Files
- ✅ docs/guide.md
- ✅ docs/reference.md
... (remaining files)
```

### Understanding Severity Levels

- **ERROR**: Must be fixed (validation fails)
- **WARNING**: Should be fixed (validation passes with warnings)
- **INFO**: Optional improvement

---

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` when running commands

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Configuration Errors
**Problem**: "Configuration file not found" or "Invalid configuration"

**Solution**:
- Verify `config/config.yaml` exists
- Check YAML syntax (use online YAML validator)
- Ensure all required fields are present

#### 3. Permission Errors
**Problem**: Cannot write to cache or reports directory

**Solution**:
```bash
# Create directories with proper permissions
mkdir -p _meta logs
chmod 755 _meta logs  # macOS/Linux only
```

#### 4. Test Failures
**Problem**: Tests failing after installation

**Solution**:
```bash
# Run tests in verbose mode to see details
pytest -v

# Check specific failing test
pytest tests/path/to/test_file.py::test_name -v
```

---

## Best Practices

### Document Organization

**For Symphony Core Mode:**
- Keep technical docs in organized folders
- Use clear, descriptive filenames
- Include complete YAML frontmatter
- Link related documents

**For Business Docs Mode:**
- Organize by topic (pricing, policies, etc.)
- Use consistent tagging
- Keep content up-to-date
- Version documents appropriately

### Writing Good Frontmatter

**Required Fields**:
- Use descriptive, clear titles
- Keep versions semantic (1.0, 1.1, 2.0)
- Use YYYY-MM-DD for all dates
- Apply relevant tags
- Set appropriate status

**Recommended Fields**:
- Add `author` for accountability
- Include `audience` to clarify readers
- Use `related_docs` for cross-referencing

### Maintaining Document Quality

1. **Run validation regularly** (after each edit session)
2. **Fix errors immediately** (don't let them accumulate)
3. **Review warnings** (they indicate best practice violations)
4. **Keep configuration updated** (as your needs evolve)
5. **Use caching** (for fast incremental validation)

---

## Frequently Asked Questions

### General Questions

**Q: Do I need to validate every time I edit?**
A: Not necessarily. Validate after significant changes or before committing to version control.

**Q: Can I disable specific validation rules?**
A: Yes! Edit `config.yaml` and set rules to `enabled: false`.

**Q: How does incremental processing work?**
A: The system uses SHA-256 file hashing to detect changes. Only changed files are revalidated.

**Q: Where is the cache stored?**
A: In `_meta/.document-cache.json` (gitignored by default).

**Q: Can I use this for other markdown documents?**
A: Yes! Configure it for your document type using business-docs mode or create a custom configuration.

### Technical Questions

**Q: What Python version do I need?**
A: Python 3.11 or higher is required.

**Q: Can I run this on Windows?**
A: Yes! It works on Windows, macOS, and Linux.

**Q: How do I reset the cache?**
A: Delete `_meta/.document-cache.json` or run with `--force` flag.

**Q: Can I integrate this into CI/CD?**
A: Yes (planned for v1.1). It returns proper exit codes for automation.

**Q: Does this modify my documents?**
A: No in v1.0 (validation only). v1.1 will add optional auto-fix features.

### Configuration Questions

**Q: Can I have multiple configuration files?**
A: Yes, you can create profile-specific configs. See `config/config.yaml` for examples.

**Q: What if I want different rules for different directories?**
A: v1.0 uses one configuration. v1.1 will support per-directory configs.

**Q: Can I validate non-markdown files?**
A: No, only markdown (.md) files are supported.

---

## Getting Help

### Resources

- **README**: Quick start and project overview
- **CLAUDE.md**: Development standards and guidelines
- **PRD**: Product requirements and roadmap
- **Architecture Docs**: Technical design
- **Sprint Tracking**: Implementation progress

### Support Channels

- **Issues**: Report bugs via GitHub issues
- **Questions**: Check this guide first, then ask in discussions
- **Feature Requests**: Submit via GitHub issues with "enhancement" label

### Contributing

See [CLAUDE.md](../CLAUDE.md) for:
- Code quality standards
- Testing requirements
- Development workflow
- Pull request process

---

## Roadmap

### Current Status: v1.0-dev

**Sprint 1** ✅ COMPLETED (Nov 7-13):
- Foundation infrastructure
- Configuration system
- Caching and change detection

**Sprint 2** ⏳ UPCOMING (Nov 11-15):
- YAML frontmatter validation
- YAML parser
- Error reporting

**Sprint 3** ⏳ UPCOMING (Nov 18-22):
- Markdown syntax validation
- Naming convention validation
- Report generator

**Sprint 4** ⏳ UPCOMING (Nov 25-29):
- CLI interface (Click)
- User documentation
- Final polish and testing

### Future Releases

**v1.1** (2-3 weeks after v1.0):
- Intelligent document routing
- Automated tagging
- Basic conflict detection
- Auto-fix capabilities

**v2.0** (4-6 weeks after v1.1):
- Semantic conflict detection
- FAQ generation
- Workflow automation
- Advanced features

---

## Appendix

### Configuration Reference

See `config/config.yaml` for the complete configuration reference with detailed comments on every option.

### Validation Rules Reference

Full list of validation rules (available after Sprint 2-3):

**YAML Rules**:
- YAML-001: YAML block present
- YAML-002: Required fields present
- YAML-003: Date format correct
- YAML-004: Status value valid
- (More in Sprint 2)

**Markdown Rules**:
- MD-001: Heading hierarchy correct
- MD-002: No skipped heading levels
- MD-003: Code blocks have language
- MD-004: Relative links only
- (More in Sprint 3)

**Naming Rules**:
- NAME-001: Lowercase with hyphens
- NAME-002: Length within limit
- NAME-003: No version numbers
- (More in Sprint 3)

### Exit Codes

```
0: Success - all documents passed validation
1: Failures - some documents have validation errors
2: Configuration error - check config.yaml
3: System error - check logs for details
```

---

## Quick Reference

### Essential Commands (When Complete)

```bash
# Validate everything
python main.py validate

# Validate one file
python main.py validate --file path/to/doc.md

# Force revalidation
python main.py validate --force

# Help
python main.py --help
```

### File Locations

```
_meta/
├── .document-cache.json    # Cache file
└── reports/                # Validation reports

config/
└── config.yaml             # Configuration

logs/
└── symphony-core.log       # Application logs
```

### Common Fixes

| Issue | Fix |
|-------|-----|
| Wrong date format | Use YYYY-MM-DD format |
| Uppercase filename | Rename to lowercase-with-hyphens |
| Missing YAML | Add frontmatter at top of file |
| Code block no language | Add language after \`\`\` |
| Skipped heading | Don't skip heading levels |

---

**Version**: 1.0-dev
**Status**: In Development (Sprint 1 Complete)
**Last Updated**: 2025-11-07
**Next Update**: After Sprint 2
