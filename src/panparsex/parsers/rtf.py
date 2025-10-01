from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class RTFParser(ParserProtocol):
    name = "rtf"
    content_types: Iterable[str] = ("application/rtf", "text/rtf")
    extensions: Iterable[str] = (".rtf",)

    def can_parse(self, meta: Metadata) -> bool:
        return (meta.content_type in self.content_types or 
                (meta.path or "").endswith(".rtf"))

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        doc = UnifiedDocument(meta=meta, sections=[])
        
        try:
            # Try using striprtf for better RTF parsing
            try:
                from striprtf.striprtf import rtf_to_text
                with open(target, "r", encoding="utf-8", errors="ignore") as f:
                    rtf_content = f.read()
                text = rtf_to_text(rtf_content)
                
                if text.strip():
                    doc.sections.append(Section(
                        heading="Content",
                        chunks=[Chunk(text=text.strip(), order=0, meta={"type": "content"})],
                        meta={"type": "content", "parser": "striprtf"}
                    ))
                else:
                    doc.sections.append(Section(
                        heading="Content",
                        chunks=[Chunk(text="[panparsex:rtf] No text content found", order=0, meta={"type": "empty"})],
                        meta={"type": "empty"}
                    ))
                    
            except ImportError:
                # Fallback to simple RTF parsing
                with open(target, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                # Simple RTF text extraction
                text = self._simple_rtf_extract(content)
                
                if text.strip():
                    doc.sections.append(Section(
                        heading="Content",
                        chunks=[Chunk(text=text.strip(), order=0, meta={"type": "content"})],
                        meta={"type": "content", "parser": "simple"}
                    ))
                else:
                    doc.sections.append(Section(
                        heading="Content",
                        chunks=[Chunk(text="[panparsex:rtf] No text content found", order=0, meta={"type": "empty"})],
                        meta={"type": "empty"}
                    ))
                    
        except Exception as e:
            error_text = f"[panparsex:rtf] unable to parse: {e}"
            doc.sections.append(Section(
                heading="Error",
                chunks=[Chunk(text=error_text, order=0, meta={"error": True})],
                meta={"error": True}
            ))
        
        return doc
    
    def _simple_rtf_extract(self, rtf_content: str) -> str:
        """Simple RTF text extraction by removing RTF control codes."""
        import re
        
        # Remove RTF header
        text = re.sub(r'\\[a-z]+\d*\s?', '', rtf_content)
        
        # Remove braces
        text = re.sub(r'[{}]', '', text)
        
        # Remove remaining control characters
        text = re.sub(r'\\[^a-zA-Z]', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

register_parser(RTFParser())
