# Installation Guide for panparsex

This guide provides detailed installation instructions for panparsex on different platforms and environments.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

## System Requirements

### Minimum Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512 MB RAM (1 GB recommended)
- **Disk Space**: 100 MB for installation

### Supported Python Versions

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

### Dependencies

panparsex automatically installs the following dependencies:

- **pydantic** (>=2.5) - Data validation
- **beautifulsoup4** (>=4.12) - HTML parsing
- **lxml** (>=5.0) - XML processing
- **html5lib** (>=1.1) - HTML5 parsing
- **requests** (>=2.31) - HTTP requests
- **tqdm** (>=4.66) - Progress bars
- **markdown-it-py** (>=3.0) - Markdown parsing
- **pypdf** (>=3.0) - PDF parsing
- **pdfminer.six** (>=20221105) - PDF text extraction
- **PyYAML** (>=6.0) - YAML parsing
- **python-docx** (>=0.8.11) - Word document parsing
- **openpyxl** (>=3.1.0) - Excel spreadsheet parsing
- **python-pptx** (>=0.6.21) - PowerPoint parsing
- **python-magic** (>=0.4.27) - File type detection
- **chardet** (>=5.0.0) - Character encoding detection

## Installation Methods

### Method 1: pip (Recommended)

#### Standard Installation

```bash
pip install panparsex
```

#### User Installation (No Admin Rights)

```bash
pip install --user panparsex
```

#### Specific Version

```bash
pip install panparsex==0.1.0
```

#### Latest Development Version

```bash
pip install git+https://github.com/dhruvildarji/panparsex.git
```

### Method 2: conda

```bash
# Add conda-forge channel
conda config --add channels conda-forge

# Install panparsex
conda install panparsex
```

### Method 3: From Source

```bash
# Clone the repository
git clone https://github.com/dhruvildarji/panparsex.git
cd panparsex

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Method 4: Virtual Environment (Recommended for Development)

```bash
# Create virtual environment
python -m venv panparsex-env

# Activate virtual environment
# On Windows:
panparsex-env\Scripts\activate
# On macOS/Linux:
source panparsex-env/bin/activate

# Install panparsex
pip install panparsex
```

## Platform-Specific Instructions

### Windows

#### Using pip

1. **Open Command Prompt or PowerShell**
2. **Install Python** (if not already installed):
   ```bash
   # Download from https://python.org
   # Or use Microsoft Store
   ```
3. **Install panparsex**:
   ```bash
   pip install panparsex
   ```

#### Using Anaconda

1. **Install Anaconda** from https://anaconda.com
2. **Open Anaconda Prompt**
3. **Install panparsex**:
   ```bash
   conda install -c conda-forge panparsex
   ```

#### Troubleshooting Windows Issues

- **Python not found**: Add Python to PATH
- **Permission denied**: Use `pip install --user panparsex`
- **SSL errors**: Update certificates or use `--trusted-host`

### macOS

#### Using Homebrew

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python
   ```

3. **Install panparsex**:
   ```bash
   pip install panparsex
   ```

#### Using MacPorts

1. **Install MacPorts** from https://macports.org
2. **Install Python**:
   ```bash
   sudo port install python39
   ```

3. **Install panparsex**:
   ```bash
   pip install panparsex
   ```

#### Troubleshooting macOS Issues

- **Xcode command line tools**: Install with `xcode-select --install`
- **Permission issues**: Use `pip install --user panparsex`
- **SSL errors**: Update certificates

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install panparsex
pip3 install panparsex
```

#### CentOS/RHEL/Fedora

```bash
# Install Python and pip
sudo yum install python3 python3-pip
# Or on newer versions:
sudo dnf install python3 python3-pip

# Install panparsex
pip3 install panparsex
```

#### Arch Linux

```bash
# Install Python and pip
sudo pacman -S python python-pip

# Install panparsex
pip install panparsex
```

#### Troubleshooting Linux Issues

- **Package not found**: Update package lists
- **Permission denied**: Use `sudo` or `pip install --user`
- **Missing dependencies**: Install system packages

## Verification

### Basic Verification

```bash
# Check installation
python -c "import panparsex; print('panparsex installed successfully')"

