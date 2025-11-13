# Merge Conflict Mitigation Strategy for Parallel Development

**Version**: 1.0
**Date**: 2025-11-13
**Audience**: Developers, Claude Code for Cloud instances, DevOps

---

## 🎯 Goal

Enable **3-5 developers** (or Claude Code instances) to work in parallel on Symphony Core v1.1 features with **<5% merge conflict rate** and **<1 hour conflict resolution time**.

---

## 📐 Architecture: Module Isolation Strategy

Symphony Core is structured with **clear module boundaries** that enable parallel development:

```
src/
├── cli.py                    # CLI interface (Track C)
├── core/
│   ├── validators/
│   │   ├── yaml_validator.py       # YAML validation (Track B)
│   │   ├── naming_validator.py     # Naming validation (Track B)
│   │   ├── markdown_validator.py   # Markdown validation (Track B)
│   │   └── conflict_detector.py    # Conflict detection (Track A)
│   ├── auto_fixer.py               # Auto-fix logic (Track D)
│   └── frontmatter_manager.py      # NEW: Frontmatter ops (Track C)
├── reporting/
│   ├── __init__.py                 # Report orchestration (Track A)
│   ├── console_reporter.py
│   ├── markdown_reporter.py
│   └── conflict_reporter.py        # Conflict reports (Track A)
└── utils/
    ├── config.py                   # Configuration (SHARED - HIGH RISK)
    ├── logger.py
    └── cache.py                    # Cache management (Track E)
```

### Module Ownership by Track

| Track | Module | Conflict Risk | Notes |
|-------|--------|---------------|-------|
| **Track A** | Reporting & Conflicts | ⚠️ MEDIUM | Multiple features touch reporting |
| **Track B** | Validation | ⚠️ HIGH | yaml_validator touched by 2 features |
| **Track C** | CLI & New Commands | ⚠️ LOW | New commands = new code paths |
| **Track D** | Auto-Fix | ⚠️ MEDIUM | 2 features in Sprint 8 |
| **Track E** | Performance & Utilities | ⚠️ LOW | Isolated improvements |

---

## 🚦 Branching Strategy: Ordered Merges

### Model: **Sequential Merge with Parallel Development**

```
master (v1.0.0)
  │
  ├──────────────────── SPRINT 7 (Week 1) ─────────────────────┐
  │                                                              │
  ├─ [P1] feature/severity-filtering        (Dev 1) ⚠️ LOW     │
  │     └─ MERGE: End of Day 1 → master                        │
  │                                                              │
  ├─ [P2] feature/conflict-line-numbers     (Dev 2) ⚠️ LOW     │
  │     └─ MERGE: End of Day 2 → master                        │
  │                                                              │
  ├─ [P2] feature/bulk-frontmatter-add      (Dev 3) ⚠️ VERY LOW│
  │     └─ MERGE: End of Day 2 → master                        │
  │                                                              │
  ├─ [P3] feature/exclude-patterns          (Dev 4) ⚠️ MEDIUM  │
  │     └─ Rebase from master (get severity-filtering changes) │
  │     └─ MERGE: End of Day 3 → master                        │
  │                                                              │
  ├─ [P4] feature/frontmatter-completeness  (Dev 5) ⚠️ HIGH    │
  │     └─ Rebase from master (get exclude-patterns changes)   │
  │     └─ MERGE: End of Day 4 → master                        │
  │                                                              │
  └───────────────────────────────────────────────────────────┘
        │
        ├─ Sprint 7 complete → v1.1.0-alpha1 tag
        │
  ├──────────────────── SPRINT 8 (Week 2-3) ───────────────────┐
  ...
```

### Key Principles

1. **Merge Priority = Dependency Order + Risk Level**
   - Low-risk, no-dependency items merge first
   - High-risk, dependent items merge last (after rebasing)

2. **Daily Merge Windows**
   - End of day merges (5pm UTC)
   - All devs rebase at start of next day (9am UTC)

