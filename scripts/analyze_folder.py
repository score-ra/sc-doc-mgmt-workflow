#!/usr/bin/env python3
"""
Comprehensive analysis of a documentation folder

Runs all validators and generates detailed report
"""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.logger import Logger
from src.core.validators.yaml_validator import YAMLValidator
from src.core.validators.naming_validator import NamingValidator
from src.core.validators.markdown_validator import MarkdownValidator
from src.core.validators.conflict_detector import ConflictDetector


def analyze_folder(folder_path: Path):
    """Analyze a folder with all validators."""

    # Setup
    config = Config()
    # Disable trailing whitespace check (too noisy)
    config.config_data['validation']['markdown']['check_trailing_whitespace'] = False

    logger = Logger("analyzer", console_output=False, log_level="ERROR")

    yaml_validator = YAMLValidator(config, logger)
    naming_validator = NamingValidator(config, logger)
    markdown_validator = MarkdownValidator(config, logger)
    conflict_detector = ConflictDetector(config, logger)

    # Find all markdown files (excluding README.md)
    all_docs = list(folder_path.glob("**/*.md"))
    all_docs = [d for d in all_docs if d.name != "README.md"]

    if not all_docs:
        print(f"No markdown documents found in {folder_path}")
        return

    # Print header
    print("\n" + "="*80)
    print("SYMPHONY CORE - COMPREHENSIVE FOLDER ANALYSIS")
    print("="*80)
    print(f"\nFolder: {folder_path}")
    print(f"Documents: {len(all_docs)}\n")

    # List files
    print("-"*80)
    print("DOCUMENTS FOUND:")
    print("-"*80)
    for doc in sorted(all_docs):
        relative = doc.relative_to(folder_path)
        print(f"  - {relative}")

    # Run YAML validation
    print("\n" + "="*80)
    print("1. YAML FRONTMATTER VALIDATION")
    print("="*80)

    yaml_results = {}
    yaml_passed = 0
    yaml_failed = 0
    yaml_issues_by_rule = defaultdict(int)

    for doc in all_docs:
        issues = yaml_validator.validate(doc)
        if issues:
            yaml_results[doc] = issues
            yaml_failed += 1
            for issue in issues:
                yaml_issues_by_rule[issue.rule_id] += 1
        else:
            yaml_passed += 1

    print(f"\nPassed: {yaml_passed}/{len(all_docs)} ({yaml_passed/len(all_docs)*100:.1f}%)")
    print(f"Failed: {yaml_failed}/{len(all_docs)} ({yaml_failed/len(all_docs)*100:.1f}%)")

    if yaml_issues_by_rule:
        print("\nIssues by Rule:")
        for rule_id in sorted(yaml_issues_by_rule.keys()):
            print(f"  {rule_id}: {yaml_issues_by_rule[rule_id]}")

    if yaml_results:
        print("\nDetailed Issues:")
        for doc, issues in sorted(yaml_results.items()):
            relative = doc.relative_to(folder_path)
            print(f"\n  {relative}:")
            for issue in issues:
                print(f"    [{issue.severity.value.upper()}] {issue.rule_id}: {issue.message}")
                if issue.suggestion:
                    print(f"    Suggestion: {issue.suggestion[:100]}...")

    # Run Naming validation
    print("\n" + "="*80)
    print("2. NAMING CONVENTION VALIDATION")
    print("="*80)

    naming_results = {}
    naming_passed = 0
    naming_failed = 0
    naming_issues_by_rule = defaultdict(int)

    for doc in all_docs:
        issues = naming_validator.validate(doc, base_path=folder_path)
        if issues:
            naming_results[doc] = issues
            naming_failed += 1
            for issue in issues:
                naming_issues_by_rule[issue.rule_id] += 1
        else:
            naming_passed += 1

    print(f"\nPassed: {naming_passed}/{len(all_docs)} ({naming_passed/len(all_docs)*100:.1f}%)")
    print(f"Failed: {naming_failed}/{len(all_docs)} ({naming_failed/len(all_docs)*100:.1f}%)")

    if naming_issues_by_rule:
        print("\nIssues by Rule:")
        for rule_id in sorted(naming_issues_by_rule.keys()):
            print(f"  {rule_id}: {naming_issues_by_rule[rule_id]}")

    if naming_results:
        print("\nDetailed Issues:")
        for doc, issues in sorted(naming_results.items()):
            relative = doc.relative_to(folder_path)
            print(f"\n  {relative}:")
            for issue in issues:
                print(f"    [{issue.severity.value.upper()}] {issue.rule_id}: {issue.message}")
                if issue.suggestion:
                    print(f"    Suggestion: {issue.suggestion}")

    # Run Markdown validation
    print("\n" + "="*80)
    print("3. MARKDOWN SYNTAX VALIDATION")
    print("="*80)

    markdown_results = {}
    markdown_passed = 0
    markdown_failed = 0
    markdown_issues_by_rule = defaultdict(int)

    for doc in all_docs:
        issues = markdown_validator.validate(doc, base_path=folder_path)
        if issues:
            markdown_results[doc] = issues
            markdown_failed += 1
            for issue in issues:
                markdown_issues_by_rule[issue.rule_id] += 1
        else:
            markdown_passed += 1

    print(f"\nPassed: {markdown_passed}/{len(all_docs)} ({markdown_passed/len(all_docs)*100:.1f}%)")
    print(f"Failed: {markdown_failed}/{len(all_docs)} ({markdown_failed/len(all_docs)*100:.1f}%)")

    if markdown_issues_by_rule:
        print("\nIssues by Rule:")
        for rule_id in sorted(markdown_issues_by_rule.keys()):
            print(f"  {rule_id}: {markdown_issues_by_rule[rule_id]}")

    if markdown_results:
        print("\nSample Issues (first 3 per file):")
        for doc, issues in sorted(markdown_results.items()):
            relative = doc.relative_to(folder_path)
            print(f"\n  {relative}:")
            for issue in issues[:3]:
                print(f"    [{issue.severity.value.upper()}] {issue.rule_id} Line {issue.line_number}: {issue.message}")
            if len(issues) > 3:
                print(f"    ... and {len(issues) - 3} more issues")

    # Run Conflict detection
    print("\n" + "="*80)
    print("4. CONFLICT DETECTION (Corpus-Level)")
    print("="*80)

    conflicts = conflict_detector.detect_conflicts(all_docs, base_path=folder_path)
    total_conflicts = sum(len(issues) for issues in conflicts.values())

    print(f"\nTotal Conflicts: {total_conflicts}")

    for conflict_type, issues in conflicts.items():
        if issues:
            print(f"\n{conflict_type.upper()} Conflicts: {len(issues)}")
            for issue in issues:
                print(f"  [{issue.rule_id}] {issue.message}")
                if issue.suggestion:
                    print(f"  Suggestion: {issue.suggestion}")

    # Overall Summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)

    total_issues = (
        sum(len(issues) for issues in yaml_results.values()) +
        sum(len(issues) for issues in naming_results.values()) +
        sum(len(issues) for issues in markdown_results.values()) +
        total_conflicts
    )

    print(f"\nTotal Documents Analyzed: {len(all_docs)}")
    print(f"\nValidation Results:")
    print(f"  YAML:      {yaml_passed}/{len(all_docs)} passed")
    print(f"  Naming:    {naming_passed}/{len(all_docs)} passed")
    print(f"  Markdown:  {markdown_passed}/{len(all_docs)} passed")
    print(f"  Conflicts: {total_conflicts} detected")
    print(f"\nTotal Issues Found: {total_issues}")

    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    if yaml_failed > 0:
        print(f"\n1. YAML Frontmatter: {yaml_failed} document(s) need attention")
        if 'YAML-001' in yaml_issues_by_rule:
            print("   - Add frontmatter blocks to documents missing them")
        if 'YAML-002' in yaml_issues_by_rule:
            print("   - Add required fields (title, tags, status)")
        if 'YAML-003' in yaml_issues_by_rule:
            print("   - Fix invalid status values")

    if naming_failed > 0:
        print(f"\n2. Naming Conventions: {naming_failed} document(s) need attention")
        if 'NAME-001' in naming_issues_by_rule:
            print("   - Rename files/directories to lowercase-with-hyphens")
        if 'NAME-002' in naming_issues_by_rule:
            print("   - Remove spaces from filenames (use hyphens)")

    if markdown_failed > 0:
        print(f"\n3. Markdown Syntax: {markdown_failed} document(s) need attention")
        if 'MD-002' in markdown_issues_by_rule:
            print(f"   - Add language specifications to {markdown_issues_by_rule['MD-002']} code block(s)")
        if 'MD-003' in markdown_issues_by_rule:
            print(f"   - Fix {markdown_issues_by_rule['MD-003']} broken or problematic link(s)")
        if 'MD-001' in markdown_issues_by_rule:
            print(f"   - Fix {markdown_issues_by_rule['MD-001']} heading hierarchy issue(s)")

    if total_conflicts > 0:
        print(f"\n4. Conflicts: {total_conflicts} conflict(s) detected")
        print("   - Review and resolve metadata conflicts across documents")

    if total_issues == 0:
        print("\n[PASS] No issues found! This folder is in excellent shape.")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80 + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_folder.py <folder_path>")
        sys.exit(1)

    folder_path = Path(sys.argv[1])

    if not folder_path.exists():
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)

    if not folder_path.is_dir():
        print(f"Error: Not a directory: {folder_path}")
        sys.exit(1)

    analyze_folder(folder_path)
