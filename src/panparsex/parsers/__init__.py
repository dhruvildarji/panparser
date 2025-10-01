# Import all parsers to ensure they are registered
from . import text
from . import json_
from . import yaml_
from . import xml
from . import html
from . import pdf
from . import web
from . import csv
from . import docx
from . import markdown
from . import rtf
from . import excel
from . import pptx

__all__ = [
    "text",
    "json_",
    "yaml_",
    "xml",
    "html",
    "pdf",
    "web",
    "csv",
    "docx",
    "markdown",
    "rtf",
    "excel",
    "pptx",
]
