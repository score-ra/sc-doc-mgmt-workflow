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
from src.core.validators.yaml_validator import YAMLValidator
from src.core.validators.naming_validator import NamingValidator
from src.core.validators.markdown_validator import MarkdownValidator
from src.core.validators.conflict_detector import ConflictDetector
from src.core.auto_fixer import AutoFixer
from src.core.change_detector import ChangeDetector


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

    # Set default path to docs directory from config or current directory
    if path is None:
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
        if conflicts or force:
            # Conflict detection and force mode process all documents
            documents = _find_all_documents(path, tag_list)
        else:
            # Incremental validation uses change detection
            change_detector = ChangeDetector(config)
            documents = change_detector.get_files_to_process(
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
                output
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
    output: Optional[Path]
):
    """Run full validation on documents."""
    all_issues = []

    with click.progressbar(
        documents,
        label='Validating documents',
        show_pos=True
    ) as bar:
        for doc in bar:
            # YAML validation
            yaml_issues = yaml_validator.validate(doc)
            all_issues.extend(yaml_issues)

            # Naming validation
            naming_issues = naming_validator.validate(doc)
            all_issues.extend(naming_issues)

            # Markdown validation
            markdown_issues = markdown_validator.validate(doc)
            all_issues.extend(markdown_issues)

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

    conflicts = conflict_detector.detect_conflicts(documents)

    click.echo()

    # Generate report
    report = conflict_detector.generate_conflict_report(conflicts)

    if output:
        output.write_text(report, encoding='utf-8')
        click.echo(f"Report saved to: {output}")
    else:
        click.echo(report)

    # Exit with appropriate code
    if len(conflicts) > 0:
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
    """Generate validation report in specified format."""
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

    # Generate console report (default)
    if format == 'console':
        click.echo("=" * 80)
        click.echo("VALIDATION REPORT")
        click.echo("=" * 80)
        click.echo()
        click.echo(f"Documents Scanned: {total_docs}")
        click.echo(f"Passed: {passed_docs} ({passed_docs/total_docs*100:.1f}%)")
        click.echo(f"Failed: {failed_docs} ({failed_docs/total_docs*100:.1f}%)")
        click.echo()
        click.echo(f"Total Errors: {total_errors}")
        click.echo(f"Total Warnings: {total_warnings}")
        click.echo()

        if issues:
            click.echo("VIOLATIONS BY RULE:")
            rule_counts = {}
            for issue in issues:
                rule_id = issue.rule_id
                if rule_id not in rule_counts:
                    rule_counts[rule_id] = 0
                rule_counts[rule_id] += 1

            for rule_id, count in sorted(rule_counts.items()):
                click.echo(f"  {rule_id}: {count}")

            click.echo()
            click.echo("FAILED DOCUMENTS:")
            for file_path, file_issues in sorted(issues_by_file.items()):
                click.echo(f"\n  {file_path}")
                for issue in file_issues:
                    # Handle both string and Enum severity
                    severity_label = issue.severity.value.upper() if hasattr(issue.severity, 'value') else str(issue.severity).upper()
                    click.echo(f"    [{severity_label}] {issue.rule_id}: {issue.message}")
                    if issue.suggestion:
                        click.echo(f"    Suggestion: {issue.suggestion}")

        click.echo()
        click.echo("=" * 80)

    elif format == 'json':
        import json
        report_data = {
            'summary': {
                'total': total_docs,
                'passed': passed_docs,
                'failed': failed_docs,
                'errors': total_errors,
                'warnings': total_warnings
            },
            'violations': [
                {
                    'file': str(issue.file_path),
                    'rule_id': issue.rule_id,
                    'severity': issue.severity.value if hasattr(issue.severity, 'value') else str(issue.severity),
                    'message': issue.message,
                    'line': getattr(issue, 'line', None) or getattr(issue, 'line_number', None),
                    'suggestion': issue.suggestion
                }
                for issue in issues
            ]
        }

        report_json = json.dumps(report_data, indent=2)

        if output:
            output.write_text(report_json, encoding='utf-8')
            click.echo(f"Report saved to: {output}")
        else:
            click.echo(report_json)

    elif format == 'markdown':
        lines = [
            "# Symphony Core Validation Report",
            "",
            "## Summary",
            f"- **Documents Scanned**: {total_docs}",
            f"- **Passed**: {passed_docs} ({passed_docs/total_docs*100:.1f}%)",
            f"- **Failed**: {failed_docs} ({failed_docs/total_docs*100:.1f}%)",
            f"- **Total Errors**: {total_errors}",
            f"- **Total Warnings**: {total_warnings}",
            "",
        ]

        if issues:
            lines.append("## Violations by Rule")
            lines.append("")
            lines.append("| Rule ID | Count |")
            lines.append("|---------|-------|")

            rule_counts = {}
            for issue in issues:
                rule_id = issue.rule_id
                if rule_id not in rule_counts:
                    rule_counts[rule_id] = 0
                rule_counts[rule_id] += 1

            for rule_id, count in sorted(rule_counts.items()):
                lines.append(f"| {rule_id} | {count} |")

            lines.append("")
            lines.append("## Failed Documents")
            lines.append("")

            for file_path, file_issues in sorted(issues_by_file.items()):
                lines.append(f"### {file_path}")
                lines.append("")
                for issue in file_issues:
                    severity_label = issue.severity.value.upper() if hasattr(issue.severity, 'value') else str(issue.severity).upper()
                    lines.append(f"- **[{severity_label}]** {issue.rule_id}: {issue.message}")
                    if issue.suggestion:
                        lines.append(f"  - Suggestion: {issue.suggestion}")
                lines.append("")

        report_md = '\n'.join(lines)

        if output:
            output.write_text(report_md, encoding='utf-8')
            click.echo(f"Report saved to: {output}")
        else:
            click.echo(report_md)


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


if __name__ == '__main__':
    cli(obj={})
