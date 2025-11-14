# Remote Agent Prompts for Test Fixtures

**Purpose**: Execution-ready prompts for fixing documentation issues in `test-fixtures/` directory
**Context**: Remote agents don't have access to external Windows paths, so we use in-repo test fixtures
**Source**: Based on QA findings from 01-strategy and 02-marketing-brand folder reviews

---

## Agent 1: Critical Frontmatter & Filename Fixes

```
Fix critical frontmatter and filename issues in Symphony Core test fixtures.

REPO: /home/user/sc-doc-mgmt-workflow (Claude Code for Cloud default path)
TARGET: test-fixtures/02-marketing-brand

CONTEXT: Read test-fixtures/README.md for issue details.

TASKS:
1. Add missing 'status' field to 2 docs in brand/brand-guidelines/:
   - sc-design-kit.md (missing 'status')
   - symphony_core_web_style_guide.md (missing 'status')
   - Use CLI: python -m src.cli frontmatter add-field --field status --value draft --path "test-fixtures/02-marketing-brand/brand/brand-guidelines" --preview
   - Apply: Remove --preview flag to execute

2. Manually change 'concepts' → 'draft' in 2 print-media docs:
   - test-fixtures/02-marketing-brand/brand/print-media/mailbox-sign-concepts.md
   - test-fixtures/02-marketing-brand/brand/print-media/office-door-sign-concepts.md
   - Find "status: concepts" and replace with "status: draft"

3. Rename file with spaces:
   - From: test-fixtures/02-marketing-brand/website/issues-to-fix/steps to fix domain issue.md
   - To: test-fixtures/02-marketing-brand/website/issues-to-fix/steps-to-fix-domain-issue.md
   - Use: git mv "test-fixtures/02-marketing-brand/website/issues-to-fix/steps to fix domain issue.md" "test-fixtures/02-marketing-brand/website/issues-to-fix/steps-to-fix-domain-issue.md"

4. Run validation:
   - python -m src.cli validate --path "test-fixtures/02-marketing-brand" --min-severity WARNING --force

SUCCESS CRITERIA:
- 3 frontmatter errors fixed (2 missing + 2 invalid status = 4 total)
- 1 filename violation fixed
- Validation shows only code block warnings (MD-002)
- All tests pass: pytest tests/ --cov=src

BRANCH: feature/fix-test-fixtures-critical
COMMIT: "fix: Resolve critical frontmatter and filename issues in test fixtures

- Add missing 'status' field to 2 brand guideline docs
- Fix invalid status values (concepts → draft) in print-media
- Rename file with spaces to kebab-case
- 4 critical errors resolved in 02-marketing-brand fixtures

Part of parallel documentation fix initiative"
```

---

## Agent 2: Code Block Language Specifiers & Heading Hierarchy

```
Fix markdown quality issues in Symphony Core test fixtures (both folders).

REPO: /home/user/sc-doc-mgmt-workflow
TARGET: test-fixtures/01-strategy and test-fixtures/02-marketing-brand

CONTEXT: Read test-fixtures/README.md for detailed issue locations.

TASKS:
1. Fix heading hierarchy (MD-001):
   - File: test-fixtures/01-strategy/business-plans/symphony-core-business-plan-draft-1.0.md
   - Problem: H1 "# Symphony Core Business Plan v1.0" → H3 "### Profit and Loss Statement" (skips H2)
   - Fix: Add H2 heading before the H3, e.g., "## Financial Projections"

2. Add language specifiers to code blocks (MD-002):
   - test-fixtures/01-strategy/business-plans/symphony-core-expense-tracker-guide.md (4 blocks):
     * Line 11: ```csv
     * Line 19: ```bash
     * Line 27: ```bash
     * Line 35: ```sql

   - test-fixtures/02-marketing-brand/brand/brand-guidelines/symphony_core_web_style_guide.md (2 blocks):
     * Line 11: ```html
     * Line 19: ```css

   - test-fixtures/02-marketing-brand/brand/print-media/mailbox-sign-concepts.md (6 blocks):
     * All blocks: ```text (ASCII art diagrams)

   - test-fixtures/02-marketing-brand/brand/print-media/office-door-sign-concepts.md (3 blocks):
     * All blocks: ```text (ASCII art diagrams)

3. Run validation on both folders:
   - python -m src.cli validate --path "test-fixtures/01-strategy" --min-severity WARNING --force
   - python -m src.cli validate --path "test-fixtures/02-marketing-brand" --min-severity WARNING --force

SUCCESS CRITERIA:
- 1 MD-001 violation fixed (heading hierarchy)
- 15 MD-002 violations fixed (4 + 2 + 6 + 3 = 15 code blocks)
- Both folders show 0 MD-001 and 0 MD-002 violations
- Pass rate: 100% (all 8 docs passing)
- All tests pass: pytest tests/ --cov=src

BRANCH: feature/fix-test-fixtures-markdown-quality
COMMIT: "fix: Add code block languages and fix heading hierarchy in test fixtures

- Add language specifiers to 15 code blocks (bash/csv/sql/html/css/text)
- Fix heading hierarchy skip in business-plan-draft-1.0.md
- Resolves all MD-001 and MD-002 warnings across both test folders

Part of parallel documentation fix initiative"
```

