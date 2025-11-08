---
title: Symphony Core Document Management Workflow - Product Requirements Document
version: 2.1
author: Symphony Core Systems Team
last_updated: 2025-11-07
category: Reference
tags: [prd, project-planning, document-management, automation, workflow, business-operations]
status: approved
audience: internal-technical
---

# Product Requirements Document
## Symphony Core: Document Management Workflow

---

## 1. Executive Summary

**Product Name**: Symphony Core Document Management Workflow
**Product Vision**: Automated documentation system for business operations - ensuring consistency, quality, and standards compliance for pricing, policies, product specs, support documentation, and internal operational guides.

**One-Liner**: "Continuous document intelligence for small teams"

**Target Users**:
- Business operations team members who create and maintain markdown documentation
- Documentation managers who review and approve changes
- Product managers and team leads who contribute operational documentation

**Primary Goal**: Reduce document review time from 4 hours/week to 15-30 minutes/week

**Success Metric**:
- 100% standards compliance for all business operations documents
- Eliminate customer-facing contradictions
- Process 50+ documents in < 10 minutes

---

## 2. Problem Statement

### Current State

**Symphony Core Business Operations Documentation:**
- 50-100 markdown documents covering pricing, policies, product specifications, support guides, billing information, and operational procedures
- Documents manually added through `_inbox/` system
- Manual review of YAML frontmatter, markdown syntax, and naming conventions
- Manual filing from `_inbox/` to appropriate folders
- Updated 2-3 times per week by multiple team members
- Inconsistently tagged and organized
- No automated conflict detection
- Inconsistent standards compliance across contributors
- 10-15 minutes per document for manual processing
- Source for customer-facing information (FAQs, support articles)

### Problems & Pain Points

| Problem | Impact | Frequency | User Pain (1-10) |
|---------|--------|-----------|------------------|
| No automated conflict detection | Contradictory info reaches customers | Weekly | 9 |
| Inconsistent standards compliance | Quality varies by author | Daily | 7 |
| Manual tagging inconsistent | Can't find relevant docs quickly | Daily | 7 |
| No change tracking | Don't know what was updated | Daily | 6 |
| Time-consuming manual review | 4+ hours per week | Weekly | 8 |
| Manual document routing | Misplaced files, broken structure | Weekly | 8 |

### Root Causes
- No structured validation against standards
- No automated metadata management
- Lack of change detection mechanism
- Manual processes don't scale with growing document volume
- No systematic quality control

### Why Now?
- Document volume growing (50+ documents and increasing)
- Team bandwidth shrinking
- Customer support receiving conflicting information
- Compliance and quality requirements increasing
- Technical debt from inconsistent standards accumulating

### Impact
- **Lost Productivity**: ~5 hours/week on manual document processing
- **Quality Issues**: Inconsistent formatting, broken cross-references, contradictions
- **Poor User Experience**: Hard to find information, conflicting answers
- **Technical Debt**: Accumulated standards violations require periodic cleanup

---

## 3. Goals & Success Metrics

### Business Goals
1. **Primary**: Ensure 100% standards compliance and eliminate contradictory information
2. **Secondary**: Reduce document review time by 80%
3. **Tertiary**: Enable scalable document processing (100+ documents)

### Success Metrics (OKRs)

**Objective 1**: Ensure document quality and consistency
- KR1: 100% of documents pass validation checks
- KR2: Zero customer-reported contradictions (currently ~2/month)
- KR3: 95%+ standards compliance on first submission

**Objective 2**: Increase team efficiency
- KR1: Reduce review time from 4 hours/week → 30 minutes/week
- KR2: Process new documents in < 5 minutes
- KR3: Document processing time < 2 minutes (down from 15 minutes)

**Objective 3**: Maintain quality at scale
- KR1: Support 100+ documents without performance degradation
- KR2: < 10 minutes to process 50 documents
- KR3: API costs < $50/month

### Non-Goals (Out of Scope)
- ❌ Real-time collaboration features
- ❌ Web-based UI (CLI is sufficient for v1)
- ❌ Version control integration beyond git operations
- ❌ Multi-language documentation support
- ❌ Image/video asset processing
- ❌ Document authoring/editing tools
- ❌ Permission/access control
- ❌ Automated content generation

---

## 4. User Personas & Use Cases

