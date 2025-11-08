---
title: Product Backlog - Symphony Core v1.0
version: 1.0
last_updated: 2025-11-07
---

# Product Backlog
## Symphony Core v1.0 MVP - Document Validation System

---

## Sprint Overview

| Sprint | Dates | Goal | Status | Points |
|--------|-------|------|--------|--------|
| Sprint 1 | Nov 7-13 | Foundation | ✅ Complete | 8/8 |
| Sprint 2 | Nov 11-15 | YAML Validation + Auto-Fix | ⏳ Next | 13 |
| Sprint 3 | Nov 18-22 | Markdown + Naming + Conflicts | 📋 Planned | 18 |
| Sprint 4 | Nov 25-29 | CLI & Reporting | 📋 Planned | 21 |

**Total v1.0 Effort**: ~52 story points (~125 hours)

---

## Scope Changes Based on User Decisions (2025-11-07)

### Context
Following Pareto principle analysis and scaling SaaS platform requirements, the following scope adjustments were approved. See `DECISIONS.md` for complete architectural decision records.

### Simplifications (ADR-001, ADR-005)

**Required YAML Fields**: Reduced from 5 to 3
- ✅ Keep: `title`, `tags`, `status`
- ❌ Remove: `version`, `date` (now optional)
- Impact: -2 story points in Sprint 2

**Configuration**: Single shared config (no domain overrides)
- Impact: -1 story point in implementation

### Enhancements (ADR-002, ADR-003)

**Conflict Detection**: Moved to v1.0 (was v1.1)
- Pricing conflicts detection
- Policy contradiction detection
- Duplicate SOP detection
- Batch mode for full-corpus comparison
- Impact: +5 story points in Sprint 3

**Auto-Fix with Preview**: Added to v1.0 (was v1.1)
- Auto-fix safe changes (YAML, naming)
- Preview before applying
- Backup originals
- Impact: +2 story points in Sprint 2, +3 in Sprint 4

### Net Change
- Original v1.0: 50 points
- Revised v1.0: 52 points (+2)
- Rationale: Mission-critical features for scaling SaaS platform

---

## Sprint 2: YAML Validation + Auto-Fix (13 points)

### Sprint Goal
Implement YAML frontmatter validation WITH auto-fix capabilities for safe changes.

### User Stories

#### US-2.1: YAML Frontmatter Parser (3 points)
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

**Tasks**:
- [ ] Create `src/utils/frontmatter.py`
- [ ] Implement `parse_frontmatter()` function
- [ ] Implement `add_frontmatter()` function
- [ ] Handle edge cases (empty files, only frontmatter, etc.)
- [ ] Write comprehensive tests
- [ ] Document all functions

**Files to Create**:
- `src/utils/frontmatter.py`
- `tests/utils/test_frontmatter.py`

---

#### US-2.2: YAML Validator Implementation (5 points)
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

**Tasks**:
- [ ] Create `src/core/validators/yaml_validator.py`
- [ ] Implement YAMLValidator class
- [ ] Implement all validation rules (YAML-001 through YAML-006)
- [ ] Add configuration support for rule enabling/disabling
- [ ] Generate clear error messages with suggestions
- [ ] Write comprehensive tests for each rule
- [ ] Test with various document types (pricing, policies, specs)
- [ ] Document the validator

**Files to Create**:
- `src/core/validators/yaml_validator.py`
- `tests/core/validators/test_yaml_validator.py`
- `tests/fixtures/yaml_test_documents/` (test files)

**Validation Rules** (SIMPLIFIED - ADR-001):
| Rule ID | Description |
|---------|-------------|
| YAML-001 | YAML block present |
| YAML-002 | Required fields present (title, tags, status) |
| YAML-003 | Status in allowed list |
| YAML-004 | Tags is a list |

---

#### US-2.3: Auto-Fix Engine (NEW - 5 points) ⭐
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
- Extract title from H1 if missing

**Requires Manual Review**:
- Content modifications
- Changes to existing metadata values
- Heading structure changes
- Link modifications

