# Claude Code Instructions - Symphony Core Document Management Workflow

## Project Overview
Symphony Core is an automated document processing system that ensures consistency, detects conflicts, and generates FAQs from business markdown documents. This is a Python-based CLI tool designed for internal business operations teams.

**Product Vision**: Continuous document intelligence for small teams
**Primary Goal**: Reduce document review time from 4 hours/week to 15 minutes/week

## Project Context

### What We're Building
- **Automated tagging system**: Tags documents with predefined categories (pricing, product-specs, policies, support, billing)
- **Conflict detection**: Identifies contradictory information across documents (pricing conflicts, date mismatches, policy contradictions)
- **FAQ generation**: Automatically creates and updates FAQs from document corpus
- **Change tracking**: Incremental processing to only check modified documents

### Key Technical Constraints
- Python 3.11+ required
- Anthropic Claude API for intelligent processing
- CLI-only (no GUI)
- File-based storage (no database)
- Budget: API costs must stay under $50/month
- Performance: Process 50 documents in under 10 minutes

## Development Standards

### Code Quality
- Follow PEP 8 style guidelines
- Write clean, readable code with meaningful variable names
- All functions MUST have docstrings explaining purpose, parameters, and return values
- Keep functions small and focused (single responsibility principle)
- Type hints required for all function signatures
- Comments only for "why", not "what"

### Project Structure
```
src/
├── core/           # Core processing logic
│   ├── change_detector.py    # File change detection
│   ├── tagger.py             # Document tagging (rule-based + LLM)
│   ├── conflict_detector.py  # Semantic conflict analysis
│   └── faq_generator.py      # FAQ generation
├── utils/
│   ├── frontmatter.py        # YAML frontmatter handling
│   ├── cache.py              # Document cache management
│   └── logger.py             # Logging utilities
├── cli.py          # CLI interface (Click framework)
└── config.py       # Configuration management

tests/              # Mirror src/ structure
config/             # Configuration files
scripts/            # Utility scripts
docs/               # Documentation including PRD
```

### Testing Requirements
- Write tests for ALL new features and bug fixes
- Maintain test coverage above 80%
- Run tests before committing: `pytest`
- Include both unit and integration tests
- Test edge cases (empty files, malformed YAML, API failures)

### Performance Considerations
- Use caching aggressively (file hashes, processed results)
- Implement incremental processing (only process changed docs)
- Batch API calls when possible
- Log processing time and API costs per run
- Target: <10 minutes for 50 documents, <5 minutes for incremental updates

### Error Handling
- ALL API calls must have retry logic (exponential backoff)
- Graceful degradation on API failures
- Validate all inputs before processing
- Error messages MUST be actionable (tell user what to do)
- Never expose sensitive content in logs or error messages

### Configuration Management
- NO hardcoded values - use config.yaml
- API keys ONLY in environment variables (.env)
- All paths configurable
- Validate configuration on startup
- Provide sensible defaults

## Domain-Specific Guidelines

### Document Processing
- Preserve original document content exactly (especially when adding frontmatter)
- Use file hashing (SHA-256) for change detection
- Cache ALL processed results to avoid reprocessing
- Support incremental updates by tag groups

### Tagging Strategy
- **Primary**: Rule-based tagging (keyword matching) for speed
- **Fallback**: LLM tagging when confidence < 70%
- **Tags**: pricing, product-specs, policies, support, billing (predefined only)
- Multi-tag support (documents can have multiple tags)
- Log confidence scores for quality monitoring

### Conflict Detection
- Group documents by tags before analysis
- Check for: pricing conflicts, date conflicts, specification contradictions, contact info mismatches
- Output severity levels: critical, medium, low
- Include source document references with line numbers if possible
- Only process affected tag groups on incremental runs

### FAQ Generation
- Target: 30-50 Q&A pairs from corpus
- Organize by topic/tag
- Include source document citations
- Incremental updates: only regenerate affected sections
- Tone: friendly, helpful, clear (2-4 sentences per answer)

## API Usage & Cost Management
- Track token usage per run
- Log estimated costs
- Implement batching to reduce API calls
- Cache LLM responses aggressively
- Monitor for cost spikes (alert if run exceeds expected cost)

## Version Control Practices
- Commit messages: Clear, descriptive (see PRD context in commit)
- Keep commits atomic and focused
- Branch naming:
  - `feature/feature-name` for new features
  - `fix/issue-description` for bug fixes
  - `docs/description` for documentation updates

## Before Committing Checklist
1. Run linter: `flake8 src/ tests/`
2. Run formatter: `black src/ tests/`
3. Run type checker: `mypy src/`
4. Run full test suite: `pytest`
5. Review your own changes
6. Update docs if behavior changed

## Important Reminders
- NEVER commit .env files or API keys
- ALWAYS prefer editing existing files over creating new ones (unless explicitly requested)
- Run tests after making changes
- Follow the principle of least surprise
- Consider backward compatibility
- Document configuration changes in README

## User Personas to Keep in Mind
- **Sarah (Documentation Manager)**: Needs quick conflict detection, uses CLI 3-4x/week
- **Mike (Content Contributor)**: Adds docs, needs auto-tagging, not deeply technical

## Success Criteria
- Detect 100% of pricing conflicts within 5 minutes of commit
- Zero customer-reported contradictions
- Process 50 documents in < 10 minutes
- API costs < $50/month
- 95%+ tagging accuracy
- Reduce manual review from 4 hours → 30 minutes per week