### Primary Persona 1: Documentation Manager (Sarah)
- **Role**: Operations lead responsible for business documentation accuracy
- **Context**: Manages Symphony Core business operations documentation repository
- **Technical Skill**: Comfortable with command line and Git workflows
- **Goals**: Ensure consistency, quickly review changes, maintain standards, prevent contradictions from reaching customers
- **Frustrations**: Spending hours on manual validation, cross-referencing, and standards enforcement
- **Frequency**: Uses system 3-4x per week
- **Documents Managed**: Pricing, policies, product specs, support guides, billing, procedures

**User Journey**:
1. Monday morning: Reviews weekend document changes
2. Runs validation workflow to check standards compliance
3. Reviews validation reports, makes corrections
4. Re-runs to verify compliance
5. Approves documents for publication

### Primary Persona 2: Documentation Contributor (Mike)
- **Role**: Product manager or business operations team member
- **Context**: Creates and updates business operations documentation (pricing sheets, policy updates, product specifications, support guides)
- **Technical Skill**: Basic markdown knowledge, comfortable with text editors
- **Goals**: Add/update documents quickly, meet standards, avoid creating contradictions, not break existing structure
- **Frustrations**: Unsure of all standards, worried about placement, concerned about conflicting with other docs
- **Frequency**: Adds/edits 1-3 docs per week
- **Documents Created**: Product pricing, policy documents, feature specifications, support procedures

**User Journey**:
1. Creates or updates markdown doc in `_inbox/`
2. Runs validation to check compliance
3. Fixes any validation errors reported
4. Submits for review with validation passing
5. Sarah reviews and approves routing

---

## 5. Feature Requirements - Version Roadmap

### Version 1.0 - MVP: Document Validation & Standards Enforcement (P0 - Must Have)
**Timeline**: 4 weeks
**Focus**: Core validation engine only

#### Feature 1: Document Validation Engine

**Description:** Automated validation of business operations documents against Symphony Core documentation standards.

**FR-1.1: YAML Frontmatter Validation**
- System SHALL verify presence of YAML frontmatter block
- System SHALL validate required fields:
  - title (string, non-empty)
  - version (semantic version format: X.Y or X.Y.Z)
  - date (YYYY-MM-DD format)
  - tags (list of strings, non-empty)
  - status (from approved list: draft, review, approved, deprecated, active)
- System SHALL check field formats (dates as YYYY-MM-DD, status from approved list)
- System SHALL validate tag usage (list format, no redundant tags)
- System SHALL add missing YAML frontmatter with appropriate template
- System SHALL preserve existing frontmatter when present
- **Acceptance Criteria**:
  - 100% of submitted documents validated
  - Valid YAML syntax guaranteed
  - Doesn't corrupt existing frontmatter
  - Preserves document content exactly
  - < 5 second validation time per document

**FR-1.2: Markdown Syntax Validation**
- System SHALL check compliance with SC Markdown Standard (configurable)
- System SHALL verify heading hierarchy (no skipped levels)
- System SHALL validate link formats (relative paths, proper anchors)
- System SHALL check code block language specifications
- System SHALL ensure horizontal rule usage (--- not ***)
- System SHALL validate list formatting
- System SHALL check for trailing whitespace
- **Acceptance Criteria**:
  - Detects 100% of syntax violations
  - Clear error messages with line numbers
  - Completes in < 5 seconds per document

**FR-1.3: Naming Convention Validation**
- System SHALL validate lowercase-with-hyphens pattern
- System SHALL check maximum 50 character limit
- System SHALL verify descriptive, action-oriented names
- System SHALL flag version numbers in filenames
- **Acceptance Criteria**:
  - Identifies all naming violations
  - Suggests corrected names
  - Consistent enforcement across all documents

**FR-1.4: Change Detection**
- System SHALL detect new, modified, and deleted markdown files
- System SHALL use file hashing (SHA-256) to determine changes
- System SHALL maintain a cache of processed documents
- System SHALL track last processed timestamp
- **Acceptance Criteria**:
  - Detects changes within 1 second of scan
  - Handles 100+ documents efficiently
  - Cache survives system restarts
  - Atomic cache writes (no corruption on crash)

