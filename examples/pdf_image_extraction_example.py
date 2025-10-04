#!/usr/bin/env python3
"""
panparsex v0.3.0 - PDF Image Extraction Example

This example demonstrates the new PDF image extraction capabilities in panparsex v0.3.0.
It shows how to extract images from PDF documents and analyze their metadata.

Requirements:
- panparsex>=0.3.0
- PyMuPDF (automatically installed with panparsex)
- Pillow (automatically installed with panparsex)

Usage:
    python pdf_image_extraction_example.py <pdf_file>
    
Example:
    python pdf_image_extraction_example.py document.pdf
"""

import sys
import os
from pathlib import Path
from panparsex import parse
from panparsex.types import ImageMetadata

def main():
    """Main function demonstrating PDF image extraction."""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python pdf_image_extraction_example.py <pdf_file>")
        print("Example: python pdf_image_extraction_example.py document.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(pdf_file):
        print(f"Error: File '{pdf_file}' not found")
        sys.exit(1)
    
    print("=" * 60)
    print("panparsex v0.3.0 - PDF Image Extraction Example")
    print("=" * 60)
    print(f"Processing: {pdf_file}")
    print()
    
    try:
        # Parse PDF with image extraction enabled
        print("🔍 Parsing PDF with image extraction...")
        doc = parse(
            pdf_file,
            extract_images=True,
            image_output_dir="extracted_images",
            min_image_size=(50, 50)  # Minimum image size threshold
        )
        
        print("✅ PDF parsing completed successfully!")
        print()
        
        # Display document information
        print("📄 Document Information:")
        print(f"   Title: {doc.meta.title or 'No title'}")
        print(f"   Pages: {len(doc.sections)}")
        print(f"   Content Type: {doc.meta.content_type}")
        print(f"   Images Found: {len(doc.images)}")
        print()
        
        # Display image details
        if doc.images:
            print("🖼️  Extracted Images:")
            for i, img in enumerate(doc.images, 1):
                print(f"   Image {i}:")
                print(f"     ID: {img.image_id}")
                print(f"     Page: {img.page_number}")
                print(f"     Dimensions: {img.dimensions}")
                print(f"     Format: {img.format}")
                print(f"     File: {img.file_path}")
                print(f"     Confidence: {img.confidence_score}")
                print(f"     Extracted: {img.extracted_at}")
                
                if img.associated_text:
                    print(f"     Associated Text: {img.associated_text[:100]}...")
                else:
                    print(f"     Associated Text: None")
                print()
        else:
            print("ℹ️  No images found in the PDF")
            print()
        
        # Display section information
        print("📑 Document Sections:")
        for i, section in enumerate(doc.sections, 1):
            print(f"   Section {i}: {section.heading}")
            print(f"     Text Chunks: {len(section.chunks)}")
            print(f"     Images: {len(section.images)}")
            
            if section.chunks:
                content_preview = section.chunks[0].text[:100]
                print(f"     Content Preview: {content_preview}...")
            print()
        
        # File size analysis
        if doc.images:
            print("💾 File Size Analysis:")
            total_size = 0
            for img in doc.images:
                if img.file_path and os.path.exists(img.file_path):
                    size = os.path.getsize(img.file_path)
                    total_size += size
                    print(f"   {img.image_id}: {size:,} bytes")
            
            print(f"   Total Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
            print()
        
        # Summary
        print("📊 Summary:")
        print(f"   ✅ Successfully processed PDF: {pdf_file}")
        print(f"   📄 Pages processed: {len(doc.sections)}")
        print(f"   🖼️  Images extracted: {len(doc.images)}")
        print(f"   📁 Images saved to: extracted_images/")
        
        if doc.images:
            print(f"   🎯 Ready for AI analysis with image context!")
        
        print()
        print("🎉 PDF image extraction completed successfully!")
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()