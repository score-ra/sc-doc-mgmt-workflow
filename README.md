# Symphony Core: Document Management Workflow

**Continuous document intelligence for small teams**

A standalone automated document validation tool that ensures consistency and standards compliance for markdown documentation in any document repository. This tool is designed to validate external documentation folders and business document repositories.

## Project Status

**Current Version**: 1.0.0 (Production Ready)
**Status**: All MVP features complete ✅

### v1.0 MVP Features - COMPLETE (2025-11-09)

**Sprint 1** ✅ COMPLETE:
- Document change detection with SHA-256 hashing
- Configuration management system
- Persistent caching for incremental processing

**Sprint 2** ✅ COMPLETE (13 pts):
- YAML frontmatter validation (3 required fields: title, tags, status)
- **Auto-fix engine with preview** ⭐ (moved from v1.1)

**Sprint 3** ✅ COMPLETE (18 pts):
- Markdown syntax validation
- Naming convention validation
- **Conflict detection** ⭐ (pricing, policies, duplicates - moved from v1.1)

**Sprint 4** ✅ COMPLETE (21 pts):
- CLI interface (practical commands using Click framework)
- Advanced reporting system (console, markdown, JSON)
- Enhanced conflict reporting (severity levels, impact assessment, recommendations)

**Delivery Summary**:
- Total: 52 story points completed
- Tests: 215 passing (82.01% coverage)
- Production ready: All features tested and validated

### Future Features (v1.1+)
- Intelligent document routing
- Automated tagging system
- Advanced conflict detection (semantic analysis with LLM)
- FAQ generation

See [Product Requirements Document](docs/product-requirements-document.md) for full roadmap.

## Overview

Symphony Core Document Management Workflow is an automated document validation tool designed to validate external document repositories. It helps teams maintain high-quality, consistent markdown documentation for pricing, policies, product specifications, support guides, billing information, and operational procedures across any documentation folder or repository.

**Key Benefits:**
- Reduce document review time from 4 hours/week to 30 minutes/week
- Ensure 100% standards compliance automatically
- Process 50+ documents in < 10 minutes
- Incremental processing (only check what changed)
- Configurable validation rules to match your team's needs

## Installation

### Prerequisites

- **Python 3.11 or higher** (required)
- Git (for version control)
- Anthropic API key (for future LLM features in v1.1+)

### Setup

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

   # On Unix/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (API key required for v1.1+ features only)
   ```

5. **Configure settings (optional):**
   ```bash
   # Edit config/config.yaml to customize validation rules
   ```

6. **Run tests to verify setup:**
   ```bash
   pytest
   ```

## Usage

### Working with Document Repositories

This tool is designed to validate **external document repositories**. You can:
- Point it to any folder containing markdown documents
- Validate documents in other repositories without modifying this tool's code
- Run it from this tool's directory while targeting external paths
- Use relative or absolute paths to your documentation

**Example workflow:**
```bash
# Navigate to the tool's directory
cd C:\Users\Rohit\workspace\Work\software\sc-doc-mgmt-workflow

# Validate an external document repository
python main.py validate --path C:\path\to\your\documentation

# Or use relative paths
python main.py validate --path ..\..\..\docs\your-doc-repo
```

### Command-Line Interface

**Basic Commands:**
```bash
# Get help
python main.py --help
python main.py validate --help

# Validate a document repository (uses current directory by default)
python main.py validate

# Validate specific external folder/repository
python main.py validate --path /path/to/your/docs
python main.py validate --path C:\Users\YourName\Documents\your-doc-repo

# Validate specific file(s)
python main.py validate --file document.md
python main.py validate --file doc1.md --file doc2.md

# Force full validation (ignore cache)
python main.py validate --force

# Filter by tags
python main.py validate --tags pricing
python main.py validate --tags pricing,policies
```

**Auto-Fix:**
```bash
# Preview auto-fixes (shows what will change)
python main.py validate --auto-fix --preview

# Apply auto-fixes to documents
python main.py validate --auto-fix

# Auto-fix specific external folder
python main.py validate --path /path/to/your/docs --auto-fix

# Auto-fix specific file
python main.py validate --file document.md --auto-fix
```

**Conflict Detection:**
```bash
# Run conflict detection
python main.py validate --conflicts

# With JSON output
python main.py validate --conflicts --format json --output conflicts.json

# With markdown report
python main.py validate --conflicts --format markdown --output conflicts.md
```

**Report Generation:**
```bash
# Console output (default)
python main.py validate --format console

# JSON output for CI/CD
python main.py validate --format json --output report.json

# Markdown output for documentation
python main.py validate --format markdown --output report.md
```

### Reporting Formats

**Console** (default) - Human-readable terminal output
**JSON** - Machine-readable for CI/CD integration
**Markdown** - Formatted reports for documentation

### Configuration

Edit `config/config.yaml` to customize validation rules:

```yaml
# Validation rules
validation:
  yaml:
    enabled: true
    required_fields:
      - title      # Document title
      - version    # Semantic version (1.0, 1.2.1)
      - date       # Last updated date (YYYY-MM-DD)
      - tags       # List of tags
      - status     # Document status
    allowed_statuses:
      - draft
      - review
      - approved
      - deprecated
      - active

  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true

  naming:
    enabled: true
    pattern: "lowercase-with-hyphens"
    max_length: 50