**FR-1.5: Validation Reporting**
- System SHALL generate validation reports (markdown format)
- System SHALL provide pass/fail status
- System SHALL list issues with line numbers and context
- System SHALL suggest fixes for common issues
- System SHALL categorize issues by severity (error, warning, info)
- **Acceptance Criteria**:
  - Human-readable report format
  - Actionable error messages
  - Can export to file
  - Includes auto-fix suggestions where applicable

#### Feature 2: Command Line Interface

**FR-2.1: CLI Operations**
- System SHALL provide commands for:
  - Full validation: `python main.py validate [path]`
  - Validate specific file: `python main.py validate --file [file]`
  - Force reprocess (ignore cache): `python main.py validate --force`
  - Show help: `python main.py --help`
- System SHALL provide clear progress indicators
- System SHALL return proper exit codes (0 = success, non-zero = errors)
- **Acceptance Criteria**:
  - Clear help documentation
  - Intuitive command structure
  - Progress indicators for long operations
  - Works on both Windows and Unix-like systems

**FR-2.2: Configuration Management**
- System SHALL read from config.yaml file
- System SHALL allow configuration of:
  - API key (environment variable, for future features)
  - Document directory paths
  - Output/report paths
  - Required YAML fields
  - Validation rules to enable/disable
  - Tag taxonomies (for future tagging features)
  - Allowed status values
- System SHALL validate configuration on startup
- System SHALL provide sensible defaults
- **Acceptance Criteria**:
  - Config file well-documented with examples
  - Configuration validation with clear errors
  - No hardcoded values in code
  - Easy to customize for different strictness levels

#### Feature 3: Logging & Monitoring

**FR-3.1: Activity Logging**
- System SHALL log all processing activities with timestamps
- System SHALL track processing time metrics per operation
- System SHALL log API usage and estimated costs
- System SHALL maintain separate log levels (DEBUG, INFO, WARNING, ERROR)
- System SHALL output logs to file and console (configurable)
- **Acceptance Criteria**:
  - Timestamped, structured log entries
  - API token/cost tracking
  - Performance metrics logged
  - Logs don't expose sensitive content
  - Log rotation support

---

### Version 1.1 - Enhanced Features (Post-MVP)
**Estimated Timeline**: 2-3 weeks after v1.0

#### Feature 4: Intelligent Document Routing
- AI-powered analysis to determine correct destination folder
- Content analysis (keywords, topics, document type)
- Confidence scoring (high/medium/low)
- Routing suggestions with reasoning
- Auto-route or manual approval based on confidence

#### Feature 5: Automated Tagging System
- Rule-based tagging (keyword matching) for speed
- LLM fallback tagging when confidence < 70%
- Predefined tag lists: pricing, product-specs, policies, support, billing
- Multi-tag support
- Tag validation and confidence scoring

#### Feature 6: Basic Conflict Detection
- Duplicate detection (file names, titles, content similarity)
- YAML frontmatter conflicts
- Cross-reference validation
- Broken link detection
- Simple content conflicts (contradictory definitions)

#### Feature 7: Auto-Fix Capabilities
- Automatically fix common validation issues
- Add missing YAML frontmatter
- Fix naming convention violations
- Format markdown syntax
- Update cross-references
- Preview before applying changes

---

### Version 2.0 - Advanced Features (Future)
**Estimated Timeline**: 8-12 weeks total

#### Feature 8: Semantic Conflict Detection
- AI-powered semantic understanding
- Detect contradictory pricing, dates, specifications
- Severity ratings (critical, medium, low)
- Group documents by tags for analysis
- Incremental processing (only affected groups)

#### Feature 9: FAQ Generation
- Generate 30-50 Q&A pairs from corpus
- Organize by topic/tag
- Include source document citations
- Incremental updates
- Configurable tone and length

#### Feature 10: Advanced Workflow Automation
- End-to-end workflow from `_inbox/` to final location
- Automated processing pipeline
- Notification system
- Rollback support
- Audit trail

#### Feature 11: Intelligent Content Suggestions
- Suggest missing cross-references
- Recommend related documents to link
- Identify content gaps
- Auto-generate "Related Documents" sections

---

## 6. Non-Functional Requirements

### 6.1 Performance
- **NFR-1**: Validation SHALL complete in < 5 seconds per document
- **NFR-2**: Full processing SHALL complete in < 10 minutes for 50 documents
- **NFR-3**: System SHALL handle up to 100 documents without degradation
- **NFR-4**: Memory usage SHALL stay < 500MB for typical operations

