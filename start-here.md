---
title: Sprint 5 - URL Content Extraction (IN PROGRESS)
tags: [sprint-5, url-extraction, html-to-markdown, in-progress]
status: in-progress
version: 3.0
last_updated: 2025-11-12
---

# Sprint 5: URL Content Extraction - Implementation Guide

**Status**: 🟡 IN PROGRESS - Setup Complete, Implementation Pending
**Branch**: `claude/extract-website-content-011CV4UGNJQdeHBNFPnEdaD3`
**Story Points**: 13 (Medium-Large)
**Progress**: **2/13 points complete (15%)** - Planning & Setup done

---

## 🎯 CURRENT STATE (2025-11-12)

### ✅ What's Complete
1. ✅ Sprint 5 planning document created (`sprints/sprint-05-url-extraction.md`)
2. ✅ Feature branch created and checked out
3. ✅ Dependencies added to `requirements.txt`:
   - `beautifulsoup4>=4.12.2` - HTML parsing
   - `html2text>=2020.1.16` - HTML to markdown conversion
   - `lxml>=4.9.3` - XML/HTML parser backend
4. ✅ Dependencies installed successfully
5. ✅ Requirements analyzed and approved by user

### 🔨 What Needs to Be Done
- [ ] Create `src/core/extractors/` module structure (3 files + __init__.py)
- [ ] Implement `HTMLExtractor` class (~150 lines)
- [ ] Implement `MarkdownConverter` class (~150 lines)
- [ ] Implement `FrontmatterGenerator` class (~100 lines)
- [ ] Add `extract-url` command to `src/cli.py` (~100 lines)
- [ ] Create `_output/` directory structure
- [ ] Write comprehensive tests (~400-500 lines)
- [ ] Test with provided HTML file (`_input/webpage/Comprehensive SEO Packages.html`)
- [ ] Update documentation (README, user-guide, config)
- [ ] Final testing and bug fixes
- [ ] Push to branch

**Estimated Remaining Effort**: 11 story points (~2-3 days)

---

## 📋 FEATURE OVERVIEW

### Goal
Add capability to extract website content from HTML files and convert to Symphony Core-compliant markdown documents with proper YAML frontmatter.

### Test Case
- **HTML File**: `_input/webpage/Comprehensive SEO Packages.html`
- **Source**: go.symphonycore.com/add-on-seo-packages
- **Expected Output**: SC-compliant markdown in `_output/extracted-{timestamp}/`

### CLI Command Design (Approved)
```bash
# Basic usage
python main.py extract-url --source <html-file>

# With output directory
python main.py extract-url --source page.html --output <dir>

# Full example
python main.py extract-url --source _input/webpage/page.html --output _output/docs/
```

---

## 🏗️ ARCHITECTURE & IMPLEMENTATION PLAN

### Module Structure to Create

```
src/core/extractors/               # NEW MODULE (create this)
├── __init__.py                    # Module exports
├── html_extractor.py              # HTML parsing & content extraction
├── markdown_converter.py          # HTML → Markdown conversion (SC-compliant)
└── frontmatter_generator.py       # YAML frontmatter generation

tests/core/extractors/             # NEW TEST MODULE (create this)
├── __init__.py
├── test_html_extractor.py         # ~150 lines
├── test_markdown_converter.py     # ~150 lines
└── test_frontmatter_generator.py  # ~100 lines

tests/fixtures/                    # Test data
└── html_samples/                  # Sample HTML files for testing
    ├── simple.html
    ├── complex.html
    └── malformed.html

_output/                           # NEW OUTPUT DIRECTORY (create this)
├── .gitignore                     # Ignore all contents
└── extracted-{timestamp}/         # Timestamped output folders
    └── *.md                       # Converted markdown files
```

---

## 📖 DETAILED IMPLEMENTATION GUIDE

### Step 1: Create Module Structure

**Create directories**:
```bash
mkdir -p src/core/extractors
mkdir -p tests/core/extractors
mkdir -p tests/fixtures/html_samples
mkdir -p _output
```

