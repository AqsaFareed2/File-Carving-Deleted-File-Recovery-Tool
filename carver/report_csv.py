"""
Phase 3 - Task C: CSV evidence log.

Owner:  <assign a teammate>
Tests:  tests/test_report_csv.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``write_csv(data, path)`` so it writes the recovered files as a CSV
"evidence log" -- the kind of spreadsheet-friendly list used in case management.

  * one header row, then one row per recovered file;
  * columns (in this order): index, type, offset (offset_hex), size,
    confidence, sha256, filename;
  * use the standard-library ``csv`` module and open the file with
    ``newline=""`` so rows are not double-spaced on Windows.

``data`` is the canonical summary from ``carver.report.report_data`` (see
carver/report_json.py for its full shape); iterate ``data["files"]``. You only
edit THIS file and tests/test_report_csv.py.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_report_csv.py)
--------------------------------------------------------------------------
The file opens with ``csv.reader`` and has exactly 1 + N rows (header + one per
recovered file), and the header includes offset, size, confidence and sha256.
"""


def write_csv(data: dict, path: str) -> None:
    """Write the recovered files in ``data`` to ``path`` as CSV.

    TODO(Task C): implement. This stub is a no-op (writes nothing), so the
    acceptance test fails until you implement it.
    """
    return
