# START HERE - Sprint 3 Execution Guide

**Last Updated**: 2025-11-08
**Current Status**: Sprint 1-2 Complete, Sprint 3 Ready to Execute
**Repository**: https://github.com/score-ra/sc-doc-mgmt-workflow.git

---

## Quick Context

**Project**: Symphony Core Document Management Workflow
**Purpose**: Automated validation system for business operations documentation (pricing, policies, SOPs, specs)
**Use Case**: Scaling SaaS platform with multiple contributors and expanding business domains
**Mission Critical**: Conflict detection to prevent contradictory information from reaching customers

---

## Current State ✅

### Sprint 1: COMPLETE (8/8 story points)
**What's Built**:
- ✅ Project structure (`src/`, `tests/`, `config/`)
- ✅ Configuration system (`src/utils/config.py`, `config/config.yaml`)
- ✅ Logging utilities (`src/utils/logger.py`)
- ✅ Document cache with SHA-256 hashing (`src/utils/cache.py`)
- ✅ Change detection (`src/core/change_detector.py`)
- ✅ Test framework (pytest configured)

### Sprint 2: COMPLETE (13/13 story points) ✅
**What's Built**:
- ✅ YAML Frontmatter Parser (`src/utils/frontmatter.py`) - 268 lines, 84% coverage
- ✅ YAML Validator (`src/core/validators/yaml_validator.py`) - 327 lines, 97% coverage
- ✅ Auto-Fix Engine (`src/core/auto_fixer.py`) - 354 lines, 95% coverage
- ✅ 73 tests passing (33 frontmatter, 20 validator, 20 auto-fix)
- ✅ 10 test fixture documents
- ✅ Validation scripts (`validate_strategy_docs.py`, `demo_auto_fix.py`)

**Real-World Validation**:
- ✅ 10/10 Symphony Core strategy documents validated successfully
- ✅ All documents compliant with 3-field requirement (ADR-001)
- ✅ Auto-fix demonstrated with preview and backup

**Key Features Delivered**:
- 🔒 Preview mode (show changes before applying)
- 💾 Automatic backups (timestamped for safety)
- 🎯 Smart extraction (title from H1, tags from path)
- 📝 Actionable errors (every issue has suggestion)

**Available for Use**:
```python
from src.utils.frontmatter import parse_frontmatter, add_frontmatter
from src.core.validators.yaml_validator import YAMLValidator
from src.core.auto_fixer import AutoFixer
```

---

## What's Next: Sprint 3 (18 story points)

### Sprint Goal
Complete validation engine WITH conflict detection for mission-critical scaling.

**THIS IS THE BIG ONE**: Conflict detection is why Symphony Core exists. Without it, contradictory pricing and policies reach customers.

### User Stories to Implement

**US-3.1: Markdown Syntax Validator** (5 points)
- Create `src/core/validators/markdown_validator.py`
- Validate heading hierarchy, code blocks, links, formatting
- Rules: MD-001 through MD-008
- Generate ValidationIssue objects with line numbers

**US-3.2: Naming Convention Validator** (3 points)
- Create `src/core/validators/naming_validator.py`
- Validate lowercase-with-hyphens, length limits, no version numbers
- Rules: NAME-001 through NAME-005
- Suggest corrected filenames

**US-3.3: Conflict Detection Engine** ⭐ (10 points) - MISSION CRITICAL
- Create `src/core/conflict_detector.py` and `src/core/semantic_analyzer.py`
- Detect pricing conflicts (same product, different prices)
- Detect policy contradictions (conflicting statements)
- Detect duplicate SOPs (>80% similarity)
- **Batch mode**: Validates ALL documents (not just changed - ADR-006)
- Severity classification (CRITICAL, HIGH, MEDIUM, LOW)

---

## Key Insights from Sprint 2

### Architecture Patterns That Work ✅
1. **Separation of Concerns**:
   ```
   frontmatter.py  → Parse/manipulate (84% coverage)
   validator.py    → Validate rules (97% coverage)
   auto_fixer.py   → Apply fixes (95% coverage)
   ```
   **Apply to Sprint 3**: Same pattern for markdown, naming, conflict validators

2. **Comprehensive Test Fixtures**:
   ```
   tests/fixtures/yaml_test_documents/
   ├── valid_complete.md      (happy path)
   ├── missing_frontmatter.md (error case)
   ├── malformed_yaml.md      (edge case)
   └── multiple_issues.md     (complex case)
   ```
   **Apply to Sprint 3**: Build markdown, naming, conflict fixtures EARLY

