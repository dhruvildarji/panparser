from __future__ import annotations
from typing import Iterable, Set, List, Dict, Any
from urllib.parse import urljoin, urlparse
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol
from bs4 import BeautifulSoup
import re

class HTMLParser(ParserProtocol):
    name = "html"
    content_types: Iterable[str] = ("text/html", "application/xhtml+xml")
    extensions: Iterable[str] = (".html", ".htm", ".xhtml")

    def can_parse(self, meta: Metadata) -> bool:
        # Don't handle URLs - let the web parser handle them
        if meta.url:
            return False
        return (meta.content_type.startswith("text/html") or 
                meta.content_type == "application/xhtml+xml" or
                (meta.path or "").endswith((".html", ".htm", ".xhtml")))

    def parse(self, target, meta: Metadata, recursive: bool = False, max_links: int = 50, max_depth: int = 0, **kwargs) -> UnifiedDocument:
        html = ""
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
        except Exception as e:
            html = f"[panparsex:html] unable to read: {e}"
            
        doc = UnifiedDocument(meta=meta, sections=[])
        soup = BeautifulSoup(html, "lxml")
        
        # Extract title
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            doc.meta.title = title_tag.string.strip()
            
        # Extract meta information
        meta_tags = {}
        for meta_tag in soup.find_all("meta"):
            name = meta_tag.get("name") or meta_tag.get("property")
            content = meta_tag.get("content")
            if name and content:
                meta_tags[name] = content
        doc.meta.extra["meta_tags"] = meta_tags
        
        # Extract structured content by sections
        self._extract_sections(soup, doc)
        
        # Extract links
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            links.append({"url": href, "text": text})
        doc.meta.extra["links"] = links[:max_links]
        
        # Extract images
        images = []
        for img in soup.find_all("img", src=True):
            src = img["src"]
            alt = img.get("alt", "")
            images.append({"src": src, "alt": alt})
        doc.meta.extra["images"] = images
        
        return doc
    
    def _extract_sections(self, soup: BeautifulSoup, doc: UnifiedDocument):
        """Extract content organized by headings and sections."""
        current_section = None
        current_chunks = []
        order = 0
        
        # Find all content elements in order
        elements = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "li", "blockquote", "pre", "code"])
        
        for element in elements:
            tag_name = element.name
            text = element.get_text(" ", strip=True)
            
            if not text:
                continue
                
            # Handle headings - start new section
            if tag_name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                # Save previous section if it exists
                if current_section and current_chunks:
                    doc.sections.append(Section(
                        heading=current_section,
                        chunks=current_chunks,
                        meta={"type": "content"}
                    ))
                
                # Start new section
                current_section = text
                current_chunks = []
                # Add the heading as a chunk
                chunk = Chunk(text=text, order=order, meta={"type": "heading", "tag": tag_name})
                current_chunks.append(chunk)
                order += 1
                
            else:
                # Add content to current section
                if tag_name in ["pre", "code"]:
                    # Preserve formatting for code blocks
                    chunk = Chunk(text=text, order=order, meta={"type": "code", "tag": tag_name})
                elif tag_name == "blockquote":
                    chunk = Chunk(text=text, order=order, meta={"type": "quote", "tag": tag_name})
                else:
                    chunk = Chunk(text=text, order=order, meta={"type": "text", "tag": tag_name})
                
                current_chunks.append(chunk)
                order += 1
        
        # Save final section
        if current_section and current_chunks:
            doc.sections.append(Section(
                heading=current_section,
                chunks=current_chunks,
                meta={"type": "content"}
            ))
        elif current_chunks:
            # No heading, create a default section
            doc.sections.append(Section(
                heading="Content",
                chunks=current_chunks,
                meta={"type": "content"}
            ))

register_parser(HTMLParser())