**Create `_output/.gitignore`**:
```
# Ignore all extracted content
*
!.gitignore
```

**Create empty `__init__.py` files**:
- `src/core/extractors/__init__.py`
- `tests/core/extractors/__init__.py`

---

### Step 2: Implement HTMLExtractor

**File**: `src/core/extractors/html_extractor.py`

**Purpose**: Extract structured content from HTML files using BeautifulSoup

**Key Methods**:
```python
class HTMLExtractor:
    """Extract structured content from HTML files."""

    def __init__(self, logger: Logger = None):
        """Initialize with optional logger."""

    def extract_main_content(self, html_path: Path) -> dict:
        """
        Extract main content from HTML file.

        Returns:
            dict: {
                'title': str,           # From H1 or <title>
                'html_content': str,    # Clean HTML for conversion
                'metadata': dict        # meta tags, description, etc.
            }
        """

    def _find_main_content(self, soup: BeautifulSoup) -> Tag:
        """Find main content area (avoid nav, footer, sidebar)."""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from H1 or <title> tag."""
```

**Key Requirements**:
- Use BeautifulSoup4 with lxml parser
- Find main content intelligently (look for `<main>`, `<article>`, or largest content block)
- Extract clean HTML (remove nav, footer, sidebar, scripts, styles)
- Handle malformed HTML gracefully
- Return structured data for conversion

**Implementation Hints**:
```python
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional, Dict
import logging

class HTMLExtractor:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def extract_main_content(self, html_path: Path) -> Dict:
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()

            soup = BeautifulSoup(html, 'lxml')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()

            # Find main content
            main_content = self._find_main_content(soup)
            title = self._extract_title(soup)

            return {
                'title': title,
                'html_content': str(main_content),
                'metadata': self._extract_metadata(soup)
            }
        except Exception as e:
            self.logger.error(f"Failed to extract content: {e}")
            raise
```

---

### Step 3: Implement MarkdownConverter

**File**: `src/core/extractors/markdown_converter.py`

**Purpose**: Convert HTML to SC-compliant markdown (following sc-markdown-standard.md)

**Key Methods**:
```python
class MarkdownConverter:
    """Convert HTML content to SC-compliant markdown."""

    def __init__(self, config: Config = None):
        """Initialize with optional config."""

    def convert_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML to markdown following SC standards.

        Post-processes:
        - Remove markdown tables, convert to structured content
        - Remove checkbox symbols (☐, ✓, ✅, ❌)
        - Ensure proper heading hierarchy
        - Clean up extra whitespace
        - Preserve links in markdown format
        """

    def _convert_tables_to_structured(self, markdown: str) -> str:
        """Convert markdown tables to SC-compliant structured content."""

    def _remove_checkboxes(self, markdown: str) -> str:
        """Replace checkbox symbols with text alternatives."""
```

**SC Standard Compliance Checklist**:
- ❌ NO markdown tables - convert to structured content
- ❌ NO checkbox symbols (☐, ✓, ✅, ❌) - use text alternatives
- ❌ NO square brackets for placeholders
- ✅ YES proper heading hierarchy
- ✅ YES code blocks with language specification
- ✅ YES relative links
- ✅ YES descriptive link text

**Implementation Hints**:
```python
import html2text
import re
from typing import Optional

class MarkdownConverter:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.body_width = 0  # No wrapping

    def convert_to_markdown(self, html_content: str) -> str:
        # Base conversion
        markdown = self.h2t.handle(html_content)

        # SC compliance post-processing
        markdown = self._convert_tables_to_structured(markdown)
        markdown = self._remove_checkboxes(markdown)
        markdown = self._clean_whitespace(markdown)

        return markdown

    def _convert_tables_to_structured(self, markdown: str) -> str:
        # Detect markdown tables (lines with |)
        # Convert to structured format:
        # ## Table Title
        # ### Column 1
        # Value
        # ### Column 2
        # Value
        pass
```

---

### Step 4: Implement FrontmatterGenerator

**File**: `src/core/extractors/frontmatter_generator.py`

