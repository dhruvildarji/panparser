from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata
from ..core import register_parser, ParserProtocol

class TextParser(ParserProtocol):
    name = "text"
    content_types: Iterable[str] = ("text/plain",)
    extensions: Iterable[str] = (".txt",)

    def can_parse(self, meta: Metadata) -> bool:
        return (meta.content_type == "text/plain" or 
                (meta.path or "").endswith(".txt"))

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        text = ""
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            text = f"[panparsex:text] unable to read: {e}"
        return UnifiedDocument(meta=meta, sections=[]).add_text(text)

register_parser(TextParser())