### 6.2 Reliability
- **NFR-5**: System SHALL handle API failures gracefully (retry with exponential backoff)
- **NFR-6**: System SHALL preserve data on crashes (atomic cache writes)
- **NFR-7**: System SHALL validate all inputs before processing
- **NFR-8**: System SHALL be idempotent (safe to run multiple times)
- **NFR-9**: Zero data loss or file corruption

### 6.3 Usability
- **NFR-10**: Error messages SHALL be actionable (not just stack traces)
- **NFR-11**: Setup SHALL take < 30 minutes for new team member
- **NFR-12**: Documentation SHALL include examples for common tasks
- **NFR-13**: Configuration SHALL be intuitive with clear examples and sensible defaults

### 6.4 Cost
- **NFR-14**: API costs SHALL remain under $50/month for typical usage
- **NFR-15**: System SHALL log cost per run for budgeting
- **NFR-16**: Cache results aggressively to minimize API calls

### 6.5 Maintainability
- **NFR-17**: Code SHALL follow PEP 8 style guidelines
- **NFR-18**: Functions SHALL be documented with docstrings (purpose, params, returns)
- **NFR-19**: Configuration SHALL be externalized (no hardcoded values)
- **NFR-20**: Type hints required for all function signatures
- **NFR-21**: Test coverage SHALL be > 80%

### 6.6 Security
- **NFR-22**: API keys SHALL be in environment variables (.env) only
- **NFR-23**: System SHALL not expose sensitive document content in logs
- **NFR-24**: No destructive operations without explicit approval
- **NFR-25**: Backup before modify operations

---

## 7. User Stories (Sprint-Ready for v1.0)

### Sprint 1: Foundation & Change Detection (Week 1)

```
US-1.1: As a documentation manager, I want the system to detect which
        documents changed, so I don't reprocess everything unnecessarily.

        Acceptance Criteria:
        - [ ] System identifies new files
        - [ ] System identifies modified files (content changed via hash)
        - [ ] System ignores unchanged files
        - [ ] Cache persists between runs
        - [ ] SHA-256 hashing for change detection

        Story Points: 5

US-1.2: As a developer, I want a proper project structure and configuration,
        so the codebase is maintainable and extensible.

        Acceptance Criteria:
        - [ ] Project follows src/ structure from CLAUDE.md
        - [ ] config.yaml with validation
        - [ ] .env for API keys
        - [ ] Logging utilities set up
        - [ ] Test framework configured

        Story Points: 3
```

### Sprint 2: YAML Validation (Week 2)

```
US-2.1: As a documentation manager, I want all documents to have consistent
        YAML frontmatter, so I can track metadata systematically.

        Acceptance Criteria:
        - [ ] Validates required fields (title, version, date, tags, status)
        - [ ] Checks date formats (YYYY-MM-DD)
        - [ ] Validates status from allowed list
        - [ ] Validates tags is a list
        - [ ] Adds missing frontmatter with template
        - [ ] Preserves existing frontmatter
        - [ ] Valid YAML syntax guaranteed

        Story Points: 8

US-2.2: As a documentation contributor, I want clear validation errors,
        so I know exactly how to fix my documents.

        Acceptance Criteria:
        - [ ] Error messages include line numbers
        - [ ] Clear explanation of what's wrong
        - [ ] Suggested fix provided
        - [ ] Severity levels (error, warning, info)

        Story Points: 3
```

### Sprint 3: Markdown & Naming Validation (Week 3)

```
US-3.1: As a documentation manager, I want markdown syntax validated,
        so all documents follow Symphony Core standards consistently.

        Acceptance Criteria:
        - [ ] Heading hierarchy validation
        - [ ] Link format validation (relative paths)
        - [ ] Code block language specifications
        - [ ] Horizontal rule format (---)
        - [ ] List formatting checks
        - [ ] Trailing whitespace detection
        - [ ] Configurable rules (enable/disable individual checks)

        Story Points: 8

US-3.2: As a documentation manager, I want naming conventions enforced,
        so files follow our standards automatically.

        Acceptance Criteria:
        - [ ] Lowercase-with-hyphens pattern
        - [ ] Max 50 character limit
        - [ ] No version numbers in filename
        - [ ] Descriptive name validation
        - [ ] Suggests corrected names

        Story Points: 5
```

