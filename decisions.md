---
title: Symphony Core - Architectural Decisions Record
tags: [adr, decisions, architecture, planning]
status: active
version: 1.0
last_updated: 2025-11-08
---

# Symphony Core - Architectural Decisions Record

This document tracks all major architectural and scope decisions for the Symphony Core Document Management Workflow project. Each decision is recorded with context, rationale, and impact to ensure continuity across development sessions.

---

## ADR-001: Simplified Required YAML Fields (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Sprint planning and Pareto principle analysis

### Context

Original v1.0 plan required 5 YAML frontmatter fields:
- title
- version
- date
- tags
- status

Applied Pareto principle: What delivers 80% of value with 20% of effort?

### Decision

**Required fields reduced to 3**:
- `title` - Document title (essential for identification)
- `tags` - List of tags (essential for organization and filtering)
- `status` - Document status (essential for workflow management)

**Removed from required (now optional)**:
- `version` - Not actively tracked in practice
- `date` - Nice-to-have, but not mission-critical

### Rationale

- **Simplification**: Reduces validation complexity and contributor friction
- **Focus**: Concentrates on essential metadata for organization and discovery
- **Adoption**: Lower barrier to entry for new team members
- **Maintenance**: Easier to maintain compliance with fewer required fields

### Impact

- Sprint 2 YAML validation effort: **-2 story points** (8 → 6 for validator)
- Faster contributor onboarding
- Lower validation failure rate
- Reduced auto-fix complexity

### Implementation Notes

Files: `config/config.yaml`, `src/core/validators/yaml_validator.py`

```yaml
validation:
  yaml:
    required_fields:
      - title
      - tags
      - status
```

---

## ADR-002: Conflict Detection in v1.0 (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Scaling SaaS platform requirements

### Context

**Original plan**: Conflict detection scheduled for v1.1 (future enhancement)

**User requirement**: "Without comprehensive conflict identification we will continue to face issues"

**Business context**:
- Symphony Core is a SaaS platform ready to scale rapidly
- Documentation repo will evolve with new SOPs, team members, business domains
- Multiple contributors = high risk of contradictory information
- Pricing changes need comparison across ALL existing contracts

### Decision

**Move conflict detection to v1.0 (Sprint 3)**

**Conflict types to detect**:
1. **Pricing conflicts**: Same product with different prices across documents
2. **Policy contradictions**: Conflicting statements in policies/terms
3. **Duplicate SOPs**: Multiple documents describing the same process (>80% similarity)
4. **Date/version conflicts**: Misaligned effective dates or version numbers

### Rationale

- **Mission Critical**: Prevents contradictory information from reaching customers
- **Scaling Requirement**: New team members + new domains = inevitable conflicts without automated detection
- **Risk Mitigation**: Catching conflicts before they become customer issues
- **Accuracy Priority**: "Accuracy and reliability over speed" - batch/async acceptable

### Impact

- Sprint 3 effort: **+5 story points** (13 → 18)
- Total v1.0 effort: **+2 net points** (50 → 52, accounting for simplifications)
- Increased complexity in Sprint 3
- Additional testing requirements
- New component: `ConflictDetector` class

### Implementation Notes

Files to create:
- `src/core/conflict_detector.py`
- `src/core/semantic_analyzer.py`
- `tests/core/test_conflict_detector.py`

**Batch processing mode**: Always validates ALL documents for conflicts, not just changed files.

---

## ADR-003: Auto-Fix with Preview (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Multi-contributor environment automation needs

### Context

**Question**: Should the system only report issues, or automatically fix them?

**Environment**: Multi-contributor team with varying documentation experience levels

**Concern**: Balance automation benefits with safety for business-critical documents

### Decision

**Hybrid approach: Auto-fix safe changes with preview**

**Auto-fix operations (with preview)**:
- Add missing YAML frontmatter
- Populate title from markdown H1 heading
- Suggest tags based on file path/content
- Fix file naming (uppercase → lowercase, underscores → hyphens)
- Standardize field names (e.g., `Title:` → `title:`)

**Requires manual review**:
- Content modifications
- Changes to existing metadata values
- Heading structure modifications
- Link changes

**Safety features**:
- Preview mode: Shows changes before applying
- Backup: Creates backup of original file before modification
- Report: Documents all auto-fix actions taken

### Rationale

- **Scaling**: Reduces manual bottleneck as team grows
- **Safety**: Preview + backup protects business-critical documents
- **Efficiency**: Automates repetitive, low-risk fixes
- **Human oversight**: Maintains human review for content changes

### Impact

- Sprint 2 effort: **+2 story points** (11 → 13, added US-2.3)
- Sprint 4 effort: **+3 story points** (18 → 21, preview UI and reporting)
- New component: `AutoFixer` class
- Requires backup/rollback mechanism

### Implementation Notes

Files to create:
- `src/core/auto_fixer.py`
- `tests/core/test_auto_fixer.py`

CLI usage:
```bash
python main.py validate --auto-fix --preview
```

---

## ADR-004: Practical CLI Scope (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Team collaboration and multi-domain validation

### Context

**Options evaluated**:
- **Minimal**: Single command, no options
- **Practical**: Essential options for team collaboration
- **Enterprise**: Full-featured with webhooks, JSON output, CI/CD integration

### Decision

**Practical CLI with essential options** (middle ground)

**Commands to implement**:
```bash
python main.py validate                    # Validate all documents
python main.py validate --path operations/ # Validate specific folder/domain
python main.py validate --tags pricing     # Validate by tag
python main.py validate --force            # Ignore cache, revalidate all
python main.py validate --auto-fix --preview  # Auto-fix with preview
python main.py validate --conflicts        # Conflict detection only
python main.py --help                      # Help text
```

