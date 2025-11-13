# Symphony Core Product Backlog
## Tracking Approved Tool Improvements

**Last Updated**: 2025-11-13
**Current Version**: v1.0.0
**Next Release**: v1.1.0 (TBD)

---

## Backlog Status

| Status | Description | Count |
|--------|-------------|-------|
| 🟢 APPROVED | User approved, ready for development | 0 |
| 🟡 PROPOSED | Awaiting user approval | 9 |
| 🔵 IN PROGRESS | Currently being implemented | 0 |
| ✅ COMPLETED | Shipped in a release | 0 |

---

## 🟡 PROPOSED ITEMS (Awaiting Approval)

### High Priority

#### PB-001: Add Line Numbers to Conflict Reports
- **Status**: 🟡 PROPOSED
- **Priority**: P0 (Critical)
- **Sprint**: Sprint 7
- **Effort**: 2 days
- **User Story**: As a content contributor, I need to see exactly where pricing conflicts occur (with line numbers), so I can fix them quickly without searching through 500+ line documents.
- **Current Gap**: Conflict reports only show document names and conflict values, no line numbers or section references
- **Acceptance Criteria**:
  - [ ] Conflict reports include line numbers for each detected conflict
  - [ ] Line numbers link to specific file locations (if format supports it)
  - [ ] Section headers are included in conflict context
  - [ ] Works for all conflict types (pricing, dates, specs, etc.)
- **Testing Plan**: Re-run on `01-strategy` and verify line numbers match actual conflict locations
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-002: Implement Severity-Based Filtering (`--min-severity`)
- **Status**: 🟡 PROPOSED
- **Priority**: P0 (Critical)
- **Sprint**: Sprint 7
- **Effort**: 1 day
- **User Story**: As a documentation manager running daily checks, I want to see only ERROR/WARNING issues by default, so I can focus on critical problems without INFO noise.
- **Current Gap**: 283 INFO-level violations dominate reports, burying critical errors
- **Acceptance Criteria**:
  - [ ] Add `--min-severity [ERROR|WARNING|INFO]` CLI flag
  - [ ] Add `reporting.min_severity` config option
  - [ ] Default behavior unchanged (show all severities)
  - [ ] Report header indicates if filtering is active
  - [ ] Summary statistics still show all severities (filtered display only)
- **Testing Plan**: Run with `--min-severity WARNING` on 01-strategy and verify 283 INFO issues are hidden but counted
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-003: Frontmatter Completeness Detection
- **Status**: 🟡 PROPOSED
- **Priority**: P0 (Critical)
- **Sprint**: Sprint 7
- **Effort**: 2 days
- **User Story**: As a QA tester, I need to know which documents lack frontmatter entirely, so I can ensure all documents meet SC compliance standards.
- **Current Gap**: Tool only validates existing frontmatter, doesn't report MISSING frontmatter
- **Acceptance Criteria**:
  - [ ] Report shows count of documents missing frontmatter
  - [ ] List specific documents without frontmatter
  - [ ] Distinguish between "missing" vs "invalid" frontmatter
  - [ ] Add severity level for missing frontmatter (WARNING)
  - [ ] Add auto-fix option to generate stub frontmatter
- **Testing Plan**: Create test docs with/without frontmatter, verify detection accuracy
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-004: Smart Pricing Conflict Detection
- **Status**: 🟡 PROPOSED
- **Priority**: P1 (High)
- **Sprint**: Sprint 8
- **Effort**: 5 days
- **User Story**: As a documentation manager, I want pricing conflict detection to understand tier structures, so I only get alerted to genuine pricing inconsistencies, not false positives from pricing tables.
- **Current Gap**: Flags legitimate pricing tiers as conflicts (e.g., $199/$299/$500 for Starter/Pro/Enterprise)
- **Acceptance Criteria**:
  - [ ] Detect pricing tier labels (Starter, Pro, Enterprise, Basic, etc.)
  - [ ] Only flag conflicts if same tier has multiple prices
  - [ ] Add config option: `conflict_detection.pricing.mode: smart|strict`
  - [ ] Show pricing as table in report (tier → price mapping)
  - [ ] Support custom tier name patterns in config
- **Testing Plan**: Create test doc with pricing table + intentional conflict, verify smart mode catches only real conflict
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-005: Bulk Auto-Fix Preview Workflow
- **Status**: 🟡 PROPOSED
- **Priority**: P1 (High)
- **Sprint**: Sprint 8
- **Effort**: 5 days
- **User Story**: As a documentation manager, I want to preview and selectively apply auto-fixes across multiple documents, so I can safely fix bulk issues without breaking document structure.
- **Current Gap**: `--auto-fix` is all-or-nothing, no preview or selective application
- **Acceptance Criteria**:
  - [ ] `--auto-fix --preview` shows proposed changes without applying
  - [ ] Interactive mode: prompt user to approve/reject fix categories
  - [ ] Non-interactive mode: `--auto-fix --approve-all` for CI/CD
  - [ ] Generate diff view showing before/after changes
  - [ ] Support rollback: create backup before applying fixes
