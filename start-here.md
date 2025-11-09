---
title: Sprint 4 Quick Start Guide
tags: [sprint-4, cli, reporting, quick-start]
status: active
version: 1.0
last_updated: 2025-11-08
---

# Sprint 4 Quick Start Guide

**Based on**: Sprint 1-3 completion (76 tests passing, all validators operational)
**Sprint Focus**: CLI interface and comprehensive reporting
**Story Points**: 21 (estimated 50 hours)

---

## TL;DR - Sprint 4 Objectives

**Build**: Command-line interface (CLI) for team collaboration + comprehensive reporting system

**Key Deliverables**:
1. **CLI Interface**: Practical commands using Click framework (ADR-004)
2. **Validation Reports**: Human-readable reports with actionable suggestions
3. **Conflict Reports**: Detailed conflict analysis with severity levels
4. **Exit Codes**: CI/CD integration support
5. **Help System**: Comprehensive help text and usage examples

**What's Already Done** (Sprint 1-3):
- ✅ All validators working (YAML, Naming, Markdown, Conflicts)
- ✅ Auto-fix engine with preview mode
- ✅ 76 tests passing (100%)
- ✅ Validation scripts operational
- ✅ Real documentation tested (161 files)

---

## Sprint 1-3 Accomplishments

### Sprint 1 ✅ COMPLETE (8 points)
**Foundation Infrastructure**
- Document change detection with SHA-256 hashing
- Configuration management system (`config/config.yaml`)
- Persistent caching for incremental processing
- Logger utility with file rotation

**Files Created**:
- `src/utils/config.py` (280 lines)
- `src/utils/cache.py` (307 lines)
- `src/utils/logger.py` (286 lines)
- `src/core/change_detector.py` (311 lines)

### Sprint 2 ✅ COMPLETE (13 points)
**YAML Validation + Auto-Fix**
- YAML frontmatter validator (4 rules: YAML-001 to YAML-004)
- Auto-fix engine with preview mode and backup
- Frontmatter parsing utilities
- 20 tests, 100% passing

**Files Created**:
- `src/core/validators/yaml_validator.py` (325 lines)
- `src/core/auto_fixer.py` (386 lines)
- `src/utils/frontmatter.py` (292 lines)
- `tests/core/validators/test_yaml_validator.py` (20 tests)

**Real Results**: Fixed 64 documents, achieved 100% frontmatter coverage

### Sprint 3 ✅ COMPLETE (18 points)
**Naming, Markdown, Conflict Detection**
- Naming convention validator (5 rules: NAME-001 to NAME-005)
- Markdown syntax validator (5 rules: MD-001 to MD-005)
- Conflict detector (4 types: CONFLICT-001 to CONFLICT-004)
- 56 tests, 100% passing

**Files Created**:
- `src/core/validators/naming_validator.py` (295 lines)
- `src/core/validators/markdown_validator.py` (362 lines)
- `src/core/validators/conflict_detector.py` (379 lines)
- `scripts/validate_naming.py`, `validate_markdown.py`, `detect_conflicts.py`
- `tests/core/validators/` (56 tests)

**Real Results**:
- Naming: 89.4% pass rate (25 violations in 161 docs)
- Markdown: 39.1% pass rate (1,093 violations in 161 docs)
- Conflicts: 8 conflicts detected (status, tags, pricing)

---

## Sprint 4 Scope & Requirements

### User Stories (from ADR-004)

**US-4.1: CLI Interface (10 points)**
Implement command-line interface using Click framework with essential commands:

```bash
# Basic validation
python main.py validate                    # Validate all documents
python main.py validate --path operations/ # Validate specific folder
python main.py validate --tags pricing     # Validate by tag
python main.py validate --force            # Ignore cache, revalidate all

# Auto-fix operations
python main.py validate --auto-fix         # Apply auto-fixes
python main.py validate --auto-fix --preview  # Preview auto-fixes

# Conflict detection
python main.py validate --conflicts        # Run conflict detection only

# Help and version
python main.py --help                      # Show help
python main.py --version                   # Show version
```

