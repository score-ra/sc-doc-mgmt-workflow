# Symphony Core Product Backlog - Parallel Development Edition

**Last Updated**: 2025-11-13
**Current Version**: v1.0.0
**Next Release**: v1.1.0 (Target: 2 weeks)

---

## 🎯 Parallel Development Strategy

This backlog is **architected for parallel execution** by multiple developers (or Claude Code instances) with **minimal merge conflicts**. Items are grouped by:
1. **File isolation** (different files = no conflicts)
2. **Module boundaries** (reporting vs validation vs CLI)
3. **Dependency ordering** (Sprint 7 items don't depend on each other)

---

## 📊 Backlog Overview

| Sprint | Duration | Items | Developers | Conflict Risk |
|--------|----------|-------|------------|---------------|
| Sprint 7 | 1 week | 5 items | 3-5 parallel | ⚠️ LOW |
| Sprint 8 | 2 weeks | 3 items | 2-3 parallel | ⚠️ LOW |
| Sprint 9 | 1 week | 1 item | 1 dev | ⚠️ VERY LOW |
| Backlog | Future | 4 items | TBD | Advanced features |

**Total Effort for v1.1**: 4 weeks (9 core items)
**Advanced Features**: Backlog (4 items requiring manual intervention)

---

## 🏃 SPRINT 7: Critical UX Improvements (Week 1)

**Goal**: Reduce noise, improve usability, enable migrations

**Branch Strategy**: Each developer works in separate branch, merge in order of priority

### Track A: Reporting Module (Zero Conflicts)

#### PB-002: Severity-Based Filtering (`--min-severity`)
- **Status**: 🟡 PROPOSED
- **Priority**: P0 - CRITICAL
- **Developer**: Dev 1 (or Claude Code instance A)
- **Branch**: `feature/severity-filtering`
- **Effort**: 1 day
- **Files Modified**:
  - `src/cli.py` (add CLI flag)
  - `src/utils/config.py` (add config option)
  - `src/reporting/__init__.py` (filter logic)
  - `tests/test_reporting.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ LOW (reporting module is isolated)

**User Story**: As a documentation manager, I want to see only ERROR/WARNING issues by default, so I focus on critical problems.

**Acceptance Criteria**:
- [ ] Add `--min-severity [ERROR|WARNING|INFO]` CLI flag
- [ ] Add `reporting.min_severity` config option (default: INFO)
- [ ] Report header shows if filtering is active
- [ ] Summary statistics still show all severities
- [ ] Tests cover all severity levels

**Testing**:
```bash
python -m src.cli validate --path 01-strategy --min-severity WARNING
# Should hide 283 INFO issues, show 1 ERROR + 5 WARNINGS
```

---

#### PB-001: Line Numbers in Conflict Reports
- **Status**: 🟡 PROPOSED
- **Priority**: P0 - CRITICAL
- **Developer**: Dev 2 (or Claude Code instance B)
- **Branch**: `feature/conflict-line-numbers`
- **Effort**: 2 days
- **Files Modified**:
  - `src/core/validators/conflict_detector.py` (track line numbers)
  - `src/reporting/conflict_reporter.py` (display line numbers)
  - `tests/test_conflict_detector.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ LOW (conflict module is isolated)

**User Story**: As a content contributor, I need line numbers for conflicts so I can fix them quickly.

**Acceptance Criteria**:
- [ ] Conflict reports include line numbers for each conflict
- [ ] Show section headers as context
- [ ] Works for all conflict types (pricing, dates, specs)
- [ ] Performance: no significant slowdown (<10% overhead)

**Testing**:
```bash
python -m src.cli validate --path 01-strategy --conflicts
# Should show:
# - Pricing conflict: $199 (line 142, ## Pricing Strategy)
```

---

### Track B: Validation Module (Low Conflicts)

#### NEW-001: README Exclusion Patterns
- **Status**: 🟡 PROPOSED
- **Priority**: P0 - CRITICAL
- **Developer**: Dev 3 (or Claude Code instance C)
- **Branch**: `feature/exclude-patterns`
- **Effort**: 1.5 days
- **Files Modified**:
  - `src/utils/config.py` (add exclude_patterns option)
  - `config/config.yaml` (add examples)
  - `src/core/validators/yaml_validator.py` (apply exclusions)
  - `tests/test_yaml_validator.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ MEDIUM (config.py touched by PB-002, but different sections)

**User Story**: As a documentation manager, I want to exclude READMEs from frontmatter validation.

**Acceptance Criteria**:
- [ ] Add `validation.yaml.exclude_patterns` config option
- [ ] Support glob patterns (`**/README.md`, `docs/*.md`)
- [ ] Excluded files still run other validators (markdown, naming)
- [ ] Report shows "X files excluded from YAML validation"
- [ ] Default: no exclusions (opt-in)

**Testing**:
```yaml
# config.yaml
validation:
  yaml:
    exclude_patterns:
      - "**/README.md"
```

---

#### PB-003: Frontmatter Completeness Detection
- **Status**: 🟡 PROPOSED
- **Priority**: P0 - CRITICAL
- **Developer**: Dev 4 (or Claude Code instance D)
- **Branch**: `feature/frontmatter-completeness`
- **Effort**: 1.5 days
- **Files Modified**:
  - `src/core/validators/yaml_validator.py` (detect missing frontmatter)
  - `src/reporting/__init__.py` (add summary section)
  - `tests/test_yaml_validator.py`
- **Dependencies**: NEW-001 (avoid duplicate work on yaml_validator.py)
- **Merge Conflicts**: ⚠️ MEDIUM (yaml_validator.py touched by NEW-001)

**User Story**: As a QA tester, I need to know which documents lack frontmatter entirely.

**Acceptance Criteria**:
- [ ] Report shows count of documents missing frontmatter
- [ ] List specific documents without frontmatter
- [ ] Distinguish "missing" vs "invalid" frontmatter
- [ ] Add severity: WARNING for missing frontmatter
- [ ] Add auto-fix stub frontmatter generation

**Testing**:
```bash
python -m src.cli validate --path 02-marketing-brand
# Should report: "1 document missing frontmatter: README.md"
```

---

### Track C: CLI Module (Zero Conflicts)

#### NEW-003: Bulk Frontmatter Field Addition (NEW COMMAND)
- **Status**: 🟡 PROPOSED
- **Priority**: P1 - HIGH
- **Developer**: Dev 5 (or Claude Code instance E)
- **Branch**: `feature/bulk-frontmatter-add`
- **Effort**: 2 days
- **Files Modified**:
  - `src/cli.py` (NEW command: `frontmatter add-field`)
  - `src/core/frontmatter_manager.py` (NEW module)
  - `tests/test_frontmatter_manager.py` (NEW tests)
- **Dependencies**: NONE (completely new module)
- **Merge Conflicts**: ⚠️ VERY LOW (new command, new files)

**User Story**: As a documentation manager migrating 100 docs, I want to bulk-add missing fields.

**Acceptance Criteria**:
- [ ] New command: `frontmatter add-field --field status --value draft --path .`
- [ ] Interactive mode: `--interactive` prompts per document
- [ ] Preview mode: `--preview` shows changes without applying
- [ ] Creates backups before modification
- [ ] Preserves existing frontmatter formatting

**Testing**:
```bash
python -m src.cli frontmatter add-field --field status --value draft --path 02-marketing-brand --preview
# Should show 2 documents would be updated
```

---

### Sprint 7 Merge Strategy

```
master
  ├─ feature/severity-filtering (PB-002) ← MERGE FIRST (highest priority, zero conflicts)
  │   └─ merge → master
  ├─ feature/conflict-line-numbers (PB-001) ← MERGE SECOND (zero conflicts with PB-002)
  │   └─ merge → master
  ├─ feature/exclude-patterns (NEW-001) ← MERGE THIRD (touches config.py)
  │   └─ merge → master
  ├─ feature/frontmatter-completeness (PB-003) ← MERGE FOURTH (depends on NEW-001)
  │   └─ rebase from master (get NEW-001 changes)
  │   └─ merge → master
  └─ feature/bulk-frontmatter-add (NEW-003) ← MERGE LAST (zero conflicts)
      └─ merge → master
```

**Estimated Merge Time**: 30 minutes (minimal conflicts due to module isolation)

---

## 🚀 SPRINT 8: Auto-Fix & Performance (Week 2-3)

**Goal**: Enable safe bulk operations, improve UX

### Track A: Auto-Fix Module

#### PB-005: Bulk Auto-Fix Preview Workflow
- **Status**: 🟡 PROPOSED
- **Priority**: P1 - HIGH
- **Developer**: Dev 3 (or Claude Code instance C)
- **Branch**: `feature/autofix-preview`
- **Effort**: 4 days
- **Files Modified**:
  - `src/cli.py` (add `--preview` flag)
  - `src/core/auto_fixer.py` (add preview mode)
  - `src/reporting/__init__.py` (add preview report)
  - `tests/test_auto_fixer.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ LOW (auto_fixer is isolated)

**User Story**: As a documentation manager, I want to preview auto-fixes before applying.

**Acceptance Criteria**:
- [ ] `--auto-fix --preview` shows proposed changes
- [ ] Interactive mode: prompt for approval per fix category
- [ ] Non-interactive: `--auto-fix --approve-all` for CI/CD
- [ ] Generate diff view (before/after)
- [ ] Create backups before applying

---

#### NEW-002: Auto-Fix Filename Violations + Link Updates
- **Status**: 🟡 PROPOSED
- **Priority**: P1 - HIGH
- **Developer**: Dev 4 (or Claude Code instance D)
- **Branch**: `feature/autofix-filename-links`
- **Effort**: 5 days
- **Files Modified**:
  - `src/core/auto_fixer.py` (add filename auto-fix)
  - `src/core/link_analyzer.py` (NEW module - find broken links)
  - `tests/test_auto_fixer.py`
  - `tests/test_link_analyzer.py` (NEW tests)
- **Dependencies**: PB-005 (uses preview mode)
- **Merge Conflicts**: ⚠️ MEDIUM (auto_fixer.py touched by PB-005)

**User Story**: As a content contributor, I want auto-fix to rename files AND update all links.

**Acceptance Criteria**:
- [ ] `--auto-fix` detects and renames files with spaces
- [ ] Scans all markdown for links to renamed file
- [ ] Updates internal links automatically
- [ ] Offers `--preserve-history` (use `git mv`)
- [ ] Preview shows impact analysis (3 links would break)

---

### Track B: Performance & UX

#### PB-007: Progress Indicators for Large Scans
- **Status**: 🟡 PROPOSED
- **Priority**: P2 - MEDIUM
- **Developer**: Dev 3 (or Claude Code instance C)
- **Branch**: `feature/progress-indicators`
- **Effort**: 2 days
- **Files Modified**:
  - `src/cli.py` (add progress display)
  - `src/core/change_detector.py` (emit progress events)
  - `tests/test_cli.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ LOW (CLI updates, minimal overlap)

**User Story**: As a documentation manager scanning 100+ docs, I want real-time progress.

**Acceptance Criteria**:
- [ ] Progress bar: `[████████░░] 80/100`
- [ ] Show current document being processed
- [ ] Estimated time remaining
- [ ] Suppress with `--quiet` flag

---

### Sprint 8 Merge Strategy

```
master (Sprint 7 complete)
  ├─ feature/autofix-preview (PB-005) ← MERGE FIRST (parallel track, zero conflicts)
  │   └─ merge → master
  ├─ feature/progress-indicators (PB-007) ← MERGE SECOND (parallel, CLI module)
  │   └─ merge → master
  └─ feature/autofix-filename-links (NEW-002) ← MERGE LAST (depends on PB-005)
      └─ rebase from master
      └─ merge → master
```

**Estimated Merge Time**: 20 minutes (minimal conflicts)

---

## 🔬 SPRINT 9: Reporting Enhancements (Week 4)

**Goal**: Improve report clarity and transparency

### Track A: Report Improvements

#### PB-009: Incremental Scan Status in Reports
- **Status**: 🟡 PROPOSED
- **Priority**: P3 - LOW
- **Developer**: Dev 3 (or Claude Code instance C)
- **Branch**: `feature/incremental-scan-status`
- **Effort**: 1 day
- **Files Modified**:
  - `src/reporting/__init__.py` (add cache stats)
  - `src/utils/cache.py` (track cache hits)
  - `tests/test_reporting.py`
- **Dependencies**: NONE
- **Merge Conflicts**: ⚠️ VERY LOW (reporting module, minimal overlap)

**User Story**: As a QA tester, I want to know if scan was incremental or full.

**Acceptance Criteria**:
- [ ] Report header: "Scan Type: Incremental (3 changed, 7 cached)"
- [ ] Show time saved vs full scan
- [ ] Cache hit rate in verbose mode

---

### Sprint 9 Merge Strategy

```
master (Sprint 8 complete)
  └─ feature/incremental-scan-status (PB-009) ← MERGE (zero conflicts)
      └─ merge → master
```

**Estimated Merge Time**: 5 minutes (zero conflicts)

---

## 📦 BACKLOG (Future Sprints - Advanced Features)

### Advanced Conflict Detection (Requires Manual Intervention)

#### PB-004: Smart Pricing Conflict Detection
- **Priority**: P3 - LOW (ADVANCED - Manual intervention needed)
- **Effort**: 5 days
- **Branch**: `feature/smart-pricing-detection`
- **Files**: `src/core/validators/conflict_detector.py`, `src/utils/config.py`
- **Dependencies**: PB-001, PB-006
- **Conflict Risk**: ⚠️ MEDIUM
- **Note**: Pricing conflicts often require manual review to distinguish pricing tiers from actual conflicts. This is an enhancement to reduce false positives but pricing validation will always need human judgment.

#### PB-006: Cross-Document Conflict Detection
- **Priority**: P3 - LOW (ADVANCED)
- **Effort**: 7 days
- **Branch**: `feature/cross-document-conflicts`
- **Files**: `src/core/validators/conflict_detector.py`, `src/reporting/conflict_reporter.py`
- **Dependencies**: PB-001, PB-004
- **Conflict Risk**: ⚠️ MEDIUM

#### REFINED-004: Enhanced Status Conflict Detection
- **Priority**: P3 - LOW (ADVANCED)
- **Effort**: 2 days
- **Branch**: `feature/enhanced-status-conflicts`
- **Files**: `src/core/validators/conflict_detector.py`, `src/reporting/conflict_reporter.py`
- **Dependencies**: PB-004
- **Conflict Risk**: ⚠️ MEDIUM

---

### Nice-to-Have Features

#### PB-008: HTML Report Output
- **Priority**: P4 - VERY LOW
- **Effort**: 5 days
- **Branch**: `feature/html-reports`
- **Files**: New module `src/reporting/html_reporter.py`
- **Dependencies**: NONE
- **Conflict Risk**: ⚠️ VERY LOW (completely new module)

---

## 🎯 Merge Conflict Mitigation Strategy

### File-Level Isolation Matrix

| File | Sprint 7 | Sprint 8 | Sprint 9 | Conflict Risk |
|------|----------|----------|----------|---------------|
| `src/cli.py` | PB-002, NEW-003 | PB-005 | PB-007 | ⚠️ MEDIUM |
| `src/utils/config.py` | PB-002, NEW-001 | PB-004 | - | ⚠️ MEDIUM |
| `src/core/validators/yaml_validator.py` | NEW-001, PB-003 | - | - | ⚠️ HIGH |
| `src/core/validators/conflict_detector.py` | PB-001 | PB-004, REFINED-004 | PB-006 | ⚠️ HIGH |
| `src/core/auto_fixer.py` | - | PB-005, NEW-002 | - | ⚠️ MEDIUM |
| `src/reporting/__init__.py` | PB-002, PB-003 | PB-005 | PB-009 | ⚠️ MEDIUM |

### Conflict Resolution Guidelines

**HIGH CONFLICT FILES** (`yaml_validator.py`, `conflict_detector.py`):
- ✅ **Solution**: Merge in dependency order (NEW-001 before PB-003, PB-004 before REFINED-004)
- ✅ **Tip**: Use `git rebase master` before creating PR to get latest changes
- ✅ **Review**: Senior dev reviews merge for these files

**MEDIUM CONFLICT FILES** (`cli.py`, `config.py`, `auto_fixer.py`, `reporting`):
- ✅ **Solution**: Stagger merges by 1 day to allow clean rebases
- ✅ **Tip**: Touch different sections of file when possible (e.g., PB-002 adds CLI flag, NEW-003 adds new command)

**LOW CONFLICT FILES** (new modules, isolated modules):
- ✅ **Solution**: Can merge in any order
- ✅ **Tip**: Create new files when possible to avoid conflicts

---

## 🚦 Merge Order Recommendation

### Sprint 7 Merge Order (Day-by-Day)
- **Day 1**: Merge PB-002 (severity filtering) - zero conflicts
- **Day 2**: Merge PB-001 (line numbers), NEW-003 (bulk frontmatter) - zero conflicts
- **Day 3**: Merge NEW-001 (exclusion patterns) - rebase on PB-002 changes
- **Day 4**: Merge PB-003 (frontmatter completeness) - rebase on NEW-001 changes

### Sprint 8 Merge Order (Week-by-Week)
- **Week 1**: Merge PB-005 (auto-fix preview), PB-004 (smart pricing) - parallel tracks
- **Week 2**: Merge REFINED-004 (status conflicts), NEW-002 (filename auto-fix) - rebase on Week 1

### Sprint 9 Merge Order
- **Day 1-2**: Merge PB-007, PB-009 (parallel, no conflicts)
- **Day 3**: Merge PB-006 (cross-doc conflicts) - rebase on Sprint 8 changes

---

## 📋 Developer Assignment Template

When assigning to Claude Code instances or developers, use this template:

```markdown
## Assignment: [Developer Name/Instance]

**Branch**: feature/[feature-name]
**Sprint**: Sprint X
**Estimated Effort**: X days
**Merge Priority**: [1-5] (1 = merge first)

### Your Task
[Copy user story, acceptance criteria from backlog item]

### Files You'll Modify
- src/[module]/[file].py
- tests/test_[module].py

### Dependencies
- ⚠️ Wait for [branch-name] to merge before starting (if applicable)
- ✅ No dependencies, start immediately (if applicable)

### Testing Plan
[Copy testing section from backlog item]

### Merge Instructions
1. Rebase on master: `git rebase origin/master`
2. Run full test suite: `pytest`
3. Create PR with title: "[Sprint X] [Feature Name] (PB-XXX)"
4. Notify team when ready for merge
```

---

## 📊 Progress Tracking

| Sprint | Items Complete | % Complete | Merged? | Release Date |
|--------|---------------|-----------|---------|--------------|
| Sprint 7 | 0/5 | 0% | ❌ | TBD |
| Sprint 8 | 0/4 | 0% | ❌ | TBD |
| Sprint 9 | 0/3 | 0% | ❌ | TBD |

**Overall Progress**: 0/12 items (0%)

---

## 🎯 Success Criteria

**Sprint 7 Success**:
- [ ] All 5 items merged to master
- [ ] Zero merge conflicts (or resolved in <1 hour)
- [ ] All tests passing
- [ ] Re-run on 01-strategy and 02-marketing-brand to validate improvements

**Sprint 8 Success**:
- [ ] All 4 items merged
- [ ] Pricing false positives reduced by 50%
- [ ] Auto-fix adoption increases (users trust preview mode)

**Sprint 9 Success**:
- [ ] All 3 items merged
- [ ] Cross-document conflicts detected in test folders
- [ ] Progress indicators working for 100+ document scans

---

**Document Owner**: Product Manager
**Backlog Type**: Parallel Development Ready
**Status**: READY FOR ASSIGNMENT
**Approval Status**: 🟡 PENDING USER APPROVAL
