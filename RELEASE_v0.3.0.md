# panparsex v0.3.0 Release - PDF Image Extraction

## 🎉 Major Feature Release: PDF Image Extraction

We're excited to announce **panparsex v0.3.0**, a major release that adds comprehensive PDF image extraction capabilities to our universal parser. This release transforms panparsex from a text-focused parser into a complete document analysis tool that understands both text and visual content.

## 🚀 What's New

### ✨ PDF Image Extraction
- **Automatic Image Detection**: Finds images in PDF documents using advanced parsing libraries
- **Image Extraction**: Saves images to disk with unique identifiers and metadata
- **Text-Image Association**: Links images with nearby text content for better context
- **Position Tracking**: Records exact position and dimensions of images on pages
- **AI Integration**: Includes image metadata in AI analysis for comprehensive document understanding

### 🔧 Enhanced Features
- **PyMuPDF Integration**: Primary image extraction using PyMuPDF with pypdf fallback
- **Configurable Extraction**: Customizable minimum image size thresholds and output directories
- **Robust Error Handling**: Graceful fallback when image extraction fails
- **CLI Enhancements**: New command-line options for image extraction
- **JSON Serialization**: Proper datetime handling in JSON output

## 📦 Installation

```bash
pip install panparsex==0.3.0
```

The new image extraction functionality requires additional dependencies that are automatically installed:
- `PyMuPDF>=1.23.0` - Advanced PDF image extraction
- `Pillow>=9.0.0` - Image processing

## 🎯 Quick Start

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
```

### CLI Usage

```bash
# Extract images from PDF
panparsex parse document.pdf --extract-images

# Specify output directory and minimum size
panparsex parse document.pdf --extract-images --image-output-dir ./images --min-image-size 50 50

# Combine with AI analysis
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text content"
```

## 📋 Complete Examples

### Example 1: Basic PDF Image Extraction

```python
#!/usr/bin/env python3
"""
Basic PDF image extraction example.
"""

from panparsex import parse
import os

def extract_images_from_pdf(pdf_path, output_dir="extracted_images"):
    """Extract images from a PDF document."""
    
    # Parse PDF with image extraction
    doc = parse(
        pdf_path,
        extract_images=True,
        image_output_dir=output_dir,
        min_image_size=(50, 50)  # Minimum image size threshold
    )
    
    print(f"Document: {doc.meta.title or 'Untitled'}")
    print(f"Pages: {len(doc.sections)}")
    print(f"Images found: {len(doc.images)}")
    
    # Display image information
    for i, img in enumerate(doc.images, 1):
        print(f"\nImage {i}:")
        print(f"  ID: {img.image_id}")
        print(f"  Page: {img.page_number}")
        print(f"  Dimensions: {img.dimensions}")
        print(f"  Format: {img.format}")
        print(f"  File: {img.file_path}")
        print(f"  Confidence: {img.confidence_score}")
        
        if img.associated_text:
            print(f"  Associated text: {img.associated_text[:100]}...")
    
    return doc

# Usage
if __name__ == "__main__":
    pdf_file = "sample_document.pdf"
    if os.path.exists(pdf_file):
        doc = extract_images_from_pdf(pdf_file)
    else:
        print(f"PDF file '{pdf_file}' not found")
```

### Example 2: AI Analysis with Images

```python
#!/usr/bin/env python3
"""
AI analysis of PDF documents including image context.
"""

from panparsex import parse
from panparsex.ai_processor import AIProcessor
import os
import json

