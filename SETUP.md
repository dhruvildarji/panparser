# Setup Instructions for panparsex

This document provides detailed setup instructions for developers and users of panparsex.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Building](#building)
- [Release Process](#release-process)
- [Troubleshooting](#troubleshooting)

## Quick Start

### For Users

1. **Install panparsex**:
   ```bash
   pip install panparsex
   ```

2. **Basic Usage**:
   ```bash
   # Parse a file
   panparsex parse document.pdf
   
   # Parse a website
   panparsex parse https://example.com
   
   # Parse a directory
   panparsex parse ./documents --recursive
   ```

3. **Python API**:
   ```python
   from panparsex import parse
   
   doc = parse("document.pdf")
   print(doc.meta.title)
   print(doc.sections[0].chunks[0].text)
   ```

### For Developers

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dhruvildarji/panparsex.git
   cd panparsex
   ```

2. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or conda
- git

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dhruvildarji/panparsex.git
   cd panparsex
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Install the package in development mode
   pip install -e ".[dev]"
   
   # Or install dependencies manually
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Verify installation**:
   ```bash
   python -c "from panparsex import parse; print('Installation successful')"
   ```

### Development Dependencies

The following packages are required for development:

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks
- **safety** - Security checks
- **bandit** - Security linting

### IDE Setup

#### VS Code

1. Install the Python extension
2. Configure settings in `.vscode/settings.json`:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.formatting.provider": "black",
     "python.testing.pytestEnabled": true
   }
   ```

#### PyCharm

1. Open the project in PyCharm
2. Configure the Python interpreter to use the virtual environment
3. Enable pytest as the test runner
4. Configure code style to use black

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=panparsex --cov-report=html

# Run specific test file
pytest tests/test_basic.py

# Run specific test
pytest tests/test_basic.py::test_text

# Run with verbose output
pytest -v
```

### Test Structure

- `tests/test_basic.py` - Basic functionality tests
- `tests/test_parsers.py` - Parser-specific tests
- `tests/test_integration.py` - Integration tests
- `tests/conftest.py` - Test configuration and fixtures

### Writing Tests

1. **Test file naming**: `test_*.py`
2. **Test function naming**: `test_*`
3. **Use fixtures**: Leverage `conftest.py` fixtures
4. **Test edge cases**: Include error conditions and edge cases
5. **Mock external dependencies**: Use mocks for network calls, file I/O

Example test:
```python
def test_parser_functionality(tmp_path):
    """Test parser functionality."""
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, world!")
    
    # Test parsing
    doc = parse(str(test_file))
    
    # Assertions
    assert isinstance(doc, UnifiedDocument)
    assert "Hello, world!" in doc.sections[0].chunks[0].text
```

## Building

### Building the Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Build for specific platform
python -m build --wheel
```

### Package Structure

```
panparsex/
├── src/
│   └── panparsex/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py
│       ├── types.py
│       └── parsers/
│           ├── __init__.py
│           ├── text.py
│           ├── json_.py
│           ├── yaml_.py
│           ├── xml.py
│           ├── html.py
│           ├── pdf.py
│           ├── web.py
│           ├── csv.py
│           ├── docx.py
│           ├── markdown.py
│           ├── rtf.py
│           ├── excel.py
│           └── pptx.py
├── tests/
├── examples/
├── pyproject.toml
├── README.md
└── LICENSE
```

## Release Process

### Preparing a Release

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.1.1"
   ```

2. **Update changelog** in `CHANGELOG.md`:
   ```markdown
   ## [0.1.1] - 2024-01-XX
   - Bug fixes
   - New features
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Build package**:
   ```bash
   python -m build
   ```

5. **Create release commit**:
   ```bash
   git add .
   git commit -m "chore: prepare release v0.1.1"
   ```

6. **Create and push tag**:
   ```bash
   git tag -a v0.1.1 -m "Release v0.1.1"
   git push origin main
   git push origin v0.1.1
   ```

### Automated Release

The GitHub Actions workflow will automatically:
1. Build the package
2. Upload to PyPI
3. Create a GitHub release
4. Upload release assets

### Manual Release

If you need to release manually:

```bash
# Upload to PyPI
twine upload dist/*

# Or upload to TestPyPI first
twine upload --repository testpypi dist/*
```

## Troubleshooting

### Common Issues

#### Installation Issues

1. **Permission denied**:
   ```bash
   pip install --user panparsex
   ```

2. **Python version mismatch**:
   ```bash
   python --version  # Should be 3.9+
   ```

3. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Development Issues

1. **Import errors**:
   ```bash
   pip install -e .
   ```

2. **Test failures**:
   ```bash
   pytest --tb=short -v
   ```

3. **Linting errors**:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

#### Build Issues

1. **Build failures**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   python -m build
   ```

2. **Upload failures**:
   ```bash
   twine check dist/*
   ```

### Getting Help

- **Documentation**: Check README.md and examples/
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: Contact dhruvil.darji@gmail.com

### Debug Mode

Enable debug mode for detailed logging:

```bash
export PANPARSEX_DEBUG=1
panparsex parse document.pdf
```

### Performance Issues

1. **Large files**: Use streaming for very large files
2. **Memory usage**: Monitor memory consumption
3. **Network timeouts**: Adjust timeout settings

### Platform-Specific Issues

#### Windows

- Use PowerShell or Command Prompt
- Ensure Python is in PATH
- Use forward slashes in paths

#### macOS

- Use Homebrew for Python installation
- Ensure Xcode command line tools are installed

#### Linux

- Use system package manager for Python
- Install development headers if needed

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linting
6. Submit a pull request

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints
- Write comprehensive tests
- Update documentation
- Handle errors gracefully

## Support

- **Email**: dhruvil.darji@gmail.com
- **GitHub**: https://github.com/dhruvildarji/panparsex
- **Issues**: https://github.com/dhruvildarji/panparsex/issues
- **Discussions**: https://github.com/dhruvildarji/panparsex/discussions

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
