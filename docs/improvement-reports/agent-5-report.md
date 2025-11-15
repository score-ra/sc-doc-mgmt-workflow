# Agent 5 Report: Remaining Directories

**Repository:** symphony-core-documents
**Analysis Date:** 2025-11-15
**Analyst:** Agent 5
**Scope:** 07-customer-education/, 08-reference/, 09-clients/, 10-people-operations/, _inbox/, _meta/, and root directory

## Summary

- **Docs analyzed:** 217 markdown files
- **Total issues:** 85+
  - **P0 (Critical):** 8 issues
  - **P1 (High ROI):** 42 issues
  - **P2 (Medium ROI):** 25 issues
  - **P3 (Low ROI):** 10+ issues

## P0: Critical

### Issue 1: Filename Violations - Spaces in Filenames (7 files)

**Files affected:**
- `/08-reference/platforms/Extendly/training-docs/automation ecosystem map.md`
- `/08-reference/platforms/Extendly/training-docs/custom value flow.md`
- `/08-reference/platforms/Extendly/training-docs/extendly snapshot training overview.md`
- `/08-reference/platforms/Extendly/training-docs/complete customer journey map.md`
- `/08-reference/platforms/Extendly/training-docs/the big 5 core modules.md`
- `/08-reference/platforms/Extendly/training-docs/simplified 4 stage journey.md`
- `/08-reference/platforms/Extendly/training-docs/meeting status update form - the hub.md`

**Issue:** Filenames contain spaces, violating SC Document Naming Standard

**Fix:** Rename to lowercase-with-hyphens:
- `automation ecosystem map.md` → `automation-ecosystem-map.md`
- `custom value flow.md` → `custom-value-flow.md`
- `extendly snapshot training overview.md` → `extendly-snapshot-training-overview.md`
- `complete customer journey map.md` → `complete-customer-journey-map.md`
- `the big 5 core modules.md` → `the-big-5-core-modules.md`
- `simplified 4 stage journey.md` → `simplified-4-stage-journey.md`
- `meeting status update form - the hub.md` → `meeting-status-update-form-the-hub.md`

**ROI:** High - Prevents git conflicts, CLI tool errors, and automation failures. Estimated fix time: 15 minutes.

---

### Issue 2: Duplicate YAML Frontmatter

**File:** `/08-reference/glossary/glossary-guidelines.md`

**Issue:** File contains TWO separate frontmatter blocks (lines 1-6 and lines 9-17), causing invalid YAML structure

**Current state:**
```yaml
---
title: Symphony Core Glossary Guidelines
tags:
- general
status: draft
---

---
title: Symphony Core Glossary Guidelines
version: 1.0
author: Symphony Core Systems Team
last_updated: 2025-09-27
category: Guidelines
tags: [glossary, guidelines, standards, maintenance, format]
status: approved
---
```

**Fix:** Remove first (incomplete) frontmatter block; keep only the complete second block

**ROI:** High - Fixes syntax error that breaks automated parsing. Estimated fix time: 2 minutes.

---

### Issue 3: Missing YAML Frontmatter

**File:** `/08-reference/quick-reference/symphony-core-ai-context-summary.md`

**Issue:** No YAML frontmatter at all - file starts with markdown title

**Fix:** Add complete YAML frontmatter:
```yaml
---
title: Symphony Core Business Summary
version: 1.0
author: Symphony Core Systems Team
last_updated: 2025-11-15
category: reference
tags: [business-summary, ai-context, company-info, quick-reference]
status: active
audience: internal-team
---
```

**ROI:** High - Makes file compliant with SC Markdown Standard and enables automated indexing. Estimated fix time: 5 minutes.

---

## P1: High ROI

### Issue 4: Incomplete Frontmatter - Missing Required Fields

**Files affected:** 15+ files

**Sample files:**
- `/08-reference/platforms/GHL/user-training-ghl-info.md` - Missing version, author, last_updated, category
- `/home/user/symphony-core-documents/CLAUDE.md` - Missing version, author, last_updated, category
- `/_inbox/README.md` - Missing ALL frontmatter
- `/_meta/README.md` - Missing ALL frontmatter
- `/09-clients/README.md` - Missing version field