**Tasks**:
- [ ] Create `src/core/auto_fixer.py`
- [ ] Implement AutoFixer class
- [ ] Auto-add YAML frontmatter
- [ ] Extract title from H1
- [ ] Suggest tags from file path/folder
- [ ] Implement preview mode
- [ ] Create backup mechanism
- [ ] Write comprehensive tests
- [ ] Document auto-fix operations

**Files to Create**:
- `src/core/auto_fixer.py` (~300 lines)
- `tests/core/test_auto_fixer.py` (~200 lines)

**CLI Usage**:
```bash
# Preview auto-fixes without applying
python main.py validate --auto-fix --preview

# Apply auto-fixes
python main.py validate --auto-fix
```

---

## Sprint 3: Markdown + Naming + Conflict Detection (18 points)

### Sprint Goal
Complete validation engine WITH conflict detection for mission-critical scaling.

### User Stories

#### US-3.1: Markdown Syntax Validator (5 points)
**Priority**: P0

**As a** documentation manager
**I want** markdown syntax validated
**So that** all documents follow consistent formatting standards

**Acceptance Criteria**:
- [ ] Validates heading hierarchy (no skipped levels)
- [ ] Checks code block language specifications
- [ ] Validates link formats (relative paths for internal docs)
- [ ] Checks horizontal rule format (---)
- [ ] Validates list formatting
- [ ] Detects trailing whitespace
- [ ] Configurable rules (enable/disable individual checks)
- [ ] Clear error messages with line numbers

**Tasks**:
- [ ] Create `src/core/validators/markdown_validator.py`
- [ ] Implement MarkdownValidator class
- [ ] Parse markdown with markdown-it-py
- [ ] Implement all validation rules (MD-001 through MD-008)
- [ ] Add configuration support
- [ ] Write comprehensive tests
- [ ] Test with various markdown structures
- [ ] Document the validator

**Files to Create**:
- `src/core/validators/markdown_validator.py`
- `tests/core/validators/test_markdown_validator.py`
- `tests/fixtures/markdown_test_documents/`

---

#### US-3.2: Naming Convention Validator (3 points)
**Priority**: P0

**As a** documentation manager
**I want** file naming conventions enforced
**So that** all files follow our standards automatically

**Acceptance Criteria**:
- [ ] Validates lowercase-with-hyphens pattern
- [ ] Checks maximum length (configurable, default 50)
- [ ] Detects version numbers in filename
- [ ] Validates minimum length (descriptive names)
- [ ] Suggests corrected filenames
- [ ] Configurable strictness levels

**Tasks**:
- [ ] Create `src/core/validators/naming_validator.py`
- [ ] Implement NamingValidator class
- [ ] Implement all validation rules (NAME-001 through NAME-005)
- [ ] Generate filename suggestions
- [ ] Write comprehensive tests
- [ ] Document the validator

**Files to Create**:
- `src/core/validators/naming_validator.py`
- `tests/core/validators/test_naming_validator.py`

---

#### US-3.3: Conflict Detection Engine (NEW - 10 points) ⭐
**Priority**: P0 - MISSION CRITICAL

**As an** operations manager
**I want** pricing and policy conflicts detected automatically
**So that** we avoid contradictory information across documents

**Acceptance Criteria**:
- [ ] Detects pricing conflicts across documents (same product, different prices)
- [ ] Identifies policy contradictions (conflicting statements)
- [ ] Finds duplicate SOPs (>80% content similarity)
- [ ] Batch mode validates ALL docs (not just changed - ADR-006)
- [ ] Severity classification (CRITICAL, HIGH, MEDIUM, LOW)
- [ ] Generates conflict report with document references and line numbers
- [ ] Tag-based filtering support (e.g., `--tags pricing`)
- [ ] Integration with main validation workflow

**Conflict Types** (ADR-002):

**1. Pricing Conflicts**:
- Same product with different prices
- Conflicting discount policies
- Currency inconsistencies
- Effective date mismatches

**2. Policy Contradictions**:
- Conflicting refund policies
- Contradictory terms of service
- Misaligned SLAs
- Contact information discrepancies