3. **Safety First**:
   - Preview mode for all changes
   - Timestamped backups before modifications
   - Actionable error messages with suggestions
   **Apply to Sprint 3**: Preview for naming changes, conflict resolutions

### What to Replicate
✅ Same architecture (separate validators)
✅ >80% test coverage target
✅ Dataclasses for structured results
✅ Configuration-driven behavior
✅ Real document validation before "done"

### What Needs Improvement
⚠️ Tag suggestion too generic (file path only)
⚠️ Need content-based analysis for better tags
⚠️ Consider LLM integration for semantic understanding

**For Sprint 3**: Conflict detection will need semantic analysis. Consider simple rule-based first, then LLM enhancement.

---

## Critical Architectural Decisions

**Read `DECISIONS.md` for full context. Key points:**

1. **ADR-001**: Only 3 required YAML fields (title, tags, status)
   - Sprint 2 validated this: 10/10 real docs passed

2. **ADR-002**: Conflict detection in v1.0 (MISSION CRITICAL)
   - Why: Scaling SaaS platform needs it NOW
   - Can't wait for v1.1

3. **ADR-003**: Auto-fix with preview and backup
   - Sprint 2 proved this builds user trust
   - Apply same pattern for naming fixes

4. **ADR-006**: Accuracy > Speed (batch mode acceptable)
   - Conflict detection processes ALL documents
   - Not just changed files
   - Full corpus comparison for pricing/policies

---

## Exact Prompt to Start Sprint 3

**Copy and paste this prompt to begin Sprint 3 implementation:**

```
I'm ready to start Sprint 3 implementation for Symphony Core Document Management Workflow.

Context:
- Sprint 1-2 are complete (foundation, YAML validation, auto-fix)
- Sprint 3 goal: Markdown + Naming + Conflict Detection (18 story points)
- This sprint includes MISSION CRITICAL conflict detection (ADR-002)
- 73 tests passing from Sprint 1-2 with 84-97% coverage

Sprint 2 delivered excellent results. Key learnings:
- Separation of concerns works (separate validators)
- Comprehensive test fixtures are essential
- >80% coverage is achievable and valuable
- Preview mode + backups build user trust
- Real document validation confirms design

Please implement Sprint 3 following these priorities:

1. **US-3.1: Markdown Validator** (5 points)
   - Create src/core/validators/markdown_validator.py
   - Same architecture as yaml_validator.py
   - Validate heading hierarchy, code blocks, links
   - Build comprehensive test fixtures FIRST
   - Target >80% coverage

2. **US-3.2: Naming Validator** (3 points)
   - Create src/core/validators/naming_validator.py
   - Validate lowercase-with-hyphens, length limits
   - Suggest corrected filenames
   - Preview mode for rename operations

3. **US-3.3: Conflict Detector** ⭐ (10 points) - MISSION CRITICAL
   - Create src/core/conflict_detector.py
   - Create src/core/semantic_analyzer.py
   - Detect: pricing conflicts, policy contradictions, duplicate SOPs
   - Batch mode: process ALL documents (ADR-006)
   - Severity classification
   - Start simple (rule-based), enhance with LLM if needed

Key requirements:
- Follow Sprint 2 architecture patterns (proven to work)
- Build test fixtures early (one for each validation rule)
- >80% test coverage on new modules
- Use Config, Logger from Sprint 1
- Use ValidationIssue structure from Sprint 2
- Test on real documents before declaring "done"

Start with US-3.1 (Markdown Validator). Build fixtures first, then validator, then tests.
```

---

## Critical Files to Reference

**Sprint Documentation**:
- `Sprint_2_Summary.md` - Comprehensive insights and lessons learned
- `VALIDATION_REPORT.md` - Real-world validation results from Sprint 2
- `sprints/sprint-02-yaml-validation.md` - Completed sprint with retrospective
- `sprints/BACKLOG.md` - Sprint 3 acceptance criteria

**Architectural Context**:
- `DECISIONS.md` - All 6 ADRs with rationale (especially ADR-002, ADR-006)
- `docs/architecture-v1.0-validation.md` - Technical architecture
- `docs/development-process-guide.md` - Now includes Sprint 2 lessons learned
- `docs/user-guide.md` - Updated with YAML validation and auto-fix

**Configuration**:
- `config/config.yaml` - Updated to 3 required fields (ADR-001)

**Existing Code to Study**:
- `src/core/validators/yaml_validator.py` - Template for new validators
- `src/core/auto_fixer.py` - Preview and backup patterns
- `tests/core/validators/test_yaml_validator.py` - Testing approach
- `tests/fixtures/yaml_test_documents/` - Fixture examples