**Issue:** Files missing required frontmatter fields per SC Markdown Standard

**Required fields:**
- title
- version
- author
- last_updated
- category
- tags (2-6 tags)
- status

**Fix:** Add all required fields to each file

**ROI:** High - Enables automated workflows, indexing, and document lifecycle tracking. Estimated fix time: 2-3 hours for all files.

---

### Issue 5: Tagging Violations - Too Few Tags

**Files affected:** 5+ files

**Examples:**
- `/08-reference/analysis/seo-one-time-setup-roi-analysis.md` - Only 1 tag (minimum is 2)

**Fix:** Add tags to meet 2-6 tag requirement:
- Current: `[roi-analysis]`
- Recommended: `[seo, roi-analysis, reference, pricing-strategy]`

**ROI:** High - Improves discoverability and automated categorization. Estimated fix time: 30 minutes.

---

### Issue 6: Tagging Violations - Non-Standard Tags

**Files affected:** 20+ files

**Examples:**
- `/08-reference/quick-reference/data-repository.md` - Uses `test-data` and `google-drive` (not in standard vocabulary)
- `/09-clients/README.md` - Uses `deliverables` (not standard)
- `/10-people-operations/README.md` - Uses `people-ops` and `hr` (not standard)

**Fix:** Replace with SC Tagging Standard compliant tags:
- `/08-reference/quick-reference/data-repository.md`: `[reference, platform, data-management, testing]`
- `/09-clients/README.md`: `[clients, templates, reference, operations]`
- `/10-people-operations/README.md`: `[operations, hiring, onboarding, templates]`

**ROI:** High - Ensures consistency across repository and enables reliable automated filtering. Estimated fix time: 1-2 hours.

---

### Issue 7: Improper Status Values

**Files affected:** 10+ files

**Examples:**
- Multiple glossary files using `draft` when should be `active`
- `/08-reference/glossary/glossary-guidelines.md` - First frontmatter shows `draft`, second shows `approved` (conflict)
- `/_inbox/README.md` - Missing status field
- `/home/user/symphony-core-documents/CLAUDE.md` - Using `draft` when should be `active`

**Valid status values:**
- `draft` - Work in progress
- `active` - Current, in use
- `review` - Under review
- `archived` - Historical reference
- `deprecated` - No longer valid

**Fix:** Update status values to match document state

**ROI:** High - Correct status affects automated workflows and document lifecycle tracking. Estimated fix time: 45 minutes.

---

### Issue 8: Missing Audience Field

**Files affected:** 50+ files

**Examples:**
- `/08-reference/glossary/pages/*.md` files - Should have `audience: internal-team`
- `/09-clients/*/client-profile.md` files - Should have `audience: internal-team`
- Platform documentation in `/08-reference/platforms/` - Should have `audience: internal-technical`

**Audience values:**
- `internal-team` - General team docs
- `internal-technical` - Technical implementation
- `customers` - Customer-facing
- `executives` - Leadership docs

**Fix:** Add `audience` field to frontmatter

**ROI:** High - Enables automated routing and improves document organization. Estimated fix time: 2-3 hours.

---

### Issue 9: Deprecated Files Without Proper Metadata

**Files affected:** 5+ deprecated files

**Good examples (properly deprecated):**
- `/08-reference/platforms/Extendly/training-docs/extendly snapshot training overview.md` - Has `deprecated_date` and `superseded_by`
- `/08-reference/platforms/Extendly/training-docs/complete customer journey map.md` - Proper deprecation notice

**Issue:** Some deprecated files lack proper deprecation metadata

**Required metadata for deprecated files:**
```yaml
status: deprecated
deprecated_date: YYYY-MM-DD
superseded_by: "path/to/new/document.md"
```

**Fix:** Add deprecation metadata to all deprecated files

**ROI:** High - Prevents confusion and guides users to current documentation. Estimated fix time: 1 hour.

---

## P2: Medium ROI

### Issue 10: Missing Table of Contents

**Files affected:** 4+ files >500 lines