**3. Duplicate SOPs**:
- Multiple documents describing same process
- Content similarity threshold >80%
- Recommendation to consolidate

**Batch Processing Mode** (ADR-006):
- Always processes FULL document corpus for conflicts
- Not limited to changed files
- Accuracy > Speed
- Tag-based filtering reduces scope when needed

**Tasks**:
- [ ] Create `src/core/conflict_detector.py`
- [ ] Implement ConflictDetector class
- [ ] Create semantic analyzer for content comparison
- [ ] Implement pricing conflict detection
- [ ] Implement policy contradiction detection
- [ ] Implement duplicate SOP detection (similarity algorithm)
- [ ] Add severity classification logic
- [ ] Implement batch mode (all-document processing)
- [ ] Add tag-based filtering
- [ ] Write comprehensive tests
- [ ] Create conflict test fixtures
- [ ] Document conflict detection rules

**Files to Create**:
- `src/core/conflict_detector.py` (~400 lines)
- `src/core/semantic_analyzer.py` (~300 lines)
- `tests/core/test_conflict_detector.py` (~300 lines)
- `tests/fixtures/conflict_test_documents/` (test files with conflicts)

**Severity Levels**:
| Severity | Example | Action Required |
|----------|---------|-----------------|
| CRITICAL | Pricing mismatch for same product | Immediate fix |
| HIGH | Policy contradiction | Fix before release |
| MEDIUM | Duplicate SOP | Consolidate when possible |
| LOW | Minor inconsistencies | Review and update |

---

## Sprint 4: CLI & Reporting (21 points)

### Sprint Goal
Complete MVP with CLI, conflict reporting, auto-fix preview, and documentation.

### User Stories

#### US-4.1: Validator Engine Integration (5 points)
**Priority**: P0

**As a** developer
**I want** an orchestrator to coordinate all validators
**So that** documents are validated completely

**Acceptance Criteria**:
- [ ] Integrates YAML, Markdown, Naming, and **Conflict validators**
- [ ] Processes documents through all validators
- [ ] Batch mode for conflict detection (all documents)
- [ ] Aggregates results into ValidationResult objects
- [ ] Updates cache with validation status
- [ ] Handles errors gracefully

**Tasks**:
- [ ] Create `src/core/validator_engine.py`
- [ ] Implement ValidatorEngine class
- [ ] Integrate all three validators
- [ ] Add error handling
- [ ] Write integration tests
- [ ] Document the engine

**Files to Create**:
- `src/core/validator_engine.py`
- `tests/core/test_validator_engine.py`

---

#### US-4.2: Report Generator (5 points)
**Priority**: P0

**As a** documentation manager
**I want** comprehensive validation and conflict reports
**So that** I can quickly understand and fix issues

**Acceptance Criteria**:
- [ ] Generates markdown format reports
- [ ] Shows summary statistics
- [ ] Groups issues by file and validator
- [ ] **Conflict report section with severity levels**
- [ ] Includes line numbers and suggestions
- [ ] Exports to configured directory
- [ ] Optional JSON format

**Tasks**:
- [ ] Create `src/core/report_generator.py`
- [ ] Implement ReportGenerator class
- [ ] Create markdown report template
- [ ] Add JSON export option
- [ ] Write tests for report generation
- [ ] Document the generator

**Files to Create**:
- `src/core/report_generator.py`
- `tests/core/test_report_generator.py`

---

#### US-4.3: CLI Interface (8 points)
**Priority**: P0

**As a** user
**I want** a practical CLI interface with essential options
**So that** I can validate docs by domain, auto-fix issues, and detect conflicts

**Acceptance Criteria** (ADR-004):
- [ ] Click-based CLI with clear commands
- [ ] `validate` command with options
- [ ] `--path` flag for folder/domain-specific validation
- [ ] `--tags` flag for tag-based validation (e.g., `--tags pricing`)
- [ ] `--force` flag to ignore cache
- [ ] **`--auto-fix` flag with `--preview` option**
- [ ] **`--conflicts` flag for conflict-only detection**
- [ ] Progress indicators for batch operations
- [ ] Proper exit codes (0=success, 1=failures)
- [ ] Help text for all commands

