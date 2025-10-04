# PDF Image Extraction with panparsex

This document describes the image extraction capabilities added to panparsex for PDF documents. The feature allows you to automatically detect, extract, and associate images with text content during PDF parsing.

## Features

- **Automatic Image Detection**: Detects images in PDF documents using PyMuPDF (preferred) or pypdf (fallback)
- **Image Extraction**: Saves extracted images to disk with configurable output directory
- **Text Association**: Associates images with nearby text content for better context
- **Metadata Tracking**: Tracks image position, dimensions, format, and page numbers
- **AI Integration**: Includes image metadata in AI analysis for comprehensive document understanding
- **CLI Support**: Command-line interface with image extraction options

## Installation

The image extraction functionality requires additional dependencies:

```bash
pip install panparsex[image]
```

Or install the required packages manually:

```bash
pip install PyMuPDF Pillow
```

## Usage

### Basic Usage

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
```

### Advanced Configuration

```python
from panparsex import parse

doc = parse(
    "document.pdf",
    extract_images=True,
    image_output_dir="my_images",  # Custom output directory
    min_image_size=(100, 100)       # Minimum image size threshold
)
```

### CLI Usage

```bash
# Extract images from PDF
panparsex parse document.pdf --extract-images

# Specify output directory and minimum size
panparsex parse document.pdf --extract-images --image-output-dir ./images --min-image-size 50 50

# Combine with AI processing
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text content"
```

## Image Metadata

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

## Document Structure

Images are integrated into the document structure:

```python
# Access images at document level
doc.images  # List of all images

# Access images by page
page_images = doc.get_images_by_page(1)

# Access images by section
section_images = doc.get_images_by_section(0)

# Images are also associated with sections
for section in doc.sections:
    print(f"Section '{section.heading}' has {len(section.images)} images")
```

## AI Analysis with Images

The AI processor now includes image metadata in analysis:

```python
from panparsex.ai_processor import AIProcessor

processor = AIProcessor(api_key="your-openai-key")

result = processor.process_document(
    doc,
    task="Analyze this document including images and their context",
    output_format="structured_json"
)

# Result includes image analysis
if 'images_analysis' in result:
    analysis = result['images_analysis']
    print(f"Total images: {analysis['total_images']}")
    print(f"Images by page: {analysis['images_by_page']}")
    print(f"Image contexts: {analysis['image_contexts']}")
```

## Example: Complete Workflow

```python
#!/usr/bin/env python3
from panparsex import parse
from panparsex.ai_processor import AIProcessor
import os

# Parse PDF with image extraction
doc = parse(
    "offer_letter.pdf",
    extract_images=True,
    image_output_dir="extracted_images",
    min_image_size=(50, 50)
)

print(f"Document: {doc.meta.title}")
print(f"Pages: {len(doc.sections)}")
print(f"Images: {len(doc.images)}")

# Display image information
for img in doc.images:
    print(f"\nImage: {img.image_id}")
    print(f"  Page: {img.page_number}")
    print(f"  Size: {img.dimensions}")
    print(f"  File: {img.file_path}")
    if img.associated_text:
        print(f"  Context: {img.associated_text[:100]}...")

# AI analysis including images
if os.getenv("OPENAI_API_KEY"):
    processor = AIProcessor()
    result = processor.process_document(
        doc,
        task="Analyze this document including any images and their relationship to text content",
        output_format="structured_json"
    )
    
    print(f"\nAI Analysis Summary: {result['summary']}")
    if 'images_analysis' in result:
        print(f"Image Analysis: {result['images_analysis']}")
```

## Configuration Options

### Image Extraction Parameters

- `extract_images`: Enable/disable image extraction (default: True for PDFs)
- `image_output_dir`: Directory to save extracted images (default: "extracted_images")
- `min_image_size`: Minimum width and height threshold (default: (50, 50))

### Image Processing Libraries

The system uses PyMuPDF (fitz) as the primary library for image extraction, with pypdf as a fallback:

1. **PyMuPDF**: Better image extraction, position detection, and text association
2. **pypdf**: Fallback when PyMuPDF is not available

## Error Handling

The image extraction is designed to be robust:

- If image extraction fails, parsing continues with text-only content
- Warnings are logged for failed extractions
- Minimum size thresholds prevent extraction of tiny images
- Graceful fallback between PyMuPDF and pypdf

## Performance Considerations

- Image extraction adds processing time to PDF parsing
- Large images may consume significant disk space
- Consider setting appropriate `min_image_size` thresholds
- Use `extract_images=False` for text-only parsing when images aren't needed

## Troubleshooting

### Common Issues

1. **No images extracted**: Check if images meet the minimum size threshold
2. **PyMuPDF import error**: Install with `pip install PyMuPDF`
3. **Permission errors**: Ensure write access to the output directory
4. **Memory issues**: Process large PDFs in smaller batches

### Debug Mode

Enable debug logging to see detailed extraction information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

Planned improvements include:

- OCR text extraction from images
- Image classification and tagging
- Batch processing for multiple PDFs
- Support for other document formats (DOCX, PPTX)
- Image similarity detection and deduplication
