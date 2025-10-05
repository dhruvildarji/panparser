#!/usr/bin/env python3
"""
panparsex v0.5.0 - Batch PDF Processing with Image Extraction

This example demonstrates batch processing of multiple PDF files with image extraction,
showing how to efficiently process large collections of documents.

Requirements:
- panparsex>=0.5.0
- PyMuPDF (automatically installed with panparsex)
- Pillow (automatically installed with panparsex)

Usage:
    python batch_pdf_processing_example.py <input_directory>
    
Example:
    python batch_pdf_processing_example.py ./pdf_documents
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from panparsex import parse

def main():
    """Main function for batch PDF processing with image extraction."""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python batch_pdf_processing_example.py <input_directory>")
        print("Example: python batch_pdf_processing_example.py ./pdf_documents")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found")
        sys.exit(1)
    
    print("=" * 70)
    print("panparsex v0.5.0 - Batch PDF Processing with Image Extraction")
    print("=" * 70)
    print(f"Input Directory: {input_dir}")
    print()
    
    # Find all PDF files
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in '{input_dir}'")
        sys.exit(1)
    
    print(f"📁 Found {len(pdf_files)} PDF files to process")
    print()
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"batch_results_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}")
    print()
    
    # Process each PDF
    results = []
    successful = 0
    failed = 0
    total_images = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"🔄 Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        
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
                "status": "success",
                "image_details": []
            }
            
            # Add image details
            for img in doc.images:
                img_detail = {
                    "id": img.image_id,
                    "page": img.page_number,
                    "dimensions": img.dimensions,
                    "format": img.format,
                    "file_path": img.file_path,
                    "confidence": img.confidence_score,
                    "extracted_at": img.extracted_at.isoformat() if img.extracted_at else None
                }
                
                if img.associated_text:
                    img_detail["associated_text"] = img.associated_text[:200]  # Truncate for JSON
                
                result["image_details"].append(img_detail)
            
            results.append(result)
            successful += 1
            total_images += len(doc.images)
            
            print(f"   ✅ Success: {len(doc.sections)} pages, {len(doc.images)} images")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
            results.append({
                "file": str(pdf_file),
                "error": str(e),
                "processed_at": datetime.now().isoformat(),
                "status": "failed"
            })
            
            failed += 1
    
    print()
    print("=" * 70)
    print("📊 Batch Processing Results")
    print("=" * 70)
    
    # Save detailed results
    results_file = os.path.join(output_dir, "batch_processing_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Summary statistics
    print(f"📁 Total files processed: {len(pdf_files)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"🖼️  Total images extracted: {total_images}")
    print(f"📄 Results saved to: {results_file}")
    print()
    
    # Detailed breakdown
    if successful > 0:
        print("📋 Successful Processing Details:")
        for result in results:
            if result["status"] == "success":
                print(f"   📄 {Path(result['file']).name}:")
                print(f"      Pages: {result['pages']}")
                print(f"      Images: {result['images']}")
                if result['title']:
                    print(f"      Title: {result['title']}")
                print()
    
    # Error details
    if failed > 0:
        print("❌ Failed Processing Details:")
        for result in results:
            if result["status"] == "failed":
                print(f"   📄 {Path(result['file']).name}: {result['error']}")
        print()
    
    # Image statistics
    if total_images > 0:
        print("🖼️  Image Statistics:")
        
        # Count images by format
        format_counts = {}
        page_counts = {}
        
        for result in results:
            if result["status"] == "success":
                for img in result["image_details"]:
                    fmt = img.get("format", "unknown")
                    format_counts[fmt] = format_counts.get(fmt, 0) + 1
                    
                    page = img.get("page", 0)
                    page_counts[page] = page_counts.get(page, 0) + 1
        
        print(f"   Total images: {total_images}")
        print(f"   Formats: {format_counts}")
        print(f"   Images per page: {dict(sorted(page_counts.items()))}")
        print()
    
    # File size analysis
    total_size = 0
    image_files = 0
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                total_size += size
                image_files += 1
    
    if image_files > 0:
        print(f"💾 Storage Analysis:")
        print(f"   Image files created: {image_files}")
        print(f"   Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        print(f"   Average size: {total_size/image_files:,} bytes")
        print()
    
    print("🎉 Batch processing completed successfully!")
    print(f"📁 All results saved in: {output_dir}")

if __name__ == "__main__":
    main()
