# START HERE - Sprint 2 Execution Guide

**Last Updated**: 2025-11-07
**Current Status**: Sprint 1 Complete, Sprint 2 Ready to Execute
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
- ✅ All tests passing

**Available for Use**:
```python
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.cache import DocumentCache
from src.core.change_detector import ChangeDetector
```

---

## What's Next: Sprint 2 (13 story points)

### Sprint Goal
Build YAML frontmatter validation WITH auto-fix capabilities for safe changes.

### Required YAML Fields (ADR-001)
**ONLY 3 fields required** (simplified from original 5):
1. `title` - Document title
2. `tags` - List of tags (must be a list, not a string)
3. `status` - Document status (draft, review, approved, active, deprecated)

**NOT required** (optional): `version`, `date`, `author`, `category`, `audience`

### User Stories to Implement

**US-2.1: YAML Frontmatter Parser** (3 points)
- Create `src/utils/frontmatter.py`
- Functions: `parse_frontmatter()`, `add_frontmatter()`, `has_frontmatter()`
- Handle edge cases (missing, malformed YAML)

**US-2.2: YAML Validator** (5 points)
- Create `src/core/validators/yaml_validator.py`
- Validate 4 rules: YAML-001 (block present), YAML-002 (3 fields), YAML-003 (status valid), YAML-004 (tags is list)
- Generate ValidationIssue objects

**US-2.3: Auto-Fix Engine** (5 points) ⭐ NEW
- Create `src/core/auto_fixer.py`
- Auto-add missing YAML frontmatter
- Extract title from H1 heading
- Suggest tags from file path
- Preview mode (--preview flag)
- Backup mechanism before modifications

---

## Key Architectural Decisions

**Read `DECISIONS.md` for full details. Key points:**

1. **ADR-001**: Only 3 required YAML fields (not 5) - title, tags, status
2. **ADR-002**: Conflict detection moved to v1.0 Sprint 3 (mission critical)
3. **ADR-003**: Auto-fix hybrid approach (safe changes only, preview mode)
4. **ADR-006**: Accuracy > Speed (batch mode acceptable, full document comparison for conflicts)

---

## Exact Prompt to Start Sprint 2

**Copy and paste this prompt to begin Sprint 2 implementation:**

```
I'm ready to start Sprint 2 implementation for Symphony Core Document Management Workflow.

Context:
- Sprint 1 is complete (foundation, config, cache, change detection)
- Sprint 2 goal: YAML validation + auto-fix (13 story points)
- Required YAML fields: title, tags, status (3 fields only - ADR-001)
- User wants auto-fix with preview capability (ADR-003)

Please implement Sprint 2 following this plan:

1. Read sprints/sprint-02-yaml-validation.md for detailed execution plan
2. Read DECISIONS.md for architectural context (especially ADR-001, ADR-003)
3. Implement all 3 user stories:
   - US-2.1: YAML Frontmatter Parser (src/utils/frontmatter.py)
   - US-2.2: YAML Validator (src/core/validators/yaml_validator.py)
   - US-2.3: Auto-Fix Engine (src/core/auto_fixer.py)
4. Write comprehensive tests for each component
5. Ensure >80% test coverage
6. Update sprint-02-yaml-validation.md with progress as you go

Key requirements:
- Use Config, Logger, Cache from Sprint 1
- Follow PEP 8, add docstrings and type hints
- Test-driven development approach
- Update Daily Progress Log in sprint-02-yaml-validation.md
- Mark tasks as complete in implementation checklists

Start with US-2.1 (YAML Parser). Ask if you need clarification before proceeding.
```

---

## Critical Files to Reference

**Sprint Execution Plan**:
- `sprints/sprint-02-yaml-validation.md` - Complete implementation guide with checklists

**Architectural Context**:
- `DECISIONS.md` - All 6 user decisions with rationale
- `sprints/BACKLOG.md` - Full acceptance criteria for all user stories
- `docs/architecture-v1.0-validation.md` - Technical architecture

**Configuration**:
- `config/config.yaml` - Required fields configuration (3 fields only)
- `.env.example` - Environment variable template

**Dependencies**:
- `requirements.txt` - Python dependencies (PyYAML, pytest, etc.)

---

## Success Criteria for Sprint 2

### Code Deliverables
- [ ] `src/utils/frontmatter.py` (~200 lines)
- [ ] `src/core/validators/yaml_validator.py` (~250 lines)
- [ ] `src/core/auto_fixer.py` (~300 lines)
- [ ] `tests/utils/test_frontmatter.py` (~150 lines)
- [ ] `tests/core/validators/test_yaml_validator.py` (~200 lines)
- [ ] `tests/core/test_auto_fixer.py` (~200 lines)

