"""
Phase 3 - Reporting (shared scaffolding).

Every report format (JSON, HTML, CSV) is rendered from ONE canonical, JSON-safe
summary produced by :func:`report_data`. The renderers never re-walk the scan
result, so they stay independent of one another -- each task implements one
renderer that consumes this dict.

    data = report_data(result)          # this module (scaffolding, done)
    write_json(data, "report.json")     # Task A -> carver/report_json.py
    write_html(data, "report.html")     # Task B -> carver/report_html.py
    write_csv(data,  "report.csv")      # Task C -> carver/report_csv.py

``write_report(result, kind, path)`` is the convenience dispatcher the CLI uses.
"""

from collections import Counter
from datetime import datetime, timezone

from . import __version__
from .report_json import write_json
from .report_html import write_html
from .report_csv import write_csv


def _record(index, c) -> dict:
    """One JSON-safe record for a carved file."""
    return {
        "index": index,
        "format": c.fmt,
        "offset": c.start,
        "offset_hex": f"{c.start:#x}",
        "size": c.size,
        "confidence": c.confidence,
        "sha256": c.sha256,
        "note": c.note,
        "duplicate_of": c.duplicate_of,
        "embedded_in": c.embedded_in,
        "filename": f"{index:04d}_{c.fmt}_{c.start:x}.{c.ext}",
    }


def report_data(result) -> dict:
    """Build the canonical, serializable summary of a :class:`ScanResult`.

    This is the single source of truth for all report formats. It is a plain
    dict of built-in types (safe for ``json.dump`` and easy to iterate).
    """
    recovered = result.recovered
    return {
        "tool": "carver",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "image": {"path": result.image_path, "size": result.image_size},
        "summary": {
            "recovered": len(recovered),
            "duplicates": len(result.duplicates),
            "embedded": len(result.embedded),
            "by_format": dict(Counter(c.fmt for c in recovered)),
            "by_confidence": dict(Counter(c.confidence for c in recovered)),
        },
        "files": [_record(i, c) for i, c in enumerate(recovered, 1)],
        "duplicates": [_record(i, c) for i, c in enumerate(result.duplicates, 1)],
        "embedded": [_record(i, c) for i, c in enumerate(result.embedded, 1)],
    }


_WRITERS = {"json": write_json, "html": write_html, "csv": write_csv}


def write_report(result, kind: str, path: str) -> None:
    """Render ``result`` to ``path`` in the given format ('json'/'html'/'csv')."""
    _WRITERS[kind](report_data(result), path)