**NOT included in v1.0**:
- JSON output format
- Webhook notifications
- Complex severity filtering
- CI/CD-specific integrations (exit codes yes, but not GitHub Actions integration)

### Rationale

- **Team Collaboration**: `--path` and `--tags` support different teams validating their domains
- **Practical**: Covers real use cases without over-engineering
- **Extensible**: Foundation for future enterprise features
- **Simple**: Easy to learn and use

### Impact

- Sprint 4 CLI implementation: Moderate complexity
- Good balance of functionality vs. development time
- Future-proof: Can add enterprise features in v1.1+

### Implementation Notes

Framework: Click (Python CLI framework)

Files to create:
- `src/cli.py`
- `src/main.py` (entry point)
- `tests/test_cli.py`

---

## ADR-005: Single Shared Configuration (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Configuration complexity vs. flexibility

### Context

**Options evaluated**:
- **Single shared config**: One `config.yaml` for all documents
- **Domain-specific overrides**: Different rules for different folders
- **Profile-based**: Multiple named profiles (operations, marketing, legal, etc.)

### Decision

**Single shared `config.yaml` for all documents**

**Configuration structure**:
```yaml
# Required fields (same for all docs)
validation:
  yaml:
    required_fields:
      - title
      - tags
      - status
    allowed_statuses:
      - draft
      - review
      - approved
      - active
      - deprecated

# Validation rules
  markdown:
    enabled: true
  naming:
    enabled: true

# Conflict detection
  conflicts:
    enabled: true
    batch_mode: true
```

**No domain-specific overrides in v1.0**

### Rationale

- **Simplicity**: Easier to understand and maintain
- **Consistency**: Same standards across all business domains
- **Reduced complexity**: Less configuration code to write and test
- **User preference**: "Single shared config" selected over alternatives

### Impact

- Cleaner implementation
- Less testing surface area
- Future flexibility: Can add overrides in v1.1 if needed

### Implementation Notes

File: `config/config.yaml`

All validation rules apply uniformly across:
- Business plans
- SOPs
- Policies
- Pricing documents
- Financial documents

---

## ADR-006: Accuracy Over Speed (2025-11-07)

**Status**: ✅ APPROVED
**Decision Maker**: Product Owner
**Context**: Conflict detection performance philosophy

### Context

**Question**: For conflict detection, validate only changed files (fast) or all files (accurate)?

**Use case**: "When a new pricing change is made we will need to compare that with existing contracts so it may be required to always check all docs"

**User statement**: "Speed is not important here, it is the accuracy and reliability of the process. This operation is not being built to provide results in real time, batch/asynchronous mode is completely acceptable"

### Decision

**Always validate all documents for conflict detection**

**Implementation**:
- Conflict detection runs on **full document corpus**, not just changed files
- Cache still used for incremental file detection (Sprint 1 feature)
- But conflict analysis always compares across ALL documents
- Batch/async mode acceptable - no real-time requirement

### Rationale

- **Accuracy**: Missing a pricing conflict = business risk
- **Completeness**: Pricing changes need comparison with ALL existing contracts
- **Reliability**: Cannot risk false negatives from incomplete comparisons
- **Business context**: Contracts and pricing are mission-critical

### Impact

- Conflict detection may take longer (minutes instead of seconds)
- No impact on user experience (batch mode acceptable)
- Higher confidence in results
- Simpler logic (no complex caching for conflicts)

### Implementation Notes

**Two-tier approach**:
1. **File-level validation** (YAML, Markdown, Naming): Uses cache, incremental
2. **Conflict detection**: Always processes full corpus, ignores cache

CLI behavior:
```bash
# Fast: Only validates changed files for YAML/Markdown/Naming
python main.py validate

# Comprehensive: Validates ALL files for conflicts
python main.py validate --conflicts

# Force: Validates ALL files for everything
python main.py validate --force
```

Files: `src/core/conflict_detector.py`

---

## Decision Impact Summary

| Decision | Impact on v1.0 | Story Points Change |
|----------|---------------|---------------------|
| ADR-001: Simplified YAML | Easier validation | -2 points |
| ADR-002: Conflicts in v1.0 | Major feature add | +5 points |
| ADR-003: Auto-fix | New capability | +2 points |
| ADR-004: Practical CLI | Moderate scope | 0 (as planned) |
| ADR-005: Single config | Simpler | -1 point |
| ADR-006: Accuracy priority | Simpler logic | -2 points |
| **NET CHANGE** | | **+2 points** |

**Original v1.0**: 50 story points (~120 hours)
**Revised v1.0**: 52 story points (~125 hours)

---

## Sprint Allocation

| Sprint | Original | Revised | Changes |
|--------|----------|---------|---------|
| Sprint 1 | 8 | 8 | No change (complete) |
| Sprint 2 | 11 | 13 | +2 (auto-fix added) |
| Sprint 3 | 13 | 18 | +5 (conflict detection) |
| Sprint 4 | 18 | 21 | +3 (conflict reporting) |

---

## Future Considerations

**Potential v1.1 enhancements** (not committed):
- Domain-specific configuration overrides
- Advanced conflict detection (semantic analysis with LLM)
- Enterprise CLI features (webhooks, JSON output)
- Performance optimizations if needed
- CI/CD integration templates

**Deferred from original v1.1 plan** (now in v1.0):
- ✅ Conflict detection (moved to Sprint 3)
- ✅ Auto-fix capabilities (moved to Sprint 2)

---

**Last Updated**: 2025-11-07
**Maintained By**: Engineering Team
**Status**: Active Development - Sprint 1 Complete, Sprint 2 Ready
