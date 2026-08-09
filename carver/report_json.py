"""
Phase 3 - Task A: JSON report.

Owner:  <assign a teammate>
Tests:  tests/test_report_json.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``write_json(data, path)`` so it writes the report ``data`` to
``path`` as a valid, pretty-printed JSON file (machine-readable output that
other tools can consume).

``data`` is the canonical summary produced by ``carver.report.report_data`` --
you do NOT build it yourself. Its shape is:

    {
      "tool", "version", "generated_utc",
      "image": {"path", "size"},
      "summary": {"recovered", "duplicates", "embedded",
                  "by_format": {...}, "by_confidence": {...}},
      "files":      [ {index, format, offset, offset_hex, size, confidence,
                       sha256, note, duplicate_of, embedded_in, filename}, ... ],
      "duplicates": [ ...same shape... ],
      "embedded":   [ ...same shape... ],
    }

Everything is already JSON-safe (plain ints/strings/lists/dicts), so this is
essentially ``json.dump`` with indentation and UTF-8. You only edit THIS file
and tests/test_report_json.py.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_report_json.py)
--------------------------------------------------------------------------
The written file parses with ``json.load``; its "summary" and "files" match the
input data (one entry per recovered file, each with a 64-char sha256).
"""


def write_json(data: dict, path: str) -> None:
    """Write ``data`` to ``path`` as JSON.

    TODO(Task A): implement. This stub is a no-op (writes nothing), so the
    acceptance test fails until you implement it.
    """
    return
