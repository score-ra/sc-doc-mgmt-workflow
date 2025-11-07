---
title: Symphony Core Document Management Workflow - Architecture & Solution Design
version: 1.0
author: Engineering Team
date: 2025-10-09
status: draft
related_docs:
  - product-requirements-document.md
---

# Architecture & Solution Design
## Symphony Core: Document Management Workflow

---

## 1. Document Overview

**Purpose**: This document describes the technical architecture and implementation approach for Symphony Core, a document management workflow system.

**Audience**: Development team, technical stakeholders

**Related Documents**:
- Product Requirements Document (PRD): Defines WHAT we're building and WHY
- This document: Defines HOW we'll build it

---

## 2. Architecture Principles

### Design Philosophy
1. **Simplicity First**: Prefer straightforward solutions over complex ones
2. **Incremental Processing**: Only process what changed
3. **Fail Fast**: Validate early, report errors clearly
4. **Cost Conscious**: Optimize for API efficiency
5. **Maintainable**: Code should be readable and well-documented

### Technology Choices Rationale

**Python 3.11+**
- Team expertise
- Rich ecosystem for text processing
- Excellent LLM library support

**Anthropic Claude API (Sonnet 4)**
- Superior reasoning for conflict detection
- Excellent structured output support
- Strong context handling for long documents

**File-based Storage**
- No database overhead
- Version control friendly (Git)
- Simple backup/restore
- Sufficient for 100-document scale

**YAML for Configuration**
- Human-readable
- Easy to edit
- Standard Python library support

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Symphony Core System                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │         CLI Entry Point             │
        │          (main.py)                  │
        └─────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │      Orchestrator / Controller      │
        │    (DocumentProcessor class)        │
        └─────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐        ┌─────────┐
    │ Tagging │         │Conflict │        │   FAQ   │
    │ Engine  │         │Detector │        │Generator│
    └─────────┘         └─────────┘        └─────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Claude API      │
                    │  Client Wrapper  │
                    └──────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐        ┌─────────┐
    │  Cache  │         │  Files  │        │  Config │
    │ Manager │         │ Handler │        │ Manager │
    └─────────┘         └─────────┘        └─────────┘
```

### 3.2 Data Flow

```
User runs CLI command
       │
       ▼
Load configuration & cache
       │
       ▼
Scan document directory
       │
       ▼
Identify changed files (hash comparison)
       │
       ▼
┌──────────────────────────────────┐
│   FOR EACH CHANGED FILE          │
│   1. Read content                │
│   2. Add/update YAML frontmatter │
│   3. Apply rule-based tagging    │
│   4. If confidence < 70%:        │
│      - Call Claude API for tags  │
│   5. Write file back             │
│   6. Update cache                │
└──────────────────────────────────┘
       │
       ▼
Group documents by affected tags
       │
       ▼
┌──────────────────────────────────┐
│   FOR EACH AFFECTED TAG GROUP    │
│   1. Gather all docs with tag    │
│   2. Batch content preparation   │
│   3. Call Claude API for         │
│      conflict detection          │
│   4. Parse and format results    │
│   5. Generate report section     │
└──────────────────────────────────┘
       │
       ▼
Combine conflict reports
       │
       ▼
Generate/update FAQs
       │
       ▼
┌──────────────────────────────────┐
│   FOR EACH AFFECTED TAG          │
│   1. Gather relevant docs        │
│   2. Call Claude API for         │
│      FAQ generation              │
│   3. Update FAQ section          │
│   4. Preserve unchanged sections │
└──────────────────────────────────┘
       │
       ▼
Write output files
       │
       ▼
Update cache & log metrics
       │
       ▼
Display summary to user
```

---

## 4. Component Design

### 4.1 DocumentProcessor (Orchestrator)

**Responsibility**: Main controller that orchestrates the entire workflow

**Key Methods**:
```python
class DocumentProcessor:
    def __init__(self, config: Config):
        """Initialize with configuration"""
        
    def process_incrementally(self) -> ProcessingResult:
        """Main entry point for incremental processing"""
        
    def process_full(self, force: bool = False) -> ProcessingResult:
        """Full reprocessing of all documents"""
        
    def get_changed_files(self) -> List[Path]:
        """Identify files that changed since last run"""
        
    def load_cache(self) -> Dict:
        """Load processing cache from disk"""
        
    def update_cache(self, files: List[Path]) -> None:
        """Update cache with processed files"""
