# Sprint 3 Quick Start Guide

**Based on**: Full Documentation Repository Review (Nov 8, 2025)
**Full Report**: See `DOCUMENTATION_REVIEW_REPORT.md` for complete analysis

---

## TL;DR - What You Need to Know

**Repository**: `C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents`

**Key Stats**:
- 174 markdown files across 9 sections
- 42.5% (74 files) **missing YAML frontmatter** ← MAJOR ISSUE
- 44 files with **naming violations** (uppercase dirs, spaces)
- 10+ **status value conflicts** (draft vs Draft, non-standard values)
- Strong sections: 01-strategy, 05-platform, 08-reference
- Weak sections: 02-marketing-brand, 03-sales (missing metadata)

---

## Critical Findings for Sprint 3

### 1. Markdown Validator (US-3.1) Will Encounter

✅ **Good Test Data Available**:
- `05-platform/platforms-config/*.md` - Well-structured docs
- `08-reference/glossary/pages/*.md` - Consistent formatting
- `01-strategy/business-plans/*.md` - Clean markdown

⚠️ **Challenges**:
- **42.5% of files have NO frontmatter** - Must handle gracefully
- Marketing/sales content has inconsistent formatting
- Need to validate heading hierarchy, code blocks, links
- Cross-references to deprecated docs exist

**Implementation Tip**: Don't crash on missing frontmatter. Validate markdown body separately from YAML metadata.

### 2. Naming Validator (US-3.2) Will Encounter

❌ **44 Known Violations** (excellent test data!):
- **34 files** in uppercase directories:
  ```
  08-reference/platforms/Extendly/  → should be: extendly/
  08-reference/platforms/GHL/       → should be: ghl/
  ```
- **10+ files** with spaces in names:
  ```
  steps to fix domain issue.md
  automation ecosystem map.md
  CV - B-000 Foundations.csv
  ```

**Implementation Tip**: Create rename suggestion function. Provide migration script for bulk fixes.

**Exception Handling**:
- README.md files: Allow uppercase ✅
- *.csv files: Different rules (document this)

### 3. Conflict Detector (US-3.3) Will Encounter

🔥 **Real Conflicts to Test Against**:

**Status Conflicts**:
```yaml
status: draft          # Lowercase, no quotes
status: "Draft"        # Capitalized, quoted ❌
status: published      # Non-standard value ❌
status: complete       # Non-standard value ❌
```

**Tag Conflicts** (synonyms):
```yaml
tags: [gohighlevel, ...]
tags: [ghl, ...]            # Same platform, different tag
tags: [GoHighLevel, ...]    # Case conflict
```

**Pricing Conflicts** (CRITICAL - test this!):
- Pricing info scattered across:
  - `03-sales/pricing-strategy/*.md`
  - `02-marketing-brand/website/*.md`
- **Risk**: Inconsistent pricing across marketing and sales docs
- **Detection**: Regex extract $X/month mentions, compare

**Deprecated Doc References**:
- Some active docs reference deprecated content
- Need cross-reference validation

**Implementation Tip**: Start with status/tag conflicts (easier). Build to pricing conflicts (harder). Use tag normalization dictionary.

---

## Sprint 3 Recommended Approach

### Week 1: Naming Validator (3 points) - EASIEST
**Why Start Here**: Immediate impact, clear test cases, low complexity

1. Implement directory case checker
2. Implement filename space checker
3. Generate rename suggestions
4. Test on 44 known violations
5. **Success**: Flag all violations, provide fixes

**Test Command**:
```bash
python -m pytest tests/core/validators/test_naming_validator.py -v
```

**Real Test Data**:
```python
# Use actual violating files from review
test_files = [
    Path("08-reference/platforms/Extendly/training-docs/automation ecosystem map.md"),
    Path("02-marketing-brand/website/issues-to-fix/steps to fix domain issue.md"),
]
```

### Week 2: Markdown Validator (5 points) - MODERATE
**Why Second**: Builds on frontmatter work from Sprint 2, moderate complexity

1. Handle docs without frontmatter gracefully
2. Implement heading hierarchy checker
3. Implement code block validator
4. Implement link integrity checker
5. **Success**: Validate all 174 docs without crashing

**Test Command**:
```bash
python -m pytest tests/core/validators/test_markdown_validator.py -v
```

**Real Test Data**:
```python
# Good structure examples
test_good = [
    Path("05-platform/platforms-config/claude-config-standard.md"),
    Path("08-reference/glossary/pages/ai-glossary.md"),
]

# Missing frontmatter examples
test_no_frontmatter = [
    Path("02-marketing-brand/website/homepage_copy.md"),
    Path("03-sales/pricing-strategy/core_plans_pricing_copy.md"),
]
```

### Week 3: Conflict Detector (10 points) - HARDEST
**Why Last**: Most complex, highest value, needs other validators complete

**Sub-tasks**:
- Day 1-2: Document grouping, metadata extraction
- Day 3-4: Status/tag conflict detection
- Day 5-6: Pricing extraction and comparison
- Day 7-8: Cross-reference validation
- Day 9-10: Testing, refinement, confidence scoring

