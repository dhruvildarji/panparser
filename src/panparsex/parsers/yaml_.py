from __future__ import annotations
from typing import Iterable
from ..types import UnifiedDocument, Metadata
from ..core import register_parser, ParserProtocol

class YAMLParser(ParserProtocol):
    name = "yaml"
    content_types: Iterable[str] = ("application/yaml","text/yaml","text/x-yaml","application/x-yaml")
    extensions: Iterable[str] = (".yml",".yaml")

    def can_parse(self, meta: Metadata) -> bool:
        return (meta.path or "").endswith((".yaml",".yml")) or "yaml" in (meta.content_type or "")

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        try:
            import yaml  # optional
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                data = yaml.safe_load(f)
            text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        except Exception as e:
            text = f"[panparsex:yaml] unable to parse: {e}"
        return UnifiedDocument(meta=meta, sections=[]).add_text(text)

register_parser(YAMLParser())