```

**State Management**:
```python
{
    "filepath": {
        "hash": "md5_hash_string",
        "last_processed": "2025-10-09T10:30:00Z",
        "tags": ["pricing", "policies"],
        "tag_confidence": 0.95
    }
}
```

### 4.2 TaggingEngine

**Responsibility**: Assign tags to documents using hybrid approach

**Key Methods**:
```python
class TaggingEngine:
    def __init__(self, valid_tags: List[str], claude_client: ClaudeClient):
        """Initialize with tag list and API client"""
        
    def tag_document(self, content: str, filepath: Path) -> TagResult:
        """Main tagging method - tries rules first, then LLM"""
        
    def rule_based_tag(self, content: str) -> Tuple[List[str], float]:
        """Fast keyword-based tagging with confidence score"""
        
    def llm_based_tag(self, content: str) -> List[str]:
        """LLM fallback for ambiguous documents"""
        
    def add_frontmatter(self, filepath: Path, tags: List[str]) -> None:
        """Add or update YAML frontmatter with tags"""
```

**Tagging Logic**:
```python
TAG_PATTERNS = {
    "pricing": {
        "keywords": ["price", "cost", "fee", "payment", "$"],
        "patterns": [r'\$\d+(?:\.\d{2})?', r'(?i)pricing', r'(?i)cost\s+of'],
        "weight": 1.0
    },
    "product-specs": {
        "keywords": ["specification", "feature", "technical", "requirement"],
        "patterns": [r'(?i)spec(?:ification)?', r'(?i)feature', r'(?i)technical'],
        "weight": 1.0
    },
    # ... other tags
}

def calculate_confidence(matches: Dict[str, int]) -> float:
    """
    Confidence = weighted_matches / (expected_matches_threshold)
    Returns 0.0 to 1.0
    """
```

**LLM Prompt Template**:
```python
TAGGING_PROMPT = """Analyze this document and select relevant tags from the list below.

Valid tags: {valid_tags}

Document title: {filename}
Document content:
{content}

Rules:
- Select ALL applicable tags
- Use only tags from the valid list
- Consider the document's primary purpose and content

Respond with ONLY a JSON array of tags, like: ["tag1", "tag2"]
"""
```

### 4.3 ConflictDetector

**Responsibility**: Identify contradictions across documents

**Key Methods**:
```python
class ConflictDetector:
    def __init__(self, claude_client: ClaudeClient):
        """Initialize with API client"""
        
    def detect_conflicts(self, documents: List[Document], tag: str) -> ConflictReport:
        """Detect conflicts within a tag group"""
        
    def batch_documents(self, documents: List[Document], max_tokens: int) -> List[List[Document]]:
        """Group documents into batches that fit context window"""
        
    def parse_conflict_response(self, response: str) -> List[Conflict]:
        """Parse LLM response into structured conflicts"""
```

**Conflict Detection Prompt**:
```python
CONFLICT_DETECTION_PROMPT = """Review these {tag}-related documents for contradictions and conflicts.

Focus on detecting conflicts in:
- Pricing and costs
- Dates and timelines
- Product specifications
- Policy statements
- Contact information

Documents:
{document_content}

For each conflict found, provide:
1. Conflict type (pricing, date, specification, policy, contact)
2. Severity (critical, medium, low)
3. Description of the contradiction
4. Source documents involved (use document titles/names)
5. Specific quotes or references from each document
6. Recommendation for resolution

Respond in this JSON format:
[
  {{
    "type": "pricing",
    "severity": "critical",
    "description": "Product X has conflicting prices",
    "sources": [
      {{"document": "pricing-2024.md", "quote": "Product X costs $100/month"}},
      {{"document": "new-pricing.md", "quote": "Product X is $150/month"}}
    ],
    "recommendation": "Clarify which is current pricing"
  }}
]

If no conflicts are found, return an empty array: []
"""
```

**Conflict Report Structure**:
```python
@dataclass
class Conflict:
    type: str  # pricing, date, specification, policy, contact
    severity: str  # critical, medium, low
    description: str
    sources: List[ConflictSource]
    recommendation: str
    detected_at: datetime

@dataclass
class ConflictSource:
    document: str
    quote: str
    line_number: Optional[int] = None

