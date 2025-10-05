"""
AI-powered post-processing module for panparsex.
Uses OpenAI GPT to analyze, restructure, and filter parsed content.
"""

from __future__ import annotations
import json
import os
import tiktoken
from typing import Dict, Any, Optional, List, Tuple
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
        
        # Model context limits (approximate)
        self.model_limits = {
            "gpt-4o-mini": 128000,
            "gpt-4o": 128000,
            "gpt-4": 8192,
            "gpt-3.5-turbo": 16384,
            "gpt-3.5-turbo-16k": 16384
        }
        
        # Safety margin for context (reserve 20% for response)
        self.max_input_tokens = int(self.model_limits.get(model, 128000) * 0.8)
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base encoding for unknown models
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def process_document(
        self, 
        doc: UnifiedDocument, 
        task: str = "analyze and restructure",
        output_format: str = "structured_json",
        max_tokens: int = 4000,
        temperature: float = 0.3,
        chunk_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a parsed document using OpenAI GPT with automatic chunking for large content.
        
        Args:
            doc: The parsed document to process
            task: The task description for the AI
            output_format: Desired output format (structured_json, markdown, summary, etc.)
            max_tokens: Maximum tokens for the response
            temperature: Temperature for the AI response
            chunk_size: Override automatic chunk size calculation
            
        Returns:
            Dictionary containing the AI-processed result
        """
        try:
            import openai
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        # Prepare the content for AI processing
        content = self._prepare_content_for_ai(doc)
        
        # Check if content needs chunking
        content_tokens = len(self.tokenizer.encode(content))
        
        if content_tokens <= self.max_input_tokens:
            # Process in single call
            return self._process_single_chunk(content, task, output_format, max_tokens, temperature)
        else:
            # Process with chunking
            print(f"Content exceeds token limit ({content_tokens} > {self.max_input_tokens}). Using chunking...", file=sys.stderr)
            return self._process_with_chunking(doc, content, task, output_format, max_tokens, temperature, chunk_size)
    
    def _process_single_chunk(self, content: str, task: str, output_format: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Process a single chunk of content."""
        import openai
        
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
    
    def _process_with_chunking(self, doc: UnifiedDocument, content: str, task: str, output_format: str, max_tokens: int, temperature: float, chunk_size: Optional[int]) -> Dict[str, Any]:
        """Process large content by chunking it and combining results."""
        import openai
        
        # Calculate chunk size
        if chunk_size is None:
            # Reserve space for system prompt and context
            system_prompt = self._create_system_prompt(task, output_format)
            system_tokens = len(self.tokenizer.encode(system_prompt))
            context_tokens = 1000  # Reserve for context and response
            chunk_size = self.max_input_tokens - system_tokens - context_tokens
        
        # Split content into chunks
        chunks = self._split_content_into_chunks(content, chunk_size)
        
        # Process each chunk
        chunk_results = []
        context_summary = ""
        
        print(f"Processing {len(chunks)} chunks...", file=sys.stderr)
        
        for i, chunk in enumerate(chunks):
            # Create context-aware prompt
            if i == 0:
                # First chunk - no previous context
                context_prompt = ""
            else:
                # Subsequent chunks - include summary of previous chunks
                context_prompt = f"Previous context summary: {context_summary}\n\n"
            
            # Process chunk
            print(f"Processing chunk {i+1}/{len(chunks)}...", file=sys.stderr)
            chunk_result = self._process_chunk_with_context(
                chunk, context_prompt, task, output_format, max_tokens, temperature, i + 1, len(chunks)
            )
            chunk_results.append(chunk_result)
            
            # Update context summary for next chunk
            if output_format == "structured_json" and isinstance(chunk_result, dict) and "summary" in chunk_result:
                context_summary = chunk_result["summary"]
            elif isinstance(chunk_result, dict) and "content" in chunk_result:
                context_summary = chunk_result["content"][:500] + "..." if len(chunk_result["content"]) > 500 else chunk_result["content"]
            else:
                context_summary = str(chunk_result)[:500] + "..." if len(str(chunk_result)) > 500 else str(chunk_result)
        
        # Combine results
        return self._combine_chunk_results(chunk_results, output_format, task)
    
    def _split_content_into_chunks(self, content: str, chunk_size: int) -> List[str]:
        """Split content into chunks that fit within token limits."""
        # Split by sections first to maintain structure
        sections = content.split("\n--- Section")
        chunks = []
        current_chunk = ""
        
        for i, section in enumerate(sections):
            if i > 0:
                section = "--- Section" + section  # Restore the section header
            
            section_tokens = len(self.tokenizer.encode(section))
            
            if section_tokens > chunk_size:
                # Section is too large, split by paragraphs
                paragraphs = section.split("\n\n")
                for para in paragraphs:
                    para_tokens = len(self.tokenizer.encode(para))
                    
                    if len(self.tokenizer.encode(current_chunk + "\n\n" + para)) > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = para
                        else:
                            # Single paragraph is too large, split by sentences
                            sentences = para.split(". ")
                            for sent in sentences:
                                if len(self.tokenizer.encode(current_chunk + ". " + sent)) > chunk_size:
                                    if current_chunk:
                                        chunks.append(current_chunk.strip())
                                        current_chunk = sent
                                    else:
                                        # Single sentence is too large, force split
                                        chunks.append(sent)
                                else:
                                    current_chunk += ". " + sent if current_chunk else sent
                    else:
                        current_chunk += "\n\n" + para if current_chunk else para
            else:
                # Section fits, add to current chunk
                if len(self.tokenizer.encode(current_chunk + "\n\n" + section)) > chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = section
                    else:
                        chunks.append(section)
                else:
                    current_chunk += "\n\n" + section if current_chunk else section
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _process_chunk_with_context(self, chunk: str, context_prompt: str, task: str, output_format: str, max_tokens: int, temperature: float, chunk_num: int, total_chunks: int) -> Dict[str, Any]:
        """Process a single chunk with context from previous chunks."""
        import openai
        
        # Create chunk-specific system prompt
        system_prompt = self._create_chunk_system_prompt(task, output_format, chunk_num, total_chunks)
        user_prompt = f"{context_prompt}Please process this chunk ({chunk_num}/{total_chunks}):\n\n{chunk}"
        
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
                parsed_result = json.loads(result)
                parsed_result["chunk_number"] = chunk_num
                return parsed_result
            except json.JSONDecodeError:
                return {"raw_response": result, "format": "text", "chunk_number": chunk_num}
        else:
            return {"content": result, "format": output_format, "chunk_number": chunk_num}
    
    def _combine_chunk_results(self, chunk_results: List[Dict[str, Any]], output_format: str, task: str) -> Dict[str, Any]:
        """Combine results from multiple chunks into a final result."""
        if output_format == "structured_json":
            return self._combine_json_results(chunk_results, task)
        else:
            return self._combine_text_results(chunk_results, output_format)
    
    def _combine_json_results(self, chunk_results: List[Dict[str, Any]], task: str) -> Dict[str, Any]:
        """Combine JSON results from multiple chunks."""
        # Extract summaries and key points from each chunk
        summaries = []
        all_key_topics = []
        all_important_points = []
        all_insights = []
        all_recommendations = []
        structured_content = {}
        images_analysis = {"total_images": 0, "images_by_page": {}, "image_contexts": []}
        
        for i, result in enumerate(chunk_results):
            if isinstance(result, dict):
                if "summary" in result:
                    summaries.append(f"Chunk {i+1}: {result['summary']}")
                
                if "key_topics" in result:
                    all_key_topics.extend(result["key_topics"])
                
                if "important_points" in result:
                    all_important_points.extend(result["important_points"])
                
                if "insights" in result:
                    all_insights.extend(result["insights"])
                
                if "recommendations" in result:
                    all_recommendations.extend(result["recommendations"])
                
                if "structured_content" in result:
                    for key, value in result["structured_content"].items():
                        structured_content[f"chunk_{i+1}_{key}"] = value
                
                if "images_analysis" in result:
                    img_analysis = result["images_analysis"]
                    images_analysis["total_images"] += img_analysis.get("total_images", 0)
                    images_analysis["image_contexts"].extend(img_analysis.get("image_contexts", []))
        
        # Create final combined result
        combined_result = {
            "summary": " ".join(summaries) if summaries else "Content processed across multiple chunks",
            "key_topics": list(set(all_key_topics)) if all_key_topics else [],
            "important_points": list(set(all_important_points)) if all_important_points else [],
            "structured_content": structured_content,
            "images_analysis": images_analysis,
            "insights": list(set(all_insights)) if all_insights else [],
            "recommendations": list(set(all_recommendations)) if all_recommendations else [],
            "processing_info": {
                "total_chunks": len(chunk_results),
                "chunked_processing": True,
                "task": task
            }
        }
        
        return combined_result
    
    def _combine_text_results(self, chunk_results: List[Dict[str, Any]], output_format: str) -> Dict[str, Any]:
        """Combine text results from multiple chunks."""
        combined_content = []
        
        for i, result in enumerate(chunk_results):
            if isinstance(result, dict) and "content" in result:
                combined_content.append(f"--- Chunk {i+1} ---\n{result['content']}")
            elif isinstance(result, dict) and "raw_response" in result:
                combined_content.append(f"--- Chunk {i+1} ---\n{result['raw_response']}")
            else:
                combined_content.append(f"--- Chunk {i+1} ---\n{str(result)}")
        
        return {
            "content": "\n\n".join(combined_content),
            "format": output_format,
            "processing_info": {
                "total_chunks": len(chunk_results),
                "chunked_processing": True
            }
        }
    
    def _create_chunk_system_prompt(self, task: str, output_format: str, chunk_num: int, total_chunks: int) -> str:
        """Create a system prompt for processing individual chunks."""
        base_prompt = f"""You are an expert data analyst and content processor. Your task is to: {task}

You are processing chunk {chunk_num} of {total_chunks} total chunks. This is part of a larger document that has been split for processing.

The content will be provided in a structured format with sections and chunks. The document may also contain images with associated metadata including page numbers, dimensions, and nearby text. Please analyze the content thoroughly and provide your response in the requested format.

Output Format: {output_format}

Guidelines:
1. Understand the content deeply and identify key themes, topics, and important information
2. Focus on the specific content in this chunk while being aware it's part of a larger document
3. Filter out irrelevant or redundant information
4. Maintain accuracy and preserve important details
5. Provide clear, well-organized output
6. When images are present, consider their context and associated text in your analysis
7. Note the relationship between images and surrounding text content
8. If this is not the first chunk, consider the previous context provided

For structured_json format, return a JSON object with the following structure:
{{
    "summary": "Brief overview of this chunk's content",
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
For summary format, return a concise summary of the key points in this chunk.
"""
        return base_prompt
    
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
            **kwargs: Additional arguments for process_document (including chunk_size)
            
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
