# Claude Code Execution Prompts - Symphony Core v1.1

**Date**: 2025-11-13
**Purpose**: Prompt templates for parallel Claude Code for Cloud instances
**Project**: Symphony Core Document Management Workflow

---

## 📋 Overview

Use these prompts to launch **5 parallel Claude Code sessions** (Sprint 7) working on isolated features with minimal merge conflicts.

**Repository**: `C:\Users\Rohit\workspace\Work\software\sc-doc-mgmt-workflow`
**Base Branch**: `master`

---

## 🚀 Sprint 7: 5 Parallel Sessions (Week 1)

### Session 1 (Dev A): Severity Filtering - PB-002

**Branch**: `feature/severity-filtering`

**Prompt**:
```
You are implementing severity-based filtering for Symphony Core validation reports (PB-002).

TASK: Add --min-severity CLI flag and config option to filter validation reports by severity level (ERROR, WARNING, INFO).

FILES TO MODIFY:
- src/cli.py (add --min-severity flag)
- src/utils/config.py (add reporting.min_severity config option)
- src/reporting/__init__.py (implement filtering logic in report generation)
- tests/test_reporting.py (add test coverage)

ACCEPTANCE CRITERIA:
1. Add --min-severity [ERROR|WARNING|INFO] CLI flag
2. Add reporting.min_severity to config.yaml (default: INFO)
3. Filter report output based on severity, but keep summary statistics showing all severities
4. Report header shows "Filtered by: WARNING+" when filtering is active
5. Tests cover all severity levels

TESTING:
After implementation, test with:
python -m src.cli validate --path "C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\01-strategy" --min-severity WARNING

Expected: Should hide 283 INFO issues, show 1 ERROR + 5 WARNINGS

MERGE PRIORITY: P1 (merge first - no dependencies)
```

---

### Session 2 (Dev B): Conflict Line Numbers - PB-001

**Branch**: `feature/conflict-line-numbers`

**Prompt**:
```
You are adding line number references to conflict detection reports for Symphony Core (PB-001).

TASK: Enhance conflict detection to track and display line numbers where conflicts occur.

FILES TO MODIFY:
- src/core/validators/conflict_detector.py (track line numbers during conflict detection)
- src/reporting/conflict_reporter.py (display line numbers in conflict reports)
- tests/test_conflict_detector.py (add test coverage)

ACCEPTANCE CRITERIA:
1. Conflict reports include line numbers for each detected conflict
2. Show section headers as context (e.g., "Line 142, ## Pricing Strategy")
3. Works for all conflict types (pricing, dates, specs, status)
4. Performance overhead <10% (no significant slowdown)
5. Format: "Pricing conflict: $199 (line 142, ## Pricing Strategy)"

TESTING:
After implementation, test with:
python -m src.cli validate --path "C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\01-strategy" --conflicts

Expected: Should show line numbers for the pricing conflict in symphony-core-business-plan-draft-0.md

MERGE PRIORITY: P2 (merge second - parallel to PB-002, no conflicts)
```

---

### Session 3 (Dev C): Bulk Frontmatter Addition - NEW-003

**Branch**: `feature/bulk-frontmatter-add`

**Prompt**:
```
You are creating a new CLI command for bulk frontmatter field addition in Symphony Core (NEW-003).

TASK: Create a new "frontmatter add-field" command to bulk-add missing frontmatter fields to multiple documents.

FILES TO CREATE/MODIFY:
- src/cli.py (add NEW command: frontmatter add-field)
- src/core/frontmatter_manager.py (NEW module for frontmatter operations)
- tests/test_frontmatter_manager.py (NEW test file)

ACCEPTANCE CRITERIA:
1. New command: python -m src.cli frontmatter add-field --field status --value draft --path <directory>
2. Interactive mode: --interactive prompts for value per document
3. Preview mode: --preview shows changes without applying
4. Creates backups before modification
5. Preserves existing frontmatter formatting (YAML block structure)

EXAMPLE USAGE:
python -m src.cli frontmatter add-field --field status --value draft --path 02-marketing-brand --preview

Expected: Should show 2 documents (sc-design-kit.md, symphony_core_web_style_guide.md) would be updated

MERGE PRIORITY: P2 (merge second - completely new module, zero conflicts)
```

---

### Session 4 (Dev D): README Exclusion Patterns - NEW-001

**Branch**: `feature/exclude-patterns`