**Examples:**
- `/home/user/symphony-core-documents/symphony-core-documentation-architecture.md` - 1,484 lines, no TOC
- `/08-reference/platforms/GHL/industry-capabilities/commercial-real-estate-ct.md` - 702 lines, no TOC
- `/08-reference/quick-reference/symphony-core-ai-context-summary.md` - ~260 lines (borderline)
- `/08-reference/platforms/GHL/user-training-ghl-info.md` - ~270 lines (borderline)

**SC Markdown Standard:** Documents >500 lines should include TOC

**Fix:** Add TOC after frontmatter:
```markdown
## Table of Contents

1. [Purpose](#purpose)
2. [Main Section](#main-section)
   - [Subsection](#subsection)
3. [Related Documents](#related-documents)
```

**ROI:** Medium - Improves navigation in long documents. Estimated fix time: 1-2 hours.

---

### Issue 11: Heading Hierarchy Violations

**Files affected:** 15+ files

**Issue:** Files skip heading levels (e.g., H1 → H3 without H2)

**Affected areas:**
- Glossary pages in `/08-reference/glossary/pages/`
- Platform documentation in `/08-reference/platforms/`
- Various files with inconsistent heading patterns

**SC Markdown Standard:** Never skip heading levels

**Fix:** Audit heading structure; ensure proper hierarchy

**ROI:** Medium - Improves accessibility and document structure. Estimated fix time: 2-3 hours.

---

### Issue 12: Missing Required Sections

**Files affected:** 30+ files

**Missing sections:**
- **Purpose** section - Required by SC Markdown Standard, missing in many files
- **Scope** section - Required by standard, missing in many files
- **Related Documents** section - Recommended, rarely present
- **Revision History** - Recommended for SOPs, often missing

**Fix:** Add required sections per SC Markdown Standard template

**ROI:** Medium - Improves document quality and consistency. Estimated fix time: 4-6 hours.

---

### Issue 13: Inconsistent Link Formats

**Files affected:** 20+ files

**Issue:** Mix of absolute and relative links; some broken cross-references

**Examples:**
- Some files use `../../folder/file.md` (relative)
- Others use full paths `/folder/file.md` (absolute)
- Broken links in deprecated files pointing to moved content

**Fix:**
- Standardize on relative links for internal documentation
- Validate all links (use automated link checker)
- Update deprecated file links to point to superseding content

**ROI:** Medium - Reduces broken links and improves maintainability. Estimated fix time: 3-4 hours.

---

### Issue 14: Code Blocks Without Language Specification

**Files affected:** 25+ files

**Issue:** Code blocks without language identifiers harm syntax highlighting

**Example violations:**
````markdown
```
code here without language
```
````

**Should be:**
````markdown
```yaml
code here with language
```
````

**Fix:** Add language identifiers (yaml, bash, python, javascript, etc.) to all code blocks

**ROI:** Medium - Improves readability and code presentation. Estimated fix time: 2-3 hours.

---

### Issue 15: Incorrect Date Formats

**Files affected:** 10+ files

**Issue:** Some files use inconsistent date formats

**Required format per SC Markdown Standard:** `YYYY-MM-DD`

**Fix:** Validate all date fields use YYYY-MM-DD format

**ROI:** Medium - Ensures consistency and enables automated date parsing. Estimated fix time: 1 hour.

---

### Issue 16: Files in Wrong Directories

**Files affected:** 20+ files in `_inbox/`

**Issue:** Content appears misplaced based on repository architecture

**Examples:**
- `/_inbox/seo-services/` - Large directory tree in inbox should be processed and moved
- Files marked as `active` still in `_inbox/` - should be in permanent locations
- Some client files in wrong subdirectories

**Fix:** Review `_inbox/` and move all `status: active` or `status: approved` files to permanent locations per routing logic

**ROI:** Medium - Improves organization and findability. Estimated fix time: 3-4 hours.

---

## P3: Low ROI

### Issue 17: Inconsistent List Formatting

**Files affected:** 50+ files

**Issue:** Mix of `-`, `*`, and `+` for bullet lists within same repository

**SC Markdown Standard:** Use `-` for unordered lists consistently

**Fix:** Standardize all lists to use `-`

**ROI:** Low - Minor visual inconsistency. Estimated fix time: Ongoing during normal edits.

