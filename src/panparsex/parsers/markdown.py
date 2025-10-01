from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class MarkdownParser(ParserProtocol):
    name = "markdown"
    content_types: Iterable[str] = ("text/markdown", "text/x-markdown")
    extensions: Iterable[str] = (".md", ".markdown", ".mdown", ".mkd")

    def can_parse(self, meta: Metadata) -> bool:
        return (meta.content_type in self.content_types or 
                (meta.path or "").endswith((".md", ".markdown", ".mdown", ".mkd")))

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        doc = UnifiedDocument(meta=meta, sections=[])
        
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Parse markdown using markdown-it-py
            from markdown_it import MarkdownIt
            from markdown_it.tree import SyntaxTreeNode
            
            md = MarkdownIt("commonmark", {"breaks": True, "html": True})
            tokens = md.parse(content)
            tree = SyntaxTreeNode(tokens)
            
            # Extract title from first heading
            for i, token in enumerate(tokens):
                if token.type == "heading_open" and token.tag == "h1":
                    # Find the next inline token
                    for j in range(i + 1, len(tokens)):
                        if tokens[j].type == "inline" and tokens[j].children:
                            doc.meta.title = tokens[j].children[0].content.strip()
                            break
                    break
            
            # Convert to sections based on headings
            current_section = None
            current_chunks = []
            order = 0
            
            for token in tokens:
                if token.type == "heading_open":
                    # Save previous section
                    if current_section and current_chunks:
                        doc.sections.append(Section(
                            heading=current_section,
                            chunks=current_chunks,
                            meta={"type": "content"}
                        ))
                    
                    # Find the heading text
                    heading_text = ""
                    for j in range(tokens.index(token) + 1, len(tokens)):
                        if tokens[j].type == "inline" and tokens[j].children:
                            heading_text = tokens[j].children[0].content.strip()
                            break
                    
                    current_section = heading_text
                    current_chunks = []
                    order += 1
                    
                elif token.type == "paragraph_open":
                    # Find paragraph text
                    paragraph_text = ""
                    for j in range(tokens.index(token) + 1, len(tokens)):
                        if tokens[j].type == "inline" and tokens[j].children:
                            paragraph_text = "".join([child.content for child in tokens[j].children if child.type == "text"])
                            break
                    
                    if paragraph_text.strip():
                        chunk = Chunk(text=paragraph_text.strip(), order=order, meta={"type": "paragraph"})
                        current_chunks.append(chunk)
                        order += 1
                        
                elif token.type == "code_block":
                    # Handle code blocks
                    code_text = token.content.strip()
                    if code_text:
                        chunk = Chunk(text=code_text, order=order, meta={"type": "code", "language": token.info or "text"})
                        current_chunks.append(chunk)
                        order += 1
                        
                elif token.type == "blockquote_open":
                    # Handle blockquotes
                    quote_text = ""
                    for j in range(tokens.index(token) + 1, len(tokens)):
                        if tokens[j].type == "inline" and tokens[j].children:
                            quote_text = "".join([child.content for child in tokens[j].children if child.type == "text"])
                            break
                    
                    if quote_text.strip():
                        chunk = Chunk(text=quote_text.strip(), order=order, meta={"type": "quote"})
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
                doc.sections.append(Section(
                    heading="Content",
                    chunks=current_chunks,
                    meta={"type": "content"}
                ))
            
            # Extract links and images
            links = []
            images = []
            for token in tokens:
                if token.type == "link_open":
                    href = token.attrGet("href")
                    if href:
                        # Find link text
                        link_text = ""
                        for j in range(tokens.index(token) + 1, len(tokens)):
                            if tokens[j].type == "inline" and tokens[j].children:
                                link_text = "".join([child.content for child in tokens[j].children if child.type == "text"])
                                break
                        links.append({"url": href, "text": link_text})
                        
                elif token.type == "image":
                    src = token.attrGet("src")
                    alt = token.attrGet("alt")
                    if src:
                        images.append({"src": src, "alt": alt or ""})
            
            doc.meta.extra["links"] = links
            doc.meta.extra["images"] = images
            
        except ImportError:
            # Fallback to simple text parsing
            try:
                with open(target, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                doc.sections.append(Section(
                    heading="Content",
                    chunks=[Chunk(text=content, order=0, meta={"type": "raw_text"})],
                    meta={"type": "fallback"}
                ))
            except Exception as e:
                error_text = f"[panparsex:markdown] unable to parse: {e}"
                doc.sections.append(Section(
                    heading="Error",
                    chunks=[Chunk(text=error_text, order=0, meta={"error": True})],
                    meta={"error": True}
                ))
        except Exception as e:
            error_text = f"[panparsex:markdown] unable to parse: {e}"
            doc.sections.append(Section(
                heading="Error",
                chunks=[Chunk(text=error_text, order=0, meta={"error": True})],
                meta={"error": True}
            ))
        
        return doc

register_parser(MarkdownParser())