def analyze_pdf_with_images(pdf_path, api_key=None):
    """Analyze a PDF document including images using AI."""
    
    # Parse PDF with image extraction
    doc = parse(
        pdf_path,
        extract_images=True,
        image_output_dir="analysis_images",
        min_image_size=(30, 30)
    )
    
    print(f"Parsed PDF: {len(doc.sections)} pages, {len(doc.images)} images")
    
    # Check for OpenAI API key
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        return doc
    
    # Initialize AI processor
    processor = AIProcessor(api_key=api_key)
    
    # Analyze document including image context
    result = processor.process_document(
        doc,
        task="Analyze this document including any images and their relationship to the text content. Identify key information, themes, and insights.",
        output_format="structured_json",
        max_tokens=2000
    )
    
    print("\n=== AI Analysis Results ===")
    print(f"Summary: {result.get('summary', 'N/A')}")
    
    if 'key_topics' in result:
        print(f"\nKey Topics: {', '.join(result['key_topics'])}")
    
    if 'important_points' in result:
        print("\nImportant Points:")
        for point in result['important_points']:
            print(f"  • {point}")
    
    if 'images_analysis' in result:
        img_analysis = result['images_analysis']
        print(f"\nImage Analysis:")
        print(f"  Total images: {img_analysis.get('total_images', 0)}")
        if 'image_contexts' in img_analysis:
            print("  Image contexts:")
            for context in img_analysis['image_contexts']:
                print(f"    - {context}")
    
    if 'insights' in result:
        print("\nInsights:")
        for insight in result['insights']:
            print(f"  💡 {insight}")
    
    # Save analysis result
    with open('pdf_analysis_result.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Analysis saved to: pdf_analysis_result.json")
    
    return doc, result

# Usage
if __name__ == "__main__":
    pdf_file = "offer_letter.pdf"
    if os.path.exists(pdf_file):
        doc, analysis = analyze_pdf_with_images(pdf_file)
    else:
        print(f"PDF file '{pdf_file}' not found")
```

### Example 3: Batch Processing with Image Extraction

```python
#!/usr/bin/env python3
"""
Batch process multiple PDFs with image extraction.
"""

from panparsex import parse
import os
import json
from pathlib import Path
from datetime import datetime

def batch_process_pdfs(input_dir, output_dir="batch_results"):
    """Process multiple PDFs and extract images from each."""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\nProcessing {i}/{len(pdf_files)}: {pdf_file.name}")
        
        try:
            # Create subdirectory for this PDF's images
            pdf_output_dir = os.path.join(output_dir, f"{pdf_file.stem}_images")
            
            # Parse PDF with image extraction
            doc = parse(
                str(pdf_file),
                extract_images=True,
                image_output_dir=pdf_output_dir,
                min_image_size=(50, 50)
            )
            
            # Collect results
            result = {
                "file": str(pdf_file),
                "title": doc.meta.title,
                "pages": len(doc.sections),
                "images": len(doc.images),
                "processed_at": datetime.now().isoformat(),
                "image_details": []
            }
            
            # Add image details
            for img in doc.images:
                result["image_details"].append({
                    "id": img.image_id,
                    "page": img.page_number,
                    "dimensions": img.dimensions,
                    "format": img.format,
                    "file_path": img.file_path,
                    "confidence": img.confidence_score
                })
            
            results.append(result)
            print(f"  ✅ Processed: {len(doc.sections)} pages, {len(doc.images)} images")
            
        except Exception as e:
            print(f"  ❌ Error processing {pdf_file.name}: {e}")
            results.append({
                "file": str(pdf_file),
                "error": str(e),
                "processed_at": datetime.now().isoformat()
            })
    
    # Save batch results
    results_file = os.path.join(output_dir, "batch_processing_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Batch processing complete!")
    print(f"Results saved to: {results_file}")
    
    # Summary
    successful = len([r for r in results if "error" not in r])
    total_images = sum([r.get("images", 0) for r in results if "error" not in r])
    
    print(f"Successfully processed: {successful}/{len(pdf_files)} files")
    print(f"Total images extracted: {total_images}")
    
    return results

# Usage
if __name__ == "__main__":
    input_directory = "pdf_documents"
    if os.path.exists(input_directory):
        results = batch_process_pdfs(input_directory)
    else:
        print(f"Input directory '{input_directory}' not found")
```

### Example 4: Advanced Image Analysis

```python
#!/usr/bin/env python3
"""
Advanced image analysis and metadata extraction.
"""

from panparsex import parse
from panparsex.types import ImageMetadata
import os
from pathlib import Path

def advanced_image_analysis(pdf_path):
    """Perform advanced analysis of extracted images."""
    
    # Parse PDF with image extraction
    doc = parse(
        pdf_path,
        extract_images=True,
        image_output_dir="advanced_images",
        min_image_size=(30, 30)
    )
    
    print(f"=== Advanced Image Analysis ===")
    print(f"Document: {doc.meta.title or 'Untitled'}")
    print(f"Total images: {len(doc.images)}")
    
    # Analyze images by page
    images_by_page = {}
    for img in doc.images:
        page = img.page_number
        if page not in images_by_page:
            images_by_page[page] = []
        images_by_page[page].append(img)
    
    print(f"\nImages by page:")
    for page, images in images_by_page.items():
        print(f"  Page {page}: {len(images)} images")
    
    # Analyze image dimensions
    dimensions_analysis = {}
    for img in doc.images:
        if img.dimensions:
            width = img.dimensions.get('width', 0)
            height = img.dimensions.get('height', 0)
            size_category = categorize_image_size(width, height)
            
            if size_category not in dimensions_analysis:
                dimensions_analysis[size_category] = []
            dimensions_analysis[size_category].append(img)
    
    print(f"\nImage size analysis:")
    for category, images in dimensions_analysis.items():
        print(f"  {category}: {len(images)} images")
        for img in images[:3]:  # Show first 3 examples
            print(f"    - {img.image_id}: {img.dimensions}")
    
    # Analyze image-text associations
    print(f"\nImage-text associations:")
    for img in doc.images:
        if img.associated_text:
            print(f"  {img.image_id}:")
            print(f"    Text: {img.associated_text[:80]}...")
        else:
            print(f"  {img.image_id}: No associated text")
    
    # File size analysis
    print(f"\nFile size analysis:")
    total_size = 0
    for img in doc.images:
        if img.file_path and os.path.exists(img.file_path):
            size = os.path.getsize(img.file_path)
            total_size += size
            print(f"  {img.image_id}: {size:,} bytes")
    
    print(f"Total extracted image size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
    
    return doc

def categorize_image_size(width, height):
    """Categorize image size."""
    area = width * height
    
    if area < 10000:  # < 100x100
        return "Small (< 100x100)"
    elif area < 100000:  # < 316x316
        return "Medium (< 316x316)"
    elif area < 1000000:  # < 1000x1000
        return "Large (< 1000x1000)"
    else:
        return "Very Large (>= 1000x1000)"

# Usage
if __name__ == "__main__":
    pdf_file = "complex_document.pdf"
    if os.path.exists(pdf_file):
        doc = advanced_image_analysis(pdf_file)
    else:
        print(f"PDF file '{pdf_file}' not found")
```

## 🔧 Configuration Options

### Image Extraction Parameters

- `extract_images`: Enable/disable image extraction (default: True for PDFs)
- `image_output_dir`: Directory to save extracted images (default: "extracted_images")
- `min_image_size`: Minimum width and height threshold (default: (50, 50))

### CLI Options

```bash
# Basic image extraction
panparsex parse document.pdf --extract-images

# Custom output directory
panparsex parse document.pdf --extract-images --image-output-dir ./my_images

# Minimum image size
panparsex parse document.pdf --extract-images --min-image-size 100 100

# Combined with AI analysis
panparsex parse document.pdf --extract-images --ai-process --ai-task "Analyze images and text"

# Pretty print output
panparsex parse document.pdf --extract-images --pretty --output results.json
```

## 📊 Performance Considerations

- **Memory Usage**: Image extraction adds memory overhead, especially for large images
- **Processing Time**: Image extraction increases parsing time, but is optimized for efficiency
- **Disk Space**: Extracted images consume disk space; consider cleanup for batch processing
- **Size Thresholds**: Use `min_image_size` to avoid extracting tiny decorative images

## 🛠️ Troubleshooting

### Common Issues

1. **No images extracted**: Check if images meet the minimum size threshold
2. **PyMuPDF import error**: Install with `pip install PyMuPDF`
3. **Permission errors**: Ensure write access to the output directory
4. **Memory issues**: Process large PDFs in smaller batches

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your parsing code here
doc = parse("document.pdf", extract_images=True)
```

## 🔄 Migration from v0.2.x

The new image extraction features are **backward compatible**. Existing code will continue to work without changes. To enable image extraction, simply add the `extract_images=True` parameter:

```python
# Old code (still works)
doc = parse("document.pdf")

# New code with image extraction
doc = parse("document.pdf", extract_images=True)
```

## 🎯 What's Next

Future releases will include:
- OCR text extraction from images
- Image classification and tagging
- Support for other document formats (DOCX, PPTX)
- Image similarity detection and deduplication
- Advanced image analysis with computer vision

## 📞 Support

- **Documentation**: [GitHub README](https://github.com/dhruvildarji/panparsex#readme)
- **Issues**: [GitHub Issues](https://github.com/dhruvildarji/panparsex/issues)
- **Email**: dhruvil.darji@gmail.com

## 🙏 Acknowledgments

Thanks to the PyMuPDF and Pillow communities for providing excellent image processing libraries that made this feature possible.

---

**Download panparsex v0.3.0 now and start extracting images from your PDFs!** 🚀

```bash
pip install panparsex==0.3.0
```
