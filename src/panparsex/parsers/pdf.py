from __future__ import annotations
from typing import Iterable, Optional
from ..types import UnifiedDocument, Metadata, Section, Chunk, ImageMetadata
from ..core import register_parser, ParserProtocol
from ..image_extractor import ImageExtractor

class PDFParser(ParserProtocol):
    name = "pdf"
    content_types: Iterable[str] = ("application/pdf",)
    extensions: Iterable[str] = (".pdf",)

    def can_parse(self, meta: Metadata) -> bool:
        return meta.content_type == "application/pdf" or (meta.path or "").endswith(".pdf")

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        # Extract parameters for image processing
        extract_images = kwargs.get('extract_images', True)
        image_output_dir = kwargs.get('image_output_dir', None)
        min_image_size = kwargs.get('min_image_size', (50, 50))
        
        doc = UnifiedDocument(meta=meta, sections=[])
        text = ""
        error = None
        
        # Initialize image extractor if image extraction is enabled
        image_extractor = None
        if extract_images:
            try:
                image_extractor = ImageExtractor(
                    output_dir=image_output_dir,
                    min_image_size=min_image_size
                )
            except Exception as e:
                print(f"Warning: Could not initialize image extractor: {e}")
                extract_images = False
        
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
            
            # Extract all images once at the beginning if enabled
            all_images = []
            if extract_images and image_extractor:
                try:
                    all_images = image_extractor.extract_images_from_pdf(str(target), extract_images=True)
                except Exception as e:
                    print(f"Warning: Could not extract images: {e}")
            
            # Extract text page by page and associate images
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                
                # Get images for this page
                page_images = [img for img in all_images if img.page_number == i + 1]
                
                if page_text.strip() or page_images:
                    # Create a section for each page
                    section = Section(
                        heading=f"Page {i + 1}",
                        chunks=[Chunk(text=page_text.strip(), order=i)],
                        meta={"page_number": i + 1},
                        images=page_images
                    )
                    doc.sections.append(section)
                    text += page_text + "\n"
                    
                    # Add images to document
                    for img in page_images:
                        doc.add_image(img, section_index=len(doc.sections) - 1)
                    
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
                    
                    # Try to extract images even with pdfminer fallback
                    if extract_images and image_extractor:
                        try:
                            all_images = image_extractor.extract_images_from_pdf(str(target), extract_images=True)
                            for img in all_images:
                                doc.add_image(img)
                        except Exception as e:
                            print(f"Warning: Could not extract images with pdfminer fallback: {e}")
                            
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
