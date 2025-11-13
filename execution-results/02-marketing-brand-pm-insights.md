# Product Manager Review: 02-marketing-brand New Insights

**Review Date**: 2025-11-13
**Reviewed By**: Product Manager (Claude)
**Test Scenario**: 02-marketing-brand folder documentation scan (21 docs)
**Current Version**: Symphony Core v1.0.0

---

## Context

After testing on a second folder (`02-marketing-brand`), **3 NEW capability gaps** emerged that weren't visible in the `01-strategy` test. These insights refine and expand the original backlog.

---

## 🆕 NEW Capability Gaps (from 02-marketing-brand)

### 🔴 HIGH PRIORITY (New)

#### NEW-001: File Exclusion Patterns (README Exception Handling)

**Current Behavior**:
- `README.md` flagged for missing frontmatter
- No way to exclude specific files/patterns from frontmatter validation
- All `.md` files treated identically

**Gap**:
- READMEs are typically index/navigation files that shouldn't require SC frontmatter
- No config option to exclude files by pattern (e.g., `**/README.md`, `**/CHANGELOG.md`)
- Forces teams to either:
  - Add frontmatter to READMEs (clutters navigation docs)
  - Accept validation failures

**Proposed Enhancement**:
```yaml
# config.yaml
validation:
  yaml:
    enabled: true
    required_fields: [title, tags, status]
    # NEW: Exclude patterns
    exclude_patterns:
      - "**/README.md"
      - "**/CHANGELOG.md"
      - "**/LICENSE.md"
    # Alternative: require_frontmatter_exceptions
    exceptions:
      - pattern: "**/README.md"
        reason: "Navigation files don't need frontmatter"
        require_fields: []  # No required fields for READMEs
```

**User Story**:
> As a documentation manager, I want to exclude READMEs from frontmatter validation, so I don't clutter navigation files with unnecessary metadata.

**Impact**: **HIGH** - Reduces false positives, improves usability

**Acceptance Criteria**:
- [ ] Add `validation.yaml.exclude_patterns` config option
- [ ] Support glob patterns (`**/README.md`, `docs/*.md`)
- [ ] Excluded files still run other validators (markdown, naming)
- [ ] Report shows "X files excluded from YAML validation"
- [ ] Default exclusions: none (opt-in behavior)

---

#### NEW-002: Auto-Fix for Filename Violations

**Current Behavior**:
- Tool detects `steps to fix domain issue.md` (spaces in filename)
- Suggests rename: `steps-to-fix-domain-issue.md`
- **Does NOT auto-fix** (manual rename required)

**Gap**:
- Auto-fix works for trailing whitespace, code blocks, etc. but NOT filenames
- Renaming files is risky (breaks links, git history)
- No preview of what links would break if renamed

**Proposed Enhancement**:
```bash
# New auto-fix capability
python -m src.cli validate --path . --auto-fix --preview

# Output includes:
# FILE RENAME:
# ❌ steps to fix domain issue.md
# ✅ steps-to-fix-domain-issue.md
#
# ⚠️  IMPACT ANALYSIS:
# - 3 documents link to this file:
#   - homepage_copy.md:42 (link will break)
#   - website/README.md:15 (link will break)
# - Git history will show as delete + add (use --preserve-history flag)
#
# Apply rename + update links? [y/n]
```

**User Story**:
> As a content contributor, I want auto-fix to rename files with spaces AND update all internal links, so I don't manually chase down broken references.

**Impact**: **HIGH** - Enables safe bulk filename fixes

**Acceptance Criteria**:
- [ ] `--auto-fix` detects and renames files with naming violations
- [ ] Scans all markdown files for links to renamed file
- [ ] Updates internal links automatically (or reports what would break)
- [ ] Offers `--preserve-history` flag (use `git mv` instead of rename)
- [ ] Preview mode shows impact before applying

---

#### NEW-003: Bulk Frontmatter Field Addition

**Current Behavior**:
- 2 docs missing `status` field
- Tool reports error but doesn't offer bulk fix
- Must manually edit each file

**Gap**:
- No way to bulk-add missing fields to multiple documents
- `--auto-fix` doesn't handle frontmatter additions (only format fixes)
- Teams with 50+ docs missing `status` field face hours of manual work

**Proposed Enhancement**:
```bash
# New command
python -m src.cli frontmatter add-field \
  --field status \
  --value draft \
  --path 02-marketing-brand

# Output:
# Found 2 documents missing 'status' field:
# - brand/brand-guidelines/sc-design-kit.md
# - brand/brand-guidelines/symphony_core_web_style_guide.md
#
# Add 'status: draft' to these documents? [y/n]
# > y
#
# ✅ Updated 2 documents

# Alternative: Interactive mode
python -m src.cli frontmatter add-field --interactive

# Prompts for each document:
# sc-design-kit.md is missing 'status'
# Choose value: [draft/review/approved/deprecated/active/skip]
```

**User Story**:
> As a documentation manager migrating 100 docs to SC standards, I want to bulk-add missing frontmatter fields with default values, so I don't spend days on manual edits.

**Impact**: **HIGH** - Saves hours on bulk migrations

**Acceptance Criteria**:
- [ ] New command: `frontmatter add-field`
- [ ] Supports `--field`, `--value`, `--path` arguments
- [ ] Interactive mode for per-document value selection
- [ ] Preview mode shows what will be added
- [ ] Preserves existing frontmatter formatting
- [ ] Backups created before modification

