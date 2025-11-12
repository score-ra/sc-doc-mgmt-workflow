---
title: Sprint 5 - URL Content Extraction
tags: [sprint-5, url-extraction, html-to-markdown, feature]
status: in-progress
version: 1.0
last_updated: 2025-11-12
---

# Sprint 5: URL Content Extraction

**Sprint Focus**: Add capability to extract website content and convert to Symphony Core-compliant markdown documents

**Story Points**: 13 (Medium-Large)
**Duration**: 3-4 days
**Status**: In Progress
**Branch**: `claude/extract-website-content-011CV4UGNJQdeHBNFPnEdaD3`

---

## Sprint Goal

Enable users to extract HTML content from web pages and convert them to properly formatted markdown documents that comply with Symphony Core standards.

**Primary Deliverable**: CLI command to convert HTML files to SC-compliant markdown with proper YAML frontmatter.

---

## Context

### Current State (v1.0 Complete)
- ✅ Document validation (YAML, Markdown, Naming)
- ✅ Conflict detection
- ✅ Auto-fix capabilities
- ✅ CLI interface with multiple commands
- ✅ 215 tests passing, 82% coverage

### Problem
Teams need to migrate web content into markdown format for documentation repositories. Manual conversion is time-consuming and error-prone.

### Solution
Automated HTML-to-markdown conversion tool integrated into the existing CLI, following SC markdown standards.

---

## User Stories

### US-5.1: HTML Content Extraction (5 points)
**As a** documentation manager
**I want to** extract content from HTML files
**So that** I can convert web content to markdown documents

**Acceptance Criteria**:
- [ ] Extract main content from HTML files
- [ ] Extract title from H1 or `<title>` tag
- [ ] Extract all headings (H1-H6), paragraphs, lists
- [ ] Extract and preserve links in markdown format
- [ ] Extract tables and convert to SC-compliant format
- [ ] Ignore navigation, footer, sidebar, ads, scripts
- [ ] Handle malformed HTML gracefully

**Technical Tasks**:
- Implement `HTMLExtractor` class
- Use BeautifulSoup4 for HTML parsing
- Identify main content area intelligently
- Extract structured data (headings, paragraphs, lists, tables, links)

---

### US-5.2: Markdown Conversion (5 points)
**As a** documentation manager
**I want** extracted content converted to SC-compliant markdown
**So that** documents follow Symphony Core standards

**Acceptance Criteria**:
- [ ] Convert HTML to proper markdown syntax
- [ ] Follow SC markdown standard (no markdown tables)
- [ ] Preserve heading hierarchy (no skipped levels)
- [ ] Convert links to markdown format `[text](url)`
- [ ] Handle code blocks with language specification
- [ ] Convert tables to structured content (not markdown tables)
- [ ] Remove checkbox symbols, replace with text
- [ ] Generate clean, readable markdown output

**Technical Tasks**:
- Implement `MarkdownConverter` class
- Use html2text library as base
- Post-process to ensure SC compliance
- Handle special cases (tables, checkboxes, placeholders)

---

### US-5.3: CLI Integration & Frontmatter (3 points)
**As a** user
**I want** a CLI command to extract URL content
**So that** I can easily convert HTML to markdown

**Acceptance Criteria**:
- [ ] Add `extract-url` command to CLI
- [ ] Accept `--source` flag for HTML file path
- [ ] Accept `--output` flag for output directory (default: `_output/`)
- [ ] Generate YAML frontmatter with required fields:
  - title, version, author, last_updated, category, tags, status
- [ ] Add optional fields: source_url, extracted_date, extraction_method
- [ ] Default status: `draft`
- [ ] Save to `_output/extracted-{timestamp}/` directory
- [ ] Provide clear success/error messages
- [ ] Show output file path after completion

**Technical Tasks**:
- Implement `FrontmatterGenerator` class
- Add `extract-url` command in `src/cli.py`
- Create output directory structure
- Integrate extractor pipeline

---

## Technical Design

### Architecture

```
src/
├── core/
│   ├── extractors/               # NEW MODULE
│   │   ├── __init__.py
│   │   ├── html_extractor.py     # HTML parsing & content extraction
│   │   ├── markdown_converter.py # HTML → Markdown conversion
│   │   └── frontmatter_generator.py # YAML frontmatter generation
│   └── ...
├── cli.py                        # Add extract-url command
└── ...

_output/                          # NEW DIRECTORY (gitignored)
├── .gitignore
└── extracted-YYYYMMDD-HHMMSS/    # Timestamped output folders
    └── *.md                      # Converted markdown files
```

### Dependencies

```python
beautifulsoup4==4.12.2    # HTML parsing
html2text==2020.1.16      # HTML to markdown conversion
lxml==4.9.3               # XML/HTML parser (BeautifulSoup backend)
```

### Key Classes

#### 1. HTMLExtractor
```python
class HTMLExtractor:
    """Extract structured content from HTML files."""

    def extract_main_content(self, html_path: Path) -> dict:
        """
        Extract main content from HTML file.

        Returns:
            dict: {
                'title': str,
                'headings': list,
                'paragraphs': list,
                'lists': list,
                'tables': list,
                'links': list,
                'metadata': dict
            }
        """

    def _find_main_content(self, soup: BeautifulSoup) -> Tag:
        """Intelligently find main content area."""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from H1 or <title> tag."""
```