**US-4.2: Validation Reporting (6 points)**
Generate comprehensive validation reports:
- Summary statistics (files passed/failed, violations by rule)
- Detailed issue listings with file paths and line numbers
- Actionable suggestions for each violation
- Multiple output formats (console, markdown, JSON)
- Exit codes for CI/CD integration (0 = pass, 1 = fail)

**US-4.3: Conflict Reporting (5 points)**
Generate detailed conflict analysis reports:
- Conflict summary by type (status, tags, pricing, cross-references)
- Severity levels (error, warning, info)
- Impact assessment (number of documents affected)
- Recommendations for resolution
- Batch/async execution support (per ADR-006)

---

## Architecture & Design Patterns

### CLI Framework: Click

**Why Click?**
- Industry standard for Python CLIs
- Automatic help generation
- Command grouping and nesting
- Parameter validation
- Progress bars and styling

**Basic Structure**:
```python
import click
from pathlib import Path
from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from src.core.validators.naming_validator import NamingValidator
from src.core.validators.markdown_validator import MarkdownValidator
from src.core.validators.conflict_detector import ConflictDetector

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Symphony Core Document Management Workflow"""
    pass

@cli.command()
@click.option('--path', type=click.Path(exists=True), help='Validate specific folder')
@click.option('--tags', help='Validate documents with specific tag')
@click.option('--force', is_flag=True, help='Ignore cache, revalidate all')
@click.option('--auto-fix', is_flag=True, help='Auto-fix issues')
@click.option('--preview', is_flag=True, help='Preview auto-fixes without applying')
@click.option('--conflicts', is_flag=True, help='Run conflict detection only')
def validate(path, tags, force, auto_fix, preview, conflicts):
    """Validate markdown documents"""
    # Implementation here
    pass

if __name__ == '__main__':
    cli()
```

### Report Generation Pattern

**Console Output** (default):
```
================================================================================
SYMPHONY CORE - VALIDATION REPORT
================================================================================

Documents Scanned: 161
Passed: 144 (89.4%)
Failed: 17 (10.6%)

VIOLATIONS BY RULE:
  NAME-001: 16 (Uppercase in filenames/directories)
  NAME-002:  9 (Spaces in filenames)

FAILED DOCUMENTS:
  02-marketing-brand/website/steps to fix domain issue.md
    [ERROR] NAME-002: Filename contains spaces
    Suggestion: Rename to 'steps-to-fix-domain-issue.md'
...
```

**Markdown Output** (`--format markdown`):
```markdown
# Symphony Core Validation Report

**Date**: 2025-11-08
**Documents**: 161 scanned

## Summary
- Passed: 144 (89.4%)
- Failed: 17 (10.6%)

## Violations by Rule
| Rule ID | Count | Description |
|---------|-------|-------------|
| NAME-001 | 16 | Uppercase in filenames/directories |
| NAME-002 | 9 | Spaces in filenames |
...
```

**JSON Output** (`--format json`):
```json
{
  "timestamp": "2025-11-08T10:30:00Z",
  "summary": {
    "total": 161,
    "passed": 144,
    "failed": 17
  },
  "violations": [
    {
      "file": "02-marketing-brand/website/steps to fix domain issue.md",
      "rule_id": "NAME-002",
      "severity": "error",
      "message": "Filename contains spaces",
      "suggestion": "Rename to 'steps-to-fix-domain-issue.md'"
    }
  ]
}
```

---

## Implementation Roadmap

### Week 1: Core CLI Structure (5 points)

**Day 1-2: Setup**
- Install Click: `pip install click`
- Create `src/cli.py` and `src/main.py`
- Implement basic command structure
- Add `--help` and `--version` options

