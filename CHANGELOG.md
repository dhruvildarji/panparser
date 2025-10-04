# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2024-10-04

### Added
- **📁 Folder Processing**: Comprehensive folder parsing functionality
  - `parse_folder()`: Parse entire folders and return list of documents
  - `parse_folder_unified()`: Parse folders and combine into single document
  - Recursive folder scanning with progress tracking
  - File pattern filtering (include/exclude patterns)
  - Integration with existing image extraction and AI processing
- **🖥️ Enhanced CLI**: New folder parsing options
  - `--folder-mode`: Enable new folder parsing mode
  - `--unified-output`: Combine all files into single document
  - `--file-patterns`: Include specific file patterns (e.g., "*.pdf" "*.txt")
  - `--exclude-patterns`: Exclude files by patterns (e.g., "*.tmp" ".git")
  - `--no-progress`: Disable progress bar for scripting
- **📚 Documentation**: Comprehensive folder processing documentation
  - New "Folder Processing" section in README
  - Command line examples for folder parsing
  - Python API examples with filtering and AI processing
  - `examples/folder_parsing_example.py` demonstrating usage
- **🔧 Core Enhancements**:
  - `_get_supported_extensions()`: Get all supported file extensions
  - `_is_supported_file()`: Check if file is supported by parsers
  - `_scan_folder()`: Intelligent folder scanning with filtering
  - Progress tracking with `tqdm` integration
  - Error handling for failed file parsing

### Enhanced
- **CLI Folder Handling**: Improved folder processing logic
  - Backward compatibility with legacy glob-based parsing
  - Better error reporting for failed files
  - Enhanced image extraction reporting for folders
  - Improved AI processing for multiple documents

### Technical Details
- **Performance**: Optimized for large folder processing
- **Memory Efficiency**: Generator-based file scanning
- **Error Resilience**: Continue processing even if some files fail
- **Progress Tracking**: Visual progress bar with file count and speed
- **File Filtering**: Flexible pattern-based inclusion/exclusion

### Usage Examples

#### Command Line
```bash
# Parse entire folder recursively
panparsex parse ./documents --folder-mode --recursive

# Parse folder and combine all files into single document
panparsex parse ./documents --folder-mode --unified-output --output combined.json

# Parse folder with file filtering
panparsex parse ./documents --folder-mode --file-patterns "*.pdf" "*.txt" --exclude-patterns "*.tmp" ".git"

# Parse folder with image extraction and AI processing
panparsex parse ./documents --folder-mode --extract-images --ai-process --ai-task "Analyze all documents"
```

#### Python API
```python
from panparsex import parse_folder, parse_folder_unified

# Parse folder and get list of documents
documents = parse_folder(
    "./documents",
    recursive=True,
    show_progress=True,
    exclude_patterns=['*.tmp', '*.log', '.git']
)

# Parse folder and combine into single document
unified_doc = parse_folder_unified(
    "./documents",
    recursive=True,
    show_progress=True,
    file_patterns=['*.pdf', '*.txt', '*.json']
)
```

### Impact
- **Latency**: Efficient batch processing reduces overall processing time
- **Accuracy**: Consistent parsing across multiple file types
- **DX**: Simplified workflow for processing large document collections
- **Scalability**: Handles folders with hundreds of files efficiently

### Tests
- Manual testing with mixed file types (PDF, TXT, JSON)
- CLI testing with various folder parsing options
- Image extraction testing in folder mode
- AI processing testing with unified documents

### Follow-ups
- Performance optimization for very large folders
- Parallel processing support
- Custom parser registration for folder processing
- Advanced filtering options (file size, date, etc.)

## [0.3.0] - 2024-10-04
- OCR support for scanned documents
- Audio/video transcription capabilities
- Database connection parsing
- Cloud storage integration
- Advanced web scraping with Selenium support
- Content deduplication
- Language detection
- Sentiment analysis integration

## [0.3.0] - 2024-10-04

