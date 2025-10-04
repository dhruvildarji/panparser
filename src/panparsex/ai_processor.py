"""
AI-powered post-processing module for panparsex.
Uses OpenAI GPT to analyze, restructure, and filter parsed content.
"""

from __future__ import annotations
import json
import os
from typing import Dict, Any, Optional, List
from .types import UnifiedDocument, Section, Chunk


class AIProcessor:
    """AI-powered processor for analyzing and restructuring parsed content."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the AI processor.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from OPENAI_API_KEY env var.
            model: OpenAI model to use for processing.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
    
    def process_document(
        self, 
        doc: UnifiedDocument, 
        task: str = "analyze and restructure",
        output_format: str = "structured_json",
        max_tokens: int = 4000,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Process a parsed document using OpenAI GPT.
        
        Args:
            doc: The parsed document to process
            task: The task description for the AI
            output_format: Desired output format (structured_json, markdown, summary, etc.)
            max_tokens: Maximum tokens for the response
            temperature: Temperature for the AI response
            
        Returns:
            Dictionary containing the AI-processed result
        """
        try:
            import openai
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        # Prepare the content for AI processing
        content = self._prepare_content_for_ai(doc)
        
        # Create the prompt
        system_prompt = self._create_system_prompt(task, output_format)
        user_prompt = f"Please process the following content:\n\n{content}"
        
        # Call OpenAI API
        client = openai.OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        result = response.choices[0].message.content
        
        # Parse the result based on output format
        if output_format == "structured_json":
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"raw_response": result, "format": "text"}
        else:
            return {"content": result, "format": output_format}
    
    def _prepare_content_for_ai(self, doc: UnifiedDocument) -> str:
        """Prepare the document content for AI processing."""
        content_parts = []
        
        # Add metadata
        if doc.meta.title:
            content_parts.append(f"Title: {doc.meta.title}")
        if doc.meta.source:
            content_parts.append(f"Source: {doc.meta.source}")
        if doc.meta.content_type:
            content_parts.append(f"Content Type: {doc.meta.content_type}")
        
        # Add image summary if images are present
        if doc.images:
            content_parts.append(f"\nDocument contains {len(doc.images)} images:")
            for img in doc.images:
                img_info = f"- Image {img.image_id} on page {img.page_number}"
                if img.dimensions:
                    img_info += f" ({img.dimensions.get('width', '?')}x{img.dimensions.get('height', '?')})"
                if img.associated_text:
                    img_info += f" - Associated text: {img.associated_text[:100]}..."
                content_parts.append(img_info)
        
        # Add sections
        for i, section in enumerate(doc.sections):
            section_text = f"\n--- Section {i+1} ---"
            if section.heading:
                section_text += f"\nHeading: {section.heading}"
            
            # Add section images info
            if section.images:
                section_text += f"\nImages in this section: {len(section.images)}"
                for img in section.images:
                    section_text += f"\n  - {img.image_id}: {img.associated_text or 'No associated text'}"
            
            for j, chunk in enumerate(section.chunks):
                section_text += f"\nChunk {j+1}: {chunk.text}"
                
                # Add associated images info for this chunk
                if chunk.associated_images:
                    section_text += f"\n  Associated images: {', '.join(chunk.associated_images)}"
            
            content_parts.append(section_text)
        
        return "\n".join(content_parts)
    
    def _create_system_prompt(self, task: str, output_format: str) -> str:
        """Create the system prompt for the AI."""
        base_prompt = f"""You are an expert data analyst and content processor. Your task is to: {task}

The content will be provided in a structured format with sections and chunks. The document may also contain images with associated metadata including page numbers, dimensions, and nearby text. Please analyze the content thoroughly and provide your response in the requested format.

Output Format: {output_format}

Guidelines:
1. Understand the content deeply and identify key themes, topics, and important information
2. Restructure the information in a logical, coherent manner
3. Filter out irrelevant or redundant information
4. Maintain accuracy and preserve important details
5. Provide clear, well-organized output
6. When images are present, consider their context and associated text in your analysis
7. Note the relationship between images and surrounding text content

For structured_json format, return a JSON object with the following structure:
{{
    "summary": "Brief overview of the content",
    "key_topics": ["topic1", "topic2", "topic3"],
    "important_points": ["point1", "point2", "point3"],
    "structured_content": {{
        "section1": "content",
        "section2": "content"
    }},
    "images_analysis": {{
        "total_images": 0,
        "images_by_page": {{"page1": ["image1", "image2"]}},
        "image_contexts": ["context1", "context2"]
    }},
    "insights": ["insight1", "insight2"],
    "recommendations": ["recommendation1", "recommendation2"]
}}

For markdown format, return well-formatted markdown with headers, lists, and proper structure.
For summary format, return a concise summary of the key points.
"""
        return base_prompt
    
    def save_processed_result(self, result: Dict[str, Any], output_file: str) -> None:
        """Save the processed result to a file."""
        if result.get("format") == "structured_json" and "raw_response" not in result:
            # Save as JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            # Save as text
            content = result.get("content", result.get("raw_response", str(result)))
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def process_and_save(
        self, 
        doc: UnifiedDocument, 
        output_file: str,
        task: str = "analyze and restructure",
        output_format: str = "structured_json",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a document and save the result to a file.
        
        Args:
            doc: The parsed document to process
            output_file: Path to save the processed result
            task: The task description for the AI
            output_format: Desired output format
            **kwargs: Additional arguments for process_document
            
        Returns:
            Dictionary containing the AI-processed result
        """
        result = self.process_document(doc, task, output_format, **kwargs)
        self.save_processed_result(result, output_file)
        return result


def process_with_ai(
    doc: UnifiedDocument,
    output_file: str,
    api_key: Optional[str] = None,
    task: str = "analyze and restructure",
    output_format: str = "structured_json",
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to process a document with AI and save the result.
    
    Args:
        doc: The parsed document to process
        output_file: Path to save the processed result
        api_key: OpenAI API key
        task: The task description for the AI
        output_format: Desired output format
        **kwargs: Additional arguments for AI processing
        
    Returns:
        Dictionary containing the AI-processed result
    """
    processor = AIProcessor(api_key=api_key)
    return processor.process_and_save(doc, output_file, task, output_format, **kwargs)