---

## Success Criteria for Sprint 3

### Code Deliverables
- [ ] `src/core/validators/markdown_validator.py` (~300 lines)
- [ ] `src/core/validators/naming_validator.py` (~200 lines)
- [ ] `src/core/conflict_detector.py` (~400 lines)
- [ ] `src/core/semantic_analyzer.py` (~300 lines)
- [ ] Corresponding test files for each (~200-300 lines each)
- [ ] Test fixtures (markdown, naming, conflicts)

### Quality Gates
- [ ] All tests passing (target: 100+ new tests)
- [ ] Test coverage > 80% on new modules
- [ ] All functions have docstrings and type hints
- [ ] PEP 8 compliant
- [ ] Real document validation (test on Symphony Core docs)

### Validation
- [ ] Test markdown validator on actual docs
- [ ] Test naming validator on real filenames
- [ ] Test conflict detector on documents with known conflicts
- [ ] Verify batch mode processes all documents (not just changed)

---

## After Sprint 3 Completion

**What should work**:
```python
# Markdown validation
from src.core.validators.markdown_validator import MarkdownValidator
validator = MarkdownValidator(config, logger)
issues = validator.validate(Path("doc.md"))

# Naming validation
from src.core.validators.naming_validator import NamingValidator
validator = NamingValidator(config, logger)
issues = validator.validate(Path("My Bad Name.md"))

# Conflict detection
from src.core.conflict_detector import ConflictDetector
detector = ConflictDetector(config, logger)
conflicts = detector.detect_conflicts([Path("doc1.md"), Path("doc2.md")])
```

**Next Steps**:
- Sprint 4: CLI + Reporting (21 points)
- Integrate all validators
- Build command-line interface
- Generate comprehensive reports

---

## Important Context: Why Sprint 3 Matters

### Mission Critical Features

**Conflict Detection** is THE reason Symphony Core exists:
- **Business Risk**: Contradictory pricing = customer confusion = lost revenue
- **Scaling Requirement**: Multiple contributors = inevitable conflicts
- **User Quote**: "Without comprehensive conflict identification we will continue to face issues"

**Real-World Scenarios**:
1. **Pricing Conflict**: Product X priced at $99 in one doc, $149 in another
2. **Policy Contradiction**: Refund policy says "30 days" in one doc, "14 days" in another
3. **Duplicate SOPs**: Three different docs describe same onboarding process

**Why Batch Mode** (ADR-006):
- Pricing changes need comparison with ALL existing contracts
- Can't risk missing conflicts by only checking changed files
- Accuracy > Speed (batch/async acceptable)

---

## Quick Reference: Project Stats

**Total v1.0 Effort**: 52 story points (~125 hours)
- Sprint 1: 8 points ✅ COMPLETE
- Sprint 2: 13 points ✅ COMPLETE (exceeded expectations!)
- Sprint 3: 18 points ⏳ READY (biggest sprint - includes conflict detection)
- Sprint 4: 21 points 📋 PLANNED

**Current Progress**:
- Story Points: 21/52 completed (40%)
- Test Coverage: 84-97% on Sprint 2 modules
- Tests Passing: 73/73 (100%)
- Real Documents Validated: 10/10 (100%)

**Sprint 2 Velocity**: 13 points in 1 day (vs. estimated 3-5 days)

---

## Sprint 3 Complexity Warnings

### Don't Underestimate Conflict Detection (10 points)

**Why it's complex**:
1. **Semantic Understanding**: Detecting contradictions requires understanding MEANING
2. **LLM Integration**: May need Anthropic API for semantic analysis
3. **Performance**: Batch mode on 50+ documents takes time
4. **False Positives**: Balance sensitivity vs. specificity

**Mitigation**:
- Start with simple rule-based detection (keywords, patterns)
- Build comprehensive test fixtures with known conflicts
- Add LLM enhancement progressively
- Cache results aggressively
- Implement tag-based filtering to reduce scope

### Test Fixtures Are Critical

**Build BEFORE coding**:
```
tests/fixtures/markdown_test_documents/
├── valid_headings.md
├── skipped_h2.md
├── missing_code_lang.md
└── broken_links.md

tests/fixtures/conflict_test_documents/
├── pricing_conflict_pair/
│   ├── doc1.md (Product X = $99)
│   └── doc2.md (Product X = $149)
├── policy_contradiction/
└── duplicate_sop/
```

---

## Repository Structure (Current State)