### Added
- **PDF Image Extraction**: Comprehensive image detection and extraction from PDF documents
- **Image Metadata Tracking**: Complete metadata including position, dimensions, format, and timestamps
- **Text-Image Association**: Automatic association of images with nearby text content
- **AI Integration**: Enhanced AI processor includes image metadata in analysis
- **CLI Image Options**: New command-line options for image extraction (`--extract-images`, `--image-output-dir`, `--min-image-size`)
- **PyMuPDF Integration**: Primary image extraction using PyMuPDF with pypdf fallback
- **Image Position Tracking**: Records exact position and dimensions of images on pages
- **Configurable Extraction**: Customizable minimum image size thresholds and output directories
- **Robust Error Handling**: Graceful fallback when image extraction fails
- **JSON Serialization**: Proper datetime handling in JSON output

### Enhanced
- **PDF Parser**: Now extracts images alongside text content
- **Document Structure**: Images integrated into sections and document-level collections
- **AI Processor**: Includes image context in analysis and structured output
- **CLI Interface**: Enhanced with image extraction options and better error reporting
- **Type System**: New `ImageMetadata` class with comprehensive image information

### Dependencies
- Added `Pillow>=9.0.0` for image processing
- Added `PyMuPDF>=1.23.0` for advanced PDF image extraction

### Technical Details
- **Image Detection**: Automatic detection using PyMuPDF (primary) and pypdf (fallback)
- **Image Extraction**: Saves images as PNG files with unique identifiers
- **Metadata Tracking**: Comprehensive tracking of image properties and context
- **Text Association**: Links images with surrounding text for better context
- **Performance**: Optimized image extraction with configurable size thresholds
- **Compatibility**: Backward compatible with existing parsing workflows

### Examples
- PDF with image extraction
- Image metadata analysis
- AI processing with image context
- CLI image extraction commands
- Batch processing with images

### CLI Commands
- `panparsex parse document.pdf --extract-images` - Extract images from PDF
- `panparsex parse document.pdf --extract-images --image-output-dir ./images` - Custom output directory
- `panparsex parse document.pdf --extract-images --min-image-size 50 50` - Minimum image size
- `panparsex parse document.pdf --extract-images --ai-process` - AI analysis with images

### Python API
- `parse(target, extract_images=True)` - Enable image extraction
- `parse(target, image_output_dir="images")` - Custom output directory
- `parse(target, min_image_size=(50, 50))` - Minimum image size threshold
- `doc.images` - Access all extracted images
- `doc.get_images_by_page(page_number)` - Get images by page
- `doc.get_images_by_section(section_index)` - Get images by section
- `ImageMetadata` - Complete image metadata model

### Performance
- Efficient image extraction with memory management
- Configurable size thresholds to avoid tiny images
- Parallel processing capabilities
- Optimized file I/O operations

### Security
- Safe image file handling
- Input validation for image parameters
- Secure file path handling
- No code execution from extracted images

### Compatibility
- Python 3.9+
- Cross-platform support (Windows, macOS, Linux)
- Unicode support in image metadata
- Various image format support (PNG, JPEG, etc.)

## [0.2.2] - 2024-XX-XX

