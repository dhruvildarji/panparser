from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

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

class Chunk(BaseModel):
    text: str
    order: int = 0
    id: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)

class Section(BaseModel):
    heading: Optional[str] = None
    chunks: List[Chunk] = Field(default_factory=list)
    meta: Dict[str, Any] = Field(default_factory=dict)

class UnifiedDocument(BaseModel):
    schema_id: str = "panparsex/v1"
    meta: Metadata
    sections: List[Section] = Field(default_factory=list)

    def add_text(self, text: str, heading: Optional[str] = None, **meta):
        sec = Section(heading=heading, chunks=[Chunk(text=text, order=0)], meta=meta)
        self.sections.append(sec)
        return self
