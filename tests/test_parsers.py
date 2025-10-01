import pytest
import tempfile
import os
from pathlib import Path
from panparsex import parse, get_registry
from panparsex.types import UnifiedDocument


class TestTextParser:
    def test_text_file_parsing(self, tmp_path):
        """Test basic text file parsing."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, world!\nThis is a test file."
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert test_content in doc.sections[0].chunks[0].text
        assert doc.meta.content_type == "text/plain"

    def test_empty_text_file(self, tmp_path):
        """Test parsing empty text file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert doc.sections[0].chunks[0].text == ""


class TestJSONParser:
    def test_json_file_parsing(self, tmp_path):
        """Test JSON file parsing."""
        test_file = tmp_path / "test.json"
        test_data = {"name": "John", "age": 30, "city": "New York"}
        test_file.write_text('{"name": "John", "age": 30, "city": "New York"}')
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert "John" in doc.sections[0].chunks[0].text
        assert "30" in doc.sections[0].chunks[0].text
        assert doc.meta.content_type == "application/json"

    def test_invalid_json(self, tmp_path):
        """Test parsing invalid JSON."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text('{"invalid": json}')
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert "[panparsex:json]" in doc.sections[0].chunks[0].text


class TestYAMLParser:
    def test_yaml_file_parsing(self, tmp_path):
        """Test YAML file parsing."""
        test_file = tmp_path / "test.yaml"
        test_content = """
name: John
age: 30
city: New York
hobbies:
  - reading
  - swimming
"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert "John" in doc.sections[0].chunks[0].text
        assert doc.meta.content_type in ["application/yaml", "text/yaml"]


class TestXMLParser:
    def test_xml_file_parsing(self, tmp_path):
        """Test XML file parsing."""
        test_file = tmp_path / "test.xml"
        test_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <person>
        <name>John</name>
        <age>30</age>
    </person>
</root>"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert "John" in doc.sections[0].chunks[0].text
        assert doc.meta.content_type in ["application/xml", "text/xml"]


class TestHTMLParser:
    def test_html_file_parsing(self, tmp_path):
        """Test HTML file parsing."""
        test_file = tmp_path / "test.html"
        test_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Welcome</h1>
    <p>This is a test paragraph.</p>
    <h2>Section 2</h2>
    <p>Another paragraph.</p>
</body>
</html>"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert doc.meta.title == "Test Page"
        assert len(doc.sections) >= 1
        assert doc.sections[0].heading == "Welcome"
        # Check that the heading is in the first chunk
        assert "Welcome" in doc.sections[0].chunks[0].text
        # Check that paragraph content is in subsequent chunks
        paragraph_found = False
        for chunk in doc.sections[0].chunks:
            if "This is a test paragraph" in chunk.text:
                paragraph_found = True
                break
        assert paragraph_found
        assert doc.meta.content_type == "text/html"

    def test_html_with_meta_tags(self, tmp_path):
        """Test HTML with meta tags extraction."""
        test_file = tmp_path / "test.html"
        test_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <meta name="description" content="A test page">
    <meta name="keywords" content="test, html, parsing">
</head>
<body>
    <h1>Test</h1>
    <p>Content here.</p>
</body>
</html>"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert "meta_tags" in doc.meta.extra
        assert doc.meta.extra["meta_tags"]["description"] == "A test page"


class TestCSVParser:
    def test_csv_file_parsing(self, tmp_path):
        """Test CSV file parsing."""
        test_file = tmp_path / "test.csv"
        test_content = """name,age,city
John,30,New York
Jane,25,Los Angeles
Bob,35,Chicago"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) >= 2  # Headers + Data sections
        assert "John" in doc.sections[1].chunks[0].text  # Data section
        assert "csv_data" in doc.meta.extra
        assert len(doc.meta.extra["csv_data"]["headers"]) == 3

    def test_csv_with_different_delimiter(self, tmp_path):
        """Test CSV with semicolon delimiter."""
        test_file = tmp_path / "test.csv"
        test_content = """name;age;city
John;30;New York
Jane;25;Los Angeles"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert "John" in doc.sections[1].chunks[0].text


class TestMarkdownParser:
    def test_markdown_file_parsing(self, tmp_path):
        """Test Markdown file parsing."""
        test_file = tmp_path / "test.md"
        test_content = """# Main Title

This is a paragraph.

## Section 2

Another paragraph with **bold** text.

```python
def hello():
    print("Hello, world!")
```

> This is a quote.
"""
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert doc.meta.title == "Main Title"
        assert len(doc.sections) >= 1
        assert "Main Title" in doc.sections[0].heading
        assert "This is a paragraph" in doc.sections[0].chunks[0].text


class TestWebParser:
    def test_web_url_parsing(self):
        """Test web URL parsing (mock test)."""
        # This is a basic test - in real scenarios, you'd mock the requests
        # For now, we'll just test that the parser can handle URLs
        registry = get_registry()
        web_parser = None
        for parser in registry.parsers:
            if parser.name == "web":
                web_parser = parser
                break
        
        assert web_parser is not None
        
        # Test can_parse method
        from panparsex.types import Metadata
        meta = Metadata(source="https://example.com", content_type="text/html")
        assert web_parser.can_parse(meta)


class TestParserRegistry:
    def test_all_parsers_registered(self):
        """Test that all expected parsers are registered."""
        registry = get_registry()
        parser_names = [p.name for p in registry.parsers]
        
        expected_parsers = [
            "text", "json", "yaml", "xml", "html", "pdf", "web",
            "csv", "docx", "markdown", "rtf", "excel", "pptx"
        ]
        
        for expected in expected_parsers:
            assert expected in parser_names, f"Parser '{expected}' not found in registry"

    def test_parser_fallback(self, tmp_path):
        """Test that unknown file types fall back to text parser."""
        test_file = tmp_path / "test.unknown"
        test_content = "This is some unknown file content."
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert test_content in doc.sections[0].chunks[0].text


class TestErrorHandling:
    def test_nonexistent_file(self):
        """Test handling of nonexistent files."""
        with pytest.raises(Exception):
            parse("/nonexistent/file.txt")

    def test_permission_error(self, tmp_path):
        """Test handling of permission errors."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Make file read-only (Unix only)
        if os.name != 'nt':
            os.chmod(test_file, 0o000)
            try:
                doc = parse(str(test_file))
                # Should still work or handle gracefully
                assert isinstance(doc, UnifiedDocument)
            finally:
                os.chmod(test_file, 0o644)


class TestCLI:
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        from panparsex.cli import main
        assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__])
