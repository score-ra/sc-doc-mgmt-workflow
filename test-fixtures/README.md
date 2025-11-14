# Test Fixtures for Documentation Fixes

**Purpose**: This directory contains sample documentation files with intentional issues for testing Symphony Core CLI fixes.

**Source**: Files are simplified versions based on QA findings from:
- `execution-results/01-strategy-qa-findings.md`
- `execution-results/02-marketing-brand-qa-findings.md`

---

## Directory Structure

```
test-fixtures/
├── 01-strategy/
│   └── business-plans/
│       ├── symphony-core-business-plan-draft-1.0.md (MD-001: H1→H3 skip)
│       └── symphony-core-expense-tracker-guide.md (MD-002: 4 code blocks missing language)
│
└── 02-marketing-brand/
    ├── brand/
    │   ├── brand-guidelines/
    │   │   ├── sc-design-kit.md (Missing 'status' field)
    │   │   └── symphony_core_web_style_guide.md (Missing 'status' field + 2 code blocks)
    │   └── print-media/
    │       ├── mailbox-sign-concepts.md (Invalid status: 'concepts' + 6 code blocks)
    │       └── office-door-sign-concepts.md (Invalid status: 'concepts' + 3 code blocks)
    └── website/
        └── issues-to-fix/
            └── steps to fix domain issue.md (Filename with spaces)
```

---

## Known Issues by File

### 01-strategy/business-plans/symphony-core-business-plan-draft-1.0.md
- **MD-001**: Heading hierarchy skips from H1 to H3 (line 9: "### Profit and Loss Statement")
- **Fix**: Add H2 heading before the H3

### 01-strategy/business-plans/symphony-core-expense-tracker-guide.md
- **MD-002**: 4 code blocks missing language specifiers (lines 11, 19, 27, 35)
- **Fix**: Add language after ``` (csv, bash, bash, sql)

### 02-marketing-brand/brand/brand-guidelines/sc-design-kit.md
- **Missing Field**: Frontmatter missing required 'status' field
- **Fix**: Add `status: draft` to frontmatter

### 02-marketing-brand/brand/brand-guidelines/symphony_core_web_style_guide.md
- **Missing Field**: Frontmatter missing required 'status' field
- **MD-002**: 2 code blocks missing language specifiers (lines 11, 19)
- **Fix**: Add `status: draft` to frontmatter and add languages (html, css)

### 02-marketing-brand/brand/print-media/mailbox-sign-concepts.md
- **Invalid Status**: status: 'concepts' not in allowed values
- **MD-002**: 6 code blocks missing language specifiers (lines 9, 16, 24, etc.)
- **Fix**: Change to `status: draft` and add `text` or `ascii-art` to code blocks

### 02-marketing-brand/brand/print-media/office-door-sign-concepts.md
- **Invalid Status**: status: 'concepts' not in allowed values
- **MD-002**: 3 code blocks missing language specifiers
- **Fix**: Change to `status: draft` and add `text` or `ascii-art` to code blocks

### 02-marketing-brand/website/issues-to-fix/steps to fix domain issue.md
- **Filename Spaces**: Filename contains spaces (should be kebab-case)
- **Fix**: Rename to `steps-to-fix-domain-issue.md`

---

## Usage in Remote Agents

Remote agents should use paths relative to repo root:

```bash
# From repo root
python -m src.cli validate --path "test-fixtures/01-strategy" --min-severity WARNING
python -m src.cli validate --path "test-fixtures/02-marketing-brand" --min-severity WARNING

# Auto-fix whitespace
python -m src.cli validate --path "test-fixtures/01-strategy" --auto-fix
python -m src.cli validate --path "test-fixtures/02-marketing-brand" --auto-fix

# Add missing frontmatter
python -m src.cli frontmatter add-field --field status --value draft \
  --path "test-fixtures/02-marketing-brand/brand/brand-guidelines" --preview
```

---

## Expected Results After Fixes

- **01-strategy**: 2/2 docs passing (100%)
- **02-marketing-brand**: 6/6 docs passing (100%)
- **Total violations**: 0 (except trailing whitespace if not auto-fixed)

---

**Note**: These are simplified test files. The actual documentation repository contains more complex examples with additional content.
