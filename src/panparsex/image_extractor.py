"""
Image extraction module for PDF documents.
Handles detection, extraction, and association of images with text content.
"""

from __future__ import annotations
import os
import uuid
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import logging

from .types import ImageMetadata

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extracts images from PDF documents and associates them with text content."""
    
    def __init__(self, output_dir: Optional[str] = None, min_image_size: Tuple[int, int] = (50, 50)):
        """
        Initialize the image extractor.
        
        Args:
            output_dir: Directory to save extracted images. If None, uses temp directory.
            min_image_size: Minimum width and height for images to be extracted.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "extracted_images"
        self.min_image_size = min_image_size
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_images_from_pdf(self, pdf_path: str, extract_images: bool = True) -> List[ImageMetadata]:
        """
        Extract images from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            extract_images: Whether to actually extract and save images to disk
            
        Returns:
            List of ImageMetadata objects for all detected images
        """
        images = []
        
        try:
            # Try PyMuPDF first (better image extraction)
            images = self._extract_with_pymupdf(pdf_path, extract_images)
        except ImportError:
            logger.warning("PyMuPDF not available, falling back to pypdf")
            try:
                images = self._extract_with_pypdf(pdf_path, extract_images)
            except Exception as e:
                logger.error(f"Failed to extract images with pypdf: {e}")
                return []
        except Exception as e:
            logger.error(f"Failed to extract images with PyMuPDF: {e}")
            return []
            
        return images
    
    def _extract_with_pymupdf(self, pdf_path: str, extract_images: bool) -> List[ImageMetadata]:
        """Extract images using PyMuPDF (fitz)."""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("PyMuPDF is required for image extraction. Install with: pip install PyMuPDF")
        
        images = []
        doc = fitz.open(pdf_path)
        seen_hashes = set()  # Track image content hashes to avoid duplicates
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get image list for this page
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    # Get image data
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Skip if image is too small
                    if pix.width < self.min_image_size[0] or pix.height < self.min_image_size[1]:
                        pix = None
                        continue
                    
                    # Check for duplicate images by content hash
                    img_hash = hashlib.md5(pix.tobytes()).hexdigest()
                    if img_hash in seen_hashes:
                        pix = None
                        continue
                    seen_hashes.add(img_hash)
                    
                    # Generate unique image ID
                    image_id = f"img_{page_num + 1}_{img_index + 1}_{uuid.uuid4().hex[:8]}"
                    
                    # Get image position on page
                    img_rects = page.get_image_rects(xref)
                    position = {}
                    if img_rects:
                        rect = img_rects[0]
                        position = {
                            "x": rect.x0,
                            "y": rect.y0,
                            "width": rect.width,
                            "height": rect.height
                        }
                    
                    # Extract image if requested
                    file_path = None
                    if extract_images:
                        file_path = self._save_image(pix, image_id, page_num + 1)
                    
                    # Get associated text (text near the image)
                    associated_text = self._get_text_near_image(page, img_rects[0] if img_rects else None)
                    
                    # Create image metadata
                    image_meta = ImageMetadata(
                        image_id=image_id,
                        page_number=page_num + 1,
                        position=position,
                        file_path=file_path,
                        file_size=os.path.getsize(file_path) if file_path and os.path.exists(file_path) else None,
                        format=pix.colorspace.name if pix.colorspace else "RGB",
                        dimensions={"width": pix.width, "height": pix.height},
                        associated_text=associated_text,
                        confidence_score=0.9,  # High confidence for PyMuPDF
                        meta={
                            "extraction_method": "pymupdf",
                            "xref": xref,
                            "img_index": img_index
                        }
                    )
                    
                    images.append(image_meta)
                    pix = None  # Free memory
                    
                except Exception as e:
                    logger.warning(f"Failed to extract image {img_index} from page {page_num + 1}: {e}")
                    continue
        
        doc.close()
        return images
    
    def _extract_with_pypdf(self, pdf_path: str, extract_images: bool) -> List[ImageMetadata]:
        """Extract images using pypdf (fallback method)."""
        try:
            import pypdf
        except ImportError:
            raise ImportError("pypdf is required for PDF processing")
        
        images = []
        reader = pypdf.PdfReader(pdf_path)
        
        for page_num, page in enumerate(reader.pages):
            try:
                # Get images from page
                if hasattr(page, 'images'):
                    for img_index, img in enumerate(page.images):
                        try:
                            # Generate unique image ID
                            image_id = f"img_{page_num + 1}_{img_index + 1}_{uuid.uuid4().hex[:8]}"
                            
                            # Extract image data
                            img_data = img.data
                            
                            # Get image dimensions (approximate)
                            width, height = self._get_image_dimensions_from_data(img_data)
                            
                            # Skip if image is too small
                            if width < self.min_image_size[0] or height < self.min_image_size[1]:
                                continue
                            
                            # Extract image if requested
                            file_path = None
                            if extract_images:
                                file_path = self._save_image_data(img_data, image_id, page_num + 1)
                            
                            # Create image metadata
                            image_meta = ImageMetadata(
                                image_id=image_id,
                                page_number=page_num + 1,
                                position={},  # pypdf doesn't provide position info
                                file_path=file_path,
                                file_size=len(img_data) if img_data else None,
                                format=self._detect_image_format(img_data),
                                dimensions={"width": width, "height": height},
                                associated_text=None,  # pypdf doesn't provide text association
                                confidence_score=0.7,  # Lower confidence for pypdf
                                meta={
                                    "extraction_method": "pypdf",
                                    "img_index": img_index
                                }
                            )
                            
                            images.append(image_meta)
                            
                        except Exception as e:
                            logger.warning(f"Failed to extract image {img_index} from page {page_num + 1}: {e}")
                            continue
                            
            except Exception as e:
                logger.warning(f"Failed to process page {page_num + 1}: {e}")
                continue
        
        return images
    
    def _save_image(self, pix, image_id: str, page_num: int) -> str:
        """Save a PyMuPDF pixmap to file."""
        try:
            # Convert to PNG if not already
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_data = pix.tobytes("png")
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                img_data = pix1.tobytes("png")
                pix1 = None
            
            # Save to file
            filename = f"{image_id}_page_{page_num}.png"
            file_path = self.output_dir / filename
            
            with open(file_path, "wb") as f:
                f.write(img_data)
            
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save image {image_id}: {e}")
            return None
    
    def _save_image_data(self, img_data: bytes, image_id: str, page_num: int) -> str:
        """Save raw image data to file."""
        try:
            # Detect format from data
            format_ext = self._detect_image_format(img_data)
            filename = f"{image_id}_page_{page_num}.{format_ext}"
            file_path = self.output_dir / filename
            
            with open(file_path, "wb") as f:
                f.write(img_data)
            
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save image data {image_id}: {e}")
            return None
    
    def _detect_image_format(self, img_data: bytes) -> str:
        """Detect image format from data."""
        if img_data.startswith(b'\xff\xd8\xff'):
            return 'jpg'
        elif img_data.startswith(b'\x89PNG'):
            return 'png'
        elif img_data.startswith(b'GIF'):
            return 'gif'
        elif img_data.startswith(b'BM'):
            return 'bmp'
        else:
            return 'png'  # Default fallback
    
    def _get_image_dimensions_from_data(self, img_data: bytes) -> Tuple[int, int]:
        """Get image dimensions from raw data."""
        try:
            from PIL import Image
            import io
            
            img = Image.open(io.BytesIO(img_data))
            return img.size
        except ImportError:
            # Fallback: return default dimensions
            return (100, 100)
        except Exception:
            return (100, 100)
    
    def _get_text_near_image(self, page, img_rect) -> Optional[str]:
        """Get text that appears near an image."""
        if not img_rect:
            return None
        
        try:
            import fitz  # Import fitz here to avoid issues when PyMuPDF is not available
            
            # Get text blocks near the image
            text_blocks = page.get_text("dict")
            nearby_text = []
            
            # Expand image rectangle slightly to capture nearby text
            expanded_rect = fitz.Rect(
                img_rect.x0 - 20,
                img_rect.y0 - 20,
                img_rect.x1 + 20,
                img_rect.y1 + 20
            )
            
            for block in text_blocks.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            span_rect = fitz.Rect(span["bbox"])
                            if expanded_rect.intersects(span_rect):
                                nearby_text.append(span["text"])
            
            return " ".join(nearby_text) if nearby_text else None
            
        except Exception as e:
            logger.warning(f"Failed to get text near image: {e}")
            return None
    
    def cleanup_extracted_images(self):
        """Clean up all extracted images."""
        try:
            import shutil
            if self.output_dir.exists():
                shutil.rmtree(self.output_dir)
                self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to cleanup extracted images: {e}")


def extract_images_from_pdf(
    pdf_path: str, 
    output_dir: Optional[str] = None, 
    extract_images: bool = True,
    min_image_size: Tuple[int, int] = (50, 50)
) -> List[ImageMetadata]:
    """
    Convenience function to extract images from a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        extract_images: Whether to actually extract and save images to disk
        min_image_size: Minimum width and height for images to be extracted
        
    Returns:
        List of ImageMetadata objects for all detected images
    """
    extractor = ImageExtractor(output_dir=output_dir, min_image_size=min_image_size)
    return extractor.extract_images_from_pdf(pdf_path, extract_images=extract_images)