**Purpose**: Generate SC-compliant YAML frontmatter

**Key Methods**:
```python
class FrontmatterGenerator:
    """Generate YAML frontmatter for extracted documents."""

    def generate(
        self,
        title: str,
        tags: list = None,
        status: str = "draft",
        category: str = "KB Article",
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

**Required Frontmatter Template**:
```yaml
---
title: [Document Title]
version: 1.0
author: Web Content Extractor
last_updated: [YYYY-MM-DD]
category: KB Article
tags: [web-content, extracted]
status: draft
source_url: [original URL if available]
extracted_date: [YYYY-MM-DD HH:MM:SS]
extraction_method: html_file
---
```

**Implementation Hints**:
```python
from datetime import datetime
import yaml

class FrontmatterGenerator:
    def generate(
        self,
        title: str,
        tags: list = None,
        status: str = "draft",
        category: str = "KB Article",
        source_url: str = None,
        **kwargs
    ) -> str:
        frontmatter = {
            'title': title,
            'version': '1.0',
            'author': 'Web Content Extractor',
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'category': category,
            'tags': tags or ['web-content', 'extracted'],
            'status': status
        }

        # Add optional fields
        if source_url:
            frontmatter['source_url'] = source_url

        frontmatter['extracted_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        frontmatter['extraction_method'] = 'html_file'

        # Format as YAML (no language identifier!)
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---\n"
```

---

### Step 5: Add CLI Command

**File**: `src/cli.py`

**Add to existing CLI** (around line 200+):

```python
@cli.command()
@click.option(
    '--source',
    type=click.Path(exists=True),
    required=True,
    help='Path to HTML file to extract'
)
@click.option(
    '--output',
    type=click.Path(),
    default='_output',
    help='Output directory for converted markdown (default: _output/)'
)
@click.option(
    '--title',
    type=str,
    default=None,
    help='Custom title (default: extracted from HTML)'
)
@click.option(
    '--tags',
    type=str,
    default=None,
    help='Comma-separated tags (default: web-content,extracted)'
)
def extract_url(source, output, title, tags):
    """Extract content from HTML file and convert to markdown.

    Examples:
        python main.py extract-url --source page.html
        python main.py extract-url --source page.html --output docs/
        python main.py extract-url --source page.html --title "Guide"
    """
    from pathlib import Path
    from datetime import datetime
    from src.core.extractors.html_extractor import HTMLExtractor
    from src.core.extractors.markdown_converter import MarkdownConverter
    from src.core.extractors.frontmatter_generator import FrontmatterGenerator
    from src.utils.logger import Logger

    logger = Logger()

    try:
        click.echo(f"\n{'='*60}")
        click.echo("URL CONTENT EXTRACTION")
        click.echo(f"{'='*60}\n")

        # Extract HTML content
        click.echo(f"📄 Extracting content from: {source}")
        extractor = HTMLExtractor(logger)
        content_data = extractor.extract_main_content(Path(source))

        # Convert to markdown
        click.echo("🔄 Converting to markdown...")
        converter = MarkdownConverter()
        markdown_content = converter.convert_to_markdown(content_data['html_content'])

        # Generate frontmatter
        click.echo("📝 Generating frontmatter...")
        fm_generator = FrontmatterGenerator()
        title_to_use = title or content_data['title']
        tags_list = tags.split(',') if tags else ['web-content', 'extracted']

        frontmatter = fm_generator.generate(
            title=title_to_use,
            tags=tags_list,
            source_url=content_data['metadata'].get('url')
        )

        # Create output directory
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_dir = Path(output) / f"extracted-{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from title
        filename = title_to_use.lower().replace(' ', '-')
        filename = re.sub(r'[^a-z0-9-]', '', filename)[:50] + '.md'
        output_file = output_dir / filename

        # Write markdown file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(markdown_content)

        click.echo(f"\n✅ Success!")
        click.echo(f"📁 Output file: {output_file}")
        click.echo(f"📊 Size: {output_file.stat().st_size} bytes\n")

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)
```

---

### Step 6: Write Tests

**Create test files** in `tests/core/extractors/`:

1. **test_html_extractor.py** (~150 lines):
   - Test extracting title from H1
   - Test extracting title from `<title>` tag
   - Test finding main content
   - Test handling malformed HTML
   - Test ignoring nav/footer

2. **test_markdown_converter.py** (~150 lines):
   - Test HTML to markdown conversion
   - Test table conversion to structured content
   - Test checkbox removal
   - Test link preservation
   - Test heading hierarchy

3. **test_frontmatter_generator.py** (~100 lines):
   - Test required fields generation
   - Test optional fields
   - Test YAML formatting
   - Test date formatting

**Example test structure**:
```python
import pytest
from pathlib import Path
from src.core.extractors.html_extractor import HTMLExtractor