**Day 3-4: Validate Command**
- Implement `validate` command with basic options
- Add path filtering (`--path`)
- Add tag filtering (`--tags`)
- Add force mode (`--force`)

**Day 5: Testing**
- Write CLI tests using Click's testing utilities
- Test all command combinations
- Test error handling

**Files to Create**:
- `src/cli.py` (main CLI interface)
- `src/main.py` (entry point)
- `tests/test_cli.py` (CLI tests)

### Week 2: Reporting System (6 points)

**Day 6-7: Console Reporter**
- Create `src/reporting/console_reporter.py`
- Implement summary statistics
- Implement detailed issue listings
- Add color support (optional, use Click.echo with styles)

**Day 8-9: Markdown Reporter**
- Create `src/reporting/markdown_reporter.py`
- Generate markdown tables
- Include statistics and charts
- Save to `_meta/reports/` directory

**Day 10: JSON Reporter**
- Create `src/reporting/json_reporter.py`
- Structured JSON output
- Machine-readable format for CI/CD

**Files to Create**:
- `src/reporting/__init__.py`
- `src/reporting/console_reporter.py`
- `src/reporting/markdown_reporter.py`
- `src/reporting/json_reporter.py`
- `tests/reporting/test_reporters.py`

### Week 3: Conflict Reporting + Integration (5 points)

**Day 11-12: Conflict Reporter**
- Enhance `ConflictDetector.generate_conflict_report()`
- Add severity levels
- Add impact assessment
- Group by conflict type

**Day 13: Auto-fix Integration**
- Add `--auto-fix` flag to CLI
- Add `--preview` flag
- Integrate with AutoFixer from Sprint 2
- Show before/after in reports

**Day 14-15: Polish & Testing**
- Exit code handling (0 = pass, 1 = fail)
- Progress bars for long operations
- Comprehensive integration tests
- Update documentation (README, user-guide)

**Files to Create/Update**:
- `src/reporting/conflict_reporter.py`
- Update `src/core/conflict_detector.py`
- Update `tests/test_cli.py` (integration tests)
- Update `docs/user-guide.md`

---

## Testing Strategy

### Unit Tests
Test individual CLI commands and reporters:
```python
from click.testing import CliRunner
from src.cli import cli

def test_validate_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['validate', '--help'])
    assert result.exit_code == 0
    assert 'Validate markdown documents' in result.output

def test_validate_with_path():
    runner = CliRunner()
    result = runner.invoke(cli, ['validate', '--path', 'tests/fixtures'])
    assert result.exit_code == 0
```

### Integration Tests
Test end-to-end workflows:
```python
def test_validate_and_report():
    """Test full validation pipeline with reporting"""
    runner = CliRunner()
    result = runner.invoke(cli, [
        'validate',
        '--path', 'tests/fixtures',
        '--format', 'json',
        '--output', 'test-report.json'
    ])
    assert result.exit_code == 0
    assert Path('test-report.json').exists()
```

### Real Documentation Tests
Test on actual Symphony Core documentation:
```python
def test_validate_real_docs():
    """Test validation on real documentation repository"""
    docs_path = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")
    if not docs_path.exists():
        pytest.skip("Real docs not available")

    runner = CliRunner()
    result = runner.invoke(cli, ['validate', '--path', str(docs_path / '09-clients')])
    # 09-clients folder has 100% pass rate, should return exit code 0
    assert result.exit_code == 0
```

---

## Key Implementation Patterns

### 1. Exit Code Strategy (ADR-004, CI/CD Integration)

```python
def validate(path, tags, force, auto_fix, preview, conflicts):
    """Validate markdown documents"""
    # Run validation
    issues = run_validation(...)

    # Generate report
    generate_report(issues)

    # Exit with appropriate code
    if has_errors(issues):
        sys.exit(1)  # CI/CD will fail
    else:
        sys.exit(0)  # CI/CD will pass
```

