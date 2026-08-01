"""
File signature (magic number) definitions for Phase 1.

A carver identifies files purely from the byte patterns that mark their start
(header) and, where one exists, their end (footer). This module is the small
catalogue of signatures the engine understands; the carving logic lives in
``engine.py`` because most formats need more than a naive header/footer match
to find their true length.
"""

from dataclasses import dataclass
from typing import List, Optional

_MB = 1024 * 1024


@dataclass(frozen=True)
class Signature:
    key: str                 # short id, e.g. "jpg"
    name: str                # human friendly name
    ext: str                 # file extension for carved output
    header: bytes            # magic bytes at offset 0 of the file
    footer: Optional[bytes]  # trailing magic, if the format has one
    max_size: int            # safety cap on how far we will carve (bytes)
    description: str = ""


SIGNATURES: List[Signature] = [
    Signature("jpg", "JPEG image", "jpg",
              b"\xff\xd8\xff", b"\xff\xd9", 50 * _MB,
              "Start Of Image FF D8 FF ... End Of Image FF D9"),
    Signature("png", "PNG image", "png",
              b"\x89PNG\r\n\x1a\n", b"IEND\xae\x42\x60\x82", 50 * _MB,
              "8-byte signature; chunk-walked to the IEND chunk"),
    Signature("pdf", "PDF document", "pdf",
              b"%PDF", b"%%EOF", 200 * _MB,
              "%PDF header ... last %%EOF trailer"),
    Signature("zip", "ZIP archive", "zip",
              b"PK\x03\x04", b"PK\x05\x06", 500 * _MB,
              "Local file header PK 03 04 ... End Of Central Directory PK 05 06"),
]

# A carved ZIP is inspected for these marker parts to identify Office documents.
# marker inside archive -> (key, extension, friendly name)
OOXML_SUBTYPES = [
    ("word/document.xml",    ("docx", "docx", "Word document")),
    ("xl/workbook.xml",      ("xlsx", "xlsx", "Excel workbook")),
    ("ppt/presentation.xml", ("pptx", "pptx", "PowerPoint presentation")),
]

SIGNATURE_BY_KEY = {s.key: s for s in SIGNATURES}
ALL_FORMAT_KEYS = [s.key for s in SIGNATURES] + ["docx", "xlsx", "pptx"]
