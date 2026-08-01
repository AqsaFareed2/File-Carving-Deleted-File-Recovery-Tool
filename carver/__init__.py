"""
carver (Phase 1) -- core file-carving engine.

Phase 1 scope: read a raw or E01 disk image without a file system, scan it for
the header signatures of JPG, PNG, PDF, ZIP and DOCX, carve each candidate file
by determining its true extent, and report the byte offset and size of each.

Validation and confidence scoring, fragmentation reassembly, de-duplication by
hash, rich reports, the GUI and live drive acquisition belong to later phases
and are intentionally not part of this package.
"""

__version__ = "1.0.0-phase1"

from .engine import scan, Candidate, ScanResult
from .image_reader import DiskImage

__all__ = ["scan", "Candidate", "ScanResult", "DiskImage", "__version__"]