3. **Rebase Before PR**
   - Each dev rebases on master before creating PR
   - CI/CD runs full test suite on rebased branch

4. **Fast-Forward Merges Preferred**
   - Use `git rebase master` (not `git merge master`)
   - Keep linear history for easier conflict tracing

---

## 🔥 High-Conflict Files: Special Handling

### `src/utils/config.py` (SHARED RESOURCE)

**Why High Risk**: 3 features in Sprint 7 touch this file

**Mitigation Strategy**:

```python
# GOOD: Each feature adds to DIFFERENT sections
class Config:
    def __init__(self):
        # Sprint 7 - Feature 1 (PB-002): Add reporting config
        self.reporting_min_severity = self._load_reporting_severity()

        # Sprint 7 - Feature 2 (NEW-001): Add validation exclusions
        self.validation_exclusions = self._load_validation_exclusions()

    # Each feature gets its own private method
    def _load_reporting_severity(self):
        # PB-002 code here

    def _load_validation_exclusions(self):
        # NEW-001 code here
```

**Merge Order**:
1. PB-002 (severity filtering) merges first
2. NEW-001 (exclusions) rebases and merges
3. Clean separation = minimal conflicts

**Conflict Resolution Time**: <15 minutes

---

### `src/core/validators/yaml_validator.py` (HIGH RISK)

**Why High Risk**: 2 features in Sprint 7 modify this file (NEW-001, PB-003)

**Mitigation Strategy**:

```python
class YAMLValidator:
    def validate(self, file_path):
        # Feature 1 (NEW-001): Check exclusions FIRST
        if self._is_excluded(file_path):
            return ValidationResult(skipped=True)

        # Feature 2 (PB-003): Check frontmatter existence
        if not self._has_frontmatter(file_path):
            return ValidationResult(error="Missing frontmatter")

        # Existing validation logic (untouched by both features)
        frontmatter = self._parse_frontmatter(file_path)
        return self._validate_schema(frontmatter)

    # NEW-001: New method
    def _is_excluded(self, file_path):
        # Exclusion logic

    # PB-003: New method
    def _has_frontmatter(self, file_path):
        # Frontmatter detection logic
```

**Merge Order**:
1. NEW-001 merges first (exclusion check)
2. PB-003 rebases on master (gets exclusion logic)
3. PB-003 adds frontmatter detection AFTER exclusion check
4. Both features insert at different points in call stack

**Conflict Resolution Time**: <20 minutes

---

### `src/core/validators/conflict_detector.py` (HIGH RISK - Sprint 8 & 9)

**Why High Risk**: Touched in Sprint 7 (PB-001), Sprint 8 (PB-004, REFINED-004), Sprint 9 (PB-006)

**Mitigation Strategy**:

```python
class ConflictDetector:
    def detect_conflicts(self, documents):
        conflicts = []

        # Sprint 7 (PB-001): Add line number tracking
        conflicts.extend(self._detect_pricing_conflicts_with_lines(documents))

        # Sprint 8 (PB-004): Smart pricing detection
        if self.config.smart_mode:
            conflicts = self._filter_tier_pricing(conflicts)

        # Sprint 8 (REFINED-004): Separate status validation from conflicts
        status_conflicts = self._detect_cross_doc_status_conflicts(documents)
        conflicts.extend(status_conflicts)

        # Sprint 9 (PB-006): Cross-document comparison
        if self.config.cross_document_enabled:
            conflicts.extend(self._detect_cross_document_conflicts(documents))

        return conflicts
```

**Merge Order**:
- **Sprint 7**: PB-001 merges
- **Sprint 8**:
  1. PB-004 rebases on Sprint 7, merges
  2. REFINED-004 rebases on PB-004, merges (waits 1 day)
- **Sprint 9**: PB-006 rebases on Sprint 8 changes

**Conflict Resolution Time**: <30 minutes per sprint

---

