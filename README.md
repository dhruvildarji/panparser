# panparsex

**Pan-parse anything.** A universal, extensible parser that normalizes content from files and websites into a single, clean schema.

[![PyPI version](https://badge.fury.io/py/panparsex.svg)](https://badge.fury.io/py/panparsex)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🧩 **Plugin Architecture**: Add new parsers without touching core code
- 📄 **Comprehensive Support**: Text, JSON, YAML, XML, HTML, PDF, CSV, DOCX, Markdown, RTF, Excel, PowerPoint, and more
- 🖼️ **PDF Image Extraction**: Extract images from PDF documents with metadata and text association
- 📁 **Folder Processing**: Parse entire folders recursively with progress tracking and file filtering
- 🌐 **Web Scraping**: Intelligent website crawling with robots.txt respect and JavaScript extraction
- 🧠 **Smart Detection**: Auto-detection by MIME type, file extension, and content analysis
- 🔁 **Recursive Processing**: Folder traversal and website crawling with configurable depth
- 🧪 **Clean Schema**: Unified Pydantic-based output format for all content types
- 🤖 **AI-Powered Processing**: Use OpenAI GPT to analyze, restructure, and filter parsed content
- 🛠️ **Zero Configuration**: Works out of the box with sensible defaults
- 🚀 **High Performance**: Optimized for speed and memory efficiency

## Installation

```bash
# Basic installation
pip install panparsex

# With Selenium support for JavaScript-heavy websites
pip install panparsex[selenium]
```

## Quick Start

### Command Line Interface

```bash
# Parse a single file
panparsex parse document.pdf

# Parse a website with recursive crawling
panparsex parse https://example.com --recursive --max-links 50 --max-depth 2

# Parse a directory recursively (legacy mode)
panparsex parse ./documents --recursive --glob '**/*'

# Parse entire folder with new folder mode
panparsex parse ./documents --folder-mode --recursive

# Parse folder and combine all files into single document
panparsex parse ./documents --folder-mode --unified-output --output combined.json

# Parse folder with file filtering
panparsex parse ./documents --folder-mode --file-patterns "*.pdf" "*.txt" --exclude-patterns "*.tmp" ".git"

# Parse folder with image extraction
panparsex parse ./documents --folder-mode --extract-images --image-output-dir ./extracted_images

# Parse folder with AI processing
panparsex parse ./documents --folder-mode --ai-process --ai-task "Analyze all documents and create summary"

# Pretty-print output
panparsex parse document.html --pretty

# Parse with AI processing (quiet mode, save to files)
panparsex parse document.pdf --ai-process --ai-output analysis.json --output parsed_content.json --quiet

# Extract images from PDF
panparsex parse document.pdf --extract-images --image-output-dir ./images

# Extract images with AI analysis
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text content"

# Parse website with AI analysis (no terminal output)
panparsex parse https://example.com --ai-process --ai-format markdown --ai-task "Extract key information and create summary" --quiet

# Parse JavaScript-heavy websites with Selenium
panparsex parse https://example.com --use-selenium --quiet --output website.json

# Parse with Selenium and AI processing
panparsex parse https://example.com --use-selenium --ai-process --quiet --output parsed.json --ai-output analysis.json
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
```

## Folder Processing

panparsex can parse entire folders recursively, processing all supported file types with progress tracking and intelligent filtering.

### Command Line Examples

```bash
# Parse entire folder recursively
panparsex parse ./documents --folder-mode --recursive

# Parse folder and combine all files into single document
panparsex parse ./documents --folder-mode --unified-output --output combined.json

# Parse folder with file filtering
panparsex parse ./documents --folder-mode --file-patterns "*.pdf" "*.txt" --exclude-patterns "*.tmp" ".git"

# Parse folder with image extraction from PDFs
panparsex parse ./documents --folder-mode --extract-images --image-output-dir ./extracted_images

# Parse folder with AI processing
panparsex parse ./documents --folder-mode --ai-process --ai-task "Analyze all documents and create summary"

# Disable progress bar for scripting
panparsex parse ./documents --folder-mode --no-progress --output results.json
```

### Python API Examples

```python
from panparsex import parse_folder, parse_folder_unified

# Parse folder and get list of documents
documents = parse_folder(
    "./documents",
    recursive=True,
    show_progress=True,
    exclude_patterns=['*.tmp', '*.log', '.git']
)

print(f"Found {len(documents)} documents")
for doc in documents:
    print(f"File: {doc.meta.source}")
    print(f"Sections: {len(doc.sections)}")
    if hasattr(doc, 'images') and doc.images:
        print(f"Images: {len(doc.images)}")

# Parse folder and combine into single document
unified_doc = parse_folder_unified(
    "./documents",
    recursive=True,
    show_progress=True,
    file_patterns=['*.pdf', '*.txt', '*.json'],
    exclude_patterns=['*.tmp', '.git']
)

print(f"Combined document: {len(unified_doc.sections)} sections")
print(f"Total images: {len(unified_doc.images)}")

# Process with AI
from panparsex.ai_processor import AIProcessor

processor = AIProcessor(api_key="your-openai-key")
result = processor.process_document(
    unified_doc,
    task="Analyze all documents and create comprehensive summary",
    output_format="structured_json"
)
```

### Folder Processing Features

- **🔄 Recursive Scanning**: Process subdirectories automatically
- **📊 Progress Tracking**: Visual progress bar with file count and speed
- **🎯 File Filtering**: Include/exclude files by patterns
- **🖼️ Image Extraction**: Extract images from PDFs in batch
- **🤖 AI Processing**: Analyze entire folder contents with AI
- **📁 Unified Output**: Combine all files into single document
- **⚡ Performance**: Optimized for large folder processing
- **🛡️ Error Handling**: Continue processing even if some files fail

## PDF Image Extraction

panparsex v0.5.0 introduces comprehensive PDF image extraction capabilities that automatically detect, extract, and associate images with text content.

### Basic Image Extraction

```python
from panparsex import parse

# Parse PDF with image extraction enabled
doc = parse("document.pdf", extract_images=True)

# Access extracted images
print(f"Found {len(doc.images)} images")
for img in doc.images:
    print(f"Image {img.image_id} on page {img.page_number}")
    print(f"Dimensions: {img.dimensions}")
    print(f"File: {img.file_path}")
    if img.associated_text:
        print(f"Associated text: {img.associated_text[:100]}...")
```

### Advanced Configuration

```python
# Custom output directory and minimum image size
doc = parse(
    "document.pdf",
    extract_images=True,
    image_output_dir="my_images",
    min_image_size=(100, 100)  # Minimum width and height
)

# Access images by page or section
page_images = doc.get_images_by_page(1)
section_images = doc.get_images_by_section(0)
```

### AI Analysis with Images

```python
from panparsex.ai_processor import AIProcessor

# Parse with image extraction
doc = parse("document.pdf", extract_images=True)

# AI analysis including image context
processor = AIProcessor(api_key="your-openai-key")
result = processor.process_document(
    doc,
    task="Analyze this document including any images and their relationship to text content",
    output_format="structured_json"
)

# Access image analysis results
if 'images_analysis' in result:
    analysis = result['images_analysis']
    print(f"Total images: {analysis['total_images']}")
    print(f"Image contexts: {analysis['image_contexts']}")
```

### CLI Image Extraction

```bash
# Extract images from PDF
panparsex parse document.pdf --extract-images

# Specify output directory and minimum size
panparsex parse document.pdf --extract-images --image-output-dir ./images --min-image-size 50 50

# Combine with AI analysis
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text content"
```

### Image Metadata

Each extracted image includes comprehensive metadata:

```python
class ImageMetadata:
    image_id: str                    # Unique identifier
    page_number: int                 # Page where image appears
    position: Dict[str, float]       # Position on page (x, y, width, height)
    file_path: Optional[str]         # Path to extracted image file
    file_size: Optional[int]         # File size in bytes
    format: Optional[str]            # Image format (PNG, JPEG, etc.)
    dimensions: Optional[Dict[str, int]]  # Width and height
    extracted_at: datetime           # Extraction timestamp
    associated_text: Optional[str]   # Text near the image
    confidence_score: Optional[float]  # Detection confidence
    meta: Dict[str, Any]             # Additional metadata
```

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
  --output, -o             Output file for parsed results
  --quiet, -q              Suppress all output to terminal
  --ai-process             Process with AI after parsing
  --ai-task TEXT           AI task description
  --ai-format TEXT         AI output format (structured_json, markdown, summary)
  --ai-output TEXT         Output file for AI-processed result
  --openai-key TEXT        OpenAI API key
  --ai-model TEXT          OpenAI model to use (default: gpt-4o-mini)
  --ai-tokens INTEGER      Max tokens for AI response (default: 4000)
  --ai-temperature FLOAT   AI temperature 0.0-1.0 (default: 0.3)
  --use-selenium           Use Selenium for JavaScript-heavy websites
  --headless               Run browser in headless mode (Selenium)
  --browser-delay FLOAT    Delay between page loads (Selenium)
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

### JavaScript-Heavy Websites with Selenium

```python
from panparsex.parsers.web_selenium import SeleniumWebParser
from panparsex.types import Metadata

# Parse JavaScript-heavy websites
parser = SeleniumWebParser()
meta = Metadata(source="https://spa-website.com", content_type="text/html")
doc = parser.parse("https://spa-website.com", meta, headless=True, delay=2.0)

print(f"Pages parsed: {doc.meta.extra['pages_parsed']}")
for section in doc.sections:
    print(f"Section: {section.heading}")
    print(f"Content: {section.chunks[0].text[:200]}...")
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.5.0 (2024-10-04)
- **🚫 Programming File Filtering**: Intelligent filtering of programming files during folder parsing
- **📊 Parsing Summary**: Detailed statistics and reporting with ParsingSummary class
- **🖥️ Enhanced CLI Output**: Rich summary display with emojis and formatting
- **📁 Folder Processing**: Comprehensive folder parsing with file filtering
- **🖼️ PDF Image Extraction**: Extract images from PDF documents with metadata
- **🤖 AI-Powered Processing**: OpenAI GPT integration for content analysis

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
