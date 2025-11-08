# Symphony Core: Document Management Workflow

**Continuous document intelligence for small teams**

Automated document validation system that ensures consistency and standards compliance for markdown documentation across Symphony Core repository and business documents.

## Project Status

**Current Version**: 1.0.0-dev (MVP in development)
**Focus**: Document validation, conflict detection, and auto-fix

### v1.0 MVP Features (Revised 2025-11-07)

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

**Sprint 4** ⏳ PLANNED (21 pts):
- CLI interface (practical commands for team collaboration)
- Validation & conflict reporting

**Key Scope Changes** (see `DECISIONS.md`):
- ✅ Simplified: 3 required YAML fields (was 5)
- ✅ Enhanced: Conflict detection in v1.0 (was v1.1) - mission critical for scaling
- ✅ Enhanced: Auto-fix with preview in v1.0 (was v1.1)
- Total: 52 story points (~125 hours)

### Future Features (v1.1+)
- Intelligent document routing
- Automated tagging system
- Advanced conflict detection (semantic analysis with LLM)
- FAQ generation

See [Product Requirements Document](docs/product-requirements-document.md) for full roadmap.

## Overview

Symphony Core is an automated document validation system for business operations documentation. It helps teams maintain high-quality, consistent markdown documentation for pricing, policies, product specifications, support guides, billing information, and operational procedures.

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

## Usage (v1.0 MVP)

### Basic Validation (Coming in Sprint 2-4)

```bash
# Validate all documents in current directory
python main.py validate

# Validate specific file
python main.py validate --file docs/my-document.md

# Force reprocess all documents (ignore cache)
python main.py validate --force

# Get help
python main.py --help
```

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

### Sprint 1: Foundation ✅ COMPLETED
- [x] Project structure
- [x] Configuration system (config.yaml, config.py)
- [x] Logging utilities
- [x] Cache management
- [x] Change detection with SHA-256 hashing
- [x] Test framework setup
- [x] Tests for cache and change detector

### Sprint 2: YAML Validation ⏳ IN PROGRESS
- [ ] YAML frontmatter parser (utils/frontmatter.py)
- [ ] YAML validator (validators/yaml_validator.py)
- [ ] Required fields validation
- [ ] Date format validation
- [ ] Status/category validation
- [ ] Tests for YAML validation

### Sprint 3: Markdown & Naming ⏳ UPCOMING
- [ ] Markdown syntax validator
- [ ] Heading hierarchy validation
- [ ] Link format validation
- [ ] Naming convention validator
- [ ] Tests for markdown and naming validation

### Sprint 4: CLI & Polish ⏳ UPCOMING
- [ ] CLI interface (Click framework)
- [ ] Validation report generator
- [ ] Main entry point
- [ ] README update
- [ ] User documentation
- [ ] Final testing and polish

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

Based on the PRD, we measure success by:

- ✅ **Sprint 1**: Change detection working with SHA-256 hashing
- ⏳ **Sprint 2**: 100% of documents validated for YAML compliance
- ⏳ **Sprint 3**: Markdown and naming validation functional
- ⏳ **Sprint 4**: Complete CLI with < 5s validation per document
- ⏳ **Overall**: Test coverage > 80%, all quality gates passing

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

**Version**: 1.0.0-dev
**Status**: MVP Development - Sprint 1 Complete ✅
**Last Updated**: 2025-11-07
**Next Sprint**: Sprint 2 - YAML Validation
