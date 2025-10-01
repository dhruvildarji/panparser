#!/usr/bin/env python3
"""
Example script demonstrating AI-powered processing with panparsex.
This script shows how to parse documents and then use OpenAI GPT to analyze,
restructure, and filter the content.
"""

import os
import json
from panparsex import parse
from panparsex.ai_processor import AIProcessor

def main():
    # Set your OpenAI API key
    # You can also set it as an environment variable: export OPENAI_API_KEY="your-key-here"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable or modify this script")
        return
    
    # Example 1: Parse a PDF and process with AI
    print("=== Example 1: PDF Processing ===")
    try:
        # Parse a PDF (replace with your PDF file)
        pdf_file = "sample.pdf"  # Replace with actual PDF file
        if os.path.exists(pdf_file):
            doc = parse(pdf_file)
            print(f"Parsed PDF: {doc.meta.title or 'Untitled'}")
            
            # Process with AI
            processor = AIProcessor(api_key=api_key, model="gpt-4o-mini")
            result = processor.process_and_save(
                doc,
                "pdf_analysis.json",
                task="Extract key insights, summarize main points, and identify important topics",
                output_format="structured_json"
            )
            print("PDF analysis saved to: pdf_analysis.json")
        else:
            print(f"PDF file {pdf_file} not found, skipping...")
    except Exception as e:
        print(f"PDF processing failed: {e}")
    
    # Example 2: Parse a website and process with AI
    print("\n=== Example 2: Website Processing ===")
    try:
        # Parse a website
        url = "https://pypi.org/project/panparsex/"
        doc = parse(url, recursive=False, max_links=5)
        print(f"Parsed website: {doc.meta.title or 'Untitled'}")
        
        # Process with AI for content analysis
        processor = AIProcessor(api_key=api_key, model="gpt-4o-mini")
        result = processor.process_and_save(
            doc,
            "website_analysis.md",
            task="Analyze the website content, extract key information, and create a structured summary",
            output_format="markdown"
        )
        print("Website analysis saved to: website_analysis.md")
    except Exception as e:
        print(f"Website processing failed: {e}")
    
    # Example 3: Parse a text file and process with AI
    print("\n=== Example 3: Text File Processing ===")
    try:
        # Create a sample text file
        sample_text = """
        Project Report: Q4 2024
        
        Executive Summary:
        This quarter showed significant growth in user engagement and revenue. 
        Key metrics improved across all departments.
        
        Key Achievements:
        - User base increased by 25%
        - Revenue grew by 30%
        - Customer satisfaction improved to 4.8/5
        
        Challenges:
        - Server capacity needs expansion
        - Customer support response time increased
        - Some features delayed due to technical issues
        
        Recommendations:
        - Invest in infrastructure scaling
        - Hire additional support staff
        - Implement better project management tools
        """
        
        with open("sample_report.txt", "w") as f:
            f.write(sample_text)
        
        # Parse the text file
        doc = parse("sample_report.txt")
        print("Parsed text file: sample_report.txt")
        
        # Process with AI for business analysis
        processor = AIProcessor(api_key=api_key, model="gpt-4o-mini")
        result = processor.process_and_save(
            doc,
            "business_analysis.json",
            task="Analyze this business report, extract key metrics, identify challenges, and provide actionable recommendations",
            output_format="structured_json"
        )
        print("Business analysis saved to: business_analysis.json")
        
        # Clean up
        os.remove("sample_report.txt")
        
    except Exception as e:
        print(f"Text file processing failed: {e}")
    
    # Example 4: Custom AI task
    print("\n=== Example 4: Custom AI Task ===")
    try:
        # Create a sample document
        sample_doc = """
        Technical Documentation: API Integration Guide
        
        Overview:
        This guide explains how to integrate with our REST API for data processing.
        
        Authentication:
        Use API keys for authentication. Include the key in the Authorization header.
        
        Endpoints:
        - GET /api/data - Retrieve data
        - POST /api/process - Process data
        - PUT /api/update - Update records
        
        Rate Limits:
        - 100 requests per minute
        - 1000 requests per hour
        
        Error Codes:
        - 400: Bad Request
        - 401: Unauthorized
        - 429: Rate Limit Exceeded
        - 500: Internal Server Error
        """
        
        with open("api_docs.txt", "w") as f:
            f.write(sample_doc)
        
        # Parse the document
        doc = parse("api_docs.txt")
        print("Parsed API documentation")
        
        # Process with AI for technical analysis
        processor = AIProcessor(api_key=api_key, model="gpt-4o-mini")
        result = processor.process_and_save(
            doc,
            "api_analysis.json",
            task="Convert this API documentation into a structured format with clear sections for authentication, endpoints, rate limits, and error handling. Also provide implementation examples and best practices.",
            output_format="structured_json"
        )
        print("API analysis saved to: api_analysis.json")
        
        # Clean up
        os.remove("api_docs.txt")
        
    except Exception as e:
        print(f"Custom task processing failed: {e}")
    
    print("\n=== AI Processing Complete ===")
    print("Check the generated files for AI-processed results:")
    print("- pdf_analysis.json (if PDF was processed)")
    print("- website_analysis.md")
    print("- business_analysis.json")
    print("- api_analysis.json")

if __name__ == "__main__":
    main()
