---
title: Symphony Core v1.0 - Architecture & Solution Design
subtitle: Document Validation System (MVP)
tags: [architecture, design, v1.0]
version: 1.0
author: Engineering Team
last_updated: 2025-11-08
status: active
related_docs:
  - product-requirements-document.md
  - architecture-future-vision.md
---

# Architecture & Solution Design - v1.0 MVP
## Document Validation System

---

## 1. Document Overview

**Purpose**: Technical architecture for Symphony Core v1.0 MVP - a standalone validation tool for external markdown document repositories.

**Scope**: v1.0 focuses on validating external document repositories:
- YAML frontmatter validation
- Markdown syntax validation
- Naming convention validation
- Conflict detection (pricing, status values, tag synonyms)
- Change detection (incremental processing)
- Auto-fix with preview
- Validation reporting
- Path-based targeting of external repositories

**Out of Scope for v1.0**:
- Intelligent document routing (v1.1)
- Automated tagging (v1.1)
- Advanced semantic conflict detection with LLM (v1.1+)
- FAQ generation (v2.0)

**Related Documents**:
- **PRD**: Defines requirements and roadmap
- **Future Vision**: Architecture for v1.1+ features
- **Sprint Tracking**: Implementation progress

---

## 2. Architecture Principles

### Design Philosophy for v1.0
1. **Validation First**: Get standards enforcement right before adding intelligence
2. **Incremental Processing**: Only validate changed documents
3. **Clear Reporting**: Actionable error messages with line numbers
4. **Fail Fast**: Validate early, report clearly
5. **No External Dependencies**: No AI/LLM needed for v1.0

### Technology Choices

**Python 3.11+**
- Team expertise
- Rich ecosystem for file processing
- Excellent testing frameworks

**PyYAML / ruamel.yaml**
- YAML parsing and validation
- Preserves formatting

**markdown-it-py**
- Markdown parsing and AST generation
- Validation support

**Click**
- Modern CLI framework
- Intuitive command structure

**pytest**
- Comprehensive testing
- High coverage targets

---

## 3. System Architecture

### 3.1 High-Level Architecture (v1.0)

```
┌──────────────────────────────────────────────────────────┐
│                  Symphony Core v1.0                       │
│              Document Validation System                   │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
          ┌───────────────────────────────┐
          │     CLI Entry Point           │
          │       (main.py)               │
          │   Click-based interface       │
          └───────────────────────────────┘
                          │
                          ▼
          ┌───────────────────────────────┐
          │   Validation Orchestrator     │
          │   (validator_engine.py)       │
          │   Coordinates all validators  │
          └───────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │   YAML   │   │ Markdown │   │  Naming  │
   │Validator │   │Validator │   │Validator │
   └──────────┘   └──────────┘   └──────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
          ┌───────────────────────────────┐
          │      Report Generator         │
          │   (Validation reports)        │
          └───────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │  Config  │   │  Cache   │   │  Logger  │
   │ Manager  │   │ Manager  │   │          │
   └──────────┘   └──────────┘   └──────────┘
```

### 3.2 Data Flow

```
User runs: python main.py validate
       │
       ▼
Load configuration (config.yaml)
       │
       ▼
Initialize logger, cache, config
       │
       ▼
Scan directory for markdown files
       │
       ▼
ChangeDetector: Identify changed files (SHA-256)
       │
       ▼
FOR EACH CHANGED FILE:
│
├─→ Load file content
│
├─→ YAMLValidator: Check frontmatter
│   ├─ Required fields present?
│   ├─ Date formats correct?
│   ├─ Status values valid?
│   └─ Generate issues list
│
├─→ MarkdownValidator: Check syntax
│   ├─ Heading hierarchy correct?
│   ├─ Code blocks have language?
│   ├─ Links properly formatted?
│   └─ Generate issues list
│
├─→ NamingValidator: Check filename
│   ├─ Lowercase with hyphens?
│   ├─ Length within limit?
│   ├─ No version numbers?
│   └─ Generate issues list
│
├─→ Aggregate all issues
│
└─→ Update cache with results
       │
       ▼
Generate validation report (markdown)
       │
       ▼
Display summary to user
       │
       ▼
Exit with code (0=pass, 1=failures)
```

---

## 4. Component Design

### 4.1 ValidatorEngine (Orchestrator)

**Responsibility**: Coordinates validation workflow

**Module**: `src/core/validator_engine.py`

```python
from typing import List, Dict
from pathlib import Path
from ..utils.config import Config
from ..utils.cache import DocumentCache
from ..utils.logger import Logger
from .validators.yaml_validator import YAMLValidator
from .validators.markdown_validator import MarkdownValidator
from .validators.naming_validator import NamingValidator

class ValidatorEngine:
    """
    Orchestrates document validation workflow.

    Coordinates YAML, Markdown, and Naming validators to produce
    comprehensive validation reports.
    """

    def __init__(
        self,
        config: Config,
        cache: DocumentCache,
        logger: Logger
    ):
        """
        Initialize validator engine.

        Args:
            config: Configuration instance
            cache: Document cache instance
            logger: Logger instance
        """
        self.config = config
        self.cache = cache
        self.logger = logger

        # Initialize validators
        self.yaml_validator = YAMLValidator(config, logger)
        self.markdown_validator = MarkdownValidator(config, logger)
        self.naming_validator = NamingValidator(config, logger)

    def validate_document(self, file_path: Path) -> ValidationResult:
        """
        Validate a single document.

        Args:
            file_path: Path to markdown file

        Returns:
            ValidationResult with issues from all validators
        """

    def validate_batch(
        self,
        file_paths: List[Path]
    ) -> List[ValidationResult]:
        """
        Validate multiple documents.

        Args:
            file_paths: List of paths to validate

        Returns:
            List of ValidationResult objects
        """
```

**Data Model**:
```python
@dataclass
class ValidationResult:
    """Result of validating a single document."""
    file_path: Path
    passed: bool
    issues: List[ValidationIssue]
    processing_time: float
    timestamp: datetime

@dataclass
class ValidationIssue:
    """Single validation issue."""
    validator: str  # "yaml", "markdown", "naming"
    severity: str  # "error", "warning", "info"
    message: str
    line_number: Optional[int]
    suggestion: Optional[str]
    rule_id: str  # e.g., "YAML-001", "MD-015"
```

### 4.2 YAMLValidator

**Responsibility**: Validate YAML frontmatter

**Module**: `src/core/validators/yaml_validator.py`

```python
class YAMLValidator:
    """
    Validates YAML frontmatter in markdown documents.

    Checks:
    - Presence of YAML frontmatter
    - Required fields (title, version, date, tags, status)
    - Date format validation (YYYY-MM-DD)
    - Status values from allowed list
    - Tags is a list format
    """

    def __init__(self, config: Config, logger: Logger):
        """Initialize with configuration."""
        self.config = config
        self.logger = logger
        self.required_fields = config.get_required_yaml_fields()

    def validate(self, file_path: Path) -> List[ValidationIssue]:
        """
        Validate YAML frontmatter.

        Returns:
            List of ValidationIssue objects (empty if valid)
        """
```

**Validation Rules**:

| Rule ID | Check | Severity |
|---------|-------|----------|
| YAML-001 | YAML block present | ERROR |
| YAML-002 | Required fields present (title, version, date, tags, status) | ERROR |
| YAML-003 | Date format (YYYY-MM-DD) | ERROR |
| YAML-004 | Status in allowed list | ERROR |
| YAML-005 | Tags is a list | ERROR |
| YAML-006 | Version format (semantic) | WARNING |

### 4.3 MarkdownValidator

**Responsibility**: Validate markdown syntax

**Module**: `src/core/validators/markdown_validator.py`

