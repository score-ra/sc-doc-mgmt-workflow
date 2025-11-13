"""
Tests for bulk frontmatter field management.
"""

import pytest
from pathlib import Path
from src.core.frontmatter_manager import (
    FrontmatterManager,
    FrontmatterOperationResult
)
from src.utils.frontmatter import (
    parse_frontmatter,
    add_frontmatter,
    has_frontmatter
)


# Module-level fixtures available to all test classes
@pytest.fixture
def sample_documents(tmp_path):
    """Create sample markdown documents for testing."""
    docs = []

    # Document with frontmatter
    doc1 = tmp_path / "doc1.md"
    doc1.write_text(
        "---\ntitle: Document 1\ntags: [test]\nstatus: draft\n---\n# Content 1",
        encoding='utf-8'
    )
    docs.append(doc1)

    # Document with frontmatter but missing some fields
    doc2 = tmp_path / "doc2.md"
    doc2.write_text(
        "---\ntitle: Document 2\nstatus: review\n---\n# Content 2",
        encoding='utf-8'
    )
    docs.append(doc2)

    # Document without frontmatter
    doc3 = tmp_path / "doc3.md"
    doc3.write_text("# Document 3\n\nNo frontmatter here.", encoding='utf-8')
    docs.append(doc3)

    return docs


class TestFrontmatterManager:
    """Tests for FrontmatterManager class."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance for testing."""
        return FrontmatterManager()


class TestAddFieldToDocuments:
    """Tests for add_field_to_documents method."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance."""
        return FrontmatterManager()

    def test_add_field_to_documents_with_frontmatter(self, manager, tmp_path):
        """Test adding field to documents that already have frontmatter."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\ntags: [test]\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='John Doe',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].field_name == 'author'
        assert results[0].new_value == 'John Doe'

        # Verify field was added
        metadata = parse_frontmatter(doc)
        assert metadata['author'] == 'John Doe'
        assert metadata['title'] == 'Test'  # Original field preserved

    def test_add_field_to_documents_without_frontmatter(self, manager, tmp_path):
        """Test adding field to documents without frontmatter."""
        doc = tmp_path / "test.md"
        doc.write_text("# Just content", encoding='utf-8')

        results = manager.add_field_to_documents(
            [doc],
            field_name='status',
            field_value='draft',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 1
        assert results[0].success is True

        # Verify frontmatter was created with field
        assert has_frontmatter(doc)
        metadata = parse_frontmatter(doc)
        assert metadata['status'] == 'draft'

    def test_add_field_skip_existing(self, manager, tmp_path):
        """Test skipping documents that already have the field."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\nauthor: Jane Doe\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='John Doe',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 1
        assert results[0].success is False
        assert "already exists" in results[0].message

        # Verify field was not changed
        metadata = parse_frontmatter(doc)
        assert metadata['author'] == 'Jane Doe'

    def test_add_field_overwrite_existing(self, manager, tmp_path):
        """Test overwriting existing field values."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\nauthor: Jane Doe\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='John Doe',
            overwrite=True,
            only_if_missing=False
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].old_value == 'Jane Doe'
        assert results[0].new_value == 'John Doe'

        # Verify field was updated
        metadata = parse_frontmatter(doc)
        assert metadata['author'] == 'John Doe'

    def test_add_field_to_multiple_documents(self, manager, sample_documents):
        """Test adding field to multiple documents."""
        results = manager.add_field_to_documents(
            sample_documents,
            field_name='version',
            field_value='1.0',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 3

        # Check that all documents now have the version field
        for doc in sample_documents:
            metadata = parse_frontmatter(doc)
            assert metadata['version'] == '1.0'

    def test_add_field_preserves_content(self, manager, tmp_path):
        """Test that adding field preserves document content."""
        doc = tmp_path / "test.md"
        original_content = "# Heading\n\nSome **bold** text\n\n- List"
        doc.write_text(
            f"---\ntitle: Test\n---\n{original_content}",
            encoding='utf-8'
        )

        manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='Test Author',
            overwrite=False,
            only_if_missing=True
        )

        # Read file and check content is preserved
        content = doc.read_text(encoding='utf-8')
        assert original_content in content

    def test_add_field_with_complex_value(self, manager, tmp_path):
        """Test adding field with list or dict value."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\n---\n# Content",
            encoding='utf-8'
        )

        # Add list field
        results = manager.add_field_to_documents(
            [doc],
            field_name='tags',
            field_value=['tag1', 'tag2', 'tag3'],
            overwrite=False,
            only_if_missing=True
        )

        assert results[0].success is True
        metadata = parse_frontmatter(doc)
        assert metadata['tags'] == ['tag1', 'tag2', 'tag3']

    def test_add_field_to_nonexistent_file(self, manager, tmp_path):
        """Test handling of non-existent files."""
        doc = tmp_path / "nonexistent.md"

        results = manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='Test',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 1
        assert results[0].success is False
        assert "not found" in results[0].message.lower()

    def test_add_field_to_non_markdown_file(self, manager, tmp_path):
        """Test handling of non-markdown files."""
        doc = tmp_path / "test.txt"
        doc.write_text("Not a markdown file", encoding='utf-8')

        results = manager.add_field_to_documents(
            [doc],
            field_name='author',
            field_value='Test',
            overwrite=False,
            only_if_missing=True
        )

        assert len(results) == 1
        assert results[0].success is False
        assert "not a markdown file" in results[0].message.lower()


