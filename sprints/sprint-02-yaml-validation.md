---
title: Sprint 2 - YAML Validation + Auto-Fix
sprint_number: 2
duration: November 11-15, 2025
status: ready
team_size: 1 (Claude Code)
story_points_committed: 13
story_points_completed: 0
---

# Sprint 2: YAML Validation + Auto-Fix
## November 11-15, 2025

---

## Sprint Goal

Build YAML frontmatter validation WITH auto-fix capabilities for safe changes.

**Key Deliverables**:
- YAML frontmatter parser
- Validator for 3 required fields (title, tags, status - ADR-001)
- Auto-fix engine with preview (ADR-003)
- Backup mechanism before modifications

**Success Criteria**:
- All 13 story points completed
- Tests passing with >80% coverage
- Ready for Sprint 3 (Markdown + Naming + Conflicts)

---

## Committed User Stories (13 points)

### US-2.1: YAML Frontmatter Parser (3 points)
**Status**: ⏳ NOT STARTED
**Priority**: P0

**As a** developer
**I want** a YAML frontmatter parser
**So that** I can extract and validate metadata from markdown files

**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from markdown files
- [ ] Handles missing frontmatter gracefully
- [ ] Preserves existing frontmatter when reading
- [ ] Can add frontmatter to files without it
- [ ] Handles malformed YAML with clear errors
- [ ] Works with both `---` delimiters

**Implementation Checklist**:
- [ ] Create `src/utils/frontmatter.py`
- [ ] Implement `parse_frontmatter(file_path: Path) -> Dict[str, Any]`
- [ ] Implement `add_frontmatter(file_path: Path, metadata: Dict) -> None`
- [ ] Implement `has_frontmatter(file_path: Path) -> bool`
- [ ] Handle edge cases (empty files, only frontmatter, malformed YAML)
- [ ] Write comprehensive tests (`tests/utils/test_frontmatter.py`)
- [ ] Document all functions with docstrings

**Files to Create**:
- `src/utils/frontmatter.py` (~200 lines)
- `tests/utils/test_frontmatter.py` (~150 lines)

---

### US-2.2: YAML Validator Implementation (5 points)
**Status**: ⏳ NOT STARTED
**Priority**: P0

**As a** documentation manager
**I want** YAML frontmatter validated against standards
**So that** all documents have correct and complete metadata

**Acceptance Criteria**:
- [ ] Validates required fields: **title, tags, status** (3 fields only - ADR-001)
- [ ] Validates status from allowed list
- [ ] Validates tags is a list (not a string)
- [ ] Generates ValidationIssue objects with line numbers
- [ ] Clear error messages with suggestions

**Validation Rules** (SIMPLIFIED):
| Rule ID | Description | Severity |
|---------|-------------|----------|
| YAML-001 | YAML block present | ERROR |
| YAML-002 | Required fields present (title, tags, status) | ERROR |
| YAML-003 | Status in allowed list | ERROR |
| YAML-004 | Tags is a list | ERROR |

**Implementation Checklist**:
- [ ] Create `src/core/validators/yaml_validator.py`
- [ ] Implement YAMLValidator class
- [ ] Implement YAML-001: YAML block present check
- [ ] Implement YAML-002: Required fields check (title, tags, status)
- [ ] Implement YAML-003: Status value validation
- [ ] Implement YAML-004: Tags is list validation
- [ ] Generate ValidationIssue objects
- [ ] Add configuration support for rule enabling/disabling
- [ ] Write comprehensive tests for each rule
- [ ] Create test fixtures with valid/invalid YAML
- [ ] Document the validator

**Files to Create**:
- `src/core/validators/yaml_validator.py` (~250 lines)
- `tests/core/validators/test_yaml_validator.py` (~200 lines)
- `tests/fixtures/yaml_test_documents/` (10+ test files)

---

### US-2.3: Auto-Fix Engine (5 points) ⭐ NEW
**Status**: ⏳ NOT STARTED
**Priority**: P0

**As a** documentation manager
**I want** safe changes auto-fixed with preview
**So that** I can scale documentation without manual bottlenecks

**Acceptance Criteria**:
- [ ] Auto-add missing YAML frontmatter to files
- [ ] Auto-populate title from markdown H1 heading
- [ ] Suggest tags based on file path/content
- [ ] Default status to 'draft' for new documents
- [ ] Preview all changes before applying (--preview flag)
- [ ] Backup original file before modifications
- [ ] Generate auto-fix report showing all changes made

**Safe Auto-Fix Operations** (ADR-003):
- Add missing YAML block
- Add missing required fields (title, tags, status)
- Fix field name typos (e.g., `Title` → `title`)
- Standardize tag format (string → list)
- Extract title from first H1 heading

**Requires Manual Review**:
- Content modifications
- Changes to existing metadata values
- Heading structure changes
- Link modifications

**Implementation Checklist**:
- [ ] Create `src/core/auto_fixer.py`
- [ ] Implement AutoFixer class
- [ ] Implement `fix_document(file_path, issues, preview=True)`
- [ ] Auto-add missing YAML frontmatter
- [ ] Extract title from H1 (`# Title` → `title: Title`)
- [ ] Suggest tags from file path (e.g., `pricing/` → `[pricing]`)
- [ ] Implement preview mode (dry-run, show changes without applying)
- [ ] Create backup mechanism (`_meta/.backups/`)
- [ ] Generate AutoFixResult objects
- [ ] Write comprehensive tests
- [ ] Test backup/rollback functionality
- [ ] Document auto-fix operations