### Sprint 4: CLI, Reporting & Polish (Week 4)

```
US-4.1: As a user, I want a friendly CLI interface,
        so I can easily run validations without reading complex docs.

        Acceptance Criteria:
        - [ ] Clear help text
        - [ ] Intuitive commands (validate, --file, --force)
        - [ ] Progress indicators
        - [ ] Proper exit codes
        - [ ] Works on Windows and Unix

        Story Points: 5

US-4.2: As a documentation manager, I want comprehensive validation reports,
        so I can quickly understand and fix issues.

        Acceptance Criteria:
        - [ ] Markdown report format
        - [ ] Summary statistics (X/Y checks passed)
        - [ ] Grouped by validation type
        - [ ] Line numbers and context
        - [ ] Suggested fixes
        - [ ] Export to file

        Story Points: 5

US-4.3: As a team lead, I want comprehensive documentation and tests,
        so new team members can contribute and trust the system.

        Acceptance Criteria:
        - [ ] README with setup instructions
        - [ ] Configuration guide with examples
        - [ ] Test coverage > 80%
        - [ ] User guide with common workflows
        - [ ] Docstrings on all functions

        Story Points: 8
```

---

## 8. Technical Architecture

### System Components (v1.0)

```
src/
├── core/
│   ├── change_detector.py      # File change detection & hashing
│   ├── validators/
│   │   ├── yaml_validator.py   # YAML frontmatter validation
│   │   ├── markdown_validator.py # Markdown syntax validation
│   │   └── naming_validator.py # Naming convention validation
│   └── validator_engine.py     # Orchestrates all validators
├── utils/
│   ├── frontmatter.py          # YAML frontmatter parsing/writing
│   ├── cache.py                # Document cache management
│   ├── logger.py               # Logging utilities
│   └── config.py               # Configuration management
├── cli.py                      # CLI interface (Click framework)
└── main.py                     # Entry point

tests/                          # Mirror src/ structure
config/
└── config.yaml                 # Main configuration
docs/                           # Documentation including this PRD
.env.example                    # Example environment variables
```

### Technology Stack

**Core Requirements:**
- Python 3.11+
- Anthropic Claude API (for future LLM features)

**Libraries:**
- `PyYAML` or `ruamel.yaml` - YAML parsing
- `python-markdown` or `markdown-it-py` - Markdown parsing
- `Click` - CLI framework
- `pathlib` - File operations
- `hashlib` - SHA-256 hashing
- `pytest` - Testing
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking

### Configuration System

**config.yaml Structure:**
```yaml
version: "1.0"

# Processing settings
processing:
  doc_directories:
    - "."
  cache_file: "_meta/.document-cache.json"
  backup_dir: "_meta/.backups/"

# Validation rules
validation:
  yaml:
    enabled: true
    required_fields:
      - title      # Document title
      - version    # Semantic version (e.g., 1.0, 1.2.1)
      - date       # Last updated date (YYYY-MM-DD)
      - tags       # List of tags
      - status     # Document status
    date_format: "YYYY-MM-DD"
    allowed_statuses:
      - draft
      - review
      - approved
      - deprecated
      - active

  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true
    relative_links_only: true
    horizontal_rule_format: "---"

  naming:
    enabled: true
    pattern: "lowercase-with-hyphens"
    max_length: 50
    no_version_numbers: true

# Reporting
reporting:
  format: "markdown"
  output_dir: "_meta/reports/"
  verbose: true

# Logging
logging:
  level: "INFO"
  file: "logs/symphony-core.log"
  console: true
```

### Integration Points

**Inputs:**
- Markdown files in configured directories
- Configuration files (config.yaml, profiles)
- Cache file (for change detection)
- Environment variables (.env for API keys - future use)

**Outputs:**
- Updated YAML frontmatter in documents
- Validation reports (markdown)
- Cache file (updated hashes)
- Processing logs
- Exit codes (0 = success, non-zero = validation failures)

---

## 9. Technical Constraints

### Must Use
- Python 3.11+ (team standard)
- Anthropic Claude API (already approved/budgeted) - for future features
- Markdown format for input/output
- Git for version control
- File-based storage (no database)

### Cannot Use
- Services requiring additional credit cards (beyond Claude API)
- Desktop GUI frameworks (CLI only for v1)
- Database systems (file-based is sufficient)
- External dependencies beyond approved Python packages

