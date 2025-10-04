# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Dhruvil Darji

from __future__ import annotations
import mimetypes, os, pathlib, importlib.metadata, re
from typing import Protocol, runtime_checkable, Iterable, Optional, Dict, Any, Union, List, Generator
from .types import UnifiedDocument, Metadata, Section, Chunk
from dataclasses import dataclass
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

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

def _get_supported_extensions() -> set:
    """Get all supported file extensions from registered parsers."""
    _ensure_parsers_loaded()
    extensions = set()
    for parser in _registry.parsers:
        extensions.update(parser.extensions)
    return extensions

def _is_supported_file(file_path: pathlib.Path) -> bool:
    """Check if a file is supported by any registered parser."""
    supported_extensions = _get_supported_extensions()
    return file_path.suffix.lower() in supported_extensions

def _scan_folder(folder_path: pathlib.Path, recursive: bool = True, 
                 file_patterns: Optional[List[str]] = None,
                 exclude_patterns: Optional[List[str]] = None) -> Generator[pathlib.Path, None, None]:
    """Scan a folder for supported files."""
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError(f"Path is not a valid directory: {folder_path}")
    
    # Default file patterns if none provided
    if file_patterns is None:
        file_patterns = ['*']
    
    # Default exclude patterns
    if exclude_patterns is None:
        exclude_patterns = [
            '.*',  # Hidden files/folders
            '__pycache__',
            'node_modules',
            '.git',
            '.svn',
            '.hg',
            '*.tmp',
            '*.temp',
            '*.log',
            '*.cache'
        ]
    
    def should_exclude(file_path: pathlib.Path) -> bool:
        """Check if file should be excluded based on patterns."""
        file_str = str(file_path)
        for pattern in exclude_patterns:
            if file_path.match(pattern) or pattern in file_str:
                return True
        return False
    
    if recursive:
        # Recursive scan
        for file_path in folder_path.rglob('*'):
            if (file_path.is_file() and 
                _is_supported_file(file_path) and 
                not should_exclude(file_path)):
                yield file_path
    else:
        # Non-recursive scan
        for file_path in folder_path.iterdir():
            if (file_path.is_file() and 
                _is_supported_file(file_path) and 
                not should_exclude(file_path)):
                yield file_path

def parse_folder(folder_path: Pathish, recursive: bool = True, 
                 file_patterns: Optional[List[str]] = None,
                 exclude_patterns: Optional[List[str]] = None,
                 show_progress: bool = True,
                 **kwargs) -> List[UnifiedDocument]:
    """
    Parse all supported files in a folder.
    
    Args:
        folder_path: Path to the folder to parse
        recursive: Whether to scan subdirectories recursively
        file_patterns: List of file patterns to include (e.g., ['*.pdf', '*.txt'])
        exclude_patterns: List of patterns to exclude (e.g., ['*.tmp', '.git'])
        show_progress: Whether to show progress bar
        **kwargs: Additional arguments passed to individual file parsers
    
    Returns:
        List of UnifiedDocument objects, one for each parsed file
    """
    folder_path = pathlib.Path(folder_path)
    
    # Scan for files
    files = list(_scan_folder(folder_path, recursive, file_patterns, exclude_patterns))
    
    if not files:
        logger.warning(f"No supported files found in {folder_path}")
        return []
    
    logger.info(f"Found {len(files)} files to parse in {folder_path}")
    
    # Parse files
    documents = []
    failed_files = []
    
    # Create progress bar if requested
    if show_progress:
        file_iterator = tqdm(files, desc="Parsing files", unit="file")
    else:
        file_iterator = files
    
    for file_path in file_iterator:
        try:
            logger.debug(f"Parsing file: {file_path}")
            doc = parse(file_path, recursive=False, **kwargs)
            documents.append(doc)
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            failed_files.append((file_path, str(e)))
    
    # Log results
    logger.info(f"Successfully parsed {len(documents)} files")
    if failed_files:
        logger.warning(f"Failed to parse {len(failed_files)} files:")
        for file_path, error in failed_files:
            logger.warning(f"  {file_path}: {error}")
    
    return documents

def parse_folder_unified(folder_path: Pathish, recursive: bool = True,
                        file_patterns: Optional[List[str]] = None,
                        exclude_patterns: Optional[List[str]] = None,
                        show_progress: bool = True,
                        **kwargs) -> UnifiedDocument:
    """
    Parse all supported files in a folder and combine them into a single UnifiedDocument.
    
    Args:
        folder_path: Path to the folder to parse
        recursive: Whether to scan subdirectories recursively
        file_patterns: List of file patterns to include
        exclude_patterns: List of patterns to exclude
        show_progress: Whether to show progress bar
        **kwargs: Additional arguments passed to individual file parsers
    
    Returns:
        Single UnifiedDocument containing all parsed content
    """
    documents = parse_folder(folder_path, recursive, file_patterns, exclude_patterns, show_progress, **kwargs)
    
    if not documents:
        # Return empty document
        folder_path = pathlib.Path(folder_path)
        meta = Metadata(
            source=str(folder_path),
            content_type="application/x-folder",
            path=str(folder_path)
        )
        return UnifiedDocument(meta=meta, sections=[])
    
    # Combine all documents into one
    combined_doc = documents[0]  # Start with first document
    
    # Update metadata to reflect folder source
    folder_path = pathlib.Path(folder_path)
    combined_doc.meta.source = str(folder_path)
    combined_doc.meta.content_type = "application/x-folder"
    combined_doc.meta.path = str(folder_path)
    
    # Add sections from other documents
    for i, doc in enumerate(documents[1:], 1):
        # Add a separator section
        separator_section = Section(
            heading=f"--- File {i+1}: {doc.meta.source} ---",
            chunks=[],
            meta={"file_separator": True, "original_file": doc.meta.source}
        )
        combined_doc.sections.append(separator_section)
        
        # Add all sections from the document
        for section in doc.sections:
            # Update section metadata to include original file info
            section.meta["original_file"] = doc.meta.source
            combined_doc.sections.append(section)
        
        # Add images from the document
        for image in doc.images:
            image.meta["original_file"] = doc.meta.source
            combined_doc.images.append(image)
    
    return combined_doc
