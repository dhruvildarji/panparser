# Contributing to panparsex

Thank you for your interest in contributing to panparsex! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Adding New Parsers](#adding-new-parsers)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to dhruvil.darji@gmail.com.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Add tests for your changes
6. Ensure all tests pass
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or conda
- git

### Installation

```bash
# Clone your fork
git clone https://github.com/yourusername/panparsex.git
cd panparsex

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### Development Dependencies

The project includes development dependencies for testing, linting, and formatting:

```bash
pip install -e ".[dev]"
```

This installs:
- pytest for testing
- black for code formatting
- flake8 for linting
- mypy for type checking
- pre-commit for git hooks

## Contributing Guidelines

### General Guidelines

1. **Follow PEP 8**: Use the project's code style (enforced by black and flake8)
2. **Write Tests**: All new features must include tests
3. **Update Documentation**: Update README, docstrings, and type hints as needed
4. **Keep It Simple**: Write clear, readable code
5. **Handle Errors Gracefully**: Always include proper error handling

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for parsing RTF files
fix: handle empty CSV files gracefully
docs: update README with new parser examples
test: add tests for Excel parser
```

### Code Style

The project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Run these before submitting:

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Adding New Parsers

### Parser Structure

All parsers must implement the `ParserProtocol`:

```python
from panparsex.core import ParserProtocol, register_parser
from panparsex.types import UnifiedDocument, Metadata

class MyParser(ParserProtocol):
    name = "my_parser"
    content_types = ("application/my-type",)
    extensions = (".myext",)
    
    def can_parse(self, meta: Metadata) -> bool:
        """Return True if this parser can handle the given metadata."""
        return meta.content_type in self.content_types
    
    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        """Parse the target and return a UnifiedDocument."""
        # Your parsing logic here
        return UnifiedDocument(meta=meta, sections=[])

# Register the parser
register_parser(MyParser())
```

### Parser Requirements

1. **Error Handling**: Always handle errors gracefully
2. **Metadata Extraction**: Extract relevant metadata when possible
3. **Structured Output**: Organize content into logical sections
4. **Fallback Support**: Provide fallback behavior for unsupported content
5. **Documentation**: Include comprehensive docstrings

### Example Parser

Here's a complete example for a custom parser:

```python
from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class CustomParser(ParserProtocol):
    name = "custom"
    content_types: Iterable[str] = ("application/custom",)
    extensions: Iterable[str] = (".custom",)

    def can_parse(self, meta: Metadata) -> bool:
        """Check if this parser can handle the given metadata."""
        return (meta.content_type in self.content_types or 
                (meta.path or "").endswith(".custom"))

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        """Parse a custom file format."""
        doc = UnifiedDocument(meta=meta, sections=[])
        
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Extract structured content
            sections = self._extract_sections(content)
            
            for i, section_content in enumerate(sections):
                section = Section(
                    heading=f"Section {i + 1}",
                    chunks=[Chunk(text=section_content, order=i)],
                    meta={"type": "content"}
                )
                doc.sections.append(section)
                
        except Exception as e:
            error_text = f"[panparsex:custom] unable to parse: {e}"
            doc.sections.append(Section(
                heading="Error",
                chunks=[Chunk(text=error_text, order=0, meta={"error": True})],
                meta={"error": True}
            ))
        
        return doc
    
    def _extract_sections(self, content: str) -> list[str]:
        """Extract sections from content."""
        # Your section extraction logic here
        return [content]  # Simple fallback

register_parser(CustomParser())
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=panparsex --cov-report=html

# Run specific test file
pytest tests/test_parsers.py

# Run specific test
pytest tests/test_parsers.py::TestTextParser::test_text_file_parsing
```

### Writing Tests

All new parsers must include comprehensive tests:

```python
import pytest
from panparsex import parse
from panparsex.types import UnifiedDocument

class TestCustomParser:
    def test_custom_file_parsing(self, tmp_path):
        """Test basic custom file parsing."""
        test_file = tmp_path / "test.custom"
        test_content = "Custom content here"
        test_file.write_text(test_content)
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        assert len(doc.sections) == 1
        assert test_content in doc.sections[0].chunks[0].text
        assert doc.meta.content_type == "application/custom"

    def test_invalid_custom_file(self, tmp_path):
        """Test parsing invalid custom file."""
        test_file = tmp_path / "invalid.custom"
        test_file.write_text("invalid content")
        
        doc = parse(str(test_file))
        
        assert isinstance(doc, UnifiedDocument)
        # Test error handling
        assert "[panparsex:custom]" in doc.sections[0].chunks[0].text
```

### Test Requirements

1. **Coverage**: Aim for 90%+ test coverage
2. **Edge Cases**: Test error conditions and edge cases
3. **Integration**: Include integration tests
4. **Performance**: Test with larger files when relevant

## Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Include type hints for all function parameters and return values
- Document complex algorithms and business logic

### User Documentation

- Update README.md for new features
- Add examples for new parsers
- Update the supported file types table
- Include configuration options

### API Documentation

- Document all public APIs
- Include usage examples
- Explain error conditions and return values

## Submitting Changes

### Pull Request Process

1. **Create a Branch**: Use a descriptive branch name
   ```bash
   git checkout -b feature/add-rtf-parser
   ```

2. **Make Changes**: Implement your feature or fix
   ```bash
   git add .
   git commit -m "feat: add RTF parser with striprtf support"
   ```

3. **Push Changes**: Push to your fork
   ```bash
   git push origin feature/add-rtf-parser
   ```

4. **Create Pull Request**: Use the GitHub interface to create a PR

### Pull Request Template

When creating a pull request, include:

- **Description**: What changes were made and why
- **Testing**: How the changes were tested
- **Documentation**: What documentation was updated
- **Breaking Changes**: Any breaking changes (if applicable)
- **Related Issues**: Link to related issues

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer must approve
3. **Testing**: All tests must pass
4. **Documentation**: Documentation must be updated

## Release Process

Releases are managed by maintainers. To request a release:

1. Ensure all tests pass
2. Update version in `pyproject.toml`
3. Update `CHANGELOG.md`
4. Create a release PR
5. Tag the release after merge

## Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact dhruvil.darji@gmail.com for private matters

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to panparsex! 🚀
