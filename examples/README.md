# panparsex Examples

This directory contains comprehensive examples demonstrating how to use panparsex for various parsing tasks.

## Files

### Sample Files
- `sample_files/` - Directory containing sample files in various formats for testing
  - `sample.txt` - Plain text file
  - `sample.json` - JSON document
  - `sample.yaml` - YAML configuration
  - `sample.xml` - XML document
  - `sample.html` - HTML web page
  - `sample.csv` - CSV spreadsheet
  - `sample.md` - Markdown document

### Example Scripts
- `basic_usage.py` - Basic usage examples for all supported file types
- `advanced_usage.py` - Advanced features like web scraping, custom parsers, and batch processing

## Running Examples

### Prerequisites

Make sure panparsex is installed:

```bash
pip install panparsex
```

### Basic Examples

Run the basic usage examples:

```bash
python examples/basic_usage.py
```

This will demonstrate:
- Text file parsing
- JSON file parsing
- HTML file parsing
- CSV file parsing
- YAML file parsing
- XML file parsing
- Markdown file parsing
- Parser registry inspection
- Batch processing

### Advanced Examples

Run the advanced usage examples:

```bash
python examples/advanced_usage.py
```

This will demonstrate:
- Web scraping (requires internet connection)
- Custom parser creation and registration
- Batch directory processing
- Content analysis and search
- Error handling and recovery
- Performance testing

### Using Sample Files

You can test panparsex with the provided sample files:

```bash
# Parse individual files
panparsex parse examples/sample_files/sample.txt
panparsex parse examples/sample_files/sample.json
panparsex parse examples/sample_files/sample.html

# Parse with pretty output
panparsex parse examples/sample_files/sample.yaml --pretty

# Parse all files in the directory
panparsex parse examples/sample_files --recursive
```

### Python API Examples

```python
from panparsex import parse

# Parse a sample file
doc = parse("examples/sample_files/sample.txt")
print(f"Content: {doc.sections[0].chunks[0].text}")

# Parse JSON with metadata extraction
doc = parse("examples/sample_files/sample.json")
print(f"JSON content: {doc.sections[0].chunks[0].text}")

# Parse HTML with structured extraction
doc = parse("examples/sample_files/sample.html")
print(f"Title: {doc.meta.title}")
print(f"Sections: {len(doc.sections)}")
```

## Example Outputs

### Text File Parsing
```
=== Text File Parsing ===
File: /tmp/tmpXXXXXX.txt
Content Type: text/plain
Sections: 1
Section 1:
  Chunk 1: Hello, world!
This is a sample text file.
It contains multiple lines.
```

### JSON File Parsing
```
=== JSON File Parsing ===
File: /tmp/tmpXXXXXX.json
Content Type: application/json
Content: {
  "name": "panparsex",
  "version": "0.1.0",
  "features": ["universal", "extensible"]
}
```

### HTML File Parsing
```
=== HTML File Parsing ===
File: /tmp/tmpXXXXXX.html
Title: Sample Page
Sections: 3
Section 1: Welcome to panparsex
  Content: This is a sample paragraph.
Section 2: Features
  Content: Universal parsing
Plugin architecture
Web scraping
Section 3: Contact & Support
  Content: Author: Dhruvil Darji
Email: dhruvil.darji@gmail.com
```

### CSV File Parsing
```
=== CSV File Parsing ===
File: /tmp/tmpXXXXXX.csv
Sections: 3
Section 1: Headers
  Content: name | age | city
Section 2: Data
  Content: John | 30 | New York
Jane | 25 | Los Angeles
Bob | 35 | Chicago
Section 3: Summary
  Content: CSV Summary: 3 columns, 3 data rows
```

## Customization

### Creating Custom Parsers

See `advanced_usage.py` for examples of creating custom parsers:

```python
from panparsex import register_parser, ParserProtocol
from panparsex.types import UnifiedDocument, Metadata, Section, Chunk

class CustomParser(ParserProtocol):
    name = "custom"
    content_types = ("application/custom",)
    extensions = (".custom",)
    
    def can_parse(self, meta: Metadata) -> bool:
        return meta.content_type == "application/custom"
    
    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        # Your parsing logic here
        return UnifiedDocument(meta=meta, sections=[])

# Register the parser
register_parser(CustomParser())
```

### Batch Processing

```python
from pathlib import Path
from panparsex import parse

def process_directory(directory: str):
    results = []
    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            try:
                doc = parse(str(file_path))
                results.append({
                    "file": str(file_path),
                    "sections": len(doc.sections),
                    "content_length": sum(len(chunk.text) for section in doc.sections for chunk in section.chunks)
                })
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return results
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure panparsex is installed
   ```bash
   pip install panparsex
   ```

2. **File Not Found**: Check that sample files exist
   ```bash
   ls examples/sample_files/
   ```

3. **Permission Error**: Ensure you have read permissions for the files

4. **Network Error**: Web scraping examples require internet connection

### Getting Help

- Check the main README.md for detailed documentation
- Look at the test files in `tests/` for more examples
- Open an issue on GitHub if you encounter problems

## Contributing

If you have additional examples or improvements, please:

1. Fork the repository
2. Add your examples to this directory
3. Update this README
4. Submit a pull request

## License

These examples are part of the panparsex project and are licensed under the Apache License 2.0.