```python
class MarkdownValidator:
    """
    Validates markdown syntax and structure.

    Checks:
    - Heading hierarchy (no skipped levels)
    - Code block language specifications
    - Link formats (relative paths)
    - Horizontal rule format
    - List formatting
    - Trailing whitespace
    """

    def __init__(self, config: Config, logger: Logger):
        """Initialize with configuration."""
        self.config = config
        self.logger = logger

    def validate(self, file_path: Path) -> List[ValidationIssue]:
        """
        Validate markdown syntax.

        Returns:
            List of ValidationIssue objects
        """
```

**Validation Rules**:

| Rule ID | Check | Severity |
|---------|-------|----------|
| MD-001 | Heading hierarchy correct | ERROR |
| MD-002 | No skipped heading levels | ERROR |
| MD-003 | Code blocks have language | ERROR/WARNING |
| MD-004 | Relative links only | ERROR |
| MD-005 | Horizontal rules use --- | WARNING |
| MD-006 | List formatting consistent | WARNING |
| MD-007 | No trailing whitespace | INFO |
| MD-008 | No bare URLs | WARNING |

### 4.4 NamingValidator

**Responsibility**: Validate file naming conventions

**Module**: `src/core/validators/naming_validator.py`

```python
class NamingValidator:
    """
    Validates file naming conventions.

    Checks:
    - Lowercase with hyphens pattern
    - Maximum length (default 50 chars)
    - No version numbers in filename
    - Descriptive names (minimum length)
    """

    def __init__(self, config: Config, logger: Logger):
        """Initialize with configuration."""
        self.config = config
        self.logger = logger
        self.max_length = config.get_max_filename_length()
        self.pattern = config.get_naming_pattern()

    def validate(self, file_path: Path) -> List[ValidationIssue]:
        """
        Validate filename.

        Returns:
            List of ValidationIssue objects
        """
```

**Validation Rules**:

| Rule ID | Check | Severity |
|---------|-------|----------|
| NAME-001 | Lowercase with hyphens | ERROR |
| NAME-002 | Length <= max | ERROR |
| NAME-003 | No version numbers | ERROR |
| NAME-004 | Minimum length | WARNING |
| NAME-005 | Descriptive name | WARNING |

### 4.5 ReportGenerator

**Responsibility**: Generate validation reports

**Module**: `src/core/report_generator.py`

```python
class ReportGenerator:
    """
    Generates validation reports in various formats.

    Supports:
    - Markdown format (default)
    - JSON format (for programmatic access)
    - Text format (simple console output)
    """

    def __init__(self, config: Config):
        """Initialize with configuration."""
        self.config = config
        self.output_dir = config.get_report_output_dir()

    def generate_report(
        self,
        results: List[ValidationResult],
        format: str = "markdown"
    ) -> Path:
        """
        Generate validation report.

        Args:
            results: List of validation results
            format: Output format ("markdown", "json", "text")

        Returns:
            Path to generated report file
        """
```

**Report Structure**:
```markdown
# Document Validation Report

**Generated**: 2025-11-07 10:30:00
**Mode**: Symphony Core
**Total Files**: 5
**Passed**: 3
**Failed**: 2

---

## Summary

- ✅ **3 files passed** all validation checks
- ❌ **2 files failed** with 8 total issues
  - Errors: 5
  - Warnings: 3
  - Info: 0

---

## Failed Files

### ❌ docs/my-document.md (5 issues)

#### YAML Frontmatter (2 errors)
- **YAML-003** [Line 5]: Date format incorrect
  - Current: `11/07/2025`
  - Expected: `2025-11-07`
  - Severity: ERROR

#### Naming Convention (1 error)
- **NAME-001**: Uppercase letters in filename
  - Current: `My-Document.md`
  - Expected: `my-document.md`
  - Severity: ERROR

---

## Passed Files

- ✅ docs/readme.md
- ✅ docs/guide.md
- ✅ docs/reference.md

---

**Processing Time**: 2.3 seconds
**Exit Code**: 1 (validation failed)
```

