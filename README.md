# Symphony Core: Document Management Workflow

**Continuous document intelligence for small teams**

Automated document processing system that ensures consistency, detects conflicts, and generates FAQs from business markdown documents.

## Overview

Symphony Core helps internal business operations teams manage 30-50+ markdown documents covering pricing, policies, product specs, and support information. It automatically tags documents, detects contradictory information, and generates customer-facing FAQs.

**Key Benefits:**
- Reduce document review time from 4 hours/week to 15 minutes/week
- Detect 100% of pricing/policy conflicts within 5 minutes
- Auto-generate and update FAQs from your document corpus
- Incremental processing for speed (only check what changed)

## Features

- **Automated Tagging**: Rule-based + LLM tagging for documents (pricing, product-specs, policies, support, billing)
- **Conflict Detection**: Identifies contradictory pricing, dates, specifications, and policies across documents
- **FAQ Generation**: Automatically creates 30-50 Q&A pairs organized by topic with source citations
- **Change Tracking**: Incremental processing using file hashing to avoid unnecessary reprocessing
- **Cost Optimized**: API costs stay under $50/month with intelligent caching and batching

## Installation

### Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- Git (for version control)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sc-doc-mgmt-workflow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Configure settings (optional):
```bash
# Edit config/config.yaml to customize paths, tags, etc.
```

5. Run tests to verify setup:
```bash
pytest
```

## Usage

### Basic Usage

Process all documents in the default directory:
```bash
python main.py
```

### Command Options

```bash
# Tag documents only (no conflict detection)
python main.py --tag-only

# Check conflicts only (assumes documents already tagged)
python main.py --check-conflicts

# Force reprocess all documents (ignore cache)
python main.py --force

# Specify custom document directory
python main.py --docs-dir ./my_docs

# Generate FAQs only
python main.py --faq-only
```

### Typical Workflow

1. **Initial Setup**: Run full processing on your document corpus
   ```bash
   python main.py
   ```

2. **Daily/Weekly Reviews**: Run incremental processing after document changes
   ```bash
   python main.py
   ```

3. **Review Conflicts**: Check the generated conflict report
   ```bash
   cat output/conflicts.md
   ```

4. **Publish FAQs**: Use the generated FAQ file for customer portal
   ```bash
   cat output/faq.md
   ```

## Configuration

Edit `config/config.yaml` to customize:

```yaml
# Document paths
docs_directory: "./sample_docs"
output_directory: "./output"
cache_file: "./.cache/document_cache.json"

# Tagging settings
predefined_tags:
  - pricing
  - product-specs
  - policies
  - support
  - billing

tagging_confidence_threshold: 0.70

# Conflict detection
conflict_severity_levels:
  - critical
  - medium
  - low

# FAQ settings
faq_min_questions: 30
faq_max_questions: 50
```

## Project Structure

```
sc-doc-mgmt-workflow/
├── src/                    # Source code
│   ├── core/              # Core processing modules
│   │   ├── change_detector.py
│   │   ├── tagger.py
│   │   ├── conflict_detector.py
│   │   └── faq_generator.py
│   ├── utils/             # Utility modules
│   │   ├── frontmatter.py
│   │   ├── cache.py
│   │   └── logger.py
│   ├── cli.py             # CLI interface
│   └── config.py          # Configuration management
├── tests/                 # Test files (mirrors src/)
├── docs/                  # Documentation
│   └── product-requirements-document.md
├── config/                # Configuration files
│   └── config.yaml
├── scripts/               # Utility scripts
├── output/                # Generated reports (gitignored)
├── .cache/                # Processing cache (gitignored)
├── logs/                  # Log files (gitignored)
├── sample_docs/           # Example documents
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .gitignore
└── README.md
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/core/test_tagger.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD approach)
3. Implement feature following existing patterns
4. Run full test suite and linters
5. Update documentation
6. Create pull request

## Performance

- **Full Processing**: < 10 minutes for 50 documents
- **Incremental Updates**: < 5 minutes for typical changes
- **API Costs**: < $50/month for regular usage
- **Cache Hit Rate**: ~80% on incremental runs

## Troubleshooting

### API Key Issues
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Test API connection
python -c "from anthropic import Anthropic; client = Anthropic(); print('API key valid')"
```

### Permission Errors
Ensure you have write permissions for output and cache directories:
```bash
mkdir -p output .cache logs
chmod 755 output .cache logs
```

### High API Costs
- Check cache is working: `ls -lh .cache/document_cache.json`
- Review processing logs for repeated API calls
- Use `--tag-only` or `--check-conflicts` for targeted runs

## Success Metrics

Based on the PRD, we track:

- **Conflict Detection**: 100% of pricing conflicts detected within 5 minutes
- **Time Savings**: Review time reduced from 4 hours/week → 30 minutes/week
- **Accuracy**: 95%+ tagging accuracy
- **Performance**: Process 50 documents in < 10 minutes
- **Cost**: Monthly API costs < $50

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following code quality standards
4. Run tests and linters
5. Submit a pull request

See `CLAUDE.md` for detailed development guidelines.

## Support & Documentation

- **PRD**: See `docs/product-requirements-document.md` for full requirements
- **Issues**: Report bugs or request features via GitHub issues
- **Configuration**: See `.env.example` and `config/config.yaml` for all options

## License

[Specify license here]

---

**Version**: 1.0.0
**Status**: Development
**Last Updated**: 2025-10-09
