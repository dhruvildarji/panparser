from __future__ import annotations
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import json

class Metadata(BaseModel):
    source: str
    content_type: str = Field(default="text/plain")
    encoding: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    title: Optional[str] = None
    language: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

class ImageMetadata(BaseModel):
    """Metadata for extracted images from documents."""
    image_id: str
    page_number: int
    position: Dict[str, float] = Field(default_factory=dict)  # x, y, width, height
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    format: Optional[str] = None  # PNG, JPEG, etc.
    dimensions: Optional[Dict[str, int]] = None  # width, height
    extracted_at: datetime = Field(default_factory=datetime.now)
    associated_text: Optional[str] = None  # Text near the image
    confidence_score: Optional[float] = None  # Confidence in image detection
    meta: Dict[str, Any] = Field(default_factory=dict)
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Override model_dump to handle datetime serialization."""
        data = super().model_dump(**kwargs)
        # Convert datetime to ISO string for JSON serialization
        if 'extracted_at' in data and isinstance(data['extracted_at'], datetime):
            data['extracted_at'] = data['extracted_at'].isoformat()
        return data

class Chunk(BaseModel):
    text: str
    order: int = 0
    id: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    associated_images: List[str] = Field(default_factory=list)  # List of image_ids

class Section(BaseModel):
    heading: Optional[str] = None
    chunks: List[Chunk] = Field(default_factory=list)
    meta: Dict[str, Any] = Field(default_factory=dict)
    images: List[ImageMetadata] = Field(default_factory=list)  # Images in this section

class UnifiedDocument(BaseModel):
    schema_id: str = "panparsex/v1"
    meta: Metadata
    sections: List[Section] = Field(default_factory=list)
    images: List[ImageMetadata] = Field(default_factory=list)  # All images in document

    def add_text(self, text: str, heading: Optional[str] = None, **meta):
        sec = Section(heading=heading, chunks=[Chunk(text=text, order=0)], meta=meta)
        self.sections.append(sec)
        return self
    
    def add_image(self, image: ImageMetadata, section_index: Optional[int] = None):
        """Add an image to the document and optionally to a specific section."""
        self.images.append(image)
        if section_index is not None and 0 <= section_index < len(self.sections):
            self.sections[section_index].images.append(image)
        return self
    
    def get_images_by_page(self, page_number: int) -> List[ImageMetadata]:
        """Get all images from a specific page."""
        return [img for img in self.images if img.page_number == page_number]
    
    def get_images_by_section(self, section_index: int) -> List[ImageMetadata]:
        """Get all images from a specific section."""
        if 0 <= section_index < len(self.sections):
            return self.sections[section_index].images
        return []
