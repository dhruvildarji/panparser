#!/usr/bin/env python3
"""
Advanced usage examples for panparsex.

This script demonstrates advanced features like web scraping, custom parsers, and batch processing.
"""

import os
import tempfile
from pathlib import Path
from panparsex import parse, register_parser, ParserProtocol, get_registry
from panparsex.types import UnifiedDocument, Metadata, Section, Chunk


def example_web_scraping():
    """Example: Web scraping with panparsex."""
    print("=== Web Scraping Example ===")
    
    try:
        # Parse a simple website (using a known stable URL)
        print("Parsing a simple website...")
        doc = parse("https://httpbin.org/html")
        
        print(f"URL: {doc.meta.source}")
        print(f"Title: {doc.meta.title}")
        print(f"Sections: {len(doc.sections)}")
        
        for i, section in enumerate(doc.sections):
            print(f"Section {i+1}: {section.heading}")
            if section.chunks:
                print(f"  Content: {section.chunks[0].text[:200]}...")
        
        # Show crawl statistics
        if "crawl_stats" in doc.meta.extra:
            stats = doc.meta.extra["crawl_stats"]
            print(f"Crawl stats: {stats}")
        
    except Exception as e:
        print(f"Web scraping example failed (this is expected if no internet connection): {e}")


def example_custom_parser():
    """Example: Create and register a custom parser."""
    print("\n=== Custom Parser Example ===")
    
    class CustomParser(ParserProtocol):
        name = "custom_example"
        content_types = ("application/custom",)
        extensions = (".custom",)
        
        def can_parse(self, meta: Metadata) -> bool:
            return meta.content_type == "application/custom" or (meta.path or "").endswith(".custom")
        
        def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
            doc = UnifiedDocument(meta=meta, sections=[])
            
            try:
                with open(target, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Simple parsing: split by lines and create sections
                lines = content.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        section = Section(
                            heading=f"Line {i+1}",
                            chunks=[Chunk(text=line.strip(), order=i)],
                            meta={"line_number": i+1, "type": "custom"}
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
    
    # Register the custom parser
    register_parser(CustomParser())
    
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.custom', delete=False) as f:
        f.write("Line 1: Hello, custom parser!\nLine 2: This is a test.\nLine 3: Custom parsing works!")
        temp_file = f.name
    
    try:
        # Parse with custom parser
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Parser used: {doc.meta.extra.get('parser', 'unknown')}")
        print(f"Sections: {len(doc.sections)}")
        
        for section in doc.sections:
            print(f"  {section.heading}: {section.chunks[0].text}")
        
    finally:
        os.unlink(temp_file)


def example_batch_directory_processing():
    """Example: Process an entire directory of files."""
    print("\n=== Batch Directory Processing ===")
    
    # Create a temporary directory with various file types
    temp_dir = tempfile.mkdtemp()
    
    files_to_create = {
        "document.txt": "This is a text document.",
        "data.json": '{"name": "test", "value": 123}',
        "config.yaml": "name: test\nvalue: 123",
        "page.html": "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>",
        "table.csv": "name,value\ntest,123",
    }
    
    try:
        # Create files
        for filename, content in files_to_create.items():
            file_path = Path(temp_dir) / filename
            file_path.write_text(content)
        
        # Process all files in the directory
        results = []
        for file_path in Path(temp_dir).glob("*"):
            if file_path.is_file():
                try:
                    doc = parse(str(file_path))
                    results.append({
                        "file": file_path.name,
                        "content_type": doc.meta.content_type,
                        "sections": len(doc.sections),
                        "content_length": sum(len(chunk.text) for section in doc.sections for chunk in section.chunks),
                        "title": doc.meta.title
                    })
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
        
        # Display results
        print(f"Processed {len(results)} files from {temp_dir}:")
        for result in results:
            print(f"  {result['file']}: {result['content_type']}, {result['sections']} sections, {result['content_length']} chars")
            if result['title']:
                print(f"    Title: {result['title']}")
        
    finally:
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)


def example_content_analysis():
    """Example: Analyze parsed content."""
    print("\n=== Content Analysis Example ===")
    
    # Create a sample document
    sample_content = """
    # Project Report
    
    This is a comprehensive report about our project.
    
    ## Executive Summary
    
    The project has been successful in achieving its goals.
    
    ## Key Findings
    
    1. Performance improved by 50%
    2. User satisfaction increased
    3. Cost reduced by 30%
    
    ## Recommendations
    
    - Continue current approach
    - Expand to new markets
    - Invest in technology
    
    ## Conclusion
    
    The project is ready for the next phase.
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_content)
        temp_file = f.name
    
    try:
        # Parse the document
        doc = parse(temp_file)
        
        # Analyze content
        total_chars = sum(len(chunk.text) for section in doc.sections for chunk in section.chunks)
        total_words = sum(len(chunk.text.split()) for section in doc.sections for chunk in section.chunks)
        
        print(f"Document: {doc.meta.source}")
        print(f"Total sections: {len(doc.sections)}")
        print(f"Total characters: {total_chars}")
        print(f"Total words: {total_words}")
        
        # Analyze sections
        print("\nSection analysis:")
        for i, section in enumerate(doc.sections):
            section_chars = sum(len(chunk.text) for chunk in section.chunks)
            section_words = sum(len(chunk.text.split()) for chunk in section.chunks)
            print(f"  Section {i+1}: '{section.heading}' - {section_chars} chars, {section_words} words")
        
        # Find specific content
        print("\nContent search:")
        search_terms = ["project", "success", "performance"]
        for term in search_terms:
            found = False
            for section in doc.sections:
                for chunk in section.chunks:
                    if term.lower() in chunk.text.lower():
                        print(f"  Found '{term}' in section '{section.heading}'")
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"  '{term}' not found")
        
    finally:
        os.unlink(temp_file)


def example_error_handling():
    """Example: Error handling and recovery."""
    print("\n=== Error Handling Example ===")
    
    # Test with various error conditions
    test_cases = [
        ("nonexistent.txt", "Non-existent file"),
        ("", "Empty filename"),
        ("invalid.json", "Invalid JSON content"),
    ]
    
    for filename, description in test_cases:
        print(f"\nTesting: {description}")
        
        if filename == "invalid.json":
            # Create invalid JSON file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write('{"invalid": json content}')
                test_file = f.name
        else:
            test_file = filename
        
        try:
            doc = parse(test_file)
            print(f"  Result: Successfully parsed {len(doc.sections)} sections")
            
            # Check for error sections
            error_sections = [s for s in doc.sections if s.meta.get("error")]
            if error_sections:
                print(f"  Error sections: {len(error_sections)}")
                for section in error_sections:
                    print(f"    Error: {section.chunks[0].text[:100]}...")
            
        except Exception as e:
            print(f"  Exception: {e}")
        
        finally:
            if filename == "invalid.json" and os.path.exists(test_file):
                os.unlink(test_file)


def example_performance_testing():
    """Example: Performance testing with large files."""
    print("\n=== Performance Testing ===")
    
    import time
    
    # Create a large text file
    large_content = "\n".join([f"Line {i}: This is line number {i} with some content." for i in range(1000)])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(large_content)
        temp_file = f.name
    
    try:
        # Measure parsing time
        start_time = time.time()
        doc = parse(temp_file)
        end_time = time.time()
        
        parsing_time = end_time - start_time
        total_chars = sum(len(chunk.text) for section in doc.sections for chunk in section.chunks)
        
        print(f"File: {temp_file}")
        print(f"Size: {len(large_content)} characters")
        print(f"Parsing time: {parsing_time:.3f} seconds")
        print(f"Parsed content: {total_chars} characters")
        print(f"Throughput: {total_chars / parsing_time:.0f} chars/second")
        print(f"Sections: {len(doc.sections)}")
        
    finally:
        os.unlink(temp_file)


def main():
    """Run all advanced examples."""
    print("panparsex Advanced Usage Examples")
    print("=" * 50)
    
    try:
        example_web_scraping()
        example_custom_parser()
        example_batch_directory_processing()
        example_content_analysis()
        example_error_handling()
        example_performance_testing()
        
        print("\n" + "=" * 50)
        print("All advanced examples completed successfully!")
        
    except Exception as e:
        print(f"Error running advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