---

### Issue 18: Inconsistent Spacing

**Files affected:** Many files

**Issue:** Varying amounts of blank lines between sections

**Fix:** Enforce consistent spacing in linting rules; fix gradually

**ROI:** Low - Cosmetic issue. Estimated fix time: Ongoing during normal edits.

---

### Issue 19: Missing Alt Text on Images

**Files affected:** 15+ files with images

**Issue:** Mermaid diagrams and some images lack descriptive text

**Fix:** Add descriptive alt text to all images

**ROI:** Low - Accessibility improvement. Estimated fix time: 1-2 hours.

---

### Issue 20: YAML Frontmatter Formatting Inconsistencies

**Files affected:** Many files

**Issue:** Some files use array format `tags: [tag1, tag2]`, others use list format:
```yaml
tags:
- tag1
- tag2
```

**Both are valid YAML** but inconsistent presentation

**Fix:** Standardize on array format for conciseness

**ROI:** Low - Cosmetic issue. Estimated fix time: Ongoing during normal edits.

---

## Recommended Action Plan

### Immediate Actions (P0 - Critical)

**Estimated time:** 30 minutes
**Impact:** Fixes critical errors preventing automation

1. Rename 7 files with spaces in Extendly training-docs
2. Fix duplicate frontmatter in `glossary-guidelines.md`
3. Add missing frontmatter to `symphony-core-ai-context-summary.md`

### Phase 1 (P1 - High ROI)

**Estimated time:** 8-12 hours
**Impact:** Enables full automation and improves discoverability

1. Add complete frontmatter to all files missing required fields
2. Review and fix all tags against SC Tagging Standard
3. Correct status values to use only approved values
4. Add audience field to files for better routing
5. Ensure deprecated files have proper deprecation metadata

### Phase 2 (P2 - Medium ROI)

**Estimated time:** 15-20 hours
**Impact:** Improves document quality and user experience

1. Add TOCs to files >500 lines
2. Fix heading hierarchy violations
3. Add required sections (Purpose, Scope) to non-compliant files
4. Validate and fix all links
5. Add language specs to code blocks
6. Move files from `_inbox/` to permanent locations

### Phase 3 (P3 - Polish)

**Estimated time:** Ongoing maintenance
**Impact:** Cosmetic improvements

1. Standardize list formatting
2. Normalize spacing
3. Add image alt text
4. Standardize YAML formatting
5. Document versioning strategy

### Total estimated time: 25-35 hours

---

## Automation Recommendations

To prevent future issues and reduce manual effort:

1. **Link Validator:** Implement automated link checking (e.g., markdown-link-check)
2. **Frontmatter Validator:** Script to check all required fields present
3. **Filename Validator:** Pre-commit hook to prevent spaces in filenames
4. **Tag Vocabulary Enforcer:** Validate tags against SC Tagging Standard
5. **Markdown Linter:** Enforce consistent formatting (markdownlint)

---

## Positive Observations

**What's working well:**

1. **Deprecation Notices:** Files in Extendly training-docs properly deprecated with clear superseded_by references
2. **Comprehensive Standards:** SC Markdown Standard, SC Tagging Standard, and SC Document Naming Standard are well-documented
3. **Architecture Documentation:** Repository architecture is well-defined in `symphony-core-documentation-architecture.md`
4. **Most Files Compliant:** Majority of files have valid frontmatter and follow conventions
5. **Good README Structure:** Most directories have helpful README files explaining purpose and contents

---

## Conclusion

The symphony-core-documents repository shows strong adherence to documentation standards overall. The 85+ issues identified represent systematic improvements that will enhance automation capabilities, discoverability, and consistency. Prioritizing P0 and P1 issues will deliver the highest ROI, with an estimated 10-15 hours of focused work to address critical and high-priority issues.

**Next Steps:**
1. Review and approve this report
2. Create issues/tasks for P0 and P1 items
3. Implement automation recommendations to prevent regression
4. Schedule systematic cleanup of P2 and P3 issues

---

**Report generated by:** Agent 5
**Date:** 2025-11-15
**Analysis scope:** 217 markdown files across 7 target directories
