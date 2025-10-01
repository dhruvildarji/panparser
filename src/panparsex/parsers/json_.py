from __future__ import annotations
import json
from typing import Iterable
from ..types import UnifiedDocument, Metadata
from ..core import register_parser, ParserProtocol

class JSONParser(ParserProtocol):
    name = "json"
    content_types: Iterable[str] = ("application/json",)
    extensions: Iterable[str] = (".json",)

    def can_parse(self, meta: Metadata) -> bool:
        return meta.content_type == "application/json" or (meta.path or "").endswith(".json")

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            text = json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            text = f"[panparsex:json] unable to parse: {e}"
        return UnifiedDocument(meta=meta, sections=[]).add_text(text)

register_parser(JSONParser())
