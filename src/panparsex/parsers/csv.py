from __future__ import annotations
from typing import Iterable
import csv
import io
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class CSVParser(ParserProtocol):
    name = "csv"
    content_types: Iterable[str] = ("text/csv", "application/csv")
    extensions: Iterable[str] = (".csv",)

    def can_parse(self, meta: Metadata) -> bool:
        return (meta.content_type in self.content_types or 
                (meta.path or "").endswith(".csv"))

    def parse(self, target, meta: Metadata, recursive: bool = False, **kwargs) -> UnifiedDocument:
        doc = UnifiedDocument(meta=meta, sections=[])
        
        try:
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                # Try to detect delimiter
                sample = f.read(1024)
                f.seek(0)
                
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(f, delimiter=delimiter)
                rows = list(reader)
                
                if not rows:
                    doc.sections.append(Section(
                        heading="Error",
                        chunks=[Chunk(text="[panparsex:csv] Empty CSV file", order=0, meta={"error": True})],
                        meta={"error": True}
                    ))
                    return doc
                
                # Extract headers
                headers = rows[0] if rows else []
                data_rows = rows[1:] if len(rows) > 1 else []
                
                # Create sections for different views of the data
                if headers:
                    # Header section
                    header_text = " | ".join(headers)
                    doc.sections.append(Section(
                        heading="Headers",
                        chunks=[Chunk(text=header_text, order=0, meta={"type": "headers"})],
                        meta={"row_count": len(headers)}
                    ))
                
                # Data section
                if data_rows:
                    data_text = "\n".join([" | ".join(row) for row in data_rows])
                    doc.sections.append(Section(
                        heading="Data",
                        chunks=[Chunk(text=data_text, order=1, meta={"type": "data"})],
                        meta={"row_count": len(data_rows), "column_count": len(headers)}
                    ))
                
                # Summary section
                summary = f"CSV Summary: {len(headers)} columns, {len(data_rows)} data rows"
                doc.sections.append(Section(
                    heading="Summary",
                    chunks=[Chunk(text=summary, order=2, meta={"type": "summary"})],
                    meta={"total_rows": len(rows), "data_rows": len(data_rows)}
                ))
                
                # Store raw data in metadata for programmatic access
                doc.meta.extra["csv_data"] = {
                    "headers": headers,
                    "rows": data_rows,
                    "delimiter": delimiter
                }
                
        except Exception as e:
            error_text = f"[panparsex:csv] unable to parse: {e}"
            doc.sections.append(Section(
                heading="Error",
                chunks=[Chunk(text=error_text, order=0, meta={"error": True})],
                meta={"error": True}
            ))
        
        return doc

register_parser(CSVParser())