- **Testing Plan**: Run `--auto-fix --preview` on 01-strategy, verify 283 whitespace fixes are shown correctly
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

### Medium Priority

#### PB-006: Cross-Document Conflict Detection
- **Status**: 🟡 PROPOSED
- **Priority**: P2 (Medium)
- **Sprint**: Sprint 9
- **Effort**: 7 days
- **User Story**: As a content contributor, I need to see when the same pricing tier has different values across multiple documents, so I can ensure consistency across versions.
- **Current Gap**: Conflicts only detected within single documents, not across document boundaries
- **Acceptance Criteria**:
  - [ ] Compare pricing/dates/specs across all documents in scan
  - [ ] Flag inconsistencies between documents (e.g., draft-0 vs draft-1.0)
  - [ ] Show document names, values, and last-updated dates in report
  - [ ] Add config option to ignore archived/deprecated docs
  - [ ] Support tagging "source of truth" document per topic
- **Testing Plan**: Create 3 docs with conflicting pricing, verify cross-doc detection works
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-007: Progress Indicators for Large Scans
- **Status**: 🟡 PROPOSED
- **Priority**: P2 (Medium)
- **Sprint**: Sprint 9
- **Effort**: 2 days
- **User Story**: As a documentation manager scanning 100+ documents, I want to see real-time progress, so I know the tool is working and estimate completion time.
- **Current Gap**: No progress feedback during scan (not an issue for 10 docs, critical for 100+)
- **Acceptance Criteria**:
  - [ ] Show progress bar: `Processing: [████████░░] 80/100 documents`
  - [ ] Display current document being processed
  - [ ] Show estimated time remaining
  - [ ] Support both console and CI/CD-friendly output modes
  - [ ] Suppress progress bar when `--quiet` flag is used
- **Testing Plan**: Run on 100+ document corpus, verify progress updates every second
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

### Low Priority

#### PB-008: HTML Report Output
- **Status**: 🟡 PROPOSED
- **Priority**: P3 (Low)
- **Sprint**: Backlog
- **Effort**: 5 days
- **User Story**: As a documentation manager presenting results to leadership, I want an interactive HTML report with clickable file links, so stakeholders can explore findings easily.
- **Current Gap**: Only markdown/JSON/console output, no browsable HTML report
- **Acceptance Criteria**:
  - [ ] Add `--format html` option
  - [ ] Generate self-contained HTML file (CSS inline)
  - [ ] Include clickable file:// links to source documents
  - [ ] Support collapsible sections for long reports
  - [ ] Match branding/style of other SC reports
- **Testing Plan**: Generate HTML report for 01-strategy, verify all links work and styling is consistent
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

#### PB-009: Incremental Scan Status in Reports
- **Status**: 🟡 PROPOSED
- **Priority**: P3 (Low)
- **Sprint**: Backlog
- **Effort**: 1 day
- **User Story**: As a QA tester, I want to know if a scan was incremental or full, so I can understand cache effectiveness and performance.
- **Current Gap**: Reports don't indicate if cache was used or if full scan occurred
- **Acceptance Criteria**:
  - [ ] Add to report header: "Scan Type: Incremental (3 changed, 7 cached)"
  - [ ] Show time saved vs. full scan estimate
  - [ ] Include cache hit rate in verbose mode
  - [ ] Flag documents that were skipped due to cache
- **Testing Plan**: Run incremental scan after changing 2 docs, verify report shows cache stats
- **Related Issues**: Identified in 01-strategy QA test (2025-11-13)

---

## 🟢 APPROVED ITEMS (Ready for Development)

_No items approved yet. Move items here after user approval._

---

## 🔵 IN PROGRESS

_No items in progress._

---

## ✅ COMPLETED

_No items completed in this backlog cycle._

---

## Approval Process

To approve an item for development:
1. Review the proposed item details (user story, acceptance criteria, effort)
2. Confirm priority and sprint assignment
3. Move item from 🟡 PROPOSED → 🟢 APPROVED
4. Update status to 🔵 IN PROGRESS when work begins
5. Move to ✅ COMPLETED when shipped and tested

---

## Notes for Development

- All proposed items stem from **01-strategy QA test** (2025-11-13)
- Effort estimates assume 1 developer, full-time work
- Sprint assignments are recommendations, adjust based on team capacity
- All items include testing plans to validate fixes

---

## Next Steps

1. **Review this backlog** with user to approve/reject/reprioritize items
2. **Start Sprint 7** planning if high-priority items are approved
3. **Re-test 01-strategy** after Sprint 7 to validate improvements
4. **Expand testing** to additional folders (02-marketing-brand, 03-operations, etc.)

---

**Document Owner**: Product Manager
**Backlog Status**: DRAFT (awaiting user review)