**CLI Commands** (ADR-004):
```bash
python main.py validate                    # All docs
python main.py validate --path operations/ # Specific folder
python main.py validate --tags pricing     # By tag
python main.py validate --force            # Ignore cache
python main.py validate --auto-fix --preview  # Preview auto-fixes
python main.py validate --conflicts        # Conflict detection only
```

**Tasks**:
- [ ] Create `src/cli.py`
- [ ] Implement Click command structure
- [ ] Add all command flags and options
- [ ] Integrate with ValidatorEngine
- [ ] Add progress indicators
- [ ] Write CLI tests
- [ ] Document CLI usage

**Files to Create**:
- `src/cli.py`
- `src/main.py` (entry point)
- `tests/test_cli.py`

---

#### US-4.4: Documentation & Testing (3 points)
**Priority**: P0

**As a** team lead
**I want** comprehensive documentation and tests
**So that** new users can use the system and contributors can maintain it

**Acceptance Criteria**:
- [ ] README updated for v1.0 release
- [ ] User guide complete
- [ ] All docstrings present
- [ ] Test coverage > 80%
- [ ] Integration tests passing
- [ ] CI/CD setup (optional)

**Tasks**:
- [ ] Update README for v1.0
- [ ] Complete user guide
- [ ] Run coverage report and fill gaps
- [ ] Write end-to-end integration tests
- [ ] Add usage examples
- [ ] Create troubleshooting guide

**Files to Update**:
- `README.md`
- `docs/user-guide.md`
- Various test files

---

## Icebox (Future Releases)

### v1.1 Features
- US-5.1: Intelligent document routing (8 points)
- US-5.2: Automated tagging system (8 points)
- US-5.3: Basic conflict detection (13 points)
- US-5.4: Auto-fix capabilities (8 points)
- US-5.5: Batch processing optimization (5 points)

### v2.0 Features
- US-6.1: Semantic conflict detection (13 points)
- US-6.2: FAQ generation (13 points)
- US-6.3: Workflow automation (8 points)
- US-6.4: Content suggestions (8 points)

---

## Definition of Done (All Sprints)

A story is considered done when:

- [ ] All acceptance criteria met
- [ ] Code follows PEP 8 style
- [ ] All functions have docstrings
- [ ] Type hints on all function signatures
- [ ] Unit tests written and passing
- [ ] Integration tests written (if applicable)
- [ ] Test coverage > 80% for new code
- [ ] Code reviewed (self or peer)
- [ ] Documentation updated
- [ ] No critical bugs or blockers
- [ ] Committed to main branch

---

## Velocity Tracking

| Sprint | Points Committed | Points Completed | Velocity |
|--------|-----------------|------------------|----------|
| Sprint 1 | 8 | 8 | 8 |
| Sprint 2 | 11 | TBD | TBD |
| Sprint 3 | 13 | TBD | TBD |
| Sprint 4 | 18 | TBD | TBD |

**Average Velocity** (so far): 8 points/sprint

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Underestimated complexity of markdown parsing | Medium | High | Allow buffer time, simplify validation rules if needed |
| Test coverage falls below 80% | Low | Medium | Write tests alongside code (TDD) |
| Sprint 4 overcommitted (18 points) | Medium | Medium | Can defer non-critical features to v1.1 |
| Validation rules too strict | Low | Medium | Make rules configurable, allow disabling |
| Performance issues with 100+ docs | Low | Low | Optimize in v1.1 if needed |

---

## Notes

- Sprint 1 completed successfully with 100% velocity
- Sprint 2 focuses on YAML validation (foundation for all validation)
- Sprint 3 adds markdown and naming validation (complete validation system)
- Sprint 4 ties everything together with CLI and polish
- Total estimated effort: ~50 story points (~120 hours for 2-3 people)

---

**Last Updated**: 2025-11-07
**Maintained By**: Engineering Team
**Status**: Active - Sprint 1 Complete, Sprint 2 Starting