### Assumptions
- Team has Python 3.11+ experience
- Team comfortable with CLI tools
- Documents are in English
- Maximum 100 documents in v1.0
- Single repository per run (can run on multiple repos separately)
- Windows and Unix-like OS support needed

---

## 10. Dependencies & Risks

### External Dependencies
| Dependency | Risk Level | Mitigation | Status |
|------------|-----------|------------|--------|
| Anthropic API availability | Low (v1.0) | Not critical for v1.0, cache for v1.1+ | Not needed for v1.0 |
| API rate limits | Low | Batch processing, monitoring | For v1.1+ |
| API cost increases | Low | Track costs, have budget buffer | For v1.1+ |
| Python ecosystem | Low | Use stable, well-maintained libraries | Mitigated |

### Internal Dependencies
| Dependency | Owner | Due Date | Status |
|------------|-------|----------|--------|
| Sample Symphony Core docs | Team | Sprint 1 | Available |
| Sample business docs | Sarah | Sprint 1 | Available |
| SC standards documents | Team | Sprint 1 | Available |
| Tag taxonomy definition | Team | v1.1 | Not needed for v1.0 |

### Risks

| Risk | Probability | Impact | Mitigation | Phase |
|------|------------|--------|------------|-------|
| Validation accuracy below expectations | Low | Medium | Thorough testing with real docs, iterative refinement | v1.0 |
| Performance issues with 100+ docs | Low | Medium | Caching, optimization, profiling | v1.0 |
| Team adoption resistance | Low | High | Training, clear documentation, demonstrate value | v1.0 |
| Scope creep to v1.1 features | Medium | High | **Strict scope control - validation ONLY for v1.0** | v1.0 |
| Configuration complexity | Medium | Medium | Sensible defaults, clear examples, profiles | v1.0 |
| False positives in validation | Medium | Medium | Configurable rules, severity levels, manual review | v1.0 |
| API costs exceed budget (future) | Low | Medium | Cost tracking, batching, caching | v1.1+ |
| Tagging accuracy below 95% (future) | Medium | High | Hybrid approach (rules + LLM) | v1.1+ |

---

## 11. Timeline & Milestones

### Version 1.0 - MVP (4 Weeks)

| Sprint | Week | Focus | Deliverables | Story Points |
|--------|------|-------|--------------|--------------|
| Sprint 1 | Week 1 | Foundation | Project structure, config system, change detection | 8 |
| Sprint 2 | Week 2 | YAML Validation | YAML parser, validator, frontmatter management | 11 |
| Sprint 3 | Week 3 | Markdown & Naming | Markdown syntax validation, naming validation | 13 |
| Sprint 4 | Week 4 | CLI & Polish | CLI interface, reporting, documentation, testing | 18 |

**Total v1.0 Effort**: ~50 story points (~120 hours)
**Team Size**: 2-3 people
**Delivery**: End of Week 4

### Version 1.1 - Enhanced Features (Future)
**Estimated Timeline**: 2-3 weeks
**Focus**: Routing, tagging, basic conflict detection, auto-fix

### Version 2.0 - Advanced Features (Future)
**Estimated Timeline**: 4-6 weeks
**Focus**: Semantic conflict detection, FAQ generation, workflow automation

---

## 12. Success Criteria & Acceptance

### v1.0 MVP Acceptance Criteria

**Functional Completeness:**
- [ ] All v1.0 user stories implemented and tested
- [ ] Validates YAML frontmatter with all checks
- [ ] Validates markdown syntax against SC standards
- [ ] Validates naming conventions
- [ ] Change detection working with SHA-256 hashing
- [ ] CLI commands functional and documented
- [ ] Configuration system with profiles working
- [ ] Validation reports generated correctly
- [ ] Logging system operational

**Quality Gates:**
- [ ] Test coverage > 80%
- [ ] All tests passing
- [ ] Code passes flake8 linting
- [ ] Code formatted with black
- [ ] Type checking with mypy passing
- [ ] Documentation complete (README, user guide, API docs)

**Performance:**
- [ ] < 5 seconds per document validation
- [ ] < 10 minutes for 50 documents
- [ ] < 500MB memory usage

**Usability:**
- [ ] New team member can set up in < 30 minutes
- [ ] Clear error messages for all failure modes
- [ ] Help documentation comprehensive