```
sc-doc-mgmt-workflow/
├── DECISIONS.md                    ⭐ 6 ADRs documented
├── START_HERE.md                   ⭐ This file (Sprint 3 ready)
├── Sprint_2_Summary.md             ⭐ Sprint 2 insights
├── VALIDATION_REPORT.md            ✅ Real-world validation results
├── README.md
├── config/
│   └── config.yaml                 ✅ Updated (3 required fields)
├── src/
│   ├── core/
│   │   ├── change_detector.py      ✅ Sprint 1
│   │   ├── validators/
│   │   │   └── yaml_validator.py   ✅ Sprint 2 (97% coverage)
│   │   └── auto_fixer.py           ✅ Sprint 2 (95% coverage)
│   └── utils/
│       ├── config.py               ✅ Sprint 1
│       ├── cache.py                ✅ Sprint 1
│       ├── logger.py               ✅ Sprint 1
│       └── frontmatter.py          ✅ Sprint 2 (84% coverage)
├── tests/                          ✅ 73 tests passing
│   ├── core/
│   │   ├── validators/
│   │   │   └── test_yaml_validator.py  ✅ 20 tests
│   │   └── test_auto_fixer.py          ✅ 20 tests
│   ├── utils/
│   │   └── test_frontmatter.py         ✅ 33 tests
│   └── fixtures/
│       └── yaml_test_documents/        ✅ 10 fixtures
├── sprints/
│   ├── BACKLOG.md                  ⭐ Sprint 3 details
│   ├── sprint-01-foundation.md     ✅ Complete
│   └── sprint-02-yaml-validation.md ✅ Complete with retrospective
├── docs/
│   ├── product-requirements-document.md
│   ├── architecture-v1.0-validation.md
│   ├── user-guide.md               ✅ Updated with Sprint 2 features
│   └── development-process-guide.md ✅ Updated with Sprint 2 lessons
├── validate_strategy_docs.py       ✅ Working validator script
└── demo_auto_fix.py                ✅ Working demo script
```

**TO BUILD in Sprint 3**:
```
src/core/validators/markdown_validator.py  🚧
src/core/validators/naming_validator.py    🚧
src/core/conflict_detector.py              🚧
src/core/semantic_analyzer.py              🚧
tests/core/validators/test_markdown_validator.py  🚧
tests/core/validators/test_naming_validator.py    🚧
tests/core/test_conflict_detector.py              🚧
tests/fixtures/markdown_test_documents/           🚧
tests/fixtures/naming_test_documents/             🚧
tests/fixtures/conflict_test_documents/           🚧
```

---

## Estimated Effort for Sprint 3

**Complexity Breakdown**:
- US-3.1 Markdown Validator: 5 points (moderate - similar to YAML)
- US-3.2 Naming Validator: 3 points (simple - pattern matching)
- US-3.3 Conflict Detector: 10 points (complex - semantic analysis)

**Time Estimates**:
- Best Case: 4-6 hours (if architecture flows smoothly)
- Realistic: 6-8 hours (with conflict detection complexity)
- With Buffer: 8-10 hours (including comprehensive testing)

**Token Estimate**: ~40,000-50,000 tokens
**Current Available**: ~64,000 tokens (plenty of room!)

---

## Key Success Factors

### From Sprint 2 Experience

✅ **Do This**:
1. Build test fixtures FIRST (before writing validators)
2. Follow YAML validator architecture (proven pattern)
3. Target >80% coverage (achievable and valuable)
4. Test on real documents before declaring "done"
5. Use dataclasses for structured results
6. Make errors actionable (include suggestions)
7. Document as you go (don't defer to end)

❌ **Avoid This**:
1. Don't start coding before fixtures
2. Don't skip edge cases in tests
3. Don't make config changes without updating docs
4. Don't underestimate conflict detection complexity
5. Don't chase 100% coverage (diminishing returns)

### For Conflict Detection Specifically

**Start Simple**:
1. Rule-based detection first (keywords, patterns)
2. Test with obvious conflicts
3. Measure accuracy
4. Add LLM if needed

**Test Thoroughly**:
- Create document pairs with known conflicts
- Test false positives (similar but not conflicting)
- Test severity classification
- Verify batch mode processes all documents

---

**Ready to Start? Use the prompt above!** 🚀

**Status**: ✅ All Sprint 1-2 code committed and pushed to GitHub
**Last Commit**: 2601b4a - "feat: Complete Sprint 2 - YAML Validation + Auto-Fix"
**Working Tree**: Clean
**GitHub**: https://github.com/score-ra/sc-doc-mgmt-workflow.git

---

**Sprint 3 is the MISSION CRITICAL sprint. Conflict detection is why Symphony Core exists.** 🎯