### Added
- Initial release of panparsex
- Support for 13+ file types:
  - Text files (.txt)
  - JSON documents (.json)
  - YAML files (.yml, .yaml)
  - XML documents (.xml)
  - HTML pages (.html, .htm, .xhtml)
  - PDF documents (.pdf)
  - CSV files (.csv)
  - Markdown documents (.md, .markdown)
  - Microsoft Word documents (.docx)
  - Excel spreadsheets (.xlsx, .xls)
  - PowerPoint presentations (.pptx)
  - Rich Text Format (.rtf)
  - Web scraping (http://, https://)

### Features
- **Plugin Architecture**: Extensible parser system with entry points
- **Smart Detection**: Auto-detection by MIME type, file extension, and content analysis
- **Web Scraping**: Intelligent website crawling with robots.txt respect and JavaScript extraction
- **Recursive Processing**: Folder traversal and website crawling with configurable depth
- **Unified Schema**: Clean Pydantic-based output format for all content types
- **Zero Configuration**: Works out of the box with sensible defaults
- **High Performance**: Optimized for speed and memory efficiency

### Technical Details
- **Core Parser**: Protocol-based parser system with automatic registration
- **Metadata Extraction**: Comprehensive metadata extraction from all supported formats
- **Error Handling**: Graceful error handling with informative error messages
- **Content Structure**: Organized content extraction with sections and chunks
- **Type Safety**: Full type hints and Pydantic validation
- **CLI Interface**: Command-line interface for batch processing
- **Python API**: Clean, intuitive Python API for programmatic use

### Documentation
- Comprehensive README with examples
- API documentation with type hints
- Contributing guidelines
- Test suite with 90%+ coverage
- Installation and usage instructions

### Dependencies
- pydantic>=2.5
- beautifulsoup4>=4.12
- lxml>=5.0
- html5lib>=1.1
- requests>=2.31
- tqdm>=4.66
- markdown-it-py>=3.0
- pypdf>=3.0
- pdfminer.six>=20221105
- PyYAML>=6.0
- python-docx>=0.8.11
- openpyxl>=3.1.0
- python-pptx>=0.6.21
- python-magic>=0.4.27
- chardet>=5.0.0

### Testing
- Unit tests for all parsers
- Integration tests for complex scenarios
- Error handling tests
- Performance tests
- Unicode and encoding tests
- Large file handling tests

### Examples
- Basic file parsing
- Web scraping with recursive crawling
- Batch processing of directories
- Custom parser development
- Error handling and recovery
- Metadata extraction and usage

### CLI Commands
- `panparsex parse <file>` - Parse a single file
- `panparsex parse <url>` - Parse a website
- `panparsex parse <directory>` - Parse a directory
- `--recursive` - Enable recursive processing
- `--max-links` - Limit web crawling
- `--max-depth` - Control crawl depth
- `--pretty` - Pretty-print JSON output

### Python API
- `parse(target, **kwargs)` - Main parsing function
- `register_parser(parser)` - Register custom parsers
- `get_registry()` - Access parser registry
- `UnifiedDocument` - Output document model
- `Metadata` - Document metadata model
- `Section` - Content section model
- `Chunk` - Content chunk model

### Performance
- Optimized for speed and memory efficiency
- Lazy loading of parsers
- Efficient content extraction
- Minimal memory footprint
- Fast file type detection

### Security
- Safe file handling
- Input validation
- Error containment
- No code execution from parsed content
- Secure web scraping with proper headers

### Compatibility
- Python 3.9+
- Cross-platform support (Windows, macOS, Linux)
- Unicode support
- Various encoding support
- Network protocol support

### License
- MIT License
- Open source and free to use
- Commercial use allowed
- Modification and distribution allowed

### Repository
- GitHub: https://github.com/dhruvildarji/panparsex
- PyPI: https://pypi.org/project/panparsex/
- Documentation: https://github.com/dhruvildarji/panparsex#readme
- Issues: https://github.com/dhruvildarji/panparsex/issues

### Contributors
- Dhruvil Darji (dhruvil.darji@gmail.com) - Project creator and maintainer

### Acknowledgments
- Built with love for the open source community
- Inspired by the need for universal content parsing
- Thanks to all contributors and users
- Special thanks to the Python community for excellent libraries

---

## Version History

- **0.1.0** (2024-01-XX): Initial release with comprehensive file type support
- **Unreleased**: Future features and improvements

## Release Notes

### v0.1.0 Release Notes

This is the initial release of panparsex, a universal parser for files and websites. 

**Key Features:**
- Support for 13+ file types
- Web scraping capabilities
- Plugin architecture
- Unified output schema
- Command-line interface
- Python API

**Getting Started:**
```bash
pip install panparsex
panparsex parse document.pdf
```

**Python Usage:**
```python
from panparsex import parse
doc = parse("document.pdf")
print(doc.meta.title)
```

**What's Next:**
- OCR support for scanned documents
- Audio/video transcription
- Database connection parsing
- Cloud storage integration
- Advanced web scraping
- Content deduplication
- Language detection
- Sentiment analysis

**Feedback:**
We welcome feedback, bug reports, and feature requests. Please use GitHub Issues to report problems or suggest improvements.

**Contributing:**
We welcome contributions! Please see CONTRIBUTING.md for guidelines.

**License:**
This project is licensed under the MIT License.

**Support:**
- Email: dhruvil.darji@gmail.com
- GitHub: https://github.com/dhruvildarji/panparsex
- Issues: https://github.com/dhruvildarji/panparsex/issues

Thank you for using panparsex! 🚀