#### 2. MarkdownConverter
```python
class MarkdownConverter:
    """Convert HTML content to SC-compliant markdown."""

    def convert_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML to markdown following SC standards.

        Post-processes:
        - Removes markdown tables, converts to structured content
        - Removes checkbox symbols
        - Ensures proper heading hierarchy
        - Cleans up formatting
        """

    def convert_table_to_structured(self, table_html: str) -> str:
        """Convert HTML table to SC-compliant structured content."""
```

#### 3. FrontmatterGenerator
```python
class FrontmatterGenerator:
    """Generate YAML frontmatter for extracted documents."""

    def generate(
        self,
        title: str,
        tags: list = None,
        status: str = "draft",
        source_url: str = None,
        **kwargs
    ) -> str:
        """
        Generate SC-compliant YAML frontmatter.

        Required fields:
        - title, version, author, last_updated, category, tags, status

        Optional fields:
        - source_url, extracted_date, extraction_method
        """
```

### Data Flow

```
1. User runs: python main.py extract-url --source page.html --output _output/

2. CLI parses arguments and calls extraction pipeline

3. HTMLExtractor:
   - Loads HTML file
   - Parses with BeautifulSoup
   - Finds main content area
   - Extracts structured data (title, headings, paragraphs, etc.)

4. MarkdownConverter:
   - Converts HTML elements to markdown
   - Post-processes for SC compliance
   - Converts tables to structured content
   - Cleans up formatting

5. FrontmatterGenerator:
   - Creates YAML frontmatter with required fields
   - Adds optional metadata (source_url, extracted_date)

6. Output:
   - Creates output directory if needed
   - Generates filename from title (lowercase-with-hyphens)
   - Writes markdown file with frontmatter + content
   - Displays success message with file path
```

---

## Implementation Plan

### Phase 1: Setup & Core Extraction (Day 1)

**Tasks**:
- [x] Create Sprint 5 planning document
- [ ] Install dependencies (beautifulsoup4, html2text, lxml)
- [ ] Create `src/core/extractors/` module structure
- [ ] Implement `HTMLExtractor` class
  - HTML parsing with BeautifulSoup
  - Main content identification
  - Structured data extraction
- [ ] Write unit tests for `HTMLExtractor`
- [ ] Test with sample HTML files

**Deliverable**: Working HTML content extractor

---

### Phase 2: Markdown Conversion (Day 2)

**Tasks**:
- [ ] Implement `MarkdownConverter` class
  - HTML to markdown conversion (base)
  - SC standard compliance (post-processing)
  - Table conversion to structured content
  - Checkbox removal
  - Link preservation
- [ ] Implement `FrontmatterGenerator` class
  - Required fields generation
  - Optional fields handling
  - YAML formatting
- [ ] Write unit tests for both classes
- [ ] Test with various content types

**Deliverable**: SC-compliant markdown converter with frontmatter

---

### Phase 3: CLI Integration (Day 3)

**Tasks**:
- [ ] Add `extract-url` command to `src/cli.py`
- [ ] Implement command options (--source, --output)
- [ ] Create output directory structure
- [ ] Integrate extraction pipeline
- [ ] Add error handling and user feedback
- [ ] Write integration tests
- [ ] Test with provided HTML file (`Comprehensive SEO Packages.html`)
- [ ] Verify output follows SC standards

**Deliverable**: Working CLI command with full pipeline

---

### Phase 4: Documentation & Testing (Day 4)

**Tasks**:
- [ ] Update `docs/user-guide.md` with URL extraction section
- [ ] Update `README.md` feature list
- [ ] Add extraction config to `config/config.yaml`
- [ ] Write comprehensive tests (unit + integration)
- [ ] Achieve 80%+ test coverage for new modules
- [ ] Test edge cases (malformed HTML, missing content, etc.)
- [ ] Update `_output/.gitignore`
- [ ] Final testing and bug fixes

**Deliverable**: Complete, documented, tested feature

---

## Testing Strategy

### Unit Tests

**HTMLExtractor Tests** (`tests/core/extractors/test_html_extractor.py`):
- Extract title from H1 tag
- Extract title from `<title>` tag
- Extract all heading levels
- Extract paragraphs with formatting
- Extract ordered and unordered lists
- Extract tables
- Extract links and preserve URLs
- Handle missing main content
- Handle malformed HTML

**MarkdownConverter Tests** (`tests/core/extractors/test_markdown_converter.py`):
- Convert headings (H1-H6)
- Convert paragraphs with inline formatting
- Convert lists (ordered/unordered/nested)
- Convert links to markdown format
- Convert tables to structured content (no markdown tables)
- Remove checkbox symbols
- Handle code blocks
- Clean up extra whitespace

**FrontmatterGenerator Tests** (`tests/core/extractors/test_frontmatter_generator.py`):
- Generate with all required fields
- Generate with optional fields
- Use default values correctly
- Format YAML correctly
- Handle special characters in title
- Generate valid date formats

