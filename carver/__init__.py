"""
carver -- signature-based file carving engine.

Phase 1 (done): read a raw or E01 disk image without a file system, scan it for
the header signatures of JPG, PNG, PDF, ZIP and DOCX, carve each candidate file
by determining its true extent, and report the byte offset and size of each.

Phase 2 (in progress): post-processing passes that add per-file confidence
scoring (carver/validation.py), de-duplication by SHA-256 (carver/dedup.py) and
containment/embedded-object resolution (carver/containment.py). See TASKS.md.
"""

__version__ = "3.0.0-phase3.dev"

from .engine import scan, Candidate, ScanResult
from .image_reader import DiskImage

__all__ = ["scan", "Candidate", "ScanResult", "DiskImage", "__version__"]