**Prompt**:
```
You are adding file exclusion patterns for YAML frontmatter validation in Symphony Core (NEW-001).

TASK: Allow excluding certain files (like README.md) from frontmatter validation requirements via glob patterns.

FILES TO MODIFY:
- src/utils/config.py (add validation.yaml.exclude_patterns option)
- config/config.yaml (add example exclusion patterns with comments)
- src/core/validators/yaml_validator.py (apply exclusions before validation)
- tests/test_yaml_validator.py (add test coverage for exclusions)

ACCEPTANCE CRITERIA:
1. Add validation.yaml.exclude_patterns list to config (supports glob patterns like "**/README.md")
2. Excluded files skip YAML frontmatter validation but still run other validators (markdown syntax, naming)
3. Report shows "X files excluded from YAML validation" in verbose mode
4. Default: no exclusions (empty list, opt-in behavior)
5. Supports multiple patterns: ["**/README.md", "**/CHANGELOG.md", "docs/*.md"]

TESTING:
After implementation, test with config:
validation:
  yaml:
    exclude_patterns:
      - "**/README.md"

python -m src.cli validate --path "C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\02-marketing-brand"

Expected: README.md should not be flagged for missing frontmatter

MERGE PRIORITY: P3 (merge third - config.py touched by PB-002, but different section)
REBASE BEFORE PR: git rebase origin/master (to get PB-002 changes)
```

---

### Session 5 (Dev E): Frontmatter Completeness Detection - PB-003

**Branch**: `feature/frontmatter-completeness`

**Prompt**:
```
You are adding frontmatter completeness detection to Symphony Core validation reports (PB-003).

TASK: Detect and report documents that are completely missing YAML frontmatter blocks (not just invalid frontmatter).

FILES TO MODIFY:
- src/core/validators/yaml_validator.py (detect missing frontmatter vs invalid frontmatter)
- src/reporting/__init__.py (add frontmatter status summary section)
- tests/test_yaml_validator.py (add test coverage)

ACCEPTANCE CRITERIA:
1. Report shows count of documents missing frontmatter entirely
2. List specific documents without frontmatter
3. Distinguish "missing frontmatter" vs "invalid frontmatter" in reports
4. Severity: WARNING for missing frontmatter (vs ERROR for invalid)
5. Optional: Add --auto-fix option to generate stub frontmatter with default values

REPORT FORMAT:
## Frontmatter Status
- Valid: 18 documents
- Missing: 1 document (README.md)
- Invalid: 2 documents (missing required field 'status')

TESTING:
After implementation, test with:
python -m src.cli validate --path "C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\02-marketing-brand"

Expected: Should report "1 document missing frontmatter: README.md" (unless excluded by NEW-001)

MERGE PRIORITY: P4 (merge fourth - depends on NEW-001)
DEPENDENCIES: Wait for feature/exclude-patterns to merge first
REBASE BEFORE PR: git rebase origin/master (to get NEW-001 exclusion logic)
```

---

## 📋 Pre-Execution Checklist (For All Sessions)

Before starting any session, ensure:
- [ ] You're in the correct repository: `C:\Users\Rohit\workspace\Work\software\sc-doc-mgmt-workflow`
- [ ] Master branch is up to date: `git checkout master && git pull origin master`
- [ ] Create feature branch: `git checkout -b feature/[feature-name]`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tests pass on master: `pytest tests/`

---

## 🔄 Merge Instructions (For All Sessions)

When your feature is complete:

1. **Run full test suite**:
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   # Must pass with 80%+ coverage
   ```

2. **Run linters**:
   ```bash
   flake8 src/ tests/
   black src/ tests/ --check
   mypy src/
   ```

3. **Rebase on master** (especially important for Sessions 4 & 5):
   ```bash
   git fetch origin
   git rebase origin/master
   # Resolve any conflicts
   pytest tests/  # Re-test after rebase
   ```

4. **Create PR** with title format:
   ```
   [Sprint 7] Feature Name (PB-XXX or NEW-XXX)
   ```

5. **Notify team** when ready for merge (based on priority order)

---

## 🎯 Merge Order (IMPORTANT)

DO NOT merge out of order. Follow this sequence:

1. **Day 1 EOD**: feature/severity-filtering (PB-002)
2. **Day 2 EOD**: feature/conflict-line-numbers (PB-001), feature/bulk-frontmatter-add (NEW-003)
3. **Day 3 EOD**: feature/exclude-patterns (NEW-001)
4. **Day 4 EOD**: feature/frontmatter-completeness (PB-003)

Sessions 4 & 5 MUST rebase before creating PR to get earlier changes.

---

## 🚨 Troubleshooting

**Merge Conflict in config.py (Session 4)?**
- PB-002 adds `reporting.min_severity`
- NEW-001 adds `validation.yaml.exclude_patterns`
- These are different sections - accept both changes

**Merge Conflict in yaml_validator.py (Session 5)?**
- NEW-001 adds `_is_excluded()` method
- PB-003 adds `_has_frontmatter()` method
- Both should coexist - keep both methods

**Tests failing after rebase?**
- Re-run: `pip install -r requirements.txt` (ensure all deps installed)
- Clear cache: `rm -rf .pytest_cache __pycache__`
- Check if your changes conflict with new master code

---

## 📞 Communication

After completing your feature:
1. Post in Slack/Discord: "✅ [PB-XXX] Complete, ready for PR review"
2. Tag merge master for priority assignment
3. Wait for merge before starting next sprint item

---

**Document Owner**: DevOps Team
**Last Updated**: 2025-11-13
**Sprint**: Sprint 7 (Week 1)
**Status**: READY FOR EXECUTION