**Production Readiness:**
- [ ] Deployed and working on test documents
- [ ] Team trained on usage
- [ ] No critical bugs
- [ ] Rollback plan tested

---

## 13. Open Questions

### v1.0 Decisions Needed:
- [ ] Should validation automatically fix issues or only report them? (Proposal: Report only for v1.0, auto-fix in v1.1)
- [ ] Should system fail (exit code 1) on warnings or only on errors? (Proposal: Configurable)
- [ ] How to handle documents that legitimately can't follow all standards? (Proposal: Allow .no-validate marker file)
- [ ] Should validation reports be committed to git or gitignored? (Proposal: Gitignored, in _meta/reports/)

### Future Considerations (v1.1+):
- [ ] What should happen to manually edited FAQs? Preserve or overwrite?
- [ ] Should we notify users of conflicts via email/Slack?
- [ ] What's the process for adding new tags to the taxonomy?
- [ ] Should the system auto-commit changes back to Git?
- [ ] Do we need audit logs for compliance?
- [ ] Integration with GitHub Actions or run locally only?

---

## 14. Appendices

### Appendix A: HTTP Server vs. Windows Share Question

**Context from User**: "Explain the benefit of setting up http server vs. creating a windows share for this context"

**Answer for Symphony Core Document Workflow:**

For this document management workflow system, **neither an HTTP server nor a Windows share is recommended**. Here's why:

**Recommended Approach: Local CLI Tool**
- The system is designed as a CLI tool that runs locally on the user's machine
- Documents are stored in a Git repository (local or remote)
- Users run validation commands against local file paths
- Reports are generated locally

**Why Not HTTP Server?**
- Unnecessary complexity for a CLI tool
- Requires server infrastructure and maintenance
- Doesn't align with Git-based workflow
- Adds authentication/security concerns
- Not needed for 2-3 person team

**Why Not Windows Share?**
- Cross-platform requirement (Windows + Unix-like systems)
- Git already handles document sharing/synchronization
- Windows shares have permission complexity
- Network latency for file access
- Poor version control integration

**What You Should Use:**
1. **Git repository** (local or remote on GitHub/GitLab)
   - Native version control
   - Existing team familiarity
   - Pull/push workflow

2. **CLI tool runs locally** against repository
   - Fast file access
   - No network dependency
   - Simple setup

3. **Reports can be shared via:**
   - Committed to `_meta/reports/` (gitignored or not, configurable)
   - Slack/email notifications (future feature)
   - Shared folder if needed (but not primary mechanism)

**Future Consideration:** If you wanted a dashboard to view validation results, a simple static site generator (reading report files) would be better than an HTTP server for running the tool itself.

---

### Appendix B: Sample Validation Report

```markdown
# Document Validation Report

**Document:** `docs/new-feature-guide.md`
**Processed:** 2025-11-07 10:30:00
**Mode:** Symphony Core
**Status:** ⚠️ ISSUES FOUND

---

## Summary

- **YAML Frontmatter:** 6/7 checks passed (1 error)
- **Markdown Syntax:** 8/8 checks passed
- **Naming Convention:** 2/3 checks passed (1 error)

**Overall:** ❌ VALIDATION FAILED (2 errors, 0 warnings)

---

## ✅ YAML Frontmatter (6/7 checks passed)

- ✅ YAML block present
- ✅ Required fields present: title, version, author, last_updated, category, tags, status
- ❌ **ERROR:** Date format incorrect
  - **Field:** `last_updated`
  - **Current:** `11/07/2025`
  - **Expected:** `2025-11-07` (YYYY-MM-DD format)
  - **Line:** 5
  - **Severity:** ERROR

- ✅ Status value valid: "draft"
- ✅ Tags valid: ["feature", "implementation"]
- ✅ Category valid: "Guide"
- ✅ Version format valid: "1.0"

---

## ✅ Markdown Syntax (8/8 checks passed)

- ✅ Heading hierarchy correct (H1 → H2 → H3)
- ✅ No skipped heading levels
- ✅ Code blocks have language specified
- ✅ Links use relative paths
- ✅ Horizontal rules use `---` format
- ✅ No bare URLs (all links formatted)
- ✅ Lists properly formatted
- ✅ No trailing whitespace

---

## ⚠️ Naming Convention (2/3 checks passed)

- ❌ **ERROR:** Uppercase letters in filename
  - **Current:** `New-Feature-Guide.md`
  - **Expected:** `new-feature-guide.md`
  - **Severity:** ERROR
  - **Suggested Action:** Rename file to `new-feature-guide.md`

- ✅ Length within limit (21/50 characters)
- ✅ No version numbers in filename

---

## Actions Required

1. **Fix date format** in YAML frontmatter (line 5)
   ```yaml
   # Change from:
   last_updated: 11/07/2025

   # To:
   last_updated: 2025-11-07
   ```

2. **Rename file** to lowercase
   ```bash
   git mv docs/New-Feature-Guide.md docs/new-feature-guide.md
   ```

3. **Re-run validation** after fixes:
   ```bash
   python main.py validate --file docs/new-feature-guide.md
   ```

---

**Exit Code:** 1 (validation failed)
**Report Generated:** 2025-11-07 10:30:15
**Processing Time:** 2.3 seconds
```

