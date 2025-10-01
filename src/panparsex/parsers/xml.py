from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata
from ..core import register_parser, ParserProtocol

class XMLParser(ParserProtocol):
    name = "xml"
    content_types: Iterable[str] = ("application/xml","text/xml")
    extensions: Iterable[str] = (".xml",)

    def can_parse(self, meta: Metadata) -> bool:
        return meta.content_type in self.content_types or (meta.path or "").endswith(".xml")

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        try:
            from lxml import etree
            tree = etree.parse(str(target))
            text = etree.tostring(tree, encoding="unicode", pretty_print=True)
        except Exception as e:
            text = f"[panparsex:xml] unable to parse: {e}"
        return UnifiedDocument(meta=meta, sections=[]).add_text(text)

register_parser(XMLParser())
