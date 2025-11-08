"""
Semantic conflict detection across documentation corpus.

This module detects conflicts and inconsistencies across multiple documents,
including metadata conflicts, pricing conflicts, and cross-reference issues.
"""

from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict
import re

from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.frontmatter import parse_frontmatter, has_frontmatter
from src.core.validators.yaml_validator import ValidationIssue, ValidationSeverity


class ConflictDetector:
    """
    Detects semantic conflicts across document corpus.

    Implements validation rules:
    - CONFLICT-001: Status value conflicts (non-standard values, case mismatches)
    - CONFLICT-002: Tag synonym conflicts (same concept, different tag)
    - CONFLICT-003: Pricing conflicts (inconsistent pricing information)
    - CONFLICT-004: Cross-reference validation (links to deprecated docs)
    """

    def __init__(self, config: Config, logger: Logger):
        """
        Initialize conflict detector.

        Args:
            config: Configuration object with validation settings
            logger: Logger for diagnostic messages
        """
        self.config = config
        self.logger = logger

        # Load conflict detection settings from config
        self.enabled = config.get('validation.conflicts.enabled', True)
        self.allowed_status_values = config.get(
            'validation.yaml.allowed_statuses',
            ['draft', 'review', 'approved', 'active', 'deprecated', 'archived']
        )

        # Tag synonym mapping (e.g., 'ghl' -> 'gohighlevel')
        self.tag_synonyms = config.get(
            'validation.conflicts.tag_synonyms',
            {
                'ghl': 'gohighlevel',
                'wp': 'wordpress',
                'sc': 'symphony-core'
            }
        )

        # Pricing patterns to extract
        self.pricing_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:/|per)?\s*(month|mo|year|yr)',  # $99/month, $1,200 per year
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*dollars?\s*(?:/|per)?\s*(month|mo|year|yr)',  # 99 dollars/month
        ]

    def detect_conflicts(
        self,
        file_paths: List[Path],
        base_path: Optional[Path] = None
    ) -> Dict[str, List[ValidationIssue]]:
        """
        Detect conflicts across multiple documents.

        Args:
            file_paths: List of document paths to analyze
            base_path: Base repository path

        Returns:
            Dictionary mapping conflict types to lists of issues
        """
        if not self.enabled:
            self.logger.debug("Conflict detection disabled")
            return {}

        self.logger.info(f"Analyzing {len(file_paths)} documents for conflicts...")

        # Build document corpus
        documents = self._load_documents(file_paths)

        # Detect different types of conflicts
        conflicts = {
            'status': self._detect_status_conflicts(documents),
            'tags': self._detect_tag_conflicts(documents),
            'pricing': self._detect_pricing_conflicts(documents),
            'cross_references': self._detect_cross_reference_conflicts(documents, base_path)
        }

        # Flatten into single list
        all_issues = []
        for conflict_type, issues in conflicts.items():
            all_issues.extend(issues)

        self.logger.info(f"Found {len(all_issues)} potential conflicts")

        return conflicts

    def _load_documents(self, file_paths: List[Path]) -> List[Dict]:
        """
        Load documents and extract metadata.

        Returns list of document dictionaries with:
        - path: Path to document
        - metadata: Parsed frontmatter (or empty dict)
        - content: Full document content
        """
        documents = []

        for file_path in file_paths:
            try:
                if not file_path.exists():
                    continue

                content = file_path.read_text(encoding='utf-8')

                # Try to parse frontmatter
                metadata = {}
                if has_frontmatter(file_path):
                    try:
                        metadata = parse_frontmatter(file_path)
                    except Exception as e:
                        self.logger.warning(f"Could not parse frontmatter in {file_path}: {e}")

                documents.append({
                    'path': file_path,
                    'metadata': metadata,
                    'content': content
                })

            except Exception as e:
                self.logger.error(f"Error loading document {file_path}: {e}")

        return documents

    def _detect_status_conflicts(self, documents: List[Dict]) -> List[ValidationIssue]:
        """
        Detect status value conflicts.

        Implements CONFLICT-001: Status value validation across corpus.
        Detects:
        - Non-standard status values
        - Case variations (draft vs Draft)
        """
        issues = []
        status_variations = defaultdict(list)  # status_value -> list of docs

        for doc in documents:
            metadata = doc['metadata']
            if 'status' in metadata:
                status = metadata['status']
                if isinstance(status, str):
                    status_variations[status].append(doc['path'])

        # Check for case variations of same status
        status_by_lowercase = defaultdict(set)
        for status_value in status_variations.keys():
            status_by_lowercase[status_value.lower()].add(status_value)

        for lowercase_status, variations in status_by_lowercase.items():
            if len(variations) > 1:
                # Multiple case variations exist
                doc_paths = []
                for variant in variations:
                    doc_paths.extend(status_variations[variant])

                # Report on first document with non-standard casing
                primary_docs = status_variations[list(variations)[0]]
                issues.append(ValidationIssue(
                    rule_id="CONFLICT-001",
                    severity=ValidationSeverity.WARNING,
                    message=f"Status value has case variations: {', '.join(sorted(variations))}",
                    file_path=primary_docs[0],
                    suggestion=f"Standardize to lowercase: '{lowercase_status}'"
                ))

        # Check for non-standard status values
        for status_value, doc_paths in status_variations.items():
            if status_value not in self.allowed_status_values:
                issues.append(ValidationIssue(
                    rule_id="CONFLICT-001",
                    severity=ValidationSeverity.ERROR,
                    message=f"Non-standard status value: '{status_value}' used in {len(doc_paths)} document(s)",
                    file_path=doc_paths[0],
                    suggestion=f"Use one of: {', '.join(self.allowed_status_values)}"
                ))

        return issues

    def _detect_tag_conflicts(self, documents: List[Dict]) -> List[ValidationIssue]:
        """
        Detect tag synonym conflicts.

        Implements CONFLICT-002: Tag synonym detection.
        Detects tags that are synonyms but use different names.
        """
        issues = []
        tag_usage = defaultdict(list)  # tag -> list of docs

        for doc in documents:
            metadata = doc['metadata']
            if 'tags' in metadata and isinstance(metadata['tags'], list):
                for tag in metadata['tags']:
                    if isinstance(tag, str):
                        tag_usage[tag.lower()].append(doc['path'])

        # Check for synonym usage
        for tag, doc_paths in tag_usage.items():
            # Check if this tag has a canonical form in synonym map
            if tag in self.tag_synonyms:
                canonical = self.tag_synonyms[tag]

                # Check if canonical form is also used
                if canonical.lower() in tag_usage:
                    issues.append(ValidationIssue(
                        rule_id="CONFLICT-002",
                        severity=ValidationSeverity.WARNING,
                        message=f"Tag synonym conflict: '{tag}' and '{canonical}' both used",
                        file_path=doc_paths[0],
                        suggestion=f"Standardize to canonical form: '{canonical}'"
                    ))

        return issues

    def _detect_pricing_conflicts(self, documents: List[Dict]) -> List[ValidationIssue]:
        """
        Detect pricing conflicts across documents.

        Implements CONFLICT-003: Pricing conflict detection.
        Extracts pricing information and identifies inconsistencies.
        """
        issues = []
        pricing_mentions = defaultdict(list)  # product_context -> list of (price, unit, doc_path)

        for doc in documents:
            content = doc['content']
            path = doc['path']

            # Extract pricing mentions from content
            for pattern in self.pricing_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    amount = match.group(1).replace(',', '')  # Remove commas
                    unit = match.group(2).lower()

                    # Normalize to monthly price
                    price_monthly = self._normalize_to_monthly(float(amount), unit)

                    # Try to extract context (nearby words)
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].lower()

                    # Simple product identification (can be enhanced)
                    product = self._identify_product_from_context(context, path)

                    pricing_mentions[product].append({
                        'price': price_monthly,
                        'original': match.group(0),
                        'path': path,
                        'context': context
                    })

        # Check for pricing conflicts within each product
        for product, mentions in pricing_mentions.items():
            if len(mentions) > 1:
                prices = [m['price'] for m in mentions]
                unique_prices = set(prices)

                if len(unique_prices) > 1:
                    # Price conflict detected
                    price_list = ', '.join(f"${p:.2f}/mo" for p in sorted(unique_prices))
                    doc_list = set(m['path'] for m in mentions)

                    issues.append(ValidationIssue(
                        rule_id="CONFLICT-003",
                        severity=ValidationSeverity.ERROR,
                        message=f"Pricing conflict for '{product}': {price_list} across {len(doc_list)} document(s)",
                        file_path=list(doc_list)[0],
                        suggestion="Review and standardize pricing across all documents"
                    ))

        return issues

    def _detect_cross_reference_conflicts(
        self,
        documents: List[Dict],
        base_path: Optional[Path]
    ) -> List[ValidationIssue]:
        """
        Detect cross-reference conflicts.

        Implements CONFLICT-004: Cross-reference validation.
        Detects references to deprecated or non-existent documents.
        """
        issues = []

        if not base_path:
            return issues

        # Build map of deprecated documents
        deprecated_docs = set()
        for doc in documents:
            metadata = doc['metadata']
            if metadata.get('status') == 'deprecated':
                deprecated_docs.add(doc['path'])

        # Check for links to deprecated docs
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for doc in documents:
            content = doc['content']
            path = doc['path']
            metadata = doc['metadata']

            # Skip if this document itself is deprecated
            if metadata.get('status') == 'deprecated':
                continue

            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_url = match.group(2)

                # Skip external links and anchors
                if link_url.startswith(('http://', 'https://', '#')):
                    continue

                # Resolve relative link
                link_target = link_url.split('#')[0]
                if link_target:
                    target_path = (path.parent / link_target).resolve()

                    # Check if target is deprecated
                    if target_path in deprecated_docs:
                        issues.append(ValidationIssue(
                            rule_id="CONFLICT-004",
                            severity=ValidationSeverity.WARNING,
                            message=f"Link to deprecated document: '{link_url}'",
                            file_path=path,
                            suggestion="Update link to current documentation or remove if obsolete"
                        ))

        return issues

    def _normalize_to_monthly(self, amount: float, unit: str) -> float:
        """Normalize pricing to monthly rate."""
        unit_lower = unit.lower()
        if unit_lower in ['year', 'yr', 'annual', 'annually']:
            return amount / 12
        return amount  # Already monthly

    def _identify_product_from_context(self, context: str, path: Path) -> str:
        """
        Identify product/service from context.

        Simple heuristic: look for common product keywords.
        Can be enhanced with more sophisticated NLP.
        """
        # Extract from path
        path_parts = path.parts
        if 'pricing' in path_parts or 'sales' in path_parts:
            # Look for common product names in context
            products = ['basic', 'standard', 'premium', 'pro', 'enterprise', 'starter']
            for product in products:
                if product in context:
                    return product

        # Default to generic
        return "general"

    def generate_conflict_report(
        self,
        conflicts: Dict[str, List[ValidationIssue]]
    ) -> str:
        """
        Generate a human-readable conflict report.

        Args:
            conflicts: Dictionary of conflict type to issues

        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("CONFLICT DETECTION REPORT")
        lines.append("=" * 80)
        lines.append("")

        total_conflicts = sum(len(issues) for issues in conflicts.values())
        lines.append(f"Total Conflicts Found: {total_conflicts}")
        lines.append("")

        for conflict_type, issues in conflicts.items():
            if issues:
                lines.append(f"\n{conflict_type.upper()} CONFLICTS ({len(issues)}):")
                lines.append("-" * 80)

                for issue in issues[:10]:  # Show first 10
                    lines.append(f"\n[{issue.rule_id}] {issue.file_path.name}")
                    lines.append(f"  {issue.message}")
                    if issue.suggestion:
                        lines.append(f"  Suggestion: {issue.suggestion}")

                if len(issues) > 10:
                    lines.append(f"\n... and {len(issues) - 10} more {conflict_type} conflicts")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)
