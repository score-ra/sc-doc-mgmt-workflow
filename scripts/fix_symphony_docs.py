#!/usr/bin/env python3
"""
Fix Missing Frontmatter in Symphony Core Documentation

This script uses the Sprint 2 auto-fixer to add YAML frontmatter to documents
in the Symphony Core documentation repository that are missing it.

Based on documentation review findings:
- 74 documents (42.5%) lack YAML frontmatter
- Primarily in: 02-marketing-brand, 03-sales, 04-operations
- Auto-fix will extract title from H1, suggest tags from path, set status to draft

Usage:
    # Preview mode (shows what will change, no modifications)
    python scripts/fix_symphony_docs.py --preview

    # Apply mode (makes changes with backups)
    python scripts/fix_symphony_docs.py --apply

    # Target specific section
    python scripts/fix_symphony_docs.py --preview --section 02-marketing-brand

    # Dry run on single file
    python scripts/fix_symphony_docs.py --preview --file path/to/doc.md
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from src.core.auto_fixer import AutoFixer
from src.utils.frontmatter import has_frontmatter


class SymphonyDocsFixer:
    """Fix missing frontmatter in Symphony Core documentation"""

    def __init__(self, docs_repo_path: Path, preview_mode: bool = True):
        """
        Initialize fixer for Symphony Core docs

        Args:
            docs_repo_path: Path to symphony-core-documents repository
            preview_mode: If True, only show what would change (no modifications)
        """
        self.docs_repo_path = Path(docs_repo_path)
        self.preview_mode = preview_mode

        # Initialize Sprint 2 components
        self.config = Config()
        self.logger = Logger("symphony-docs-fixer", console_output=True, log_level="INFO")
        self.validator = YAMLValidator(self.config, self.logger)
        self.fixer = AutoFixer(self.config, self.logger)

        # Statistics
        self.stats = {
            'total_scanned': 0,
            'missing_frontmatter': 0,
            'fixed': 0,
            'errors': 0,
            'by_section': defaultdict(lambda: {'scanned': 0, 'missing': 0, 'fixed': 0})
        }

    def find_documents_without_frontmatter(
        self,
        section: str = None,
        single_file: Path = None
    ) -> List[Path]:
        """
        Find all markdown documents without YAML frontmatter

        Args:
            section: Optional section to limit search (e.g., '02-marketing-brand')
            single_file: Optional single file to process

        Returns:
            List of Path objects for documents without frontmatter
        """
        if single_file:
            if not has_frontmatter(single_file):
                return [single_file]
            return []

        search_path = self.docs_repo_path
        if section:
            search_path = self.docs_repo_path / section
            if not search_path.exists():
                self.logger.error(f"Section not found: {section}")
                return []

        self.logger.info(f"Scanning for documents in: {search_path}")

        # Find all markdown files
        all_docs = list(search_path.glob("**/*.md"))
        self.logger.info(f"Found {len(all_docs)} markdown files")

        # Filter to those without frontmatter
        docs_without_frontmatter = []
        for doc in all_docs:
            # Skip README files
            if doc.name == "README.md":
                continue

            if not has_frontmatter(doc):
                docs_without_frontmatter.append(doc)

                # Track by section
                section_name = self._get_section_name(doc)
                self.stats['by_section'][section_name]['missing'] += 1

            # Update section stats
            section_name = self._get_section_name(doc)
            self.stats['by_section'][section_name]['scanned'] += 1
            self.stats['total_scanned'] += 1

        self.stats['missing_frontmatter'] = len(docs_without_frontmatter)

        self.logger.info(f"Found {len(docs_without_frontmatter)} documents without frontmatter")
        return docs_without_frontmatter

    def _get_section_name(self, file_path: Path) -> str:
        """Extract section name from file path (e.g., '02-marketing-brand')"""
        try:
            relative = file_path.relative_to(self.docs_repo_path)
            parts = relative.parts
            if parts[0].startswith(('0', '_')):  # Numbered sections or special folders
                return parts[0]
            return 'root'
        except ValueError:
            return 'unknown'

    def fix_documents(self, documents: List[Path]) -> Dict:
        """
        Fix frontmatter for list of documents

        Args:
            documents: List of document paths to fix

        Returns:
            Dictionary with results summary
        """
        results = {
            'successful': [],
            'failed': [],
            'skipped': []
        }

        mode_str = "[PREVIEW]" if self.preview_mode else "[APPLY]"
        self.logger.info(f"\n{mode_str} Processing {len(documents)} documents...")

        for i, doc in enumerate(documents, 1):
            try:
                self.logger.info(f"\n--- [{i}/{len(documents)}] {doc.name} ---")

                # Validate to get issues
                issues = self.validator.validate(doc)

                if not issues:
                    self.logger.info(f"[OK] {doc.name} has no issues")
                    results['skipped'].append(doc)
                    continue

                # Log issues
                self.logger.info(f"Found {len(issues)} issues:")
                for issue in issues:
                    self.logger.info(f"  - {issue.rule_id}: {issue.message}")

                # Fix document
                fix_result = self.fixer.fix_document(
                    doc,
                    issues,
                    preview=self.preview_mode
                )

                if fix_result.success:
                    results['successful'].append((doc, fix_result))
                    self.stats['fixed'] += 1

                    # Update section stats
                    section_name = self._get_section_name(doc)
                    self.stats['by_section'][section_name]['fixed'] += 1

                    # Log what was done
                    self.logger.info(f"[OK] Fixes applied:")
                    for fix in fix_result.fixes_applied:
                        self.logger.info(f"  + {fix}")

                    if not self.preview_mode and fix_result.backup_path:
                        self.logger.info(f"  Backup: {fix_result.backup_path}")
                else:
                    results['failed'].append((doc, fix_result))
                    self.stats['errors'] += 1

                    self.logger.error(f"[ERROR] Failed to fix {doc.name}")
                    if fix_result.errors:
                        for error in fix_result.errors:
                            self.logger.error(f"  ! {error}")

            except Exception as e:
                self.logger.error(f"[ERROR] Exception processing {doc.name}: {e}")
                results['failed'].append((doc, str(e)))
                self.stats['errors'] += 1

        return results

    def generate_report(self, results: Dict) -> str:
        """
        Generate summary report of fixing operation

        Args:
            results: Results dictionary from fix_documents()

        Returns:
            Formatted report string
        """
        mode_str = "PREVIEW MODE" if self.preview_mode else "APPLY MODE"

        report = f"""
{'='*80}
Symphony Core Documentation Frontmatter Fix Report
{'='*80}