---

## 5. File Structure

```
sc-doc-mgmt-workflow/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── change_detector.py       ✅ Sprint 1
│   │   ├── validator_engine.py      ⏳ Sprint 2-3
│   │   ├── report_generator.py      ⏳ Sprint 4
│   │   └── validators/
│   │       ├── __init__.py
│   │       ├── yaml_validator.py    ⏳ Sprint 2
│   │       ├── markdown_validator.py ⏳ Sprint 3
│   │       └── naming_validator.py  ⏳ Sprint 3
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                ✅ Sprint 1
│   │   ├── cache.py                 ✅ Sprint 1
│   │   ├── logger.py                ✅ Sprint 1
│   │   └── frontmatter.py           ⏳ Sprint 2
│   ├── cli.py                       ⏳ Sprint 4
│   └── main.py                      ⏳ Sprint 4
│
├── tests/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── test_change_detector.py  ✅ Sprint 1
│   │   ├── test_validator_engine.py ⏳ Sprint 2-3
│   │   └── validators/
│   │       ├── test_yaml_validator.py    ⏳ Sprint 2
│   │       ├── test_markdown_validator.py ⏳ Sprint 3
│   │       └── test_naming_validator.py  ⏳ Sprint 3
│   └── utils/
│       ├── __init__.py
│       ├── test_config.py           ⏳ Sprint 1
│       └── test_cache.py            ✅ Sprint 1
│
├── config/
│   └── config.yaml                  ✅ Sprint 1
│
├── docs/
│   ├── product-requirements-document.md     ✅
│   ├── architecture-v1.0-validation.md      ✅ This doc
│   ├── architecture-future-vision.md        📋 v1.1+
│   ├── development-process-guide.md         ✅
│   └── user-guide.md                        ⏳ Sprint 4
│
├── sprints/
│   ├── sprint-01-foundation.md      ✅ Complete
│   ├── sprint-02-yaml-validation.md ⏳ Next
│   ├── sprint-03-markdown-naming.md ⏳ Upcoming
│   └── sprint-04-cli-polish.md      ⏳ Upcoming
│
├── _meta/
│   ├── .document-cache.json         (gitignored)
│   └── reports/                     (gitignored)
│
├── logs/                            (gitignored)
├── main.py                          ⏳ Sprint 4
├── requirements.txt                 ✅ Sprint 1
├── pytest.ini                       ✅ Sprint 1
├── .env.example                     ✅ Sprint 1
├── .gitignore                       ✅ Sprint 1
├── CLAUDE.md                        ✅ Dev standards
└── README.md                        ✅ Updated for v1.0
```

---

## 6. Error Handling Strategy

### 6.1 Error Categories

**Category 1: Configuration Errors** (User fixable)
- Missing config file
- Invalid YAML in config
- Missing required configuration fields

**Action**: Clear error message with fix suggestion, exit code 2

**Category 2: Validation Errors** (Document issues)
- YAML frontmatter invalid
- Markdown syntax violations
- Naming convention violations

**Action**: Generate report, exit code 1 (failures present)

**Category 3: System Errors** (Non-recoverable)
- File permission issues
- Disk full
- Corrupted cache

**Action**: Log error, display message, exit code 3

### 6.2 Error Handling Implementation

```python
class ValidationError(Exception):
    """Base exception for validation issues."""
    pass

class ConfigurationError(Exception):
    """Configuration-related errors."""
    pass

class CacheError(Exception):
    """Cache operation errors."""
    pass

# Usage in main.py
try:
    engine = ValidatorEngine(config, cache, logger)
    results = engine.validate_batch(files)

    if any(not r.passed for r in results):
        sys.exit(1)  # Validation failures
    else:
        sys.exit(0)  # All passed

except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
    print(f"❌ Configuration error: {e}")
    print(f"💡 Check your config.yaml file")
    sys.exit(2)

except CacheError as e:
    logger.error(f"Cache error: {e}")
    print(f"⚠️  Cache error: {e}")
    print(f"💡 Try deleting cache file and rerunning")
    sys.exit(3)
```