---

### ⚠️ MEDIUM PRIORITY (Refinements)

#### REFINED-004: Enhanced Status Conflict Detection

**Original Issue**: Pricing conflict detection needs improvement
**New Insight**: Status conflicts also need better handling

**Current Behavior**:
- Detects 'concepts' as non-standard status value
- Reports as "STATUS conflict" in conflict report
- Also reports as "YAML-003 error" in validation report (duplicate)

**Gap**:
- Inconsistent: Same issue reported in TWO different ways
- Conflict report says "STATUS conflict" but it's really a validation error
- Confusing for users: "Is this a conflict or a validation error?"

**Proposed Enhancement**:
```markdown
# Conflict report should focus on CROSS-DOCUMENT conflicts only
# Validation report should handle schema violations

## Validation Report:
❌ YAML-003: Invalid status 'concepts' (not in allowed list)

## Conflict Report (only if status differs across related docs):
⚠️  STATUS CONFLICT:
- mailbox-sign-concepts.md uses 'concepts'
- mailbox-sign-final.md uses 'approved'
Recommendation: Standardize status values for related documents
```

**User Story**:
> As a QA tester, I want validation errors and conflicts reported separately, so I understand whether it's a schema violation (one doc) or inconsistency (multiple docs).

**Impact**: **MEDIUM** - Improves report clarity

---

## Updated Priority Assessment

Based on two folder tests, here's the revised priority ranking:

### Must-Have (Sprint 7 - Week 1)
1. **PB-002**: Severity filtering (`--min-severity`) - reduces noise
2. **PB-001**: Line numbers in conflict reports - saves time
3. **NEW-001**: README exclusion patterns - reduces false positives

### High-Value (Sprint 8 - Week 2-3)
4. **NEW-003**: Bulk frontmatter field addition - migration enabler
5. **PB-004**: Smart pricing conflict detection - reduces false positives
6. **PB-005**: Bulk auto-fix preview - enables safe bulk operations

### Important (Sprint 9 - Week 4)
7. **NEW-002**: Auto-fix filename violations + link updates - risky but valuable
8. **PB-003**: Frontmatter completeness detection - compliance visibility
9. **REFINED-004**: Enhanced status conflict detection - improves clarity

### Nice-to-Have (Backlog)
10. **PB-006**: Cross-document conflict detection
11. **PB-007**: Progress indicators
12. **PB-008**: HTML report output
13. **PB-009**: Incremental scan status

---

## Key Insights from Two-Folder Testing

### Pattern Recognition

| Issue Type | 01-strategy | 02-marketing-brand | Pattern |
|------------|-------------|-------------------|---------|
| Trailing Whitespace | 283 (98%) | 98 (85%) | **Pervasive** - affects all folders |
| Pricing Conflicts | 1 | 1 | **Common** - likely in all folders |
| Frontmatter Missing | 0 | 3 | **Variable** - depends on folder age/author |
| Invalid Status Values | 0 | 2 | **New pattern** - training needed |
| Filename Spaces | 0 | 1 | **Rare** - but breaks automation |

### Tool Maturity Assessment

**What's Working**:
- ✅ Core validation engine is solid
- ✅ Conflict detection finds real issues
- ✅ Markdown syntax validation is accurate

**What Needs Work**:
- ⚠️ Too much noise (trailing whitespace drowns out critical issues)
- ⚠️ No exclusion patterns (forces validation of all .md files)
- ⚠️ Auto-fix is incomplete (doesn't handle filenames, frontmatter)
- ⚠️ No bulk operations for migrations

### User Experience Friction Points

Based on two tests, users would likely struggle with:

1. **"Why is README.md failing?"** → Need exclusion patterns
2. **"I have 50 docs missing 'status', now what?"** → Need bulk frontmatter tool
3. **"How do I safely rename files with spaces?"** → Need link-aware auto-fix
4. **"I can't find the critical errors in all this whitespace noise"** → Need severity filtering

---

## Success Metrics (Revised)

If NEW gaps are addressed:

- **70% reduction** in false positives (README exclusions)
- **90% faster** bulk migrations (frontmatter bulk-add tool)
- **80% safer** filename fixes (link-aware auto-fix)
- **50% fewer** "how do I..." support questions

---

## Competitive Advantage Analysis

After two folder tests, Symphony Core's **unique differentiators** are:
1. **Conflict detection** (pricing, dates, specs) - no other tool does this
2. **Frontmatter schema validation** - most tools only lint markdown syntax
3. **Business-focused** (not just code documentation)

But to compete on UX, we need:
- ✅ Exclusion patterns (Vale has this, we don't)
- ✅ Bulk operations (DocFX has this, we don't)
- ✅ Smart auto-fix (Markdownlint has partial, we need full)

---

## Recommendations for Next Folders

When testing additional folders:
1. Look for **new patterns** (e.g., date conflicts, specification conflicts)
2. Track **issue frequency** (which issues appear in ALL folders?)
3. Identify **folder-specific issues** (e.g., 02-marketing-brand had filename spaces)
4. Build **priority matrix** based on frequency + impact

---

**Document Owner**: Product Manager
**Review Type**: New Insights from 02-marketing-brand Test
**Status**: READY FOR BACKLOG INTEGRATION
