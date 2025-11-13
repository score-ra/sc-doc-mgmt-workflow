# Product Manager Review: Symphony Core Capability Gaps

**Review Date**: 2025-11-13
**Reviewed By**: Product Manager (Claude)
**Test Scenario**: 01-strategy folder documentation scan
**Current Version**: Symphony Core v1.0.0

---

## Context

After running Symphony Core CLI on real-world documentation (`01-strategy` folder), several capability gaps emerged that would significantly improve the tool's effectiveness for documentation teams. This review focuses on **tool improvements**, not documentation quality issues.

---

## Capability Gaps Identified

### 🔴 HIGH PRIORITY

#### 1. **Intelligent Pricing Conflict Detection**

**Current Behavior**:
- Flags "$199, $299, $500" as conflicts even when they represent different pricing tiers
- Cannot distinguish between legitimate variance (multiple tiers) vs. true conflicts (same tier, different prices)
- No context about whether prices are draft/final/historical

**Gap**:
- No semantic understanding of pricing tier names (Starter, Pro, Enterprise)
- Reports false positives for documents with pricing tables
- Wastes reviewer time investigating non-issues

**Proposed Enhancement**:
```yaml
# New config option
conflict_detection:
  pricing:
    mode: "smart"  # vs "strict"
    ignore_if_labeled: true  # Ignore if prices have tier labels like "Starter: $199"
    report_format: "table"  # Show pricing as table with tier → price mapping
    threshold: 2  # Only flag if same tier has 2+ different prices
```

**User Story**:
> As a documentation manager, I want pricing conflict detection to understand tier structures, so I only get alerted to genuine pricing inconsistencies, not false positives from pricing tables.

**Impact**: **HIGH** - Reduces noise, increases trust in conflict detection

---

#### 2. **Line Number References in Conflict Reports**

**Current Behavior**:
- Conflict report says: "Pricing conflict for 'general': $199.00/mo, $299.00/mo, $500.00/mo"
- No indication of WHERE in the document these prices appear
- Reviewer must manually search through entire document

**Gap**:
- No line numbers or section headers referenced
- No "jump to conflict" links or file paths with line numbers

**Proposed Enhancement**:
```markdown
### PRICING CONFLICT

**Document**: `symphony-core-business-plan-draft-0.md`

| Tier | Price | Location |
|------|-------|----------|
| general | $199.00/mo | Line 142 (## Pricing Strategy) |
| general | $299.00/mo | Line 287 (## Revenue Projections) |
| general | $500.00/mo | Line 412 (## Financial Appendix) |

**Quick Fix**: Click to view → `file:///.../draft-0.md:142`
```

**User Story**:
> As a content contributor, I need to see exactly where pricing conflicts occur (with line numbers), so I can fix them quickly without searching through 500+ line documents.

**Impact**: **HIGH** - Saves 5-10 minutes per conflict resolution

---

#### 3. **Bulk Auto-Fix with Preview**

**Current Behavior**:
- `--auto-fix` flag exists but no safe bulk operation workflow
- 283 trailing whitespace issues require manual review or blind auto-fix
- No "preview → approve → apply" workflow

**Gap**:
- Cannot preview fixes before applying to 10+ documents
- No rollback mechanism if auto-fix breaks something
- All-or-nothing approach is risky for teams

**Proposed Enhancement**:
```bash
# New command workflow
python -m src.cli validate --path 01-strategy --auto-fix --preview

# Output:
# ✓ 283 trailing whitespace fixes (safe)
# ✓ 4 code block language additions (requires review)
# ⚠ 1 heading hierarchy fix (may change TOC - review recommended)
#
# Apply all? [y/n/select]
# > select
#
# [✓] Trailing whitespace (283 fixes)
# [ ] Code block languages (4 fixes)
# [✓] Heading hierarchy (1 fix)
#
# Apply selected fixes? [y/n]
```

**User Story**:
> As a documentation manager, I want to preview and selectively apply auto-fixes across multiple documents, so I can safely fix bulk issues without breaking document structure.

**Impact**: **HIGH** - Enables confident bulk operations

---

### ⚠️ MEDIUM PRIORITY

#### 4. **Frontmatter Completeness Detection**

**Current Behavior**:
- No violations reported for frontmatter (unusual for 10 docs)
- Unclear if docs have frontmatter at all or if validation is skipped

**Gap**:
- Tool doesn't report MISSING frontmatter, only invalid frontmatter
- No summary of "5 documents missing frontmatter entirely"
- Silent pass may indicate documents aren't SC-compliant

**Proposed Enhancement**:
```markdown
## Frontmatter Status

| Status | Count | Documents |
|--------|-------|-----------|
| ✅ Valid | 3 | README.md, draft-1.0.md, ueni_analysis.md |
| ⚠️ Missing | 5 | in-progress.md, ct-marketing-agencies.md, ... |
| ❌ Invalid | 2 | draft-0.md (missing 'status' field) |
```

**User Story**:
> As a QA tester, I need to know which documents lack frontmatter entirely, so I can ensure all documents meet SC compliance standards.

**Impact**: **MEDIUM** - Improves compliance visibility

---

#### 5. **Severity-Based Noise Filtering**

**Current Behavior**:
- 283 INFO-level violations (trailing whitespace) dominate report
- CRITICAL pricing conflict gets buried in noise
- No way to run "errors-only" or "warnings+" mode

**Gap**:
- Cannot filter report by severity during scan
- Report format doesn't prioritize critical issues visually
- Teams may miss urgent issues in wall of INFO logs

**Proposed Enhancement**:
```bash
# New flag
python -m src.cli validate --min-severity WARNING