class TestRemoveFieldFromDocuments:
    """Tests for remove_field_from_documents method."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance."""
        return FrontmatterManager()

    def test_remove_field_from_document(self, manager, tmp_path):
        """Test removing a field from a document."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\nauthor: John Doe\ntags: [test]\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.remove_field_from_documents(
            [doc],
            field_name='author',
            ignore_missing=True
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].old_value == 'John Doe'

        # Verify field was removed
        metadata = parse_frontmatter(doc)
        assert 'author' not in metadata
        assert metadata['title'] == 'Test'  # Other fields preserved

    def test_remove_field_from_multiple_documents(self, manager, sample_documents):
        """Test removing field from multiple documents."""
        # First add a field to all documents
        manager.add_field_to_documents(
            sample_documents,
            field_name='temp_field',
            field_value='temp',
            overwrite=False,
            only_if_missing=True
        )

        # Now remove it
        results = manager.remove_field_from_documents(
            sample_documents,
            field_name='temp_field',
            ignore_missing=True
        )

        assert len(results) == 3

        # Verify field was removed from all
        for doc in sample_documents:
            metadata = parse_frontmatter(doc)
            assert 'temp_field' not in metadata

    def test_remove_nonexistent_field_ignore(self, manager, tmp_path):
        """Test removing non-existent field with ignore_missing=True."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.remove_field_from_documents(
            [doc],
            field_name='nonexistent',
            ignore_missing=True
        )

        assert len(results) == 1
        assert results[0].success is True  # Success when ignoring

    def test_remove_nonexistent_field_no_ignore(self, manager, tmp_path):
        """Test removing non-existent field with ignore_missing=False."""
        doc = tmp_path / "test.md"
        doc.write_text(
            "---\ntitle: Test\n---\n# Content",
            encoding='utf-8'
        )

        results = manager.remove_field_from_documents(
            [doc],
            field_name='nonexistent',
            ignore_missing=False
        )

        assert len(results) == 1
        assert results[0].success is False

    def test_remove_field_preserves_content(self, manager, tmp_path):
        """Test that removing field preserves document content."""
        doc = tmp_path / "test.md"
        original_content = "# Heading\n\nContent here"
        doc.write_text(
            f"---\ntitle: Test\nauthor: John\n---\n{original_content}",
            encoding='utf-8'
        )

        manager.remove_field_from_documents(
            [doc],
            field_name='author',
            ignore_missing=True
        )

        content = doc.read_text(encoding='utf-8')
        assert original_content in content


class TestFindDocumentsWithField:
    """Tests for find_documents_with_field method."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance."""
        return FrontmatterManager()

    def test_find_documents_with_field(self, manager, sample_documents):
        """Test finding documents that have a specific field."""
        results = manager.find_documents_with_field(
            sample_documents,
            field_name='tags'
        )

        # Only doc1 has tags
        assert len(results) == 1
        assert results[0][0] == sample_documents[0]
        assert results[0][1] == ['test']

    def test_find_documents_with_field_and_value(self, manager, sample_documents):
        """Test finding documents with specific field value."""
        results = manager.find_documents_with_field(
            sample_documents,
            field_name='status',
            field_value='draft'
        )

        # Only doc1 has status: draft
        assert len(results) == 1
        assert results[0][0] == sample_documents[0]

    def test_find_documents_with_field_no_matches(self, manager, sample_documents):
        """Test finding documents with field that doesn't exist."""
        results = manager.find_documents_with_field(
            sample_documents,
            field_name='nonexistent_field'
        )

        assert len(results) == 0


