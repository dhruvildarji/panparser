# panparsex

**Pan-parse anything.** A universal, extensible parser that normalizes content from files and websites into a single, clean schema.

[![PyPI version](https://badge.fury.io/py/panparsex.svg)](https://badge.fury.io/py/panparsex)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- 🧩 **Plugin Architecture**: Add new parsers without touching core code
- 📄 **Comprehensive Support**: Text, JSON, YAML, XML, HTML, PDF, CSV, DOCX, Markdown, RTF, Excel, PowerPoint, and more
- 🌐 **Web Scraping**: Intelligent website crawling with robots.txt respect and JavaScript extraction
- 🧠 **Smart Detection**: Auto-detection by MIME type, file extension, and content analysis
- 🔁 **Recursive Processing**: Folder traversal and website crawling with configurable depth
- 🧪 **Clean Schema**: Unified Pydantic-based output format for all content types
- 🤖 **AI-Powered Processing**: Use OpenAI GPT to analyze, restructure, and filter parsed content
- 🛠️ **Zero Configuration**: Works out of the box with sensible defaults
- 🚀 **High Performance**: Optimized for speed and memory efficiency

## Installation

```bash
pip install panparsex
```

## Quick Start

### Command Line Interface

```bash
# Parse a single file
panparsex parse document.pdf

# Parse a website with recursive crawling
panparsex parse https://example.com --recursive --max-links 50 --max-depth 2

# Parse a directory recursively
panparsex parse ./documents --recursive --glob '**/*'

# Pretty-print output
panparsex parse document.html --pretty

# Parse with AI processing
panparsex parse document.pdf --ai-process --ai-output analysis.json

# Parse website with AI analysis
panparsex parse https://example.com --ai-process --ai-format markdown --ai-task "Extract key information and create summary"
```

### Python API

```python
from panparsex import parse

# Parse a file
doc = parse("document.pdf")
print(doc.meta.title)
print(doc.sections[0].chunks[0].text)

# Parse with AI processing
from panparsex.ai_processor import AIProcessor

processor = AIProcessor(api_key="your-openai-key")
result = processor.process_and_save(
    doc,
    "analysis.json",
    task="Analyze and restructure the content",
    output_format="structured_json"
)

# Parse a website
doc = parse("https://example.com", recursive=True, max_links=10)
for section in doc.sections:
    print(f"Section: {section.heading}")
    for chunk in section.chunks:
        print(f"  {chunk.text[:100]}...")

# Parse with custom options
doc = parse("data.csv", content_type="text/csv")
print(doc.meta.extra["csv_data"]["headers"])
```

## Supported File Types

| Type | Extensions | Description |
|------|------------|-------------|
| **Text** | `.txt` | Plain text files |
| **JSON** | `.json` | JSON documents with structured data |
| **YAML** | `.yml`, `.yaml` | YAML configuration files |
| **XML** | `.xml` | XML documents |
| **HTML** | `.html`, `.htm`, `.xhtml` | HTML web pages with metadata extraction |
| **PDF** | `.pdf` | PDF documents with page-by-page extraction |
| **CSV** | `.csv` | Comma-separated values with header detection |
| **Markdown** | `.md`, `.markdown` | Markdown documents with structure preservation |
| **Word** | `.docx` | Microsoft Word documents |
| **Excel** | `.xlsx`, `.xls` | Excel spreadsheets with sheet extraction |
| **PowerPoint** | `.pptx` | PowerPoint presentations with slide extraction |
| **RTF** | `.rtf` | Rich Text Format documents |
| **Web** | `http://`, `https://` | Websites with intelligent content extraction |

## Output Schema

All parsed content follows a unified schema:

```python
class UnifiedDocument(BaseModel):
    schema_id: str = "panparsex/v1"
    meta: Metadata
    sections: List[Section]

class Metadata(BaseModel):
    source: str
    content_type: str
    title: Optional[str]
    url: Optional[str]
    path: Optional[str]
    extra: Dict[str, Any]

class Section(BaseModel):
    heading: Optional[str]
    chunks: List[Chunk]
    meta: Dict[str, Any]

class Chunk(BaseModel):
    text: str
    order: int
    meta: Dict[str, Any]
```

## Advanced Usage

### Web Scraping with JavaScript

```python
# Extract JavaScript content from websites
doc = parse("https://spa-website.com", extract_js=True)

# Find JavaScript sections
for section in doc.sections:
    if section.meta.get("type") == "javascript":
        print(f"JS from {section.meta['url']}: {section.chunks[0].text[:200]}...")
```

### Custom Parser Registration

```python
from panparsex import register_parser, ParserProtocol
from panparsex.types import UnifiedDocument, Metadata

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
import os
from pathlib import Path
from panparsex import parse

def process_directory(directory: str):
    """Process all files in a directory."""
    results = []
    
    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            try:
                doc = parse(str(file_path))
                results.append({
                    "file": str(file_path),
                    "title": doc.meta.title,
                    "content_length": sum(len(chunk.text) for section in doc.sections for chunk in section.chunks),
                    "sections": len(doc.sections)
                })
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    return results

# Process a directory
results = process_directory("./documents")
for result in results:
    print(f"{result['file']}: {result['sections']} sections, {result['content_length']} chars")
```

## Configuration

### Environment Variables

- `PANPARSEX_USER_AGENT`: Custom user agent for web scraping
- `PANPARSEX_TIMEOUT`: Request timeout in seconds (default: 15)
- `PANPARSEX_DELAY`: Delay between requests in seconds (default: 0)
- `OPENAI_API_KEY`: OpenAI API key for AI processing features

### CLI Options

```bash
panparsex parse [OPTIONS] TARGET

Options:
  --recursive              Enable recursive processing
  --glob TEXT              Glob pattern for directory processing
  --max-links INTEGER      Maximum links to follow (web scraping)
  --max-depth INTEGER      Maximum crawl depth (web scraping)
  --same-origin            Restrict crawling to same origin
  --pretty                 Pretty-print JSON output
  --ai-process             Process with AI after parsing
  --ai-task TEXT           AI task description
  --ai-format TEXT         AI output format (structured_json, markdown, summary)
  --ai-output TEXT         Output file for AI-processed result
  --openai-key TEXT        OpenAI API key
  --ai-model TEXT          OpenAI model to use (default: gpt-4o-mini)
  --ai-tokens INTEGER      Max tokens for AI response (default: 4000)
  --ai-temperature FLOAT   AI temperature 0.0-1.0 (default: 0.3)
  --help                   Show help message
```

## Examples

### Extract Text from PDF

```python
from panparsex import parse

doc = parse("report.pdf")
for section in doc.sections:
    print(f"Page {section.meta.get('page_number', 'Unknown')}:")
    print(section.chunks[0].text[:200] + "...")
```

### Parse Excel Spreadsheet

```python
from panparsex import parse

doc = parse("data.xlsx")
for section in doc.sections:
    if section.meta.get("type") == "sheet":
        print(f"Sheet: {section.meta['sheet_name']}")
        print(f"Rows: {section.meta['rows']}, Cols: {section.meta['cols']}")
        print(section.chunks[0].text[:300] + "...")
```

### Scrape Website Content

```python
from panparsex import parse

doc = parse("https://news-website.com", recursive=True, max_links=20, max_depth=2)

print(f"Crawled {doc.meta.extra['pages_parsed']} pages")
print(f"Unique domains: {doc.meta.extra['crawl_stats']['unique_domains']}")

for section in doc.sections:
    if section.meta.get("url"):
        print(f"\nFrom {section.meta['url']}:")
        print(f"Title: {section.heading}")
        print(f"Content: {section.chunks[0].text[:200]}...")
```

### AI-Powered Content Analysis

```python
from panparsex import parse
from panparsex.ai_processor import AIProcessor

# Parse a document
doc = parse("business_report.pdf")

# Process with AI
processor = AIProcessor(api_key="your-openai-key")
result = processor.process_and_save(
    doc,
    "analysis.json",
    task="Extract key metrics, identify challenges, and provide recommendations",
    output_format="structured_json"
)

# The result will contain structured analysis
print("Summary:", result.get("summary"))
print("Key Topics:", result.get("key_topics"))
print("Recommendations:", result.get("recommendations"))
```

### AI Processing with Custom Task

```python
from panparsex import parse
from panparsex.ai_processor import AIProcessor

# Parse a website
doc = parse("https://company.com", recursive=True, max_links=10)

# Custom AI analysis
processor = AIProcessor(api_key="your-openai-key")
result = processor.process_and_save(
    doc,
    "company_analysis.md",
    task="Analyze the company's services, extract contact information, and identify key features",
    output_format="markdown"
)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Adding New Parsers

1. Create a new parser class implementing `ParserProtocol`
2. Add it to the `parsers/` directory
3. Register it in the core module
4. Add tests and documentation

### Development Setup

```bash
git clone https://github.com/dhruvildarji/panparsex.git
cd panparsex
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0 (2024-01-XX)
- Initial release
- Support for 13+ file types
- Web scraping capabilities
- Plugin architecture
- Comprehensive test suite

## Support

- 📧 Email: dhruvil.darji@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/dhruvildarji/panparsex/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/dhruvildarji/panparsex/wiki)

## Roadmap

- [ ] OCR support for scanned documents
- [ ] Audio/video transcription
- [ ] Database connection parsing
- [ ] Cloud storage integration
- [ ] Advanced web scraping (Selenium support)
- [ ] Content deduplication
- [ ] Language detection
- [ ] Sentiment analysis integration