@dataclass
class ConflictReport:
    tag: str
    conflicts: List[Conflict]
    documents_analyzed: int
    generated_at: datetime
```

### 4.4 FAQGenerator

**Responsibility**: Generate and maintain FAQ documentation

**Key Methods**:
```python
class FAQGenerator:
    def __init__(self, claude_client: ClaudeClient, criteria: FAQCriteria):
        """Initialize with API client and FAQ criteria"""
        
    def generate_faqs(self, documents: List[Document], tag: str) -> FAQSection:
        """Generate FAQ section for a tag group"""
        
    def update_faqs(self, existing_faq: FAQ, affected_tags: List[str]) -> FAQ:
        """Update only affected sections of existing FAQ"""
        
    def merge_sections(self, old_section: FAQSection, new_section: FAQSection) -> FAQSection:
        """Intelligently merge FAQ sections"""
```

**FAQ Generation Prompt**:
```python
FAQ_GENERATION_PROMPT = """Generate a comprehensive FAQ section based on these {tag} documents.

Documents:
{document_content}

FAQ Criteria:
- Target audience: {target_audience}
- Tone: {tone}
- Answer length: {answer_length}
- Include specific examples: {include_examples}
- Avoid: {avoid_list}

Generate 8-12 frequently asked questions with clear, helpful answers. Each answer should:
1. Directly address the question
2. Be 2-4 sentences long
3. Include specific examples where helpful
4. Reference source documents in parentheses

Respond in this JSON format:
{{
  "tag": "{tag}",
  "faqs": [
    {{
      "question": "What is the pricing for Product X?",
      "answer": "Product X is priced at $100/month for the basic plan. This includes features A, B, and C. (Source: pricing-2024.md)",
      "source_documents": ["pricing-2024.md"],
      "keywords": ["pricing", "product x", "cost"]
    }}
  ]
}}
"""
```

### 4.5 ClaudeClient (API Wrapper)

**Responsibility**: Centralized API interaction with retry logic and cost tracking

**Key Methods**:
```python
class ClaudeClient:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """Initialize Anthropic client"""
        
    def complete(self, prompt: str, max_tokens: int = 4000) -> CompletionResult:
        """Call Claude API with retry logic"""
        
    def complete_with_retry(self, prompt: str, max_retries: int = 3) -> CompletionResult:
        """Wrapper with exponential backoff"""
        
    def track_usage(self, input_tokens: int, output_tokens: int) -> None:
        """Track token usage for cost calculation"""
        
    def get_usage_stats(self) -> UsageStats:
        """Get current session usage statistics"""
```

**Cost Tracking**:
```python
@dataclass
class UsageStats:
    total_requests: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float  # Based on current pricing
    
    def calculate_cost(self) -> float:
        """
        Claude Sonnet 4 pricing (as of Oct 2025):
        Input: $3 per million tokens
        Output: $15 per million tokens
        """
        input_cost = (self.input_tokens / 1_000_000) * 3.00
        output_cost = (self.output_tokens / 1_000_000) * 15.00
        return input_cost + output_cost
```

**Retry Logic**:
```python
def complete_with_retry(self, prompt: str, max_retries: int = 3) -> CompletionResult:
    """
    Retry strategy:
    - Retry on: Rate limit errors, temporary server errors
    - Don't retry on: Invalid API key, malformed requests
    - Backoff: Exponential (1s, 2s, 4s, 8s)
    """
    for attempt in range(max_retries):
        try:
            return self.complete(prompt)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
        except (InvalidRequestError, AuthenticationError):
            # Don't retry these
            raise