### Integration Tests

**CLI Tests** (`tests/test_cli_extract.py`):
- Test `extract-url` command with valid HTML file
- Test with --source flag
- Test with --output flag
- Test with malformed HTML
- Test with missing file
- Test output file creation
- Verify frontmatter structure
- Verify markdown compliance

**Real Content Test**:
- Test with `_input/webpage/Comprehensive SEO Packages.html`
- Verify complete extraction
- Verify SC compliance
- Verify frontmatter correctness

---

## Configuration

Add to `config/config.yaml`:

```yaml
# URL Extraction Configuration
extraction:
  enabled: true
  default_output_dir: "_output"
  default_status: "draft"
  default_category: "KB Article"
  default_author: "Web Content Extractor"
  frontmatter:
    include_source_url: true
    include_extracted_date: true
    include_extraction_method: true
  conversion:
    remove_navigation: true
    remove_footer: true
    remove_ads: true
    convert_tables_to_structured: true
    preserve_links: true
```

---

## CLI Usage Examples

### Basic Extraction
```bash
# Extract from HTML file (saves to _output/extracted-{timestamp}/)
python main.py extract-url --source _input/webpage/page.html

# Specify output directory
python main.py extract-url --source page.html --output docs/extracted/

# With custom title
python main.py extract-url --source page.html --title "Custom Title"
```

### Advanced Options
```bash
# Extract with specific tags
python main.py extract-url --source page.html --tags "seo,marketing,guide"

# Specify category
python main.py extract-url --source page.html --category "Guide"

# Dry run (preview without saving)
python main.py extract-url --source page.html --preview
```

---

## Success Criteria

### Functional Requirements
- [x] Sprint 5 planning document created
- [ ] Can extract content from HTML files
- [ ] Generates SC-compliant markdown
- [ ] Adds proper YAML frontmatter with all required fields
- [ ] CLI command `extract-url` functional
- [ ] Saves to `_output/` directory with proper structure
- [ ] Follows SC markdown standard (no markdown tables, etc.)
- [ ] Works with provided test case (SEO Packages HTML)

### Quality Requirements
- [ ] 80%+ test coverage for new modules
- [ ] All tests passing (215+ existing tests + new tests)
- [ ] PEP 8 compliant code
- [ ] Type hints on all functions
- [ ] Docstrings on all classes and methods
- [ ] No linting errors

### Documentation Requirements
- [ ] Sprint 5 document complete
- [ ] User guide updated with extraction examples
- [ ] README updated with feature
- [ ] Configuration documented
- [ ] CLI help text clear and comprehensive

---

## Dependencies & Risks

### External Dependencies
| Dependency | Version | Risk | Mitigation |
|------------|---------|------|------------|
| beautifulsoup4 | 4.12.2 | Low | Well-maintained, stable library |
| html2text | 2020.1.16 | Low | Mature library, large user base |
| lxml | 4.9.3 | Low | Standard HTML parser |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Complex HTML structures not handled | Medium | Medium | Extensive testing with various HTML samples |
| SC standard compliance edge cases | Medium | High | Post-processing validation, manual review |
| Performance with large HTML files | Low | Low | Stream processing if needed |
| Malformed HTML breaking parser | Medium | Medium | Try-except handling, graceful degradation |

---

## Future Enhancements (Sprint 6+)

### Post-Sprint 5 Improvements
- **URL Fetching**: Fetch HTML directly from URLs (not just local files)
- **Auto-Validation**: Run validation after extraction
- **Auto-Tagging**: Intelligent tag detection based on content
- **Batch Processing**: Extract multiple URLs in one command
- **Custom Templates**: User-defined frontmatter templates
- **Content Filtering**: Fine-grained control over what to extract
- **Image Handling**: Download and reference images
- **Link Validation**: Check extracted links for validity

---

## Timeline

**Day 1** (Tuesday): Setup & HTML Extraction
- Create module structure
- Implement HTMLExtractor
- Write tests

**Day 2** (Wednesday): Markdown Conversion
- Implement MarkdownConverter
- Implement FrontmatterGenerator
- Write tests

**Day 3** (Thursday): CLI Integration
- Add extract-url command
- Integration tests
- Test with real HTML

**Day 4** (Friday): Documentation & Polish
- Update all documentation
- Final testing
- Bug fixes
- Commit & push

**Total Effort**: 3-4 days (13 story points)

---

## Related Documents

- [Product Requirements Document](../docs/product-requirements-document.md)
- [SC Markdown Standard](C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\08-reference\standards\sc-markdown-standard.md)
- [User Guide](../docs/user-guide.md)
- [README](../README.md)

---

## Status Updates

### 2025-11-12 - Sprint Started
- Sprint 5 planning document created
- Requirements analyzed
- Implementation plan approved
- Ready to begin development

---

**Sprint Status**: 🟡 In Progress
**Next Update**: After Phase 1 completion
**Branch**: `claude/extract-website-content-011CV4UGNJQdeHBNFPnEdaD3`