### Quality Gates
- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] All functions have docstrings
- [ ] Type hints on all signatures
- [ ] PEP 8 compliant
- [ ] No critical bugs

### Documentation
- [ ] Update sprint-02-yaml-validation.md with daily progress
- [ ] Mark completed tasks in implementation checklists
- [ ] Update README.md: Sprint 2 status
- [ ] Document any deviations in DECISIONS.md

---

## After Sprint 2 Completion

**What should work**:
```bash
# Parse YAML from markdown file
from src.utils.frontmatter import parse_frontmatter
metadata = parse_frontmatter(Path("doc.md"))

# Validate document
from src.core.validators.yaml_validator import YAMLValidator
validator = YAMLValidator(config, logger)
issues = validator.validate(Path("doc.md"))

# Auto-fix with preview
from src.core.auto_fixer import AutoFixer
fixer = AutoFixer(config, logger)
result = fixer.fix_document(Path("doc.md"), issues, preview=True)
```

**Next Steps**:
- Sprint 3: Markdown + Naming + Conflict Detection (18 points)
- Sprint 4: CLI + Reporting (21 points)

---

## Important Context: Why These Choices?

**Scaling SaaS Platform**:
- Symphony Core will have multiple contributors and new business domains
- Without conflict detection, contradictory pricing/policies will reach customers
- New team members need auto-fix to reduce manual bottleneck

**Accuracy is Mission Critical**:
- "Speed is not important, accuracy and reliability is" (user quote)
- Batch/async mode acceptable
- Full document comparison for conflicts (not just changed files)

**Simplified to Focus on Value**:
- 3 YAML fields (not 5) delivers 80% of value
- Focus on essential metadata for organization (title, tags, status)

---

## Quick Reference: Project Stats

**Total v1.0 Effort**: 52 story points (~125 hours)
- Sprint 1: 8 points ✅ COMPLETE
- Sprint 2: 13 points ⏳ READY
- Sprint 3: 18 points 📋 PLANNED
- Sprint 4: 21 points 📋 PLANNED

**Test Coverage Target**: >80%
**Python Version**: 3.11+
**Framework**: pytest, Click (CLI), PyYAML

---

## Troubleshooting / Common Questions

**Q: Why only 3 required YAML fields?**
A: User decision (ADR-001) based on Pareto principle. Title, tags, status deliver core value.

**Q: Why is conflict detection in v1.0?**
A: User decision (ADR-002) - mission critical for scaling SaaS. Can't wait for v1.1.

**Q: What if I need to make an architectural decision during Sprint 2?**
A: Add it to DECISIONS.md as ADR-007. Document context, decision, rationale, impact.

**Q: Where do I track progress?**
A: Update `sprints/sprint-02-yaml-validation.md` Daily Progress Log and mark checkboxes in implementation checklists.

**Q: Tests failing?**
A: Run `pytest -v` to see details. Ensure virtual environment activated. Check requirements.txt installed.

---

## Repository Structure

```
sc-doc-mgmt-workflow/
├── DECISIONS.md                    ⭐ Read this first for context
├── START_HERE.md                   ⭐ This file
├── README.md
├── config/
│   └── config.yaml                 (3 required fields configured)
├── src/
│   ├── core/
│   │   ├── change_detector.py      ✅ Sprint 1
│   │   ├── validators/
│   │   │   └── yaml_validator.py   🚧 Sprint 2 - TO BUILD
│   │   └── auto_fixer.py           🚧 Sprint 2 - TO BUILD
│   └── utils/
│       ├── config.py               ✅ Sprint 1
│       ├── cache.py                ✅ Sprint 1
│       ├── logger.py               ✅ Sprint 1
│       └── frontmatter.py          🚧 Sprint 2 - TO BUILD
├── tests/                          (mirror src/ structure)
├── sprints/
│   ├── BACKLOG.md
│   ├── sprint-01-foundation.md     ✅ Complete
│   └── sprint-02-yaml-validation.md ⭐ Execution plan
└── docs/
    ├── product-requirements-document.md
    ├── architecture-v1.0-validation.md
    └── user-guide.md
```

---

## Estimated Time for Sprint 2

**Best Case**: 2-3 hours (if no blockers)
**Realistic**: 3-4 hours (with testing and documentation)
**With Buffer**: 4-5 hours (including edge cases and polish)

**Token Estimate**: ~20,000-25,000 tokens

---

**Ready to Start? Use the prompt above!** 🚀

**Status**: ✅ All documentation committed and pushed to GitHub
**Last Commit**: f915834 - "docs: Implement sprint continuity strategy with user decisions"
**Working Tree**: Clean