```

### 4.6 CacheManager

**Responsibility**: Manage persistent cache for change detection

**Key Methods**:
```python
class CacheManager:
    def __init__(self, cache_file: Path):
        """Initialize with cache file path"""
        
    def load(self) -> Dict:
        """Load cache from disk"""
        
    def save(self, cache: Dict) -> None:
        """Atomically write cache to disk"""
        
    def get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file"""
        
    def is_changed(self, filepath: Path) -> bool:
        """Check if file changed since last processing"""
        
    def update_entry(self, filepath: Path, metadata: Dict) -> None:
        """Update cache entry for a file"""
```

**Cache Structure**:
```json
{
  "version": "1.0",
  "last_updated": "2025-10-09T14:30:00Z",
  "files": {
    "docs/pricing-2024.md": {
      "hash": "5d41402abc4b2a76b9719d911017c592",
      "last_processed": "2025-10-09T14:30:00Z",
      "tags": ["pricing"],
      "tag_confidence": 0.95,
      "file_size": 2048,
      "last_modified": "2025-10-09T10:00:00Z"
    }
  }
}
```

### 4.7 ConfigManager

**Responsibility**: Load and validate configuration

**Configuration File Structure** (`config.yaml`):
```yaml
# Symphony Core Configuration

# Document Processing
documents:
  input_directory: "./docs"
  file_pattern: "**/*.md"
  exclude_patterns:
    - "**/node_modules/**"
    - "**/.git/**"

# Tagging
tagging:
  valid_tags:
    - pricing
    - product-specs
    - policies
    - support
    - billing
  confidence_threshold: 0.7
  rule_based_first: true

# Conflict Detection
conflict_detection:
  batch_size: 10  # documents per API call
  severity_levels:
    - critical
    - medium
    - low

# FAQ Generation
faq:
  criteria:
    target_audience: "end customers"
    tone: "friendly, helpful, clear"
    answer_length: "2-4 sentences"
    include_examples: true
  questions_per_tag: 10

# API Configuration
api:
  provider: "anthropic"
  model: "claude-sonnet-4-20250514"
  max_tokens: 4000
  timeout: 30  # seconds

# Output
output:
  directory: "./output"
  conflict_report: "conflicts.md"
  faq_file: "faq.md"
  log_file: "symphony-core.log"

# Cache
cache:
  file: ".cache/processing_cache.json"
  enabled: true

# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  track_costs: true
```

---

## 5. Data Models

### 5.1 Core Models

```python
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

@dataclass
class Document:
    """Represents a markdown document"""
    filepath: Path
    content: str
    metadata: Dict  # YAML frontmatter
    tags: List[str]
    last_modified: datetime
    hash: str

@dataclass
class TagResult:
    """Result of tagging operation"""
    tags: List[str]
    confidence: float
    method: str  # "rule-based" or "llm-based"
    processing_time: float

@dataclass
class ProcessingResult:
    """Overall processing result"""
    files_processed: int
    files_changed: int
    conflicts_detected: int
    faqs_generated: int
    processing_time: float
    api_cost: float
    errors: List[str]

@dataclass
class FAQSection:
    """FAQ section for a specific tag"""
    tag: str
    faqs: List[FAQItem]
    generated_at: datetime
    source_documents: List[str]

@dataclass
class FAQItem:
    """Single FAQ entry"""
    question: str
    answer: str
    source_documents: List[str]
    keywords: List[str]
```

---

## 6. File Structure

```
symphony-core/
├── README.md                    # Project overview and setup
├── requirements.txt             # Python dependencies
├── config.yaml                  # Configuration file
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
│
├── src/                         # Source code
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── processor.py             # DocumentProcessor
│   ├── tagging.py               # TaggingEngine
│   ├── conflicts.py             # ConflictDetector
│   ├── faq_generator.py         # FAQGenerator
│   ├── claude_client.py         # ClaudeClient wrapper
│   ├── cache_manager.py         # CacheManager
│   ├── config_manager.py        # ConfigManager
│   ├── models.py                # Data models
│   └── utils.py                 # Utility functions
│
├── docs/                        # Input documents (user content)
│   └── *.md
│
├── output/                      # Generated outputs
│   ├── conflicts.md
│   ├── faq.md
│   └── symphony-core.log
│
├── .cache/                      # Cache directory
│   └── processing_cache.json
│
└── tests/                       # Test suite
    ├── __init__.py
    ├── test_processor.py
    ├── test_tagging.py
    ├── test_conflicts.py
    ├── test_faq.py
    └── fixtures/                # Test data
        └── sample_docs/
```

---

## 7. API Integration Details

### 7.1 Anthropic Claude API Usage

**Authentication**:
```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```

**Basic Request Pattern**:
```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4000,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

response_text = message.content[0].text
```

**Token Management**:
- Input limit: ~200K tokens (Claude Sonnet 4)
- Output limit: 8K tokens max per request
- Typical document: ~500-1000 tokens
- Batch up to 10-20 documents per conflict detection call

**Cost Optimization Strategies**:
1. **Batch Processing**: Combine multiple documents in single API call
2. **Incremental Processing**: Only process changed content
3. **Rule-based First**: Use LLM only when necessary
4. **Caching**: Store results, don't reprocess
5. **Token Estimation**: Pre-calculate token count before API call

---

## 8. Error Handling Strategy

### 8.1 Error Categories

**Category 1: User Errors** (Recoverable)
- Missing configuration file
- Invalid document format
- Missing API key
- Invalid tag in configuration

**Action**: Clear error message, suggest fix, exit gracefully

**Category 2: API Errors** (Potentially Recoverable)
- Rate limit exceeded
- Temporary server error
- Timeout

**Action**: Retry with exponential backoff (max 3 attempts)

**Category 3: System Errors** (Non-recoverable)
- File permission issues
- Disk full
- Corrupted cache

**Action**: Log error, attempt cleanup, exit with error code

### 8.2 Error Handling Implementation

```python
class SymphonyCoreError(Exception):
    """Base exception for Symphony Core"""
    pass

class ConfigurationError(SymphonyCoreError):
    """Configuration-related errors"""
    pass

class APIError(SymphonyCoreError):
    """API-related errors"""
    pass

class ProcessingError(SymphonyCoreError):
    """Document processing errors"""
    pass

# Usage example
try:
    processor.process_incrementally()
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
    print(f"❌ Configuration error: {e}")
    print("💡 Check your config.yaml file")
    sys.exit(1)
except APIError as e:
    logger.error(f"API error: {e}")
    print(f"❌ API error: {e}")
    print("💡 Check your ANTHROPIC_API_KEY environment variable")
    sys.exit(2)
except ProcessingError as e:
    logger.error(f"Processing error: {e}")
    print(f"❌ Processing error: {e}")
    sys.exit(3)
```

---

## 9. Performance Considerations

### 9.1 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Full processing (50 docs) | < 10 minutes | End-to-end |
| Incremental processing | < 5 minutes | End-to-end |
| Change detection | < 1 second | File scanning |
| Rule-based tagging | < 30 seconds | 50 documents |
| Cache operations | < 100ms | Load/save |

### 9.2 Optimization Techniques

**File Operations**:
- Use pathlib for efficient file handling
- Stream large files instead of loading entirely
- Parallel file hashing using multiprocessing

**API Efficiency**:
- Batch documents in single API calls
- Reuse connections (keep-alive)
- Implement request pooling for parallel calls
- Pre-calculate token counts to optimize batch sizes

**Caching Strategy**:
- Use MD5 for fast file change detection
- Lazy load cache (only when needed)
- Atomic writes to prevent corruption
- Compress cache if it grows large

**Memory Management**:
- Process documents in streams for large files
- Clear processed content from memory
- Use generators for large document lists

---

## 10. Security Considerations

### 10.1 API Key Management

**Storage**:
- NEVER commit API keys to version control
- Use environment variables
- Consider using `.env` files (gitignored)
- Validate key format before use

**Example `.env` file**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

### 10.2 Data Privacy

**Document Content**:
- Documents are sent to Anthropic API (review their privacy policy)
- No document content stored in logs by default
- Option to enable verbose logging (development only)

**Cache Security**:
- Cache contains file hashes and metadata only
- No sensitive document content in cache
- Cache file permissions: 600 (owner read/write only)

### 10.3 Input Validation

**Configuration**:
- Validate all config values on load
- Sanitize file paths
- Validate tag names (alphanumeric, dash, underscore only)

**Documents**:
- Validate markdown syntax
- Check file size limits
- Verify YAML frontmatter format

---

## 11. Testing Strategy

### 11.1 Test Pyramid

```
        /\
       /  \
      / E2E\         5% - End-to-end tests
     /------\
    /  Integ \       15% - Integration tests
   /----------\
  /   Unit     \     80% - Unit tests
 /--------------\
```

### 11.2 Test Categories

**Unit Tests** (80% coverage target):
- TaggingEngine rule-based logic
- CacheManager file operations
- ConfigManager validation
- Utility functions

**Integration Tests** (15% coverage target):
- DocumentProcessor workflow
- API client with mock responses
- File I/O operations
- Cache persistence

**End-to-End Tests** (5% coverage target):
- Full workflow with sample documents
- CLI command execution
- Output validation

### 11.3 Test Data

**Fixtures**:
```
tests/fixtures/
├── sample_docs/
│   ├── pricing-doc.md
│   ├── policy-doc.md
│   └── specs-doc.md
├── config/
│   ├── valid-config.yaml
│   └── invalid-config.yaml
└── cache/
    └── sample-cache.json
```

---

## 12. Deployment & Operations

### 12.1 Installation

```bash
# Clone repository
git clone <repository-url>
cd symphony-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env

# Copy configuration template
cp config.yaml.example config.yaml

# Edit configuration as needed
nano config.yaml

# Run initial setup
python src/main.py --setup
```

### 12.2 Operational Commands

```bash
# Standard incremental processing
python src/main.py

# Force full reprocessing
python src/main.py --force

# Tag documents only
python src/main.py --tag-only

# Check conflicts only (skip tagging and FAQ)
python src/main.py --check-conflicts

# Generate FAQs only
python src/main.py --faq-only

# Dry run (show what would be processed)
python src/main.py --dry-run

# Verbose output
python src/main.py --verbose
```

### 12.3 Monitoring

**Metrics to Track**:
- Processing time per run
- API costs per run
- Number of conflicts detected
- Tagging accuracy (spot check)
- Cache hit rate

**Log Analysis**:
```bash
# View recent processing runs
tail -f output/symphony-core.log

# Check for errors
grep ERROR output/symphony-core.log

# Calculate total API costs
grep "API cost" output/symphony-core.log | awk '{sum+=$NF} END {print sum}'
```

---

## 13. Future Enhancements (Post-v1)

### Phase 2 Possibilities
- Web UI for conflict review
- Slack/email notifications
- Real-time processing (file watcher)
- Multi-language support
- Integration with documentation platforms
- Automated conflict resolution suggestions
- Custom tag taxonomies per project
- Version history tracking
- Bulk document import tools

### Scalability Considerations
- If document count > 500: Consider database
- If team size > 10: Add collaboration features
- If API costs > $200/month: Evaluate local LLM options

---

## 14. Decision Log

### AD-001: File-based Storage vs Database
**Date**: 2025-10-09  
**Decision**: Use file-based storage  
**Rationale**: 
- Document count < 100 in v1
- Simplicity and maintainability
- Git-friendly
- Zero infrastructure overhead

**Consequences**:
- (+) Simple backup/restore
- (+) No database maintenance
- (-) Limited query capabilities
- (-) May need migration if scale grows

### AD-002: Hybrid Tagging Approach
**Date**: 2025-10-09  
**Decision**: Rule-based primary, LLM fallback  
**Rationale**:
- Cost optimization
- Speed for frequent runs
- Accuracy for edge cases

**Consequences**:
- (+) 10x faster than pure LLM
- (+) 5x cheaper
- (-) Need to maintain rules
- (-) May miss nuanced tags

### AD-003: Batch Conflict Detection
**Date**: 2025-10-09  
**Decision**: Group documents by tag before conflict checking  
**Rationale**:
- Reduces API calls
- Focuses analysis on relevant subsets
- Enables incremental processing

**Consequences**:
- (+) Faster processing
- (+) Lower costs
- (-) May miss cross-tag conflicts
- (-) Requires careful batch sizing

---

## 15. Appendix

### A. Dependencies

```text
# requirements.txt
anthropic>=0.34.0
python-frontmatter>=1.1.0
pyyaml>=6.0.1
python-dotenv>=1.0.0
```

### B. Glossary

**Term** | **Definition**
---------|---------------
Document | A markdown (.md) file in the input directory
Tag | A category label applied to documents (e.g., "pricing")
Frontmatter | YAML metadata at the top of a markdown file
Conflict | A contradiction between two or more documents
FAQ | Frequently Asked Questions
LLM | Large Language Model (Claude)
Cache | Persistent storage of processing metadata
Batch | Group of documents processed together in one API call

### C. References

- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [Python Frontmatter Library](https://github.com/eyeseast/python-frontmatter)
- [Markdown Specification](https://spec.commonmark.org/)
- [YAML Specification](https://yaml.org/spec/)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-09 | Engineering Team | Initial architecture document |

---

**Document Status**: ☑ Draft  ☐ Review  ☐ Approved  ☐ Archived