### 2. Incremental vs. Full Validation (ADR-006)

```python
if force:
    # Full validation (ignore cache)
    documents = find_all_documents(path)
elif conflicts:
    # Conflict detection always uses all documents (ADR-006)
    documents = find_all_documents(path)
else:
    # Incremental validation (use cache)
    documents = find_changed_documents(path)
```

### 3. Report Format Selection

```python
def generate_report(issues, format='console'):
    """Generate report in specified format"""
    if format == 'console':
        reporter = ConsoleReporter()
    elif format == 'markdown':
        reporter = MarkdownReporter()
    elif format == 'json':
        reporter = JSONReporter()

    return reporter.generate(issues)
```

### 4. Progress Indication (for long operations)

```python
import click

with click.progressbar(documents, label='Validating documents') as bar:
    for doc in bar:
        validate_document(doc)
```

---

## Configuration Reference

All CLI behavior should respect `config/config.yaml`:

```yaml
# CLI Configuration
cli:
  default_format: console
  report_output_dir: _meta/reports/
  progress_bar: true
  color_output: true

# Validation toggles
validation:
  yaml:
    enabled: true
  markdown:
    enabled: true
  naming:
    enabled: true
  conflicts:
    enabled: true

# Reporting configuration
reporting:
  format: console
  output_dir: _meta/reports/
  verbose: true
  include_suggestions: true
  report_levels:
    - error
    - warning
    - info
```

---

## Example Usage Scenarios

### Scenario 1: Daily Team Validation
**Use Case**: Sarah (Documentation Manager) validates new docs before committing

```bash
# Check what changed
python main.py validate

# If issues found, see detailed report
python main.py validate --format markdown --output daily-report.md

# Auto-fix safe issues
python main.py validate --auto-fix --preview
python main.py validate --auto-fix  # Apply fixes
```

### Scenario 2: Domain-Specific Validation
**Use Case**: Mike (Content Contributor) validates only his domain

```bash
# Validate operations docs
python main.py validate --path 04-operations/

# Validate all pricing docs
python main.py validate --tags pricing
```

### Scenario 3: Pre-Release Conflict Check
**Use Case**: Team lead checks for conflicts before release

```bash
# Run comprehensive conflict detection
python main.py validate --conflicts --force

# Generate detailed conflict report
python main.py validate --conflicts --format markdown --output conflicts-report.md
```

### Scenario 4: CI/CD Integration
**Use Case**: GitHub Actions validates on every PR

```yaml
# .github/workflows/validate-docs.yml
- name: Validate Documentation
  run: |
    python main.py validate --format json --output validation-report.json
    # Exit code 1 will fail the build if validation fails
```

---

## Files to Create (Sprint 4)

### Core CLI
- `src/cli.py` (~200 lines) - Main CLI interface with Click
- `src/main.py` (~20 lines) - Entry point
- `setup.py` or `pyproject.toml` - Package configuration for CLI entry point

### Reporting System
- `src/reporting/__init__.py`
- `src/reporting/base_reporter.py` (~100 lines) - Abstract base class
- `src/reporting/console_reporter.py` (~150 lines) - Console output
- `src/reporting/markdown_reporter.py` (~200 lines) - Markdown reports
- `src/reporting/json_reporter.py` (~100 lines) - JSON output
- `src/reporting/conflict_reporter.py` (~150 lines) - Conflict-specific reports

### Tests
- `tests/test_cli.py` (~300 lines) - CLI unit and integration tests
- `tests/reporting/test_console_reporter.py` (~150 lines)
- `tests/reporting/test_markdown_reporter.py` (~150 lines)
- `tests/reporting/test_json_reporter.py` (~100 lines)

### Documentation
- Update `docs/user-guide.md` - Add CLI usage section
- Update `README.md` - Add quick start with CLI commands
- Create `docs/cli-reference.md` - Complete CLI command reference

