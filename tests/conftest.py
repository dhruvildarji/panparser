import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def tmp_path():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing."""
    files = {}
    
    # Text file
    text_file = tmp_path / "sample.txt"
    text_file.write_text("Hello, world!\nThis is a sample text file.")
    files["text"] = text_file
    
    # JSON file
    json_file = tmp_path / "sample.json"
    json_file.write_text('{"name": "John", "age": 30, "city": "New York"}')
    files["json"] = json_file
    
    # YAML file
    yaml_file = tmp_path / "sample.yaml"
    yaml_file.write_text("""
name: John
age: 30
city: New York
hobbies:
  - reading
  - swimming
""")
    files["yaml"] = yaml_file
    
    # XML file
    xml_file = tmp_path / "sample.xml"
    xml_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<person>
    <name>John</name>
    <age>30</age>
    <city>New York</city>
</person>""")
    files["xml"] = xml_file
    
    # HTML file
    html_file = tmp_path / "sample.html"
    html_file.write_text("""<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
    <meta name="description" content="A sample HTML page">
</head>
<body>
    <h1>Welcome</h1>
    <p>This is a sample paragraph.</p>
    <h2>Section 2</h2>
    <p>Another paragraph.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>""")
    files["html"] = html_file
    
    # CSV file
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("""name,age,city
John,30,New York
Jane,25,Los Angeles
Bob,35,Chicago""")
    files["csv"] = csv_file
    
    # Markdown file
    md_file = tmp_path / "sample.md"
    md_file.write_text("""# Sample Document

This is a sample markdown document.

## Section 1

This is the first section with some **bold** text.

### Subsection

- Item 1
- Item 2

## Section 2

This is the second section with a [link](https://example.com).

```python
def hello():
    print("Hello, world!")
```

> This is a blockquote.
""")
    files["markdown"] = md_file
    
    return files


@pytest.fixture
def invalid_files(tmp_path):
    """Create invalid files for testing error handling."""
    files = {}
    
    # Invalid JSON
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text('{"invalid": json}')
    files["invalid_json"] = invalid_json
    
    # Empty file
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    files["empty"] = empty_file
    
    # File with special characters
    special_file = tmp_path / "special.txt"
    special_file.write_text("Hello, 世界! 🌍 This has émojis and àccénts.")
    files["special"] = special_file
    
    return files


@pytest.fixture
def large_file(tmp_path):
    """Create a large file for testing."""
    large_file = tmp_path / "large.txt"
    content = "\n".join([f"Line {i}: This is line number {i}" for i in range(1000)])
    large_file.write_text(content)
    return large_file


@pytest.fixture
def nested_directory(tmp_path):
    """Create a nested directory structure for testing."""
    # Create subdirectories
    subdir1 = tmp_path / "subdir1"
    subdir2 = tmp_path / "subdir2"
    subdir1.mkdir()
    subdir2.mkdir()
    
    # Create files in root
    (tmp_path / "root.txt").write_text("Root file content")
    (tmp_path / "root.json").write_text('{"type": "root"}')
    
    # Create files in subdirectories
    (subdir1 / "nested1.txt").write_text("Nested file 1 content")
    (subdir1 / "nested1.yaml").write_text("type: nested1")
    
    (subdir2 / "nested2.txt").write_text("Nested file 2 content")
    (subdir2 / "nested2.xml").write_text('<root><type>nested2</type></root>')
    
    return tmp_path