# Check version
python -c "import panparsex; print(panparsex.__version__)"

# Test CLI
panparsex --help
```

### Advanced Verification

```bash
# Test parsing functionality
python -c "
from panparsex import parse
import tempfile
import os

# Create test file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('Hello, panparsex!')
    temp_file = f.name

try:
    # Parse file
    doc = parse(temp_file)
    print(f'Successfully parsed: {doc.sections[0].chunks[0].text}')
    print('Installation verification passed!')
finally:
    os.unlink(temp_file)
"
```

### Test with Sample Files

```bash
# Download sample files (if available)
# Test parsing
panparsex parse examples/sample_files/sample.txt
panparsex parse examples/sample_files/sample.json
panparsex parse examples/sample_files/sample.html
```

## Troubleshooting

### Common Installation Issues

#### 1. pip not found

**Error**: `pip: command not found`

**Solutions**:
```bash
# Try pip3 instead
pip3 install panparsex

# Install pip
python -m ensurepip --upgrade

# Use python -m pip
python -m pip install panparsex
```

#### 2. Permission denied

**Error**: `Permission denied` or `Access denied`

**Solutions**:
```bash
# Install for user only
pip install --user panparsex

# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install panparsex
```

#### 3. SSL/TLS errors

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
```bash
# Update certificates
pip install --upgrade certifi

# Use trusted host
pip install --trusted-host pypi.org --trusted-host pypi.python.org panparsex

# Update pip
python -m pip install --upgrade pip
```

#### 4. Package conflicts

**Error**: `ERROR: pip's dependency resolver does not currently take into account all the packages`

**Solutions**:
```bash
# Install in virtual environment
python -m venv venv
source venv/bin/activate
pip install panparsex

# Force reinstall
pip install --force-reinstall panparsex

# Check for conflicts
pip check
```

#### 5. Python version mismatch

**Error**: `ERROR: Package 'panparsex' requires a different Python`

**Solutions**:
```bash
# Check Python version
python --version

# Use correct Python version
python3.9 -m pip install panparsex

# Install specific version compatible with your Python
pip install "panparsex>=0.1.0,<0.2.0"
```

### Platform-Specific Issues

#### Windows

- **Long path issues**: Enable long path support
- **Antivirus blocking**: Add exception for Python/pip
- **PowerShell execution policy**: Set to RemoteSigned

#### macOS

- **Gatekeeper blocking**: Allow Python in Security & Privacy
- **Homebrew permissions**: Fix with `sudo chown -R $(whoami) /usr/local`
- **Python version conflicts**: Use pyenv for version management

#### Linux

- **Missing system packages**: Install build-essential, python3-dev
- **pip version issues**: Update with `python -m pip install --upgrade pip`
- **Permission issues**: Use virtual environment or --user flag

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look for detailed error messages
2. **Search issues**: Check GitHub issues for similar problems
3. **Create issue**: Open a new issue with:
   - Operating system and version
   - Python version
   - Full error message
   - Steps to reproduce

## Uninstallation

### Remove panparsex

```bash
# Uninstall panparsex
pip uninstall panparsex

# Remove dependencies (optional)
pip uninstall pydantic beautifulsoup4 lxml html5lib requests tqdm markdown-it-py pypdf pdfminer-six PyYAML python-docx openpyxl python-pptx python-magic chardet
```

### Clean up

```bash
# Remove cache
pip cache purge

# Remove virtual environment
rm -rf venv/  # On Windows: rmdir /s venv
```

### Verify removal

```bash
# Check if still installed
python -c "import panparsex"  # Should raise ImportError

# Check CLI
panparsex --help  # Should show command not found
```

## Next Steps

After successful installation:

1. **Read the documentation**: Check [README.md](README.md)
2. **Try examples**: Run examples in `examples/` directory
3. **Explore features**: Test different file types and options
4. **Join community**: Star the repository and contribute

## Support

- **Documentation**: [README.md](README.md)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/dhruvildarji/panparsex/issues)
- **Email**: dhruvil.darji@gmail.com

## License

This installation guide is part of the panparsex project and is licensed under the Apache License 2.0.