---

## Agent 3: Auto-Fix Trailing Whitespace

```
Auto-fix trailing whitespace in Symphony Core test fixtures (if present).

REPO: /home/user/sc-doc-mgmt-workflow
TARGET: test-fixtures/01-strategy and test-fixtures/02-marketing-brand

CONTEXT: Test fixtures may have trailing whitespace (INFO violations).

TASKS:
1. Auto-fix 01-strategy whitespace:
   - python -m src.cli validate --path "test-fixtures/01-strategy" --auto-fix

2. Auto-fix 02-marketing-brand whitespace:
   - python -m src.cli validate --path "test-fixtures/02-marketing-brand" --auto-fix

3. Validate results (should show 0 INFO violations):
   - python -m src.cli validate --path "test-fixtures/01-strategy" --force
   - python -m src.cli validate --path "test-fixtures/02-marketing-brand" --force

SUCCESS CRITERIA:
- All trailing whitespace issues removed
- Validation shows 0 INFO violations in both folders
- No changes to frontmatter or content, only whitespace cleanup
- All tests pass: pytest tests/ --cov=src

BRANCH: feature/fix-test-fixtures-whitespace
COMMIT: "fix: Remove trailing whitespace from test fixtures

- Auto-fix trailing whitespace in 01-strategy test files
- Auto-fix trailing whitespace in 02-marketing-brand test files
- All INFO violations resolved using --auto-fix

Part of parallel documentation fix initiative"
```

---

## Execution Strategy

**Order of Execution**: All 3 agents can run in parallel

**Merge Order**:
1. **Agent 3** (P1) - Zero conflicts (whitespace only)
2. **Agent 1** (P2) - Frontmatter/filename (minimal conflict risk)
3. **Agent 2** (P3) - Code blocks/headings (may touch same files as Agent 1, but different sections)

**Expected Conflicts**: 0-1 (unlikely since Agent 1 modifies frontmatter, Agent 2 modifies body)

**Testing After Merge**:
```bash
# Run full validation
python -m src.cli validate --path "test-fixtures/01-strategy" --force
python -m src.cli validate --path "test-fixtures/02-marketing-brand" --force

# Expected: 8/8 docs passing (100%)
# Expected: 0 violations

# Run test suite
pytest tests/ --cov=src --cov-report=term-missing
# Expected: All tests passing, coverage >80%
```

---

## Key Differences from Original Prompts

**Changed**:
- Paths: `C:\Users\Rohit\...` → `test-fixtures/`
- Repo: External docs repo → In-repo test fixtures
- Scope: 31 real docs → 8 test fixture files
- Removed: Pricing conflict fix (not in test fixtures)
- Removed: README.md frontmatter (not in test fixtures)

**Unchanged**:
- CLI commands and flags
- Fix strategies
- Success criteria logic
- Merge order and conflict mitigation

---

**Created**: 2025-11-13
**For Use With**: Claude Code for Cloud remote agents
**Expected Runtime**: 5-10 minutes per agent
