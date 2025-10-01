# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- OCR support for scanned documents
- Audio/video transcription capabilities
- Database connection parsing
- Cloud storage integration
- Advanced web scraping with Selenium support
- Content deduplication
- Language detection
- Sentiment analysis integration

## [0.1.0] - 2024-01-XX

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
- Apache License 2.0
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
This project is licensed under the Apache License 2.0.

**Support:**
- Email: dhruvil.darji@gmail.com
- GitHub: https://github.com/dhruvildarji/panparsex
- Issues: https://github.com/dhruvildarji/panparsex/issues

Thank you for using panparsex! 🚀
