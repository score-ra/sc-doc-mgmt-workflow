#!/usr/bin/env python3
"""
Demo script to show auto-fix capabilities on a test document.
"""

from pathlib import Path
from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from src.core.auto_fixer import AutoFixer
from src.utils.frontmatter import parse_frontmatter


def main():
    """Demonstrate auto-fix capabilities."""
    # Initialize components
    config = Config()
    logger = Logger("demo", console_output=True, log_level="WARNING")
    validator = YAMLValidator(config, logger)
    fixer = AutoFixer(config, logger)

    # Test document
    test_doc = Path("test_document.md")

    print("=" * 80)
    print("AUTO-FIX DEMONSTRATION")
    print("=" * 80)

    # Step 1: Validate
    print("\n[STEP 1] Validating test document...")
    issues = validator.validate(test_doc)

    if issues:
        print(f"Found {len(issues)} issue(s):\n")
        for issue in issues:
            print(f"  - {issue.rule_id}: {issue.message}")
    else:
        print("No issues found!")
        return

    # Step 2: Preview fixes
    print("\n[STEP 2] Previewing auto-fixes...")
    preview_result = fixer.fix_document(test_doc, issues, preview=True)

    if preview_result.fixes_applied:
        print(f"\nProposed fixes ({len(preview_result.fixes_applied)}):")
        for fix in preview_result.fixes_applied:
            print(f"  - {fix}")
    else:
        print("No auto-fixes available for these issues.")
        return

    # Step 3: Apply fixes
    print("\n[STEP 3] Applying fixes...")
    fix_result = fixer.fix_document(test_doc, issues, preview=False)

    if fix_result.success:
        print("[OK] Fixes applied successfully!")
        if fix_result.backup_path:
            print(f"Backup created: {fix_result.backup_path}")
    else:
        print("[ERROR] Failed to apply fixes")
        for error in fix_result.errors:
            print(f"  - {error}")
        return

    # Step 4: Verify
    print("\n[STEP 4] Verifying fixes...")
    issues_after = validator.validate(test_doc)

    if not issues_after:
        print("[OK] Document is now valid!")
    else:
        print(f"[!] Still has {len(issues_after)} issue(s)")

    # Step 5: Show final frontmatter
    print("\n[STEP 5] Final YAML frontmatter:")
    print("-" * 40)
    metadata = parse_frontmatter(test_doc)
    import yaml
    print(yaml.dump(metadata, default_flow_style=False, sort_keys=False))
    print("-" * 40)

    print("\n[DEMO COMPLETE]")


if __name__ == "__main__":
    main()
