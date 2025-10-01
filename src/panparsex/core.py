from __future__ import annotations
import mimetypes, os, pathlib, importlib.metadata, re
from typing import Protocol, runtime_checkable, Iterable, Optional, Dict, Any, Union, List
from .types import UnifiedDocument, Metadata, Section, Chunk
from dataclasses import dataclass

Pathish = Union[str, os.PathLike]

@runtime_checkable
class ParserProtocol(Protocol):
    name: str
    content_types: Iterable[str]  # e.g. ['text/plain', 'application/json']
    extensions: Iterable[str]     # e.g. ['.txt', '.json']

    def can_parse(self, meta: Metadata) -> bool: ...
    def parse(self, target: Pathish, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument: ...

@dataclass
class _Registry:
    parsers: List[ParserProtocol]

    def add(self, parser: ParserProtocol):
        self.parsers.append(parser)

_registry = _Registry(parsers=[])

def get_registry() -> _Registry:
    return _registry

def register_parser(parser: ParserProtocol):
    _registry.add(parser)
    return parser

def _guess_meta(target: Pathish, content_type: Optional[str] = None, url: Optional[str] = None) -> Metadata:
    p = pathlib.Path(str(target))
    ctype = content_type
    if not ctype:
        if url and re.match(r"^https?://", str(target)):
            ctype = "text/html"
        else:
            ctype, _ = mimetypes.guess_type(p.name)
    ctype = ctype or "application/octet-stream"
    return Metadata(source=str(target), content_type=ctype, path=str(p) if p.exists() else None, url=url)

def _load_entrypoint_parsers():
    for ep in importlib.metadata.entry_points(group="panparsex.parsers"):
        try:
            maker = ep.load()
            parser = maker()  # must return ParserProtocol
            register_parser(parser)
        except Exception as e:
            # Fail open; keep core working even if a plugin is broken
            pass

_loaded_eps = False

def parse(target: Pathish, recursive: bool = False, **kwargs) -> UnifiedDocument:
    global _loaded_eps
    if not _loaded_eps:
        _load_entrypoint_parsers()
        _loaded_eps = True

    # Ensure built-ins are registered (import side-effect)
    from .parsers import text as _p_text  # noqa
    from .parsers import json_ as _p_json  # noqa
    from .parsers import yaml_ as _p_yaml  # noqa
    from .parsers import xml as _p_xml  # noqa
    from .parsers import html as _p_html  # noqa
    from .parsers import pdf as _p_pdf  # noqa
    from .parsers import web as _p_web  # noqa
    from .parsers import csv as _p_csv  # noqa
    from .parsers import docx as _p_docx  # noqa
    from .parsers import markdown as _p_markdown  # noqa
    from .parsers import rtf as _p_rtf  # noqa
    from .parsers import excel as _p_excel  # noqa
    from .parsers import pptx as _p_pptx  # noqa

    url = kwargs.pop("url", None)
    meta = _guess_meta(target, content_type=kwargs.pop("content_type", None), url=url)

    # Choose a parser
    best: Optional[ParserProtocol] = None
    for p in _registry.parsers:
        try:
            if p.can_parse(meta):
                best = p
                break
        except Exception:
            continue

    if not best:
        # fallback to text parser
        for p in _registry.parsers:
            if getattr(p, "name", "") == "text":
                best = p
                break

    if not best:
        raise RuntimeError("No suitable parser found and no text fallback available.")

    return best.parse(target, meta, recursive=recursive, **kwargs)
