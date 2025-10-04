# panparsex v0.3.0 Release Instructions

## 🎉 Release Summary

**panparsex v0.3.0** is ready for release! This major version introduces comprehensive PDF image extraction capabilities that transform panparsex from a text-focused parser into a complete document analysis tool.

## 📦 What's Been Prepared

### ✅ Version & Dependencies
- **Version**: Updated to `0.3.0` in `pyproject.toml`
- **Dependencies**: Added `PyMuPDF>=1.23.0` and `Pillow>=9.0.0`
- **Package**: Built and tested successfully (`dist/panparsex-0.3.0-py3-none-any.whl`)

### ✅ Documentation
- **CHANGELOG.md**: Comprehensive v0.3.0 release notes
- **README.md**: Updated with PDF image extraction section
- **RELEASE_v0.3.0.md**: Complete release documentation with examples
- **Examples**: Three standalone Python examples for different use cases

### ✅ Code Changes
- **Types**: New `ImageMetadata` class with comprehensive image information
- **Image Extractor**: Complete `ImageExtractor` class with PyMuPDF/pypdf support
- **PDF Parser**: Enhanced with image extraction integration
- **AI Processor**: Updated to include image metadata in analysis
- **CLI**: New image extraction options (`--extract-images`, `--image-output-dir`, `--min-image-size`)
- **JSON Serialization**: Fixed datetime handling for proper JSON output

### ✅ Testing
- **Package Build**: Successfully built and installed
- **Functionality Test**: Verified with NVIDIA PDF (2 images extracted)
- **CLI Test**: Command-line interface working correctly
- **JSON Output**: Proper serialization with datetime handling

## 🚀 Release Steps

### 1. Upload to PyPI

```bash
# Install build tools if not already installed
pip install build twine

# Build the package (already done)
python -m build

# Upload to PyPI
twine upload dist/panparsex-0.3.0*
```

### 2. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. **Tag version**: `v0.3.0`
4. **Release title**: `panparsex v0.3.0 - PDF Image Extraction`
5. **Description**: Copy content from `RELEASE_v0.3.0.md`
6. **Attach files**: Upload the built wheel and source distribution

### 3. Update Documentation

1. **GitHub README**: Already updated with image extraction section
2. **PyPI Description**: Will use README.md content
3. **Examples**: Three example files ready for release page

## 📋 Release Content

### New Features
- **PDF Image Extraction**: Automatic detection and extraction of images from PDFs
- **Image Metadata Tracking**: Complete metadata including position, dimensions, format
- **Text-Image Association**: Links images with nearby text content
- **AI Integration**: Enhanced AI analysis includes image context
- **CLI Enhancements**: New command-line options for image extraction

### Technical Improvements
- **PyMuPDF Integration**: Primary image extraction with pypdf fallback
- **Robust Error Handling**: Graceful fallback when image extraction fails
- **JSON Serialization**: Proper datetime handling in output
- **Performance Optimization**: Configurable size thresholds and efficient processing

### Backward Compatibility
- **100% Compatible**: Existing code continues to work without changes
- **Opt-in Feature**: Image extraction enabled with `extract_images=True` parameter
- **No Breaking Changes**: All existing APIs remain unchanged

## 🎯 Usage Examples for Release Page

### Basic Image Extraction
```python
from panparsex import parse

# Parse PDF with image extraction
doc = parse("document.pdf", extract_images=True)

# Access extracted images
for img in doc.images:
    print(f"Image {img.image_id} on page {img.page_number}")
    print(f"Dimensions: {img.dimensions}")
    print(f"File: {img.file_path}")
```

### CLI Usage
```bash
# Extract images from PDF
panparsex parse document.pdf --extract-images

# With AI analysis
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text"
```

### AI Analysis with Images
```python
from panparsex.ai_processor import AIProcessor

processor = AIProcessor(api_key="your-openai-key")
result = processor.process_document(
    doc,
    task="Analyze this document including any images and their relationship to text content",
    output_format="structured_json"
)
```

## 📊 Test Results

### NVIDIA PDF Test
- ✅ **2 images detected and extracted** (4001x3337 pixels each)
- ✅ **Images saved as PNG files** (62KB and 73KB)
- ✅ **Complete text content parsed** from the offer letter
- ✅ **Full metadata tracking** (page numbers, dimensions, timestamps)
- ✅ **CLI functionality working** with all new options
- ✅ **JSON serialization working** with proper datetime handling

## 🔧 Installation Instructions

```bash
# Install the new version
pip install panparsex==0.3.0

# Or upgrade from previous version
pip install --upgrade panparsex
```

## 📞 Support & Feedback

- **Documentation**: Updated README with comprehensive examples
- **Examples**: Three standalone Python examples provided
- **Issues**: GitHub Issues for bug reports and feature requests
- **Email**: dhruvil.darji@gmail.com

## 🎉 Release Checklist

- [x] Version number updated to 0.3.0
- [x] Dependencies added (PyMuPDF, Pillow)
- [x] CHANGELOG.md updated with comprehensive release notes
- [x] README.md updated with image extraction section
- [x] Release documentation created (RELEASE_v0.3.0.md)
- [x] Python examples created for release page
- [x] Package built and tested successfully
- [x] Functionality verified with real PDF
- [x] CLI tested and working
- [x] JSON serialization fixed
- [x] Backward compatibility confirmed

## 🚀 Ready for Release!

panparsex v0.3.0 is fully prepared and tested. The package builds successfully, all functionality works as expected, and comprehensive documentation is ready. This release represents a major milestone in making panparsex a complete document analysis solution that understands both text and visual content.

**The release is ready to go live!** 🎉