---

### Appendix C: Configuration Customization Examples

**Strict Validation (Default):**
```yaml
validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - version
      - date
      - tags
      - status
  markdown:
    enabled: true
    enforce_heading_hierarchy: true
    require_language_in_code_blocks: true
  naming:
    enabled: true
    max_length: 50
```

**Lenient Validation (For Migration/Legacy Docs):**
```yaml
validation:
  yaml:
    enabled: true
    required_fields:
      - title
      - tags
      - status
    # Only essential fields required
  markdown:
    enabled: false  # Disable markdown checks during migration
  naming:
    enabled: true
    max_length: 60  # Allow slightly longer names
```

**Report-Only Mode (No Enforcement):**
```yaml
validation:
  yaml:
    enabled: true
    required_fields: []  # Report on all fields, require none
  markdown:
    enabled: true
    enforce_heading_hierarchy: false  # Warn but don't fail
  naming:
    enabled: true
```

---

### Appendix D: Sample Tag Definitions (For v1.1+)

| Tag | Description | Example Keywords | Document Type |
|-----|-------------|------------------|---------------|
| pricing | Cost, fees, payment terms | price, cost, $, fee, payment | Business Operations |
| product-specs | Features, technical specs | specification, feature, technical, requirement | Business Operations |
| policies | Terms, conditions, legal | policy, terms, conditions, agreement, legal | Business Operations |
| support | Help, contact information | contact, support, help, email, phone | Business Operations |
| billing | Invoicing, payment process | invoice, billing, charge, receipt | Business Operations |
| standards | Standards and guidelines | standard, guideline, convention, best-practice | Business Operations |
| sop | Standard operating procedures | procedure, process, workflow, sop | Business Operations |
| procedures | Step-by-step instructions | how-to, guide, instructions, steps | Business Operations |

---

## Document Control

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|---------|
| 1.0 | 2025-10-09 | Initial draft PRD (business focus) | Product Team |
| 1.5 | 2025-11-05 | Expanded PRD (Symphony Core focus) | Symphony Core Systems Team |
| 2.0 | 2025-11-07 | **Unified PRD - Merged both use cases, focused v1.0 on validation only** | Symphony Core Systems Team |
| 2.1 | 2025-11-07 | **Simplified PRD - Removed artificial distinction between "technical" and "business" docs. Symphony Core IS business operations documentation.** | Symphony Core Systems Team |

**Review & Approval:**

| Role | Name | Status | Date |
|------|------|--------|------|
| Product Owner | TBD | ✅ Approved (v2.0 scope) | 2025-11-07 |
| Technical Lead | TBD | Pending Review | - |
| Documentation Lead | TBD | Pending Review | - |

**Next Review Date:** 2025-12-07 (or after v1.0 delivery)

---

## Related Documents

- [Symphony Core CLAUDE.md](../CLAUDE.md) - Development standards and guidelines
- [Repository Guide](../_meta/repository-guide.md) - Symphony Core repository structure (if exists)
- [SC Markdown Standard](../08-reference/standards/sc-markdown-standard.md) - Markdown validation rules (if exists)
- [SC Document Naming Standard](../08-reference/standards/sc-document-naming-standard.md) - Naming conventions (if exists)

---

**Document Status**: ☑ Approved (v2.0)  ☐ Review  ☐ Archived
**Maintained By:** Symphony Core Systems Team
**Location:** `docs/product-requirements-document.md`
