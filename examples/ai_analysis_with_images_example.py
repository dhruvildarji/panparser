#!/usr/bin/env python3
"""
panparsex v0.3.0 - AI Analysis with Image Context Example

This example demonstrates how to use panparsex v0.3.0 with AI analysis
that includes image metadata and context for comprehensive document understanding.

Requirements:
- panparsex>=0.3.0
- openai>=1.0.0
- PyMuPDF (automatically installed with panparsex)
- Pillow (automatically installed with panparsex)

Environment Variables:
- OPENAI_API_KEY: Your OpenAI API key

Usage:
    python ai_analysis_with_images_example.py <pdf_file>
    
Example:
    python ai_analysis_with_images_example.py offer_letter.pdf
"""

import sys
import os
import json
from datetime import datetime
from panparsex import parse
from panparsex.ai_processor import AIProcessor

def main():
    """Main function demonstrating AI analysis with image context."""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python ai_analysis_with_images_example.py <pdf_file>")
        print("Example: python ai_analysis_with_images_example.py offer_letter.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(pdf_file):
        print(f"Error: File '{pdf_file}' not found")
        sys.exit(1)
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    print("=" * 70)
    print("panparsex v0.3.0 - AI Analysis with Image Context Example")
    print("=" * 70)
    print(f"Processing: {pdf_file}")
    print(f"AI Model: GPT-4o-mini")
    print()
    
    try:
        # Step 1: Parse PDF with image extraction
        print("🔍 Step 1: Parsing PDF with image extraction...")
        doc = parse(
            pdf_file,
            extract_images=True,
            image_output_dir="ai_analysis_images",
            min_image_size=(30, 30)  # Lower threshold for better coverage
        )
        
        print("✅ PDF parsing completed!")
        print(f"   Pages: {len(doc.sections)}")
        print(f"   Images: {len(doc.images)}")
        print()
        
        # Step 2: Initialize AI processor
        print("🤖 Step 2: Initializing AI processor...")
        processor = AIProcessor(api_key=api_key, model="gpt-4o-mini")
        print("✅ AI processor ready!")
        print()
        
        # Step 3: Perform AI analysis with image context
        print("🧠 Step 3: Performing AI analysis with image context...")
        
        analysis_task = """
        Analyze this document including any images and their relationship to the text content. 
        Focus on:
        1. Key information and important details
        2. The role and context of any images
        3. How images relate to the text content
        4. Overall document structure and purpose
        5. Any insights about the document's content and context
        """
        
        result = processor.process_document(
            doc,
            task=analysis_task,
            output_format="structured_json",
            max_tokens=2000,
            temperature=0.3
        )
        
        print("✅ AI analysis completed!")
        print()
        
        # Step 4: Display results
        print("📊 Analysis Results:")
        print("-" * 50)
        
        # Summary
        if 'summary' in result:
            print(f"📝 Summary:")
            print(f"   {result['summary']}")
            print()
        
        # Key topics
        if 'key_topics' in result:
            print(f"🏷️  Key Topics:")
            for topic in result['key_topics']:
                print(f"   • {topic}")
            print()
        
        # Important points
        if 'important_points' in result:
            print(f"⭐ Important Points:")
            for point in result['important_points']:
                print(f"   • {point}")
            print()
        
        # Image analysis
        if 'images_analysis' in result:
            img_analysis = result['images_analysis']
            print(f"🖼️  Image Analysis:")
            print(f"   Total Images: {img_analysis.get('total_images', 0)}")
            
            if 'images_by_page' in img_analysis:
                print(f"   Images by Page: {img_analysis['images_by_page']}")
            
            if 'image_contexts' in img_analysis:
                print(f"   Image Contexts:")
                for context in img_analysis['image_contexts']:
                    print(f"     • {context}")
            print()
        
        # Structured content
        if 'structured_content' in result:
            print(f"📋 Structured Content:")
            for section, content in result['structured_content'].items():
                print(f"   {section}: {content[:100]}...")
            print()
        
        # Insights
        if 'insights' in result:
            print(f"💡 Insights:")
            for insight in result['insights']:
                print(f"   • {insight}")
            print()
        
        # Recommendations
        if 'recommendations' in result:
            print(f"🎯 Recommendations:")
            for rec in result['recommendations']:
                print(f"   • {rec}")
            print()
        
        # Step 5: Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"ai_analysis_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {results_file}")
        print()
        
        # Step 6: Summary
        print("📈 Analysis Summary:")
        print(f"   ✅ Document processed: {pdf_file}")
        print(f"   📄 Pages analyzed: {len(doc.sections)}")
        print(f"   🖼️  Images included: {len(doc.images)}")
        print(f"   🤖 AI model used: GPT-4o-mini")
        print(f"   📁 Images saved to: ai_analysis_images/")
        print(f"   📄 Results saved to: {results_file}")
        
        if doc.images:
            print(f"   🎯 Image context successfully integrated into analysis!")
        
        print()
        print("🎉 AI analysis with image context completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