**Test Command**:
```bash
python -m pytest tests/core/validators/test_conflict_detector.py -v
```

**Real Test Data**:
```python
# Test status conflicts
test_status_conflicts = [
    # Mix of draft, "Draft", published, complete, etc.
    all_docs_with_frontmatter  # ~100 files
]

# Test pricing conflicts
test_pricing_conflicts = [
    Path("03-sales/pricing-strategy/*.md"),
    Path("02-marketing-brand/website/*.md"),
]
```

---

## Key Implementation Patterns (From Sprint 2)

### Pattern 1: Graceful Degradation
```python
def validate(self, file_path: Path) -> List[ValidationIssue]:
    issues = []

    try:
        # Attempt frontmatter extraction
        metadata = parse_frontmatter(file_path)
    except FrontmatterError:
        # Don't crash - report and continue
        issues.append(ValidationIssue(
            rule_id='MD-001',
            severity=ValidationSeverity.WARNING,
            message='Missing YAML frontmatter',
            suggestion='Add frontmatter block at top of file'
        ))
        metadata = {}  # Empty dict, validation continues

    # Continue with markdown body validation
    issues.extend(self._validate_markdown_body(file_path))
    return issues
```

### Pattern 2: Real Document Testing
```python
# Sprint 2 approach: Use actual Symphony Core docs
class TestYAMLValidatorRealDocs:
    @pytest.fixture
    def real_docs_path(self):
        return Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")

    def test_validate_strategy_docs(self, validator, real_docs_path):
        """Test against actual business strategy documents"""
        strategy_docs = list((real_docs_path / "01-strategy").glob("**/*.md"))
        assert len(strategy_docs) == 10  # From review

        for doc in strategy_docs:
            issues = validator.validate(doc)
            # Most strategy docs should pass
            critical_issues = [i for i in issues if i.severity == ValidationSeverity.ERROR]
            assert len(critical_issues) == 0, f"{doc.name} has critical issues"
```

### Pattern 3: Configuration-Driven Validation
```python
# config.yaml
validation:
  naming:
    enabled: true
    allow_uppercase_files:
      - "README.md"
    allow_spaces_in_extensions:
      - ".csv"
    max_length: 50

  markdown:
    enabled: true
    require_frontmatter: false  # Too many docs lack it currently
    check_heading_hierarchy: true
    check_code_block_language: true

  conflicts:
    enabled: true
    allowed_status_values:
      - draft
      - review
      - approved
      - active
      - archived
      - deprecated
    tag_synonyms:
      ghl: gohighlevel
      wp: wordpress
```

---

## Auto-Fix Opportunities (Prioritized)

### Priority 1: Missing Frontmatter (74 files)
**Impact**: HIGH - Enables all other validation

```python
# Auto-fix approach
def fix_missing_frontmatter(file_path: Path) -> AutoFixResult:
    # Extract title from H1 heading
    title = extract_title_from_h1(file_path)

    # Suggest tags from file path
    tags = suggest_tags_from_path(file_path)

    # Default status
    status = 'draft'

    # Add frontmatter
    frontmatter = {
        'title': title,
        'tags': tags,
        'status': status
    }

    # Create backup first
    backup_path = create_backup(file_path)

    # Add frontmatter to file
    add_frontmatter(file_path, frontmatter)

    return AutoFixResult(
        file_path=file_path,
        fixes_applied=['Added YAML frontmatter', f'Extracted title: {title}'],
        backup_path=backup_path
    )
```

**Test Files**: All 74 files without frontmatter (see Appendix A in full report)

### Priority 2: Status Normalization (100 files)
**Impact**: MEDIUM - Enables conflict detection

```python
def normalize_status_value(status: str) -> str:
    """Normalize status to standard vocabulary"""
    # Remove quotes
    status = status.strip('"').strip("'")

    # Convert to lowercase
    status = status.lower()

    # Map non-standard to standard
    mapping = {
        'published': 'active',
        'complete': 'approved',
        'concepts': 'draft',
    }

    return mapping.get(status, status)
```

### Priority 3: Tag Normalization
**Impact**: MEDIUM - Improves conflict detection

```python
def normalize_tags(tags: List[str]) -> List[str]:
    """Normalize tag vocabulary"""
    # Lowercase all
    tags = [t.lower() for t in tags]

    # Apply synonyms
    synonyms = {
        'ghl': 'gohighlevel',
        'wp': 'wordpress',
    }

    tags = [synonyms.get(t, t) for t in tags]

    # Remove duplicates, maintain order
    return list(dict.fromkeys(tags))
```

### Priority 4: Filename Fixes (44 files)
**Impact**: LOW-MEDIUM - Improves consistency

Provide migration script, don't auto-fix (risk of breaking references).

---

## Validation Exception Patterns

Create `config/validation-exceptions.yaml`:

