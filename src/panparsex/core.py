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
    target_str = str(target)
    is_url = target_str.startswith(('http://', 'https://'))
    
    ctype = content_type
    if not ctype:
        if is_url or (url and re.match(r"^https?://", target_str)):
            ctype = "text/html"
        else:
            p = pathlib.Path(target_str)
            ctype, _ = mimetypes.guess_type(p.name)
            # Handle common file types that mimetypes doesn't recognize
            if not ctype:
                if p.suffix.lower() in ['.yaml', '.yml']:
                    ctype = "text/yaml"
                elif p.suffix.lower() in ['.md', '.markdown']:
                    ctype = "text/markdown"
                elif p.suffix.lower() in ['.csv']:
                    ctype = "text/csv"
    ctype = ctype or "application/octet-stream"
    
    if is_url:
        return Metadata(source=target_str, content_type=ctype, path=None, url=target_str)
    else:
        p = pathlib.Path(target_str)
        return Metadata(source=target_str, content_type=ctype, path=str(p) if p.exists() else None, url=url)

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

def _ensure_parsers_loaded():
    """Ensure all parsers are loaded and registered."""
    global _loaded_eps
    if not _loaded_eps:
        _load_entrypoint_parsers()
        _loaded_eps = True
    
    # Ensure built-ins are registered (import side-effect)
    from . import parsers  # noqa

def parse(target: Pathish, recursive: bool = False, **kwargs) -> UnifiedDocument:
    _ensure_parsers_loaded()

    url = kwargs.pop("url", None)
    meta = _guess_meta(target, content_type=kwargs.pop("content_type", None), url=url)

    # Check if file exists (for non-URL targets)
    target_str = str(target)
    is_url = target_str.startswith(('http://', 'https://'))
    if not is_url and not pathlib.Path(target_str).exists():
        raise FileNotFoundError(f"File not found: {target}")

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
