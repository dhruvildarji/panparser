from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class PDFParser(ParserProtocol):
    name = "pdf"
    content_types: Iterable[str] = ("application/pdf",)
    extensions: Iterable[str] = (".pdf",)

    def can_parse(self, meta: Metadata) -> bool:
        return meta.content_type == "application/pdf" or (meta.path or "").endswith(".pdf")

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        doc = UnifiedDocument(meta=meta, sections=[])
        text = ""
        error = None
        
        # Try pypdf first (faster and more reliable)
        try:
            import pypdf
            reader = pypdf.PdfReader(str(target))
            
            # Extract metadata
            if reader.metadata:
                if reader.metadata.title:
                    doc.meta.title = reader.metadata.title
                if reader.metadata.author:
                    doc.meta.extra["author"] = reader.metadata.author
                if reader.metadata.subject:
                    doc.meta.extra["subject"] = reader.metadata.subject
                if reader.metadata.creator:
                    doc.meta.extra["creator"] = reader.metadata.creator
            
            # Extract text page by page
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    # Create a section for each page
                    section = Section(
                        heading=f"Page {i + 1}",
                        chunks=[Chunk(text=page_text.strip(), order=i)],
                        meta={"page_number": i + 1}
                    )
                    doc.sections.append(section)
                    text += page_text + "\n"
                    
        except Exception as e:
            error = e
            
        # Fallback to pdfminer.six if pypdf fails
        if not text:
            try:
                from pdfminer.high_level import extract_text
                text = extract_text(str(target)) or ""
                if text:
                    # Create a single section for the entire document
                    doc.sections.append(Section(
                        heading="Document Content",
                        chunks=[Chunk(text=text.strip(), order=0)],
                        meta={"extraction_method": "pdfminer"}
                    ))
            except Exception as e2:
                error = e2
                
        if not text:
            text = f"[panparsex:pdf] unable to extract text: {error}"
            doc.sections.append(Section(
                heading="Error",
                chunks=[Chunk(text=text, order=0)],
                meta={"error": True}
            ))
            
        return doc

register_parser(PDFParser())