---

## 7. Performance Considerations

### 7.1 Performance Targets (v1.0)

| Metric | Target | Rationale |
|--------|--------|-----------|
| Single document validation | < 5 seconds | Acceptable for interactive use |
| 50 documents (full) | < 10 minutes | Within acceptable batch time |
| Change detection | < 1 second | Near-instant feedback |
| Cache load/save | < 100ms | Negligible overhead |
| Report generation | < 2 seconds | Fast feedback loop |

### 7.2 Optimization Techniques

**File I/O Optimization**:
- Use `pathlib` for efficient path operations
- Read files once, pass content to validators
- Stream large files if needed

**Caching Strategy**:
- SHA-256 hashing for reliable change detection
- Cache validation results per file
- Lazy load cache only when needed
- Atomic cache writes (no corruption)

**Memory Management**:
- Process documents one at a time (generators)
- Clear content after validation
- Don't keep all results in memory for large batches

**Parallel Processing** (v1.1 consideration):
- Current v1.0: Sequential processing (simple, sufficient)
- Future v1.1: Consider multiprocessing for large document sets

---

## 8. Security Considerations

### 8.1 Input Validation

**File Paths**:
- Validate all file paths before reading
- Check for directory traversal attempts
- Ensure files are within configured directories

**Configuration**:
- Validate config.yaml on load
- Sanitize all configuration values
- Use safe YAML loader

**Document Content**:
- No arbitrary code execution
- Safe markdown parsing
- Validate YAML with safe loader

### 8.2 Data Privacy

**No External Dependencies**:
- v1.0 has NO external API calls
- All processing is local
- No data leaves the system

**Cache Security**:
- Cache contains only hashes and metadata
- No sensitive document content in cache
- File permissions: 600 (owner only)

---

## 9. Testing Strategy

### 9.1 Test Coverage Targets

```
         /\
        /  \
       / E2E\          5% - End-to-end CLI tests
      /------\
     / Integ \        15% - Integration tests
    /----------\
   /   Unit     \     80% - Unit tests
  /--------------\
```

**Overall Target**: > 80% code coverage

### 9.2 Test Categories

**Unit Tests** (80% of tests):
- YAMLValidator: Each rule individually
- MarkdownValidator: Each rule individually
- NamingValidator: Each rule individually
- ChangeDetector: File hashing, cache operations
- Config: Loading, validation, accessors
- Cache: All operations

**Integration Tests** (15% of tests):
- ValidatorEngine: Full validation workflow
- Cache + ChangeDetector interaction
- Config + all validators
- Report generation from results

**End-to-End Tests** (5% of tests):
- Full CLI workflow with sample documents
- Error handling paths
- Different validation strictness levels

### 9.3 Test Fixtures

```
tests/fixtures/
├── valid_documents/
│   ├── pricing-policy.md          (Valid pricing document)
│   ├── product-specification.md   (Valid product spec)
│   └── support-guide.md           (Valid support guide)
├── invalid_documents/
│   ├── missing-yaml.md
│   ├── invalid-date-format.md
│   ├── bad-heading-hierarchy.md
│   └── uppercase-filename.md
└── config/
    ├── valid-config.yaml
    ├── strict-config.yaml
    └── lenient-config.yaml
```

---

## 10. Deployment & Operations

### 10.1 Installation (v1.0)

```bash
# Prerequisites: Python 3.11+

# Clone repository
git clone <repository-url>
cd sc-doc-mgmt-workflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify
pytest

# Ready to use!
```

### 10.2 Usage Commands (v1.0)

