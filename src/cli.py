"""
Command-line interface for Symphony Core Document Management Workflow.

Provides commands for validating markdown documents, detecting conflicts,
and generating reports.
"""

import sys
import json
import click
from pathlib import Path
from typing import Optional

from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.cache import DocumentCache
from src.core.validators.yaml_validator import YAMLValidator
from src.core.validators.naming_validator import NamingValidator
from src.core.validators.markdown_validator import MarkdownValidator
from src.core.validators.conflict_detector import ConflictDetector
from src.core.auto_fixer import AutoFixer
from src.core.change_detector import ChangeDetector
from src.reporting import (
    ReportData,
    ConsoleReporter,
    MarkdownReporter,
    JSONReporter,
    ConflictReporter
)


# Version information
VERSION = "1.0.0"


@click.group()
@click.version_option(version=VERSION, prog_name="Symphony Core")
@click.pass_context
def cli(ctx):
    """
    Symphony Core Document Management Workflow

    Automated document processing system for validating, fixing, and analyzing
    markdown documentation.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Initialize configuration
    try:
        config = Config()
        ctx.obj['config'] = config
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--path',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help='Validate specific folder (default: current directory)'
)
@click.option(
    '--file',
    'files',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    multiple=True,
    help='Validate specific file(s) - can be specified multiple times'
)
@click.option(
    '--tags',
    help='Validate documents with specific tag (comma-separated for multiple)'
)
@click.option(
    '--force',
    is_flag=True,
    help='Ignore cache and revalidate all documents'
)
@click.option(
    '--auto-fix',
    is_flag=True,
    help='Automatically fix issues where possible'
)
@click.option(
    '--preview',
    is_flag=True,
    help='Preview auto-fixes without applying (requires --auto-fix)'
)
@click.option(
    '--conflicts',
    is_flag=True,
    help='Run conflict detection only'
)
@click.option(
    '--format',
    type=click.Choice(['console', 'markdown', 'json'], case_sensitive=False),
    default='console',
    help='Output format for reports (default: console)'
)
@click.option(
    '--output',
    type=click.Path(path_type=Path),
    help='Output file for report (default: stdout)'
)
@click.pass_context
def validate(
    ctx,
    path: Optional[Path],
    files: tuple,
    tags: Optional[str],
    force: bool,
    auto_fix: bool,
    preview: bool,
    conflicts: bool,
    format: str,
    output: Optional[Path]
):
    """
    Validate markdown documents against naming, YAML, and markdown rules.

    Examples:

        # Validate all documents
        python main.py validate

        # Validate specific folder
        python main.py validate --path operations/

        # Validate specific file(s)
        python main.py validate --file doc1.md
        python main.py validate --file doc1.md --file doc2.md

        # Compare two files for conflicts
        python main.py validate --file doc1.md --file doc2.md --conflicts

        # Validate documents with specific tag
        python main.py validate --tags pricing

        # Auto-fix issues with preview
        python main.py validate --auto-fix --preview

        # Run conflict detection
        python main.py validate --conflicts

        # Generate markdown report
        python main.py validate --format markdown --output report.md
    """
    config = ctx.obj['config']

    # Validate option combinations
    if preview and not auto_fix:
        click.echo("Error: --preview requires --auto-fix", err=True)
        sys.exit(1)

    if path and files:
        click.echo("Error: Cannot specify both --path and --file", err=True)
        sys.exit(1)

    # Set default path to docs directory from config or current directory
    if path is None and not files:
        path = Path(config.get('paths.docs_root', '.'))

    click.echo("=" * 80)
    click.echo("SYMPHONY CORE - DOCUMENT VALIDATION")
    click.echo("=" * 80)
    click.echo()

    # Parse tags if provided
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        click.echo(f"Filtering by tags: {', '.join(tag_list)}")

    # Display mode
    if conflicts:
        click.echo("Mode: Conflict Detection")
    elif auto_fix:
        click.echo(f"Mode: Auto-Fix ({'Preview' if preview else 'Apply'})")
    else:
        click.echo("Mode: Validation")

    if files:
        click.echo(f"Files: {len(files)} file(s) specified")
        for f in files:
            click.echo(f"  - {f}")
    else:
        click.echo(f"Path: {path}")
    click.echo(f"Force: {'Yes' if force else 'No (incremental)'}")
    click.echo()

    try:
        # Initialize logger
        log_file = Path(config.get('paths.logs_dir', 'logs')) / 'validation.log'
        logger = Logger(
            name="symphony_core.cli",
            log_file=log_file,
            log_level=config.get('logging.level', 'INFO'),
            console_output=False  # Disable to avoid interference with CLI output
        )

        # Initialize validators
        yaml_validator = YAMLValidator(config, logger)
        naming_validator = NamingValidator(config, logger)
        markdown_validator = MarkdownValidator(config, logger)
        conflict_detector = ConflictDetector(config, logger)

        # Find documents to process
        change_detector = None  # Will be set if using incremental mode

        if files:
            # Use specified files
            documents = [Path(f) for f in files]
            # Validate that all files are markdown
            for doc in documents:
                if doc.suffix.lower() != '.md':
                    click.echo(f"Error: {doc} is not a markdown file (.md)", err=True)
                    sys.exit(1)
        elif conflicts or force:
            # Conflict detection and force mode process all documents
            documents = _find_all_documents(path, tag_list)
        else:
            # Incremental validation uses change detection
            cache_file = Path(config.get('paths.cache_file', '_meta/.document-cache.json'))
            cache = DocumentCache(cache_file)
            change_detector = ChangeDetector(cache, logger)
            documents, change_summary = change_detector.get_files_to_process(
                path,
                force_reprocess=False
            )

        click.echo(f"Documents to process: {len(documents)}")
        click.echo()

        if len(documents) == 0:
            click.echo("No documents to process.")
            sys.exit(0)

        # Run validation based on mode
        if conflicts:
            _run_conflict_detection(
                conflict_detector,
                documents,
                format,
                output
            )
        elif auto_fix:
            _run_auto_fix(
                yaml_validator,
                documents,
                preview,
                format,
                output
            )
        else:
            _run_validation(
                yaml_validator,
                naming_validator,
                markdown_validator,
                documents,
                format,
                output,
                change_detector
            )

    except Exception as e:
        click.echo(f"Error during validation: {e}", err=True)
        if config.get('debug', False):
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _find_all_documents(base_path: Path, tags: Optional[list] = None) -> list:
    """
    Find all markdown documents in the given path.

    Args:
        base_path: Root path to search
        tags: Optional list of tags to filter by

    Returns:
        List of Path objects for markdown files
    """
    documents = []

    # Recursively find all .md files
    for md_file in base_path.rglob('*.md'):
        # Skip hidden directories and files
        if any(part.startswith('.') for part in md_file.parts):
            continue

        # Skip _meta directory
        if '_meta' in md_file.parts:
            continue

        # If tags filter provided, check document tags
        if tags:
            # This is a placeholder - would need to parse frontmatter to check tags
            # For now, include all documents
            pass

        documents.append(md_file)

    return sorted(documents)


def _run_validation(
    yaml_validator,
    naming_validator,
    markdown_validator,
    documents: list,
    format: str,
    output: Optional[Path],
    change_detector = None
):
    """Run full validation on documents."""
    all_issues = []
    issues_by_doc = {}  # Track issues per document for cache updates

    with click.progressbar(
        documents,
        label='Validating documents',
        show_pos=True
    ) as bar:
        for doc in bar:
            doc_issues = []

            # YAML validation
            yaml_issues = yaml_validator.validate(doc)
            all_issues.extend(yaml_issues)
            doc_issues.extend(yaml_issues)

            # Naming validation
            naming_issues = naming_validator.validate(doc)
            all_issues.extend(naming_issues)
            doc_issues.extend(naming_issues)

            # Markdown validation
            markdown_issues = markdown_validator.validate(doc)
            all_issues.extend(markdown_issues)
            doc_issues.extend(markdown_issues)

            issues_by_doc[doc] = doc_issues

            # Update cache if using incremental mode
            if change_detector:
                error_count = sum(1 for issue in doc_issues if issue.severity == 'error')
                warning_count = sum(1 for issue in doc_issues if issue.severity == 'warning')
                validation_status = 'passed' if error_count == 0 else 'failed'
                change_detector.update_cache_for_file(
                    doc,
                    validation_status=validation_status,
                    error_count=error_count,
                    warning_count=warning_count
                )

    # Save cache if using incremental mode
    if change_detector:
        change_detector.save_cache()

    click.echo()

    # Generate report
    _generate_validation_report(all_issues, documents, format, output)

    # Exit with appropriate code
    error_count = sum(1 for issue in all_issues if issue.severity == 'error')
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


def _run_conflict_detection(
    conflict_detector,
    documents: list,
    format: str,
    output: Optional[Path]
):
    """Run conflict detection on documents."""
    click.echo("Running conflict detection...")

    # Detect conflicts
    conflicts = conflict_detector.detect_conflicts(documents)

    click.echo()

    # Analyze conflicts with enhanced reporter
    reporter = ConflictReporter()
    conflict_data = reporter.analyze_conflicts(conflicts)

    # Generate report based on format
    if format == 'json':
        report = reporter.generate_json_report(conflict_data)
    elif format == 'markdown':
        report = reporter.generate_markdown_report(conflict_data)
    else:  # console (default)
        report = reporter.generate_console_report(conflict_data)

    # Output report
    if output:
        output.write_text(report, encoding='utf-8')
        click.echo(f"Report saved to: {output}")
    else:
        click.echo(report)

    # Exit with appropriate code based on critical conflicts
    total_conflicts = sum(len(issues) for issues in conflicts.values())
    if total_conflicts > 0:
        sys.exit(1)
    else:
        sys.exit(0)


def _run_auto_fix(
    yaml_validator,
    documents: list,
    preview: bool,
    format: str,
    output: Optional[Path]
):
    """Run auto-fix on documents."""
    from src.utils.config import Config

    config = Config()
    log_file = Path(config.get('paths.logs_dir', 'logs')) / 'autofix.log'
    logger = Logger(
        name="symphony_core.autofix",
        log_file=log_file,
        log_level=config.get('logging.level', 'INFO'),
        console_output=False
    )
    auto_fixer = AutoFixer(config, logger)

    results = []

    with click.progressbar(
        documents,
        label='Auto-fixing documents',
        show_pos=True
    ) as bar:
        for doc in bar:
            # Validate first to find issues
            issues = yaml_validator.validate(doc)

            # Try to fix each issue
            for issue in issues:
                if auto_fixer.can_fix(issue):
                    result = auto_fixer.fix(doc, issue, preview=preview)
                    results.append(result)

    click.echo()

    # Generate report
    _generate_autofix_report(results, preview, format, output)

    # Exit with success
    sys.exit(0)


def _generate_validation_report(
    issues: list,
    documents: list,
    format: str,
    output: Optional[Path]
):
    """Generate validation report in specified format using reporter classes."""
    # Group issues by file
    issues_by_file = {}
    for issue in issues:
        file_path = str(issue.file_path)
        if file_path not in issues_by_file:
            issues_by_file[file_path] = []
        issues_by_file[file_path].append(issue)

    # Calculate statistics
    total_docs = len(documents)
    failed_docs = len(issues_by_file)
    passed_docs = total_docs - failed_docs

    # Handle both string and Enum severity
    total_errors = sum(1 for i in issues
                      if (hasattr(i.severity, 'value') and i.severity.value == 'error')
                      or str(i.severity) == 'error')
    total_warnings = sum(1 for i in issues
                        if (hasattr(i.severity, 'value') and i.severity.value == 'warning')
                        or str(i.severity) == 'warning')

    # Calculate rule counts
    rule_counts = {}
    for issue in issues:
        rule_id = issue.rule_id
        if rule_id not in rule_counts:
            rule_counts[rule_id] = 0
        rule_counts[rule_id] += 1

    # Create report data
    report_data = ReportData(
        total_documents=total_docs,
        passed_documents=passed_docs,
        failed_documents=failed_docs,
        total_errors=total_errors,
        total_warnings=total_warnings,
        issues_by_file=issues_by_file,
        all_issues=issues,
        rule_counts=rule_counts,
        scan_mode="validation"
    )

    # Select and use appropriate reporter
    if format == 'console':
        reporter = ConsoleReporter()
        report = reporter.generate(report_data)
        click.echo(report)

    elif format == 'json':
        reporter = JSONReporter()
        report = reporter.generate(report_data)
        if output:
            reporter.save(report, output)
            click.echo(f"Report saved to: {output}")
        else:
            click.echo(report)

    elif format == 'markdown':
        reporter = MarkdownReporter()
        report = reporter.generate(report_data)
        if output:
            reporter.save(report, output)
            click.echo(f"Report saved to: {output}")
        else:
            click.echo(report)


def _generate_autofix_report(
    results: list,
    preview: bool,
    format: str,
    output: Optional[Path]
):
    """Generate auto-fix report."""
    if format == 'console':
        click.echo("=" * 80)
        click.echo(f"AUTO-FIX REPORT ({'PREVIEW' if preview else 'APPLIED'})")
        click.echo("=" * 80)
        click.echo()
        click.echo(f"Total fixes: {len(results)}")
        click.echo()

        for result in results:
            status = "WOULD FIX" if preview else "FIXED"
            click.echo(f"[{status}] {result.file_path}: {result.description}")

        click.echo()
        click.echo("=" * 80)


@cli.command()
@click.option(
    '--source',
    type=click.Path(exists=True),
    required=True,
    help='Path to HTML file to extract content from'
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
@click.option(
    '--category',
    type=str,
    default='KB Article',
    help='Document category (default: KB Article)'
)
def extract_url(source, output, title, tags, category):
    """
    Extract content from HTML file and convert to SC-compliant markdown.

    Extracts main content from an HTML file, converts it to markdown following
    Symphony Core standards, and adds proper YAML frontmatter.

    Examples:

        \b
        # Basic extraction
        python main.py extract-url --source page.html

        \b
        # With custom output directory
        python main.py extract-url --source page.html --output docs/extracted/

        \b
        # With custom title and tags
        python main.py extract-url --source page.html --title "SEO Guide" --tags "seo,marketing"
    """
    from datetime import datetime
    from src.core.extractors.html_extractor import HTMLExtractor
    from src.core.extractors.markdown_converter import MarkdownConverter
    from src.core.extractors.frontmatter_generator import FrontmatterGenerator

    logger = Logger()

    try:
        click.echo(f"\n{'='*60}")
        click.echo("URL CONTENT EXTRACTION")
        click.echo(f"{'='*60}\n")

        source_path = Path(source)

        # Extract HTML content
        click.echo(f"[1/4] Extracting content from: {source_path.name}")
        extractor = HTMLExtractor(logger)
        content_data = extractor.extract_main_content(source_path)

        extracted_title = content_data['title']
        click.echo(f"      Title: {extracted_title}")

        # Convert to markdown
        click.echo("[2/4] Converting to SC-compliant markdown...")
        converter = MarkdownConverter()
        markdown_content = converter.convert_to_markdown(content_data['html_content'])

        # Generate frontmatter
        click.echo("[3/4] Generating YAML frontmatter...")
        fm_generator = FrontmatterGenerator()
        title_to_use = title or extracted_title
        tags_list = tags.split(',') if tags else ['web-content', 'extracted']
        tags_list = [tag.strip() for tag in tags_list]  # Clean whitespace

        frontmatter = fm_generator.generate(
            title=title_to_use,
            tags=tags_list,
            category=category,
            source_url=content_data['metadata'].get('url')
        )

        # Create output directory
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_dir = Path(output) / f"extracted-{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from title (lowercase-with-hyphens)
        import re
        filename = title_to_use.lower().replace(' ', '-')
        filename = re.sub(r'[^a-z0-9-]', '', filename)[:50]
        if not filename:  # Fallback if title becomes empty after cleaning
            filename = 'extracted-document'
        filename = filename + '.md'

        output_file = output_dir / filename

        # Write markdown file
        click.echo(f"[4/4] Writing to file: {filename}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write("\n")
            f.write(markdown_content)

        # Success message
        file_size = output_file.stat().st_size
        click.echo(f"\n{'='*60}")
        click.echo("SUCCESS - EXTRACTION COMPLETE")
        click.echo(f"{'='*60}")
        click.echo(f"Output file: {output_file}")
        click.echo(f"File size: {file_size:,} bytes")
        click.echo(f"Title: {title_to_use}")
        click.echo(f"Tags: {', '.join(tags_list)}")
        click.echo(f"Category: {category}")
        click.echo(f"Status: draft")
        click.echo(f"{'='*60}\n")

        sys.exit(0)

    except FileNotFoundError as e:
        click.echo(f"\nERROR: {str(e)}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"\nERROR: Extraction failed: {str(e)}", err=True)
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