```

See [config/config.yaml](config/config.yaml) for all options.

## Project Structure

```
sc-doc-mgmt-workflow/
├── src/                           # Source code
│   ├── core/                      # Core processing modules
│   │   ├── change_detector.py     # ✅ File change detection (Sprint 1)
│   │   ├── validators/            # Validation modules
│   │   │   ├── yaml_validator.py  # ⏳ YAML validation (Sprint 2)
│   │   │   ├── markdown_validator.py  # ⏳ MD validation (Sprint 3)
│   │   │   └── naming_validator.py    # ⏳ Naming validation (Sprint 3)
│   │   └── validator_engine.py    # ⏳ Orchestrator (Sprint 2-3)
│   ├── utils/                     # Utility modules
│   │   ├── config.py              # ✅ Configuration management (Sprint 1)
│   │   ├── cache.py               # ✅ Document caching (Sprint 1)
│   │   ├── logger.py              # ✅ Logging utilities (Sprint 1)
│   │   └── frontmatter.py         # ⏳ YAML parsing (Sprint 2)
│   ├── cli.py                     # ⏳ CLI interface (Sprint 4)
│   └── main.py                    # ⏳ Entry point (Sprint 4)
├── tests/                         # Test files (mirrors src/)
│   ├── core/
│   │   └── test_change_detector.py  # ✅ Change detector tests
│   └── utils/
│       └── test_cache.py          # ✅ Cache tests
├── docs/                          # Documentation
│   └── product-requirements-document.md  # Full PRD
├── config/                        # Configuration files
│   └── config.yaml                # ✅ Main configuration
├── _meta/                         # Project metadata
│   ├── .document-cache.json       # Cache file (gitignored)
│   └── reports/                   # Validation reports (gitignored)
├── logs/                          # Log files (gitignored)
├── main.py                        # ⏳ Application entry point
├── requirements.txt               # ✅ Python dependencies
├── pytest.ini                     # ✅ Test configuration
├── .env.example                   # ✅ Environment template
├── .gitignore                     # ✅ Git ignore rules
├── CLAUDE.md                      # Development guidelines
└── README.md                      # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/core/test_change_detector.py

# Run only unit tests
pytest -m unit

# Run tests in verbose mode
pytest -v
```

### Code Quality

```bash
# Format code (PEP 8)
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest
```

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD approach)
3. Implement feature following [CLAUDE.md](CLAUDE.md) guidelines
4. Run full test suite and linters
5. Update documentation
6. Create pull request

### Coding Standards

- Follow PEP 8 style guidelines
- All functions must have docstrings (purpose, params, returns)
- Type hints required for all function signatures
- Maintain test coverage > 80%
- Keep functions small and focused (single responsibility)
- See [CLAUDE.md](CLAUDE.md) for complete standards

## Performance Targets (v1.0)

- **Validation Speed**: < 5 seconds per document
- **Batch Processing**: < 10 minutes for 50 documents
- **Incremental Processing**: < 5 minutes for typical updates
- **Memory Usage**: < 500MB for typical operations
- **Test Coverage**: > 80%

## Sprint Progress

### Sprint 1: Foundation ✅ COMPLETE
- [x] Project structure
- [x] Configuration system (config.yaml, config.py)
- [x] Logging utilities
- [x] Cache management
- [x] Change detection with SHA-256 hashing
- [x] Test framework setup
- [x] Tests for cache and change detector

### Sprint 2: YAML Validation & Auto-Fix ✅ COMPLETE
- [x] YAML frontmatter parser (utils/frontmatter.py)
- [x] YAML validator (validators/yaml_validator.py)
- [x] Required fields validation (title, tags, status)
- [x] Status value validation
- [x] Auto-fix engine with preview and backup
- [x] Tests for YAML validation and auto-fix

### Sprint 3: Markdown, Naming & Conflicts ✅ COMPLETE
- [x] Markdown syntax validator
- [x] Heading hierarchy validation
- [x] Code block language validation
- [x] Naming convention validator
- [x] Conflict detection (status, tags, pricing, cross-references)
- [x] Tests for markdown, naming, and conflict detection

### Sprint 4: CLI & Reporting ✅ COMPLETE
- [x] CLI interface (Click framework)
- [x] Validation report generator (console, JSON, markdown)
- [x] Enhanced conflict reporting (severity, impact, recommendations)
- [x] Main entry point
- [x] README and user documentation updates
- [x] Final testing and polish (215 tests passing, 82% coverage)

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Errors
Ensure write permissions for cache and log directories:
```bash
mkdir -p _meta logs
chmod 755 _meta logs  # Unix/Mac
```

### Test Failures
```bash
# Run tests in verbose mode to see details
pytest -v

# Run specific failing test
pytest tests/path/to/test_file.py::test_function -v
```

## Success Criteria (v1.0)

All success criteria achieved:

- ✅ **Sprint 1**: Change detection working with SHA-256 hashing
- ✅ **Sprint 2**: 100% of documents validated for YAML compliance + Auto-fix engine
- ✅ **Sprint 3**: Markdown and naming validation functional + Conflict detection
- ✅ **Sprint 4**: Complete CLI with < 5s validation per document + Enhanced reporting
- ✅ **Overall**: Test coverage 82.01% (exceeds 80%), all quality gates passing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following [CLAUDE.md](CLAUDE.md) standards
4. Run tests and linters
5. Submit a pull request

## Support & Documentation

- **PRD**: [docs/product-requirements-document.md](docs/product-requirements-document.md)
- **Development Standards**: [CLAUDE.md](CLAUDE.md)
- **Configuration**: [config/config.yaml](config/config.yaml)
- **Issues**: Report bugs via GitHub issues

## License

[Specify license here]

---

**Version**: 1.0.0 - Production Ready
**Status**: All MVP features complete ✅
**Last Updated**: 2025-11-09
**Tests**: 215 passing, 82.01% coverage
**Next Milestone**: v1.1 Features (see BACKLOG_FEATURES.md)
