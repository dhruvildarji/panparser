#!/usr/bin/env python3
"""
Folder Parsing Example for panparsex

This example demonstrates how to use panparsex to parse entire folders
with different file types, including recursive scanning and AI processing.
"""

import os
import json
from pathlib import Path
from panparsex import parse_folder, parse_folder_unified
from panparsex.ai_processor import AIProcessor

def main():
    # Example folder path (replace with your folder)
    folder_path = "examples/sample_files"  # Using the existing sample files
    
    print("🔄 panparsex Folder Parsing Example")
    print("=" * 50)
    
    # Check if folder exists
    if not Path(folder_path).exists():
        print(f"❌ Folder not found: {folder_path}")
        print("Please update the folder_path variable to point to a valid folder.")
        return
    
    print(f"📁 Parsing folder: {folder_path}")
    print()
    
    # Example 1: Parse folder and get list of documents
    print("1️⃣ Parsing folder (list of documents):")
    print("-" * 40)
    
    documents = parse_folder(
        folder_path,
        recursive=True,  # Scan subdirectories
        show_progress=True,
        exclude_patterns=['*.tmp', '*.log', '.git']  # Exclude certain patterns
    )
    
    print(f"✅ Found {len(documents)} documents")
    print()
    
    # Display summary of each document
    for i, doc in enumerate(documents, 1):
        print(f"   Document {i}: {Path(doc.meta.source).name}")
        print(f"     Type: {doc.meta.content_type}")
        print(f"     Sections: {len(doc.sections)}")
        if hasattr(doc, 'images') and doc.images:
            print(f"     Images: {len(doc.images)}")
        print()
    
    # Example 2: Parse folder and combine into single document
    print("2️⃣ Parsing folder (unified document):")
    print("-" * 40)
    
    unified_doc = parse_folder_unified(
        folder_path,
        recursive=True,
        show_progress=True,
        exclude_patterns=['*.tmp', '*.log', '.git']
    )
    
    print(f"✅ Combined document created")
    print(f"   Total sections: {len(unified_doc.sections)}")
    if hasattr(unified_doc, 'images') and unified_doc.images:
        print(f"   Total images: {len(unified_doc.images)}")
    print()
    
    # Example 3: Save results to files
    print("3️⃣ Saving results:")
    print("-" * 40)
    
    # Save individual documents
    with open("folder_parsing_results.json", "w", encoding="utf-8") as f:
        json.dump([doc.model_dump() for doc in documents], f, indent=2, ensure_ascii=False)
    print("✅ Individual documents saved to: folder_parsing_results.json")
    
    # Save unified document
    with open("folder_unified_result.json", "w", encoding="utf-8") as f:
        json.dump(unified_doc.model_dump(), f, indent=2, ensure_ascii=False)
    print("✅ Unified document saved to: folder_unified_result.json")
    print()
    
    # Example 4: AI Processing (if API key is available)
    print("4️⃣ AI Processing (optional):")
    print("-" * 40)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            processor = AIProcessor(api_key=api_key)
            
            print("🤖 Processing unified document with AI...")
            result = processor.process_document(
                unified_doc,
                task="Analyze the content and provide a comprehensive summary",
                output_format="structured_json",
                max_tokens=2000
            )
            
            # Save AI result
            with open("folder_ai_analysis.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("✅ AI analysis saved to: folder_ai_analysis.json")
            
        except Exception as e:
            print(f"❌ AI processing failed: {e}")
    else:
        print("⚠️  No OpenAI API key found. Set OPENAI_API_KEY environment variable for AI processing.")
    
    print()
    print("🎉 Folder parsing example completed!")
    print()
    print("📋 Generated files:")
    print("   - folder_parsing_results.json (individual documents)")
    print("   - folder_unified_result.json (combined document)")
    if api_key:
        print("   - folder_ai_analysis.json (AI analysis)")

if __name__ == "__main__":
    main()
