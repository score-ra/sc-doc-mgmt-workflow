# Symphony Core: Document Management Workflow

**Continuous document intelligence for small teams**

A standalone automated document validation tool that ensures consistency and standards compliance for markdown documentation in any document repository. This tool is designed to validate external documentation folders and business document repositories.

## Project Status

**Current Version**: 1.2.0 (Sprint 6 - Foundation Strengthening)
**Status**: Production Ready with Enhanced Foundation ✅

### Latest Release - v1.2 (2025-11-13)

**Sprint 6** ✅ COMPLETE - Technical Debt & Foundation:
- JSON Schema configuration validation
- Professional reporter architecture verified
- Comprehensive logger testing
- **304 tests passing** (83.29% coverage)
- **Actionable error messages** throughout

### Previous Releases

**Sprint 5** ✅ COMPLETE - URL Content Extraction (v1.1):
- Extract HTML to SC-compliant markdown
- Automatic YAML frontmatter generation
- Table conversion to structured content
- 256 tests passing

**Sprint 1-4** ✅ COMPLETE - MVP Foundation (v1.0):
- Document validation (YAML, Markdown, Naming)
- Auto-fix engine with preview
- Conflict detection (pricing, policies, duplicates)
- CLI interface with multiple output formats
- Advanced reporting (console, JSON, markdown)

**Quality Metrics**:
- **Tests**: 304 passing, 9 skipped
- **Coverage**: 83.29% (exceeds 80% target)
- **Architecture**: Clean, professional-grade
- **Error Handling**: Actionable messages with fix suggestions

### Upcoming Features (v1.3+)
See [BACKLOG.md](BACKLOG.md) for prioritized roadmap:
- Git pre-commit hooks integration
- FAQ generation with LLM
- Automated document tagging
- GitHub Actions integration

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

**URL Content Extraction (Sprint 5):**
```bash
# Extract content from HTML file and convert to markdown
python main.py extract-url --source page.html

# Specify output directory
python main.py extract-url --source page.html --output docs/extracted/

# With custom title and tags
python main.py extract-url --source page.html --title "SEO Guide" --tags "seo,marketing"

# With custom category
python main.py extract-url --source page.html --category "Guide"
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

### Sprint 5: URL Content Extraction ✅ COMPLETE
- [x] HTML content extraction with BeautifulSoup
- [x] SC-compliant markdown conversion
- [x] Automatic YAML frontmatter generation
- [x] Table to structured content conversion
- [x] CLI integration (extract-url command)
- [x] 50 new tests added (256 tests total)

### Sprint 6: Technical Debt & Foundation ✅ COMPLETE
- [x] JSON Schema configuration validation (TD-002)
- [x] Reporter architecture verification (TD-001)
- [x] Comprehensive logger testing (TD-004 partial)
- [x] 48 new tests added (304 tests total)
- [x] Coverage improvement: 80.51% → 83.29%
- [x] Actionable error messages throughout

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

## Success Criteria

All success criteria exceeded:

- ✅ **v1.0 MVP**: All core validation features complete (Sprints 1-4)
- ✅ **v1.1**: URL content extraction working (Sprint 5)
- ✅ **v1.2**: Foundation strengthened with validation & testing (Sprint 6)
- ✅ **Quality**: 304 tests passing, 83.29% coverage (exceeds 80% target)
- ✅ **Architecture**: Clean, professional-grade, maintainable
- ✅ **Error Handling**: Actionable messages with fix suggestions
- ✅ **Performance**: < 5s per document, < 10 min for 50 documents

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

**Version**: 1.2.0 - Enhanced Foundation
**Status**: Production Ready with Strong Foundation ✅
**Last Updated**: 2025-11-13
**Tests**: 304 passing, 83.29% coverage
**Next Milestone**: v1.3 Features (see BACKLOG.md)