```bash
# Validate external document repository (recommended)
python main.py validate --path /path/to/your/docs

# Validate current directory (if you're in a docs folder)
python main.py validate

# Validate specific file in external repository
python main.py validate --file /path/to/your/docs/my-doc.md

# Windows path example
python main.py validate --path C:\workspace\project-docs

# Force reprocess (ignore cache)
python main.py validate --force

# Verbose output
python main.py validate --verbose

# Help
python main.py --help
```

### 10.3 Configuration

Edit `config/config.yaml` to customize:
- Required YAML fields (title, version, date, tags, status)
- Validation rules to enable/disable
- Validation strictness (strict, lenient, report-only)
- Report output directory
- Log level and file location
- Allowed status values

---

## 11. Future Enhancements (v1.1+)

**Planned for v1.1** (Next 2-3 weeks):
- Intelligent document routing
- Auto-tagging system
- Basic conflict detection
- Auto-fix capabilities

**Planned for v2.0** (4-6 weeks):
- Semantic conflict detection
- FAQ generation
- Workflow automation
- Intelligent content suggestions

See `architecture-future-vision.md` for detailed design of future features.

---

## 12. Decision Log

### AD-001: v1.0 Scope - Validation Only
**Date**: 2025-11-07
**Decision**: Focus v1.0 on validation, defer intelligence features
**Rationale**:
- Get core validation solid first
- No external dependencies (simpler)
- Can deliver working system in 4 weeks
- Foundation for future features

**Consequences**:
- (+) Faster MVP delivery
- (+) No AI/LLM costs yet
- (+) Simpler testing
- (-) Less "wow factor" initially
- (-) Users must wait for routing/tagging

### AD-002: Sequential Processing for v1.0
**Date**: 2025-11-07
**Decision**: Process documents sequentially, not parallel
**Rationale**:
- Simpler implementation
- Sufficient for < 100 documents
- Can add parallelization in v1.1

**Consequences**:
- (+) Simple, easier to debug
- (+) No concurrency issues
- (-) Slower for large document sets
- (-) May need refactoring for scale

### AD-003: Markdown Reports as Primary Format
**Date**: 2025-11-07
**Decision**: Generate markdown reports, JSON as optional
**Rationale**:
- Human-readable by default
- Git-friendly
- Easy to share
- JSON available for automation

**Consequences**:
- (+) Great developer experience
- (+) Easy to read and share
- (-) May need parsing for automation
- (+/-) Can add formats later

---

## Appendix A: Sprint Roadmap

### Sprint 1: Foundation ✅ COMPLETED
- Project structure
- Configuration system
- Logging and caching
- Change detection with SHA-256
- Tests for foundation

### Sprint 2: YAML Validation ⏳ UPCOMING (Nov 11-15)
- YAML frontmatter parser
- YAML validator with all rules
- Tests for YAML validation
- Integration with validator engine

### Sprint 3: Markdown & Naming ⏳ UPCOMING (Nov 18-22)
- Markdown syntax validator
- Naming convention validator
- Tests for both validators
- Report generator

### Sprint 4: CLI & Polish ⏳ UPCOMING (Nov 25-29)
- Click-based CLI
- Main entry point
- User documentation
- Final testing and polish
- v1.0 Release!

---

## Appendix B: Code Quality Standards

All code must meet these standards (from CLAUDE.md):

- **PEP 8 compliant** (use `black` for formatting)
- **Type hints** on all function signatures
- **Docstrings** on all functions (purpose, params, returns)
- **Test coverage** > 80%
- **Linting** passes (`flake8`)
- **Type checking** passes (`mypy`)
- **Single responsibility** principle
- **Meaningful variable names** (no abbreviations)

---

## Document History

| Version | Date | Changes | Author |
|---------|------|---------|---------|
| 1.0 | 2025-11-07 | Initial v1.0 architecture (validation focus) | Engineering Team |

---

**Document Status**: ☑ Approved
**Next Review**: After Sprint 2
**Maintained By**: Engineering Team
