#!/usr/bin/env python3
"""
Validate markdown syntax in Symphony Core documentation

Runs markdown validation on entire documentation repository
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.markdown_validator import MarkdownValidator
from collections import defaultdict


def main():
    docs_repo = Path(r"C:\Users\Rohit\workspace\Work\docs\symphonycore\symphony-core-documents")

    config = Config()
    # Disable trailing whitespace check for now (too noisy)
    config.config_data['validation']['markdown']['check_trailing_whitespace'] = False

    logger = Logger("markdown-validator", console_output=True, log_level="WARNING")
    validator = MarkdownValidator(config, logger)

    # Find ALL markdown files
    all_docs = list(docs_repo.glob("**/*.md"))
    # Exclude READMEs
    all_docs = [d for d in all_docs if d.name != "README.md"]

    print(f"\n{'='*80}")
    print("SYMPHONY CORE DOCUMENTATION - MARKDOWN SYNTAX VALIDATION")
    print(f"{'='*80}")
    print(f"\nScanning: {docs_repo}")
    print(f"Found: {len(all_docs)} markdown documents\n")

    # Track results
    passed = []
    failed = []
    by_section = defaultdict(lambda: {'passed': 0, 'failed': 0, 'issues': []})
    by_rule = defaultdict(int)

    for doc in sorted(all_docs):
        relative = doc.relative_to(docs_repo)
        section = relative.parts[0] if relative.parts else 'root'

        issues = validator.validate(doc, base_path=docs_repo)

        if issues:
            failed.append((doc, issues))
            by_section[section]['failed'] += 1
            by_section[section]['issues'].extend(issues)

            for issue in issues:
                by_rule[issue.rule_id] += 1
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

    # Violations by rule
    print(f"\n{'='*80}")
    print("VIOLATIONS BY RULE")
    print(f"{'='*80}\n")
    for rule_id in sorted(by_rule.keys()):
        count = by_rule[rule_id]
        print(f"  {rule_id}: {count:3d} violations")

    # By section
    print(f"\n{'='*80}")
    print("RESULTS BY SECTION")
    print(f"{'='*80}\n")

    for section in sorted(by_section.keys()):
        stats = by_section[section]
        total = stats['passed'] + stats['failed']
        pass_rate = stats['passed'] / total * 100 if total > 0 else 0

        status = "[OK]" if stats['failed'] == 0 else "[FAIL]"
        print(f"{status} {section:25s}  {stats['passed']:3d}/{total:3d} passed ({pass_rate:.1f}%)")

    if failed:
        print(f"\n{'='*80}")
        print(f"SAMPLE VIOLATIONS (showing first 15)")
        print(f"{'='*80}\n")
        for doc, issues in failed[:15]:
            relative = doc.relative_to(docs_repo)
            print(f"\n{relative}:")
            for issue in issues[:3]:  # Show first 3 issues per file
                # Handle Unicode encoding for Windows console
                try:
                    print(f"  [{issue.rule_id}] Line {issue.line_number}: {issue.message}")
                except UnicodeEncodeError:
                    # Fallback to ASCII-safe output
                    safe_message = issue.message.encode('ascii', 'replace').decode('ascii')
                    print(f"  [{issue.rule_id}] Line {issue.line_number}: {safe_message}")

        if len(failed) > 15:
            print(f"\n... and {len(failed) - 15} more files with violations")

    print(f"\n{'='*80}")
    if failed:
        print(f"[FAIL] Found {len(failed)} files with markdown violations")
        print(f"       Total violations: {sum(by_rule.values())}")
        print(f"{'='*80}\n")
        return 1
    else:
        print(f"[OK] All {len(all_docs)} documents passed markdown validation!")
        print(f"{'='*80}\n")
        return 0


if __name__ == '__main__':
    sys.exit(main())
