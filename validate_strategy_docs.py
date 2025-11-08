#!/usr/bin/env python3
"""
Validation script for Symphony Core strategy documents.
Tests Sprint 2 YAML validation and auto-fix capabilities.
"""

from pathlib import Path
from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from src.core.auto_fixer import AutoFixer


def main():
    """Validate strategy documents."""
    # Initialize components
    config = Config()
    logger = Logger("validator", console_output=True, log_level="WARNING")
    validator = YAMLValidator(config, logger)
    fixer = AutoFixer(config, logger)

    # Documents to validate
    doc_dir = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents\01-strategy")

    if not doc_dir.exists():
        print(f"❌ Directory not found: {doc_dir}")
        return

    # Find all markdown files
    md_files = list(doc_dir.glob("**/*.md"))

    print("=" * 80)
    print("SYMPHONY CORE STRATEGY DOCUMENTS - YAML VALIDATION REPORT")
    print("=" * 80)
    print(f"\nFound {len(md_files)} markdown documents")
    print(f"Location: {doc_dir}\n")

    # Validate each document
    all_results = {}
    total_issues = 0
    fixable_count = 0

    for doc_file in sorted(md_files):
        rel_path = doc_file.relative_to(doc_dir)
        issues = validator.validate(doc_file)

        if issues:
            all_results[doc_file] = issues
            total_issues += len(issues)

            # Count fixable issues
            fixable = [i for i in issues if fixer.can_fix(i)]
            if fixable:
                fixable_count += 1

    # Display results
    if not all_results:
        print("[OK] All documents are valid! No issues found.\n")
        return

    print(f"[!] Found issues in {len(all_results)} document(s)\n")
    print("-" * 80)

    for doc_file, issues in all_results.items():
        rel_path = doc_file.relative_to(doc_dir)
        error_count = validator.get_error_count(issues)
        warning_count = validator.get_warning_count(issues)

        print(f"\n[FILE] {rel_path}")
        print(f"   Errors: {error_count}, Warnings: {warning_count}")

        for issue in issues:
            print(f"\n   {issue}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total documents: {len(md_files)}")
    print(f"Documents with issues: {len(all_results)}")
    print(f"Total issues: {total_issues}")
    print(f"Documents with auto-fixable issues: {fixable_count}")

    if fixable_count > 0:
        print("\n[TIP] Run auto-fix to automatically resolve these issues:")
        print("   Preview: python validate_strategy_docs.py --fix --preview")
        print("   Apply:   python validate_strategy_docs.py --fix")


if __name__ == "__main__":
    main()