## 📋 Pre-Merge Checklist (For Each Developer)

Before creating a PR, developers MUST complete:

### 1. Rebase on Latest Master
```bash
git checkout master
git pull origin master
git checkout feature/your-feature
git rebase master

# If conflicts occur:
# 1. Resolve conflicts
# 2. git add .
# 3. git rebase --continue
# 4. Test again after rebase
```

### 2. Run Full Test Suite
```bash
pytest tests/ --cov=src --cov-report=term-missing
# Must pass with 80%+ coverage
```

### 3. Run Linter & Formatter
```bash
flake8 src/ tests/
black src/ tests/ --check
mypy src/
```

### 4. Test on Real Data
```bash
# Test on 01-strategy folder
python -m src.cli validate --path "C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\01-strategy"

# Verify your feature works as expected
```

### 5. Create PR with Template
```markdown
## [Sprint X] Feature Name (PB-XXX)

### Summary
[One-sentence description]

### Changes
- [ ] Modified: src/[file].py (added [feature])
- [ ] Added: tests/test_[module].py (100% coverage)
- [ ] Updated: config/config.yaml (new option: [option])

### Testing
- [x] Unit tests passing (pytest)
- [x] Integration test on 01-strategy folder
- [x] Linting passing (flake8, black, mypy)
- [x] Rebased on latest master

### Dependencies
- ⚠️ Depends on: feature/[dependency] (merged ✅ / pending ❌)
- ⚠️ Blocks: feature/[blocked-feature]

### Merge Priority
[P1-P5] - Merge by [date]

### Conflict Risk
⚠️ [LOW/MEDIUM/HIGH]
Files with potential conflicts:
- src/[file].py (also touched by [other-feature])

### Reviewer Notes
[Special instructions for reviewer]
```

---

## 🔄 Merge Process (For Merge Masters)

### Role: Merge Master (Rotates Daily)

**Responsibilities**:
1. Review PRs in priority order
2. Merge branches in dependency order
3. Monitor CI/CD pipeline
4. Communicate merge status to team

### Daily Merge Workflow

#### Morning (9am UTC): Rebase Window
- All devs rebase on latest master
- No merges during this time (avoid moving target)

#### Afternoon (2pm UTC): PR Review
- Merge Master reviews all PRs
- Marks PRs as "Ready to Merge" in priority order

#### Evening (5pm UTC): Merge Window
- Merge branches in order:
  1. P1 (zero dependencies)
  2. P2 (depends on P1)
  3. P3 (depends on P2)
  4. ...

#### Post-Merge (6pm UTC): Verification
- Run full test suite on master
- Tag release if sprint complete (e.g., v1.1.0-alpha1)
- Notify team: "Master updated, rebase tomorrow morning"

---

## 🛠️ Conflict Resolution Guide

### When Conflicts Occur During Rebase

#### Step 1: Understand the Conflict
```bash
git status
# Shows conflicting files

git diff
# Shows conflict markers
```

#### Step 2: Review Upstream Changes
```bash
git log origin/master --oneline --graph
# See what was merged since you branched
```

#### Step 3: Resolve Conflict

**Scenario A: Different sections of file**
```python
# YOUR BRANCH (feature/severity-filtering):
def generate_report(self, violations):
    # Added: Filter by severity
<<<<<<< HEAD (your changes)
    filtered = self._filter_by_severity(violations)
    return self._format_report(filtered)
=======
    # MASTER (feature/conflict-line-numbers merged):
    violations_with_lines = self._add_line_numbers(violations)
    return self._format_report(violations_with_lines)
>>>>>>> master

# RESOLUTION: Keep both changes
def generate_report(self, violations):
    # Filter by severity
    filtered = self._filter_by_severity(violations)
    # Add line numbers
    filtered_with_lines = self._add_line_numbers(filtered)
    return self._format_report(filtered_with_lines)
```

**Scenario B: Same section (rare with good planning)**
- Consult with other developer
- Determine correct order of operations
- Test thoroughly after resolution