Mode: {mode_str}
Repository: {self.docs_repo_path}

OVERALL STATISTICS
------------------
Total Documents Scanned:        {self.stats['total_scanned']}
Documents Missing Frontmatter:  {self.stats['missing_frontmatter']}
Documents Fixed:                {self.stats['fixed']}
Errors:                         {self.stats['errors']}

RESULTS BREAKDOWN
-----------------
Successful Fixes:  {len(results['successful'])}
Failed:            {len(results['failed'])}
Skipped (no issues): {len(results['skipped'])}

STATISTICS BY SECTION
---------------------
"""

        for section_name in sorted(self.stats['by_section'].keys()):
            section_stats = self.stats['by_section'][section_name]
            coverage_before = ((section_stats['scanned'] - section_stats['missing']) /
                              section_stats['scanned'] * 100) if section_stats['scanned'] > 0 else 0
            coverage_after = ((section_stats['scanned'] - section_stats['missing'] + section_stats['fixed']) /
                             section_stats['scanned'] * 100) if section_stats['scanned'] > 0 else 0

            report += f"\n{section_name}:\n"
            report += f"  Scanned: {section_stats['scanned']}\n"
            report += f"  Missing Frontmatter: {section_stats['missing']}\n"
            report += f"  Fixed: {section_stats['fixed']}\n"
            report += f"  Coverage Before: {coverage_before:.1f}%\n"
            report += f"  Coverage After: {coverage_after:.1f}%\n"

        if results['successful']:
            report += f"\nSUCCESSFUL FIXES ({len(results['successful'])}):\n"
            report += "-" * 80 + "\n"
            for doc, fix_result in results['successful']:
                relative_path = doc.relative_to(self.docs_repo_path)
                report += f"\n{relative_path}:\n"
                for fix in fix_result.fixes_applied:
                    report += f"  + {fix}\n"

        if results['failed']:
            report += f"\nFAILED FIXES ({len(results['failed'])}):\n"
            report += "-" * 80 + "\n"
            for item in results['failed']:
                if isinstance(item, tuple):
                    doc, error = item
                    relative_path = doc.relative_to(self.docs_repo_path) if isinstance(doc, Path) else doc
                    report += f"\n{relative_path}:\n"
                    if hasattr(error, 'errors'):
                        for err in error.errors:
                            report += f"  ! {err}\n"
                    else:
                        report += f"  ! {error}\n"

        if self.preview_mode:
            report += f"\n{'='*80}\n"
            report += "NOTE: This was a PREVIEW run. No files were modified.\n"
            report += "Run with --apply to make actual changes.\n"
            report += f"{'='*80}\n"
        else:
            report += f"\n{'='*80}\n"
            report += "Changes have been applied with timestamped backups.\n"
            report += f"Backups location: {self.docs_repo_path.parent / '_meta' / '.backups'}\n"
            report += f"{'='*80}\n"

        return report


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Fix missing YAML frontmatter in Symphony Core documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what would be fixed (safe, no changes)
  python scripts/fix_symphony_docs.py --preview

  # Apply fixes to all documents
  python scripts/fix_symphony_docs.py --apply

  # Preview fixes for specific section
  python scripts/fix_symphony_docs.py --preview --section 02-marketing-brand

  # Apply fixes to specific section
  python scripts/fix_symphony_docs.py --apply --section 03-sales

  # Test on single file
  python scripts/fix_symphony_docs.py --preview --file path/to/doc.md
        """
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview mode: show what would be fixed without making changes'
    )

    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply mode: make actual changes with backups'
    )

    parser.add_argument(
        '--section',
        type=str,
        help='Target specific section (e.g., 02-marketing-brand, 03-sales)'
    )

    parser.add_argument(
        '--file',
        type=Path,
        help='Target single file for testing'
    )

    parser.add_argument(
        '--docs-path',
        type=Path,
        default=Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents"),
        help='Path to symphony-core-documents repository'
    )

    parser.add_argument(
        '--report-file',
        type=Path,
        help='Save report to file (optional)'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt (auto-confirm)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.preview and not args.apply:
        print("Error: Must specify either --preview or --apply")
        parser.print_help()
        sys.exit(1)

    if args.preview and args.apply:
        print("Error: Cannot specify both --preview and --apply")
        parser.print_help()
        sys.exit(1)

    # Check docs path exists
    if not args.docs_path.exists():
        print(f"Error: Documentation repository not found at: {args.docs_path}")
        sys.exit(1)

    # Initialize fixer
    preview_mode = args.preview
    fixer = SymphonyDocsFixer(args.docs_path, preview_mode=preview_mode)

    # Find documents to fix
    docs_to_fix = fixer.find_documents_without_frontmatter(
        section=args.section,
        single_file=args.file
    )

    if not docs_to_fix:
        print("\n[OK] No documents found that need fixing!")
        print("All documents already have YAML frontmatter.")
        sys.exit(0)

    # Show what will be processed
    print(f"\nFound {len(docs_to_fix)} documents without frontmatter:")
    for doc in docs_to_fix[:10]:  # Show first 10
        relative = doc.relative_to(args.docs_path)
        print(f"  - {relative}")
    if len(docs_to_fix) > 10:
        print(f"  ... and {len(docs_to_fix) - 10} more")

    # Confirm if applying
    if not preview_mode and not args.yes:
        response = input(f"\n[!] Apply fixes to {len(docs_to_fix)} documents? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            sys.exit(0)
    elif not preview_mode and args.yes:
        print(f"\n[AUTO-CONFIRMED] Applying fixes to {len(docs_to_fix)} documents...")

    # Fix documents
    results = fixer.fix_documents(docs_to_fix)

    # Generate report
    report = fixer.generate_report(results)
    print(report)

    # Save report if requested
    if args.report_file:
        args.report_file.write_text(report)
        print(f"\nReport saved to: {args.report_file}")

    # Exit code
    if results['failed']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
