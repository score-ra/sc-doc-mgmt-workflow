#!/usr/bin/env python3
"""
Validate ALL Symphony Core documentation

Runs YAML validation on entire documentation repository
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from collections import defaultdict


def main():
    docs_repo = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")

    config = Config()
    logger = Logger("validator", console_output=True, log_level="WARNING")
    validator = YAMLValidator(config, logger)

    # Find ALL markdown files
    all_docs = list(docs_repo.glob("**/*.md"))
    # Exclude READMEs
    all_docs = [d for d in all_docs if d.name != "README.md"]

    print(f"\n{'='*80}")
    print("SYMPHONY CORE DOCUMENTATION - FULL YAML VALIDATION")
    print(f"{'='*80}")
    print(f"\nScanning: {docs_repo}")
    print(f"Found: {len(all_docs)} markdown documents\n")

    # Track results
    passed = []
    failed = []
    by_section = defaultdict(lambda: {'passed': 0, 'failed': 0, 'issues': []})

    for doc in sorted(all_docs):
        relative = doc.relative_to(docs_repo)
        section = relative.parts[0] if relative.parts else 'root'

        issues = validator.validate(doc)

        if issues:
            failed.append((doc, issues))
            by_section[section]['failed'] += 1
            by_section[section]['issues'].extend(issues)
            print(f"[FAIL] {relative}")
            for issue in issues:
                print(f"   {issue.rule_id}: {issue.message}")
        else:
            passed.append(doc)
            by_section[section]['passed'] += 1

    # Summary
    print(f"\n{'='*80}")
    print("VALIDATION SUMMARY")
    print(f"{'='*80}")
    print(f"\nTotal Documents: {len(all_docs)}")
    print(f"Passed: {len(passed)} ({len(passed)/len(all_docs)*100:.1f}%)")
    print(f"Failed: {len(failed)} ({len(failed)/len(all_docs)*100:.1f}%)")

    # By section
    print(f"\n{'='*80}")
    print("RESULTS BY SECTION")
    print(f"{'='*80}\n")

    for section in sorted(by_section.keys()):
        stats = by_section[section]
        total = stats['passed'] + stats['failed']
        pass_rate = stats['passed'] / total * 100 if total > 0 else 0

        status = "[OK]" if stats['failed'] == 0 else "[FAIL]"
        print(f"{status} {section:20s}  {stats['passed']:3d}/{total:3d} passed ({pass_rate:.1f}%)")

    if failed:
        print(f"\n{'='*80}")
        print(f"FAILED DOCUMENTS ({len(failed)})")
        print(f"{'='*80}\n")
        for doc, issues in failed[:10]:  # Show first 10
            relative = doc.relative_to(docs_repo)
            print(f"{relative}:")
            for issue in issues:
                print(f"  - {issue.rule_id}: {issue.message}")
        if len(failed) > 10:
            print(f"\n... and {len(failed) - 10} more failures")

    print(f"\n{'='*80}")
    if failed:
        print(f"[FAIL] Validation found {len(failed)} documents with issues")
        print(f"{'='*80}\n")
        return 1
    else:
        print(f"[OK] All {len(all_docs)} documents passed validation!")
        print(f"{'='*80}\n")
        return 0


if __name__ == '__main__':
    sys.exit(main())