**Estimated Total**: ~2,000 lines of production code + ~700 lines of tests

---

## Success Criteria

**Sprint 4 Complete When**:
- [ ] CLI accepts all commands from ADR-004
- [ ] Reports generate in console, markdown, and JSON formats
- [ ] Exit codes work correctly (0 = pass, 1 = fail)
- [ ] Auto-fix integrated with `--auto-fix` and `--preview` flags
- [ ] Conflict detection accessible via `--conflicts` flag
- [ ] Path and tag filtering work correctly
- [ ] Help text comprehensive and accurate
- [ ] 90%+ test coverage on CLI and reporting modules
- [ ] User guide updated with CLI examples
- [ ] Can be installed as package: `pip install -e .`
- [ ] Works in CI/CD environment (GitHub Actions tested)

**Quality Metrics**:
- All existing tests still pass (76 tests from Sprint 1-3)
- New CLI tests: 25+ tests covering all commands
- New reporter tests: 15+ tests covering all formats
- Integration tests: 5+ end-to-end scenarios
- **Total target**: 120+ tests passing

---

## Common Pitfalls to Avoid

1. **Don't over-engineer**: Stick to ADR-004 scope, avoid enterprise features
2. **Validate early**: Use Click's built-in validation (paths, choices, etc.)
3. **Handle interrupts**: Catch Ctrl+C gracefully (KeyboardInterrupt)
4. **Test with real data**: Use 09-clients folder (100% pass rate) as test fixture
5. **Color carefully**: Windows console has limitations, use Click.echo with fallbacks
6. **Exit codes matter**: CI/CD relies on correct exit codes (0/1)
7. **Progress for long ops**: Show progress bar when validating 100+ documents
8. **Cache invalidation**: `--force` must truly ignore cache (test this!)

---

## Ready to Start?

**Recommended Approach**:

1. **Setup** (Day 1):
   ```bash
   pip install click pytest-click
   python -m pytest tests/core/validators/ -v  # Verify all 76 tests pass
   ```

2. **Implement Basic CLI** (Day 1-2):
   - Create `src/cli.py` with basic structure
   - Add `validate` command with `--help`
   - Test with Click's CliRunner

3. **Add Validation Logic** (Day 3-4):
   - Wire up existing validators
   - Implement path filtering
   - Implement tag filtering
   - Test on real docs

4. **Build Reporting** (Day 6-10):
   - Console reporter first (most used)
   - Markdown reporter second (for documentation)
   - JSON reporter last (for CI/CD)

5. **Polish & Test** (Day 11-15):
   - Conflict reporting integration
   - Auto-fix integration
   - Comprehensive testing
   - Documentation updates

**First Command to Build**:
```bash
python main.py validate --path tests/fixtures --format console
```

---

## Resources & References

**From Sprint 1-3**:
- Validator implementations: `src/core/validators/*.py`
- Test patterns: `tests/core/validators/*.py`
- Configuration: `config/config.yaml`
- Real test data: `C:\Users\Rohit\...\symphony-core-documents\09-clients` (100% pass)

**Architectural Decisions**:
- ADR-004: Practical CLI Scope (see `decisions.md`)
- ADR-006: Accuracy Over Speed (conflict detection always full scan)

**External Documentation**:
- Click docs: https://click.palletsprojects.com/
- Click testing: https://click.palletsprojects.com/en/8.1.x/testing/
- Python packaging: https://packaging.python.org/

---

**Status**: 🔄 SPRINT 4 IN PROGRESS (Phase 1 Complete)
**Prerequisites**: ✅ All validators operational (174 tests passing)
**Current State**: CLI interface complete, 174 tests passing, 84.72% coverage
**Next Steps**:
- Phase 2: Advanced reporting system (dedicated reporter classes)
- Phase 3: Enhanced conflict reporting
- Documentation updates

**Last Updated**: 2025-11-09
**Maintained By**: Engineering Team
