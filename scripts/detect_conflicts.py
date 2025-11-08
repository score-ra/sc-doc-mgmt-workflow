#!/usr/bin/env python3
"""
Detect conflicts in Symphony Core documentation

Runs conflict detection across entire documentation repository
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.conflict_detector import ConflictDetector


def main():
    docs_repo = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")

    config = Config()
    logger = Logger("conflict-detector", console_output=True, log_level="WARNING")
    detector = ConflictDetector(config, logger)

    # Find ALL markdown files
    all_docs = list(docs_repo.glob("**/*.md"))
    # Exclude READMEs
    all_docs = [d for d in all_docs if d.name != "README.md"]

    print(f"\n{'='*80}")
    print("SYMPHONY CORE DOCUMENTATION - CONFLICT DETECTION")
    print(f"{'='*80}")
    print(f"\nScanning: {docs_repo}")
    print(f"Found: {len(all_docs)} markdown documents\n")
    print("Analyzing conflicts across corpus...")

    # Detect conflicts
    conflicts = detector.detect_conflicts(all_docs, base_path=docs_repo)

    # Count total issues
    total_conflicts = sum(len(issues) for issues in conflicts.values())

    print(f"\n{'='*80}")
    print("CONFLICT DETECTION SUMMARY")
    print(f"{'='*80}")
    print(f"\nTotal Conflicts Found: {total_conflicts}\n")

    # Breakdown by type
    for conflict_type, issues in conflicts.items():
        if issues:
            print(f"{conflict_type.upper()}: {len(issues)} conflict(s)")

    # Detailed breakdown
    print(f"\n{'='*80}")
    print("DETAILED CONFLICT REPORT")
    print(f"{'='*80}\n")

    for conflict_type, issues in conflicts.items():
        if issues:
            print(f"\n{conflict_type.upper()} CONFLICTS ({len(issues)}):")
            print("-" * 80)

            for issue in issues[:10]:  # Show first 10
                print(f"\n[{issue.rule_id}] {issue.file_path.name}")
                print(f"  {issue.message}")
                if issue.suggestion:
                    print(f"  Suggestion: {issue.suggestion}")

            if len(issues) > 10:
                print(f"\n... and {len(issues) - 10} more {conflict_type} conflicts")

    print(f"\n{'='*80}")
    if total_conflicts > 0:
        print(f"[FAIL] Found {total_conflicts} conflicts across documentation")
        print(f"{'='*80}\n")
        return 1
    else:
        print(f"[OK] No conflicts detected in {len(all_docs)} documents!")
        print(f"{'='*80}\n")
        return 0


if __name__ == '__main__':
    sys.exit(main())
