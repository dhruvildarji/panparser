#!/usr/bin/env python3
"""
Basic usage examples for panparsex.

This script demonstrates how to use panparsex to parse various file types.
"""

import os
import tempfile
from pathlib import Path
from panparsex import parse, get_registry


def example_parse_text():
    """Example: Parse a text file."""
    print("=== Text File Parsing ===")
    
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello, world!\nThis is a sample text file.\nIt contains multiple lines.")
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Content Type: {doc.meta.content_type}")
        print(f"Sections: {len(doc.sections)}")
        
        for i, section in enumerate(doc.sections):
            print(f"Section {i+1}:")
            for j, chunk in enumerate(section.chunks):
                print(f"  Chunk {j+1}: {chunk.text[:50]}...")
        
    finally:
        os.unlink(temp_file)


def example_parse_json():
    """Example: Parse a JSON file."""
    print("\n=== JSON File Parsing ===")
    
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"name": "panparsex", "version": "0.1.0", "features": ["universal", "extensible"]}')
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Content Type: {doc.meta.content_type}")
        print(f"Content: {doc.sections[0].chunks[0].text}")
        
    finally:
        os.unlink(temp_file)


def example_parse_html():
    """Example: Parse an HTML file."""
    print("\n=== HTML File Parsing ===")
    
    # Create a temporary HTML file
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page</title>
        <meta name="description" content="A sample HTML page">
    </head>
    <body>
        <h1>Welcome to panparsex</h1>
        <p>This is a sample paragraph.</p>
        <h2>Features</h2>
        <ul>
            <li>Universal parsing</li>
            <li>Plugin architecture</li>
            <li>Web scraping</li>
        </ul>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Title: {doc.meta.title}")
        print(f"Sections: {len(doc.sections)}")
        
        for i, section in enumerate(doc.sections):
            print(f"Section {i+1}: {section.heading}")
            for chunk in section.chunks:
                print(f"  Content: {chunk.text[:100]}...")
        
        # Show extracted metadata
        if "meta_tags" in doc.meta.extra:
            print("Meta tags:")
            for key, value in doc.meta.extra["meta_tags"].items():
                print(f"  {key}: {value}")
        
    finally:
        os.unlink(temp_file)


def example_parse_csv():
    """Example: Parse a CSV file."""
    print("\n=== CSV File Parsing ===")
    
    # Create a temporary CSV file
    csv_content = """name,age,city
John,30,New York
Jane,25,Los Angeles
Bob,35,Chicago"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Sections: {len(doc.sections)}")
        
        for i, section in enumerate(doc.sections):
            print(f"Section {i+1}: {section.heading}")
            print(f"  Content: {section.chunks[0].text}")
        
        # Show CSV-specific data
        if "csv_data" in doc.meta.extra:
            csv_data = doc.meta.extra["csv_data"]
            print(f"Headers: {csv_data['headers']}")
            print(f"Rows: {len(csv_data['rows'])}")
            print(f"Delimiter: {csv_data['delimiter']}")
        
    finally:
        os.unlink(temp_file)


def example_parse_yaml():
    """Example: Parse a YAML file."""
    print("\n=== YAML File Parsing ===")
    
    # Create a temporary YAML file
    yaml_content = """
name: panparsex
version: 0.1.0
description: Universal parser
features:
  - universal
  - extensible
  - fast
author:
  name: Dhruvil Darji
  email: dhruvil.darji@gmail.com
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Content: {doc.sections[0].chunks[0].text}")
        
    finally:
        os.unlink(temp_file)


def example_parse_xml():
    """Example: Parse an XML file."""
    print("\n=== XML File Parsing ===")
    
    # Create a temporary XML file
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <name>panparsex</name>
    <version>0.1.0</version>
    <description>Universal parser</description>
    <features>
        <feature>universal</feature>
        <feature>extensible</feature>
    </features>
</project>"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(xml_content)
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Content: {doc.sections[0].chunks[0].text}")
        
    finally:
        os.unlink(temp_file)


def example_parse_markdown():
    """Example: Parse a Markdown file."""
    print("\n=== Markdown File Parsing ===")
    
    # Create a temporary Markdown file
    md_content = """# panparsex

Universal parser for files and websites.

## Features

- Plugin architecture
- 13+ file type support
- Web scraping
- Unified schema

## Installation

```bash
pip install panparsex
```

## Usage

```python
from panparsex import parse
doc = parse("document.pdf")
```
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        temp_file = f.name
    
    try:
        # Parse the file
        doc = parse(temp_file)
        
        print(f"File: {doc.meta.source}")
        print(f"Sections: {len(doc.sections)}")
        
        for i, section in enumerate(doc.sections):
            print(f"Section {i+1}: {section.heading}")
            for chunk in section.chunks:
                print(f"  Content: {chunk.text[:100]}...")
        
    finally:
        os.unlink(temp_file)


def example_show_registry():
    """Example: Show registered parsers."""
    print("\n=== Registered Parsers ===")
    
    registry = get_registry()
    print(f"Total parsers: {len(registry.parsers)}")
    
    for parser in registry.parsers:
        print(f"Parser: {parser.name}")
        print(f"  Content types: {list(parser.content_types)}")
        print(f"  Extensions: {list(parser.extensions)}")
        print()


def example_batch_processing():
    """Example: Batch process multiple files."""
    print("\n=== Batch Processing ===")
    
    # Create multiple sample files
    files = {
        "sample.txt": "This is a text file.",
        "sample.json": '{"message": "Hello, JSON!"}',
        "sample.yaml": "message: Hello, YAML!",
    }
    
    temp_files = []
    try:
        # Create temporary files
        for filename, content in files.items():
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{filename.split(".")[-1]}', delete=False) as f:
                f.write(content)
                temp_files.append(f.name)
        
        # Process each file
        results = []
        for temp_file in temp_files:
            try:
                doc = parse(temp_file)
                results.append({
                    "file": Path(temp_file).name,
                    "sections": len(doc.sections),
                    "content_length": sum(len(chunk.text) for section in doc.sections for chunk in section.chunks)
                })
            except Exception as e:
                print(f"Error processing {temp_file}: {e}")
        
        # Show results
        print("Batch processing results:")
        for result in results:
            print(f"  {result['file']}: {result['sections']} sections, {result['content_length']} chars")
        
    finally:
        # Clean up
        for temp_file in temp_files:
            os.unlink(temp_file)


def main():
    """Run all examples."""
    print("panparsex Basic Usage Examples")
    print("=" * 50)
    
    try:
        example_parse_text()
        example_parse_json()
        example_parse_html()
        example_parse_csv()
        example_parse_yaml()
        example_parse_xml()
        example_parse_markdown()
        example_show_registry()
        example_batch_processing()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