**Files to Create**:
- `src/core/auto_fixer.py` (~300 lines)
- `tests/core/test_auto_fixer.py` (~200 lines)

**CLI Usage Example**:
```bash
# Preview auto-fixes without applying
python main.py validate --auto-fix --preview

# Apply auto-fixes
python main.py validate --auto-fix
```

---

## Sprint Board

```
┌─────────────┬──────────────┬──────────────┬──────────┐
│   TO DO     │  IN PROGRESS │   TESTING    │   DONE   │
├─────────────┼──────────────┼──────────────┼──────────┤
│ US-2.1      │              │              │          │
│ (3 pts)     │              │              │          │
│             │              │              │          │
│ US-2.2      │              │              │          │
│ (5 pts)     │              │              │          │
│             │              │              │          │
│ US-2.3      │              │              │          │
│ (5 pts)     │              │              │          │
└─────────────┴──────────────┴──────────────┴──────────┘
```

**Total Points**: 13
**Completed**: 0
**Remaining**: 13

---

## Daily Progress Log

### Day 1: [Date TBD]
**Planned**: Start US-2.1 (YAML Parser)
**Actual**:
**Blockers**:
**Next**:

### Day 2: [Date TBD]
**Planned**: Complete US-2.1, start US-2.2 (YAML Validator)
**Actual**:
**Blockers**:
**Next**:

### Day 3: [Date TBD]
**Planned**: Complete US-2.2, start US-2.3 (Auto-Fix)
**Actual**:
**Blockers**:
**Next**:

### Day 4: [Date TBD]
**Planned**: Complete US-2.3
**Actual**:
**Blockers**:
**Next**:

### Day 5: [Date TBD]
**Planned**: Testing, bug fixes, documentation
**Actual**:
**Blockers**:
**Next**:

---

## Definition of Done

Sprint 2 is complete when:

**Code Quality**:
- [ ] All 3 user stories completed
- [ ] All acceptance criteria met
- [ ] Code follows PEP 8 style
- [ ] All functions have docstrings (purpose, params, returns)
- [ ] Type hints on all function signatures

**Testing**:
- [ ] Tests written and passing for all stories
- [ ] Test coverage > 80% for new code
- [ ] Integration tests pass
- [ ] Edge cases tested

**Documentation**:
- [ ] README.md updated with Sprint 2 progress
- [ ] User guide updated with auto-fix examples
- [ ] All code documented

**Quality Gates**:
- [ ] No critical bugs
- [ ] Committed to main branch
- [ ] Sprint retrospective completed

---

## Continuity Notes

### If This Sprint Is Interrupted

**To preserve state**:
1. Update this file with current progress
2. Mark user stories as `in_progress` or `completed` in Sprint Board
3. Document last completed file in Daily Progress Log
4. Note any architectural decisions made during sprint in `DECISIONS.md`
5. Commit all work to preserve state
6. Update `BACKLOG.md` story point completion

**What to document**:
- Last function/class completed
- Any deviations from planned approach
- Blockers encountered
- Tests written vs. tests pending

### To Resume Sprint 2

**Starting fresh**:
1. Read this file for current status
2. Check Sprint Board for what's in TO DO vs. DONE
3. Review `DECISIONS.md` for architectural context (especially ADR-001, ADR-003)
4. Review `BACKLOG.md` for full acceptance criteria
5. Continue from last unchecked item in Implementation Checklist

**Context needed**:
- ADR-001: Only 3 required YAML fields (title, tags, status)
- ADR-003: Auto-fix hybrid approach (safe changes only, preview mode)
- Sprint 1 complete: Config, cache, logging, change detection available

**Dependencies**:
- Uses `Config` from `src/utils/config.py` (Sprint 1)
- Uses `Logger` from `src/utils/logger.py` (Sprint 1)
- Uses `DocumentCache` from `src/utils/cache.py` (Sprint 1)

---

## Files Created This Sprint

### Source Code (Target: ~750 lines)
- `src/utils/frontmatter.py` (~200 lines)
- `src/core/validators/yaml_validator.py` (~250 lines)
- `src/core/auto_fixer.py` (~300 lines)

### Tests (Target: ~550 lines)
- `tests/utils/test_frontmatter.py` (~150 lines)
- `tests/core/validators/test_yaml_validator.py` (~200 lines)
- `tests/core/test_auto_fixer.py` (~200 lines)

### Test Fixtures
- `tests/fixtures/yaml_test_documents/` (10+ test markdown files)

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Auto-fix corrupts existing docs | Low | High | Backup mechanism, preview mode, comprehensive tests |
| Tag suggestion accuracy low | Medium | Low | Start simple (file path only), enhance in v1.1 |
| YAML parsing edge cases | Medium | Medium | Comprehensive test fixtures, handle errors gracefully |
| Test coverage below 80% | Low | Medium | Write tests alongside code (TDD approach) |

---

## Success Metrics

**After Sprint 2, we should be able to**:
- ✅ Parse YAML frontmatter from any markdown file
- ✅ Validate documents against 3 required fields
- ✅ Auto-add missing YAML frontmatter with preview
- ✅ Extract title from H1 heading
- ✅ Suggest tags from file path
- ✅ Backup documents before modification
- ✅ Run tests with >80% coverage

**Ready for Sprint 3**:
- Foundation for Markdown/Naming validators
- Auto-fix pattern established for other validators
- Validation framework ready for conflict detection

---

**Sprint Status**: ⏳ READY TO START
**Last Updated**: 2025-11-07
**Next Update**: When Sprint 2 begins
**Maintainer**: Engineering Team
