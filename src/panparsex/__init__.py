# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Dhruvil Darji

__version__ = "0.5.0"

from .core import parse, ParserProtocol, register_parser, get_registry, parse_folder, parse_folder_unified, ParsingSummary
from .types import UnifiedDocument, Section, Chunk, Metadata

__all__ = [
    "parse",
    "parse_folder",
    "parse_folder_unified",
    "ParsingSummary",
    "ParserProtocol",
    "register_parser",
    "get_registry",
    "UnifiedDocument",
    "Section",
    "Chunk",
    "Metadata",
]
