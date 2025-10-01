import pytest
import tempfile
import os
from pathlib import Path
from panparsex import parse
from panparsex.types import UnifiedDocument


class TestIntegration:
    """Integration tests for the panparsex library."""
    
    def test_parse_various_file_types(self, tmp_path):
        """Test parsing various file types in sequence."""
        # Create test files
        files = {
            "test.txt": "Hello, world!",
            "test.json": '{"message": "Hello, JSON!"}',
            "test.yaml": "message: Hello, YAML!",
            "test.xml": '<?xml version="1.0"?><root><message>Hello, XML!</message></root>',
            "test.html": '<html><head><title>Test</title></head><body><h1>Hello, HTML!</h1></body></html>',
            "test.csv": "name,message\nWorld,Hello CSV",
            "test.md": "# Hello, Markdown!\n\nThis is a test."
        }
        
        results = {}
        for filename, content in files.items():
            file_path = tmp_path / filename
            file_path.write_text(content)
            
            doc = parse(str(file_path))
            results[filename] = doc
            
            # Basic assertions
            assert isinstance(doc, UnifiedDocument)
            assert len(doc.sections) > 0
            assert doc.meta.source == str(file_path)
        
        # Verify specific content
        assert "Hello, world!" in results["test.txt"].sections[0].chunks[0].text
        assert "Hello, JSON!" in results["test.json"].sections[0].chunks[0].text
        assert "Hello, YAML!" in results["test.yaml"].sections[0].chunks[0].text
        assert "Hello, XML!" in results["test.xml"].sections[0].chunks[0].text
        assert "Hello, HTML!" in results["test.html"].sections[0].chunks[0].text
        assert "Hello CSV" in results["test.csv"].sections[1].chunks[0].text  # Data section
        assert "Hello, Markdown!" in results["test.md"].sections[0].heading

    def test_parse_directory(self, tmp_path):
        """Test parsing a directory of files."""
        # Create multiple files
        files = {
            "doc1.txt": "Document 1 content",
            "doc2.json": '{"title": "Document 2"}',
            "doc3.yaml": "title: Document 3"
        }
        
        for filename, content in files.items():
            file_path = tmp_path / filename
            file_path.write_text(content)
        
        # Parse each file
        results = []
        for file_path in tmp_path.glob("*"):
            if file_path.is_file():
                doc = parse(str(file_path))
                results.append(doc)
        
        assert len(results) == 3
        for doc in results:
            assert isinstance(doc, UnifiedDocument)

    def test_metadata_extraction(self, tmp_path):
        """Test metadata extraction from various file types."""
        # HTML with metadata
        html_file = tmp_path / "test.html"
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
    <meta name="description" content="A test document">
    <meta name="author" content="Test Author">
</head>
<body>
    <h1>Content</h1>
    <p>Some content here.</p>
</body>
</html>"""
        html_file.write_text(html_content)
        
        doc = parse(str(html_file))
        
        assert doc.meta.title == "Test Document"
        assert "meta_tags" in doc.meta.extra
        assert doc.meta.extra["meta_tags"]["description"] == "A test document"
        assert doc.meta.extra["meta_tags"]["author"] == "Test Author"

    def test_structured_content_extraction(self, tmp_path):
        """Test extraction of structured content."""
        # HTML with multiple sections
        html_file = tmp_path / "structured.html"
        html_content = """<!DOCTYPE html>
<html>
<head><title>Structured Document</title></head>
<body>
    <h1>Main Title</h1>
    <p>Introduction paragraph.</p>
    
    <h2>Section 1</h2>
    <p>Content for section 1.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    
    <h2>Section 2</h2>
    <p>Content for section 2.</p>
    <blockquote>This is a quote.</blockquote>
</body>
</html>"""
        html_file.write_text(html_content)
        
        doc = parse(str(html_file))
        
        assert len(doc.sections) >= 3  # Main title + 2 sections
        assert "Main Title" in doc.sections[0].heading
        # Check that the heading is in the first chunk
        assert "Main Title" in doc.sections[0].chunks[0].text
        # Check that paragraph content is in subsequent chunks
        paragraph_found = False
        for chunk in doc.sections[0].chunks:
            if "Introduction paragraph" in chunk.text:
                paragraph_found = True
                break
        assert paragraph_found

    def test_error_handling(self, tmp_path):
        """Test error handling for various scenarios."""
        # Invalid JSON
        json_file = tmp_path / "invalid.json"
        json_file.write_text('{"invalid": json}')
        
        doc = parse(str(json_file))
        assert isinstance(doc, UnifiedDocument)
        assert "[panparsex:json]" in doc.sections[0].chunks[0].text
        
        # Empty file
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        doc = parse(str(empty_file))
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1

    def test_content_type_detection(self, tmp_path):
        """Test automatic content type detection."""
        # Test with explicit content type
        text_file = tmp_path / "test.txt"
        text_file.write_text("Hello, world!")
        
        doc = parse(str(text_file), content_type="text/plain")
        assert doc.meta.content_type == "text/plain"
        
        # Test with URL
        doc = parse("https://example.com", url="https://example.com")
        assert doc.meta.content_type == "text/html"
        assert doc.meta.url == "https://example.com"

    def test_recursive_parsing(self, tmp_path):
        """Test recursive parsing capabilities."""
        # Create nested directory structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        files = {
            "root.txt": "Root file content",
            "subdir/nested.txt": "Nested file content"
        }
        
        for filepath, content in files.items():
            file_path = tmp_path / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        # Parse root file
        root_doc = parse(str(tmp_path / "root.txt"))
        assert "Root file content" in root_doc.sections[0].chunks[0].text
        
        # Parse nested file
        nested_doc = parse(str(tmp_path / "subdir" / "nested.txt"))
        assert "Nested file content" in nested_doc.sections[0].chunks[0].text

    def test_large_file_handling(self, tmp_path):
        """Test handling of larger files."""
        # Create a larger text file
        large_file = tmp_path / "large.txt"
        content = "Line " + "\n".join([f"Line {i}" for i in range(1000)])
        large_file.write_text(content)
        
        doc = parse(str(large_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert "Line 0" in doc.sections[0].chunks[0].text
        assert "Line 999" in doc.sections[0].chunks[0].text

    def test_unicode_handling(self, tmp_path):
        """Test handling of Unicode content."""
        # Create file with Unicode content
        unicode_file = tmp_path / "unicode.txt"
        unicode_content = "Hello, 世界! 🌍 This is a test with émojis and àccénts."
        unicode_file.write_text(unicode_content, encoding="utf-8")
        
        doc = parse(str(unicode_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert "世界" in doc.sections[0].chunks[0].text
        assert "🌍" in doc.sections[0].chunks[0].text
        assert "émojis" in doc.sections[0].chunks[0].text
        assert "àccénts" in doc.sections[0].chunks[0].text


if __name__ == "__main__":
    pytest.main([__file__])