# Or in config.yaml
reporting:
  min_severity: "WARNING"  # Skip INFO-level issues
  group_by: "severity"  # Show ERRORS first, then WARNINGS, then INFO
```

**User Story**:
> As a documentation manager running daily checks, I want to see only ERROR/WARNING issues by default, so I can focus on critical problems without INFO noise.

**Impact**: **MEDIUM** - Faster triage, better UX

---

#### 6. **Cross-Document Conflict Detection**

**Current Behavior**:
- Pricing conflict was detected within ONE document (draft-0.md)
- No evidence of cross-document scanning (e.g., draft-0 vs draft-1.0 pricing comparison)

**Gap**:
- Tool may not be comparing pricing across multiple documents
- No "draft-0.md says $199, but draft-1.0.md says $299 for Starter tier" detection
- Limited value for detecting version drift

**Proposed Enhancement**:
```markdown
### CROSS-DOCUMENT CONFLICT

**Type**: Pricing Mismatch
**Severity**: ERROR

| Document | Tier | Price | Last Updated |
|----------|------|-------|--------------|
| draft-0.md | Starter | $199/mo | 2025-01-15 |
| draft-1.0.md | Starter | $249/mo | 2025-02-20 |

**Recommendation**: Reconcile pricing between draft versions or deprecate older draft.
```

**User Story**:
> As a content contributor, I need to see when the same pricing tier has different values across multiple documents, so I can ensure consistency across versions.

**Impact**: **MEDIUM** - Catches version drift

---

### ℹ️ LOW PRIORITY (Nice-to-Have)

#### 7. **Progress Indicators for Large Scans**

**Gap**: No real-time progress for long-running scans (not an issue for 10 docs, but needed for 100+ docs)

**Enhancement**: Add progress bar: `Processing: [████████░░] 80/100 documents`

---

#### 8. **HTML Report Output**

**Gap**: Only markdown/JSON/console output. No interactive HTML report with clickable file links.

**Enhancement**: `--format html` generates browsable report with file:// links

---

#### 9. **Incremental Scan Status**

**Gap**: Report doesn't mention if cache was used or if full scan occurred

**Enhancement**: Add to report header:
```markdown
**Scan Type**: Incremental (3 changed, 7 cached)
**Time Saved**: ~8 seconds vs. full scan
```

---

## Prioritized Roadmap Recommendation

### Sprint 7 (Immediate - 1 week)
1. ✅ Add line numbers to conflict reports (#2)
2. ✅ Implement `--min-severity` filtering (#5)
3. ✅ Add frontmatter completeness detection (#4)

### Sprint 8 (Short-term - 2 weeks)
4. ✅ Smart pricing conflict detection (#1)
5. ✅ Bulk auto-fix preview workflow (#3)

### Sprint 9 (Medium-term - 1 month)
6. ✅ Cross-document conflict detection (#6)
7. ✅ Progress indicators for large scans (#7)

### Backlog (Future)
8. HTML report output (#8)
9. Incremental scan status in reports (#9)

---

## Success Metrics

If these gaps are addressed, we expect:
- **50% reduction** in false positive conflict alerts (smart pricing detection)
- **80% faster** conflict resolution (line number references)
- **90% adoption** of auto-fix (preview workflow increases confidence)
- **30% fewer support tickets** about "how do I know which docs are missing frontmatter"

---

## User Feedback Themes (Hypothetical)

Based on this test run, users would likely say:

> "I love the conflict detection, but it flags my pricing table as errors. Can it understand tiers?"

> "Finding the actual line with the conflict took me 15 minutes. Can you add line numbers?"

> "I'm scared to use --auto-fix on 283 issues. Can I preview first?"

---

## Competitive Analysis

How Symphony Core compares to similar tools:

| Feature | Symphony Core v1.0 | Markdownlint | Vale | DocFX |
|---------|-------------------|--------------|------|-------|
| Pricing Conflict Detection | ⚠️ Basic (false positives) | ❌ None | ❌ None | ❌ None |
| Line Numbers in Reports | ❌ Missing | ✅ Yes | ✅ Yes | ✅ Yes |
| Auto-fix Preview | ❌ Missing | ⚠️ Partial | ❌ No auto-fix | ❌ None |
| Frontmatter Missing Detection | ❌ Missing | ⚠️ Basic | ✅ Yes | ✅ Yes |
| Cross-Doc Conflict Detection | ⚠️ Unclear | ❌ None | ❌ None | ⚠️ Limited |

**Key Insight**: Symphony Core's conflict detection is unique, but needs refinement to compete with established linters on UX basics (line numbers, filtering, previews).

---

## Conclusion

Symphony Core v1.0 successfully validates documents and detects conflicts, but needs **UX refinements** to be production-ready for teams processing 50+ documents daily. The highest-value improvements are:

1. **Line number references** (quick wins, massive time savings)
2. **Smart conflict detection** (reduces noise, increases trust)
3. **Auto-fix preview** (enables safe bulk operations)

**Next Step**: Prioritize Sprint 7 enhancements and re-test with `01-strategy` folder to validate improvements.

---

**Document Owner**: Product Manager
**Review Type**: Capability Gap Analysis
**Status**: PENDING APPROVAL (awaiting user feedback)