class TestHTMLExtractor:
    def test_extract_title_from_h1(self, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text("<html><body><h1>Test Title</h1></body></html>")

        extractor = HTMLExtractor()
        result = extractor.extract_main_content(html_file)

        assert result['title'] == "Test Title"

    def test_extract_main_content(self, tmp_path):
        # Test main content extraction
        pass
```

---

### Step 7: Test with Real HTML

**Test file**: `_input/webpage/Comprehensive SEO Packages.html`

**Test command**:
```bash
python main.py extract-url --source "_input/webpage/Comprehensive SEO Packages.html"
```

**Expected output**:
- File created in `_output/extracted-{timestamp}/seo-packages.md`
- Valid YAML frontmatter
- SC-compliant markdown
- No markdown tables
- No checkbox symbols
- Proper heading hierarchy

---

### Step 8: Update Documentation

**Update files**:

1. **README.md** - Add to features list:
```markdown
### URL Content Extraction (Sprint 5) ✅
```bash
# Extract HTML to markdown
python main.py extract-url --source page.html
```

2. **docs/user-guide.md** - Add new section:
```markdown
## URL Content Extraction

Extract HTML content and convert to SC-compliant markdown...
```

3. **config/config.yaml** - Add extraction config:
```yaml
# URL Extraction Configuration
extraction:
  default_output_dir: "_output"
  default_status: "draft"
  default_category: "KB Article"
```

---

## 🧪 TESTING CHECKLIST

Before completing Sprint 5:

### Unit Tests
- [ ] All HTMLExtractor tests pass
- [ ] All MarkdownConverter tests pass
- [ ] All FrontmatterGenerator tests pass
- [ ] Test coverage > 80% for new modules

### Integration Tests
- [ ] CLI command runs without errors
- [ ] Output file created in correct location
- [ ] Frontmatter has all required fields
- [ ] Markdown follows SC standards
- [ ] Test with provided HTML file succeeds

### Manual Testing
- [ ] Run: `python main.py extract-url --source "_input/webpage/Comprehensive SEO Packages.html"`
- [ ] Verify output file exists
- [ ] Verify frontmatter structure
- [ ] Verify markdown compliance
- [ ] Verify no markdown tables
- [ ] Verify no checkbox symbols

### Quality Gates
- [ ] All 215+ tests passing
- [ ] No linting errors (flake8)
- [ ] Code formatted (black)
- [ ] Type hints present
- [ ] Docstrings complete

---

## 📝 KEY DECISIONS & CONTEXT

### User-Approved Decisions
1. ✅ CLI command: `extract-url` (vs html-to-md or other options)
2. ✅ Output directory: `_output/` with timestamped subdirectories
3. ✅ Default status: `draft`
4. ✅ Content scope: main content, links, tables (no nav/footer/ads)
5. ✅ Future integration: Auto-validation, auto-tagging (Sprint 6+)

### SC Markdown Standard Requirements
**Source**: `C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\08-reference\standards\sc-markdown-standard.md`

**Critical Rules**:
- ❌ NO markdown tables - convert to structured content
- ❌ NO checkbox symbols - use text alternatives
- ❌ NO language identifier with frontmatter fences
- ❌ NO square brackets for placeholders
- ✅ Required frontmatter: title, version, author, last_updated, category, tags, status
- ✅ Lowercase-with-hyphens file naming
- ✅ Proper heading hierarchy (no skipped levels)

### Dependencies Installed
```
beautifulsoup4>=4.12.2    # HTML parsing
html2text>=2020.1.16      # HTML to markdown base conversion
lxml>=4.9.3               # Fast HTML parser backend
```

---

## 🚀 NEXT STEPS FOR CLAUDE CODE

When resuming this work:

1. **Verify branch**: `git status` should show branch `claude/extract-website-content-011CV4UGNJQdeHBNFPnEdaD3`

2. **Read Sprint 5 plan**: `sprints/sprint-05-url-extraction.md` has full details

3. **Start implementation**:
   - Create module structure (Step 1)
   - Implement HTMLExtractor (Step 2)
   - Implement MarkdownConverter (Step 3)
   - Implement FrontmatterGenerator (Step 4)
   - Add CLI command (Step 5)
   - Write tests (Step 6)
   - Test with real HTML (Step 7)
   - Update docs (Step 8)

4. **Test thoroughly** with: `_input/webpage/Comprehensive SEO Packages.html`

5. **Commit and push** when complete

---

## 📊 SPRINT 5 PROGRESS TRACKER

**Phase 1: Setup & Planning** ✅ COMPLETE (2/13 points)
- [x] Sprint planning document
- [x] Feature branch created
- [x] Dependencies installed
- [x] Requirements approved

**Phase 2: Core Implementation** 🔲 PENDING (5/13 points)
- [ ] HTMLExtractor class
- [ ] MarkdownConverter class
- [ ] FrontmatterGenerator class
- [ ] Module structure
- [ ] Unit tests

**Phase 3: CLI Integration** 🔲 PENDING (3/13 points)
- [ ] extract-url command
- [ ] Output directory handling
- [ ] Integration tests
- [ ] Real HTML test

**Phase 4: Documentation** 🔲 PENDING (3/13 points)
- [ ] README update
- [ ] User guide update
- [ ] Config updates
- [ ] Final testing

---

## 📚 REFERENCE DOCUMENTS

**Essential Reading**:
1. `sprints/sprint-05-url-extraction.md` - Full sprint plan
2. `_input/input-prompt.md` - Original requirements & answers
3. `C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\08-reference\standards\sc-markdown-standard.md` - SC standards

**Test Data**:
- `_input/webpage/Comprehensive SEO Packages.html` - Test HTML file
- `_input/webpage/Comprehensive SEO Packages_files/` - Assets

**Key Files to Edit**:
- `src/core/extractors/*.py` (NEW - create these)
- `src/cli.py` (add extract-url command)
- `tests/core/extractors/*.py` (NEW - create tests)
- `config/config.yaml` (add extraction config)
- `docs/user-guide.md` (add extraction section)
- `README.md` (add feature to list)

---

**Sprint Status**: 🟡 **IN PROGRESS** (15% complete)
**Next Action**: Begin Phase 2 - Core Implementation
**Branch**: `claude/extract-website-content-011CV4UGNJQdeHBNFPnEdaD3`
**Estimated Completion**: 2-3 days of development work

---

## 🔄 PREVIOUS SPRINTS STATUS

### Sprint 4: CLI & Reporting ✅ COMPLETE (100%)
**Status**: All features delivered, 215 tests passing, 82% coverage
**Last Updated**: 2025-11-09

**Delivered Features**:
- ✅ CLI interface with Click framework
- ✅ Validation reports (console, JSON, markdown)
- ✅ Enhanced conflict reporting
- ✅ File-specific validation (--file option)
- ✅ Exit codes for CI/CD

### Sprint 1-3: Foundation & Validation ✅ COMPLETE
- ✅ Document validation (YAML, Markdown, Naming)
- ✅ Auto-fix engine
- ✅ Conflict detection
- ✅ Change detection & caching
- ✅ 215 tests, 82% coverage

---

**Document Version**: 3.0
**Last Updated**: 2025-11-12
**Maintained By**: Engineering Team
**Status**: 🟡 Sprint 5 In Progress