class TestFindDocumentsWithoutField:
    """Tests for find_documents_without_field method."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance."""
        return FrontmatterManager()

    def test_find_documents_without_field(self, manager, sample_documents):
        """Test finding documents missing a specific field."""
        results = manager.find_documents_without_field(
            sample_documents,
            field_name='tags'
        )

        # doc2 and doc3 don't have tags
        assert len(results) == 2
        assert sample_documents[1] in results
        assert sample_documents[2] in results

    def test_find_documents_without_field_all_have_it(self, manager, sample_documents):
        """Test when all documents have the field."""
        results = manager.find_documents_without_field(
            sample_documents,
            field_name='title'
        )

        # doc3 doesn't have frontmatter at all, so it's missing title
        assert len(results) == 1
        assert sample_documents[2] in results


class TestGenerateSummaryReport:
    """Tests for generate_summary_report method."""

    @pytest.fixture
    def manager(self):
        """Create a FrontmatterManager instance."""
        return FrontmatterManager()

    def test_generate_summary_report(self, manager, tmp_path):
        """Test generating summary report from results."""
        # Create some test results
        results = [
            FrontmatterOperationResult(
                file_path=tmp_path / "doc1.md",
                success=True,
                message="Added field 'author'",
                field_name='author',
                new_value='John Doe'
            ),
            FrontmatterOperationResult(
                file_path=tmp_path / "doc2.md",
                success=True,
                message="Added field 'author'",
                field_name='author',
                new_value='John Doe'
            ),
            FrontmatterOperationResult(
                file_path=tmp_path / "doc3.md",
                success=False,
                message="File not found",
                field_name='author'
            )
        ]

        summary = manager.generate_summary_report(results)

        assert summary['total_documents'] == 3
        assert summary['successful'] == 2
        assert summary['failed'] == 1
        assert summary['success_rate'] == pytest.approx(66.67, rel=0.1)
        assert 'File not found' in summary['failure_reasons']

    def test_generate_summary_report_all_successful(self, manager, tmp_path):
        """Test summary report with all successful operations."""
        results = [
            FrontmatterOperationResult(
                file_path=tmp_path / "doc1.md",
                success=True,
                message="Success",
                field_name='test'
            ),
            FrontmatterOperationResult(
                file_path=tmp_path / "doc2.md",
                success=True,
                message="Success",
                field_name='test'
            )
        ]

        summary = manager.generate_summary_report(results)

        assert summary['total_documents'] == 2
        assert summary['successful'] == 2
        assert summary['failed'] == 0
        assert summary['success_rate'] == 100.0
        assert len(summary['failure_reasons']) == 0

    def test_generate_summary_report_empty(self, manager):
        """Test summary report with no results."""
        results = []

        summary = manager.generate_summary_report(results)

        assert summary['total_documents'] == 0
        assert summary['successful'] == 0
        assert summary['failed'] == 0
        assert summary['success_rate'] == 0


class TestFrontmatterOperationResult:
    """Tests for FrontmatterOperationResult dataclass."""

    def test_operation_result_creation(self, tmp_path):
        """Test creating an operation result."""
        result = FrontmatterOperationResult(
            file_path=tmp_path / "test.md",
            success=True,
            message="Field added",
            field_name='author',
            old_value=None,
            new_value='John Doe'
        )

        assert result.file_path == tmp_path / "test.md"
        assert result.success is True
        assert result.message == "Field added"
        assert result.field_name == 'author'
        assert result.old_value is None
        assert result.new_value == 'John Doe'

    def test_operation_result_minimal(self, tmp_path):
        """Test creating result with minimal fields."""
        result = FrontmatterOperationResult(
            file_path=tmp_path / "test.md",
            success=False,
            message="Error occurred"
        )

        assert result.file_path == tmp_path / "test.md"
        assert result.success is False
        assert result.message == "Error occurred"
        assert result.field_name is None
        assert result.old_value is None
        assert result.new_value is None