#### Step 4: Test After Resolution
```bash
git add src/[resolved-file].py
git rebase --continue
pytest tests/test_[module].py
```

#### Step 5: Force Push (if already pushed)
```bash
git push origin feature/your-feature --force-with-lease
# --force-with-lease prevents overwriting others' work
```

---

## 📊 Conflict Tracking Dashboard

Track conflicts per sprint to improve planning:

| Sprint | Merges | Conflicts | Resolution Time | Notes |
|--------|--------|-----------|-----------------|-------|
| Sprint 7 | 0/5 | 0 | - | Not started |
| Sprint 8 | 0/4 | 0 | - | Not started |
| Sprint 9 | 0/3 | 0 | - | Not started |

**Target**: <5% conflict rate, <1 hour resolution time

---

## 🎯 Success Metrics

### Sprint 7 Target
- [ ] 5/5 branches merged
- [ ] 0-1 conflicts total
- [ ] <30 minutes total conflict resolution time
- [ ] All tests passing on master after each merge

### Overall Project Target
- [ ] 12/12 features merged across 3 sprints
- [ ] <3 conflicts total (25% conflict rate per merge = 0.25 * 12 = 3)
- [ ] <2 hours total conflict resolution time
- [ ] Zero bugs introduced by merge conflicts

---

## 🚨 Escalation Path

### Minor Conflict (<15 min resolution)
- Developer resolves independently
- Posts resolution in PR comments

### Medium Conflict (15-60 min resolution)
- Developer consults with Merge Master
- Pair programming session if needed

### Major Conflict (>60 min resolution)
- Escalate to team lead
- Consider re-architecting conflicting features
- May require backing out a merge

---

## 📚 Resources

### Git Commands Cheat Sheet
```bash
# Rebase on master
git rebase origin/master

# Abort rebase if stuck
git rebase --abort

# Continue after resolving conflicts
git add .
git rebase --continue

# Force push after rebase
git push origin feature/branch --force-with-lease

# View conflict history
git log --merge --oneline
```

### Testing After Merge
```bash
# Run specific module tests
pytest tests/test_config.py -v

# Run integration tests
pytest tests/integration/ -v

# Run on real data
python -m src.cli validate --path 01-strategy
```

---

## 📞 Communication Protocol

### Merge Notifications (Slack/Discord)
```
🚀 MERGED: feature/severity-filtering (PB-002)
👤 Developer: Dev 1
📦 Commit: abc123
⏰ Time: 2025-11-13 17:00 UTC
⚠️  ACTION REQUIRED: All devs rebase tomorrow morning

Files changed:
- src/cli.py
- src/utils/config.py
- src/reporting/__init__.py
```

### Conflict Alerts
```
⚠️  CONFLICT DETECTED: feature/frontmatter-completeness
📁 File: src/core/validators/yaml_validator.py
🔀 Conflicting with: feature/exclude-patterns (merged 2 hours ago)
👤 Assigned: Dev 5
🕐 ETA: 20 minutes

Status: In Progress | Resolved | Escalated
```

---

## ✅ Checklist for Merge Master

Daily checklist for Merge Master role:

### Morning
- [ ] Check all PRs for "Ready to Merge" label
- [ ] Verify all devs have rebased on latest master
- [ ] Review CI/CD pipeline status

### Afternoon
- [ ] Code review PRs in priority order
- [ ] Request changes if pre-merge checklist not complete
- [ ] Mark approved PRs with priority labels (P1, P2, ...)

### Evening
- [ ] Merge P1 branches first
- [ ] Wait for CI/CD green before merging P2
- [ ] Continue in priority order
- [ ] Run full test suite on master after all merges
- [ ] Tag release if sprint complete
- [ ] Post merge notifications to team

---

**Document Owner**: DevOps / Merge Master
**Version**: 1.0
**Last Updated**: 2025-11-13
**Status**: READY FOR USE