```yaml
# Files/paths exempt from certain validations

naming:
  allow_uppercase:
    - "README.md"
    - "**/README.md"

  allow_spaces:
    - "**/*.csv"  # CSV files use different conventions

  ignore_paths:
    - "_inbox/*"  # Drafts may have temporary names
    - "docs/archive/*"

frontmatter:
  optional_for_paths:
    - "_inbox/**/*.md"  # Drafts may lack complete metadata
    - "docs/archive/**/*.md"

  required_for_paths:
    - "01-strategy/**/*.md"  # Business-critical
    - "03-sales/pricing-strategy/**/*.md"  # Pricing must have metadata
    - "05-platform/**/*.md"  # Platform docs must be tracked

conflicts:
  ignore_deprecated_references_for_days: 90  # Allow 90-day migration period

  pricing_conflict_paths:
    - "03-sales/pricing-strategy/**/*.md"
    - "02-marketing-brand/website/**/*.md"
```

---

## Success Metrics for Sprint 3

### Naming Validator
- [ ] Flag all 34 uppercase directory violations
- [ ] Flag all 10+ space-in-filename violations
- [ ] Provide rename suggestions for all violations
- [ ] Handle exceptions (README.md, *.csv)
- [ ] 95%+ test coverage

### Markdown Validator
- [ ] Validate all 174 docs without crashing
- [ ] Handle 74 docs without frontmatter gracefully
- [ ] Identify heading hierarchy issues
- [ ] Flag code blocks without language
- [ ] Check link integrity (relative paths)
- [ ] 95%+ test coverage

### Conflict Detector
- [ ] Detect all status vocabulary conflicts (10+)
- [ ] Detect tag synonym conflicts (ghl vs gohighlevel)
- [ ] Extract pricing mentions from sales/marketing docs
- [ ] Flag pricing inconsistencies (if any)
- [ ] Identify cross-references to deprecated docs
- [ ] 90%+ test coverage (complexity allows 10% tolerance)

### Overall Sprint 3
- [ ] All 18 story points complete
- [ ] 85+ tests passing (naming: 20, markdown: 25, conflicts: 40)
- [ ] Real-world validation on 174 Symphony Core docs
- [ ] Documentation updated (user-guide, development guide)
- [ ] Ready for Sprint 4 (CLI + Reporting)

---

## Files to Reference During Sprint 3

**Architecture & Standards**:
- `C:\...\symphony-core-documents\symphony-core-documentation-architecture.md`
- `C:\...\symphony-core-documents\08-reference\standards\sc-tagging-standard.md`
- `C:\...\symphony-core-documents\08-reference\standards\sc-markdown-standard.md`

**Test Data Sources**:
- Strategy docs (clean): `C:\...\symphony-core-documents\01-strategy\**\*.md`
- Platform docs (good structure): `C:\...\symphony-core-documents\05-platform\**\*.md`
- Marketing docs (missing frontmatter): `C:\...\symphony-core-documents\02-marketing-brand\**\*.md`
- Sales docs (pricing conflicts): `C:\...\symphony-core-documents\03-sales\**\*.md`

**Sprint 2 Reference Code**:
- `src/utils/frontmatter.py` - YAML parsing utilities
- `src/core/validators/yaml_validator.py` - Validation pattern
- `src/core/auto_fixer.py` - Auto-fix pattern
- `tests/core/validators/test_yaml_validator.py` - Test pattern

---

## Common Pitfalls to Avoid (From Sprint 2)

1. **Don't crash on edge cases** - Handle missing frontmatter, malformed YAML, empty files
2. **Test with real docs early** - Don't wait until end to test on Symphony Core docs
3. **Windows path handling** - Use `Path` objects, not string concatenation
4. **Windows console encoding** - Avoid emoji in output, use ASCII
5. **Actionable error messages** - Always provide suggestion for fix
6. **Configuration-driven** - Don't hardcode business rules, use config.yaml
7. **Create backups** - Any auto-fix must create timestamped backup first

---

## Ready to Start?

**Prompt for Starting Sprint 3**:
```
I'm ready to start Sprint 3 implementation for the Symphony Core document validation system.

Sprint 3 includes:
- US-3.1: Markdown syntax validator (5 points)
- US-3.2: File naming validator (3 points)
- US-3.3: Semantic conflict detector (10 points)

I have reviewed:
- DOCUMENTATION_REVIEW_REPORT.md (full analysis of 174 docs)
- SPRINT_3_QUICK_START.md (this guide)
- Real documentation at C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents

Key findings:
- 42.5% of docs missing frontmatter (test graceful handling)
- 44 naming violations (great test data)
- Status/tag conflicts exist (real conflict scenarios)

Let's start with the Naming Validator (easiest, 3 points) and work up to the Conflict Detector (hardest, 10 points).

Ready to begin?
```

---

**Status**: ✅ SPRINT 3 READY
**Full Report**: `DOCUMENTATION_REVIEW_REPORT.md` (18 pages)
**Last Updated**: November 8, 2025
**Next Step**: Begin Sprint 3 implementation
