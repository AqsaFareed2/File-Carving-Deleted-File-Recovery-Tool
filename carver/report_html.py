"""
Phase 3 - Task B: HTML report.

Owner:  <assign a teammate>
Tests:  tests/test_report_html.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``write_html(data, path)`` so it writes a single, self-contained HTML
page (all CSS inline -- no external files) that a forensic analyst can open in a
browser. It should show:

  * a header with the image path/size and the summary counts (recovered,
    duplicates, embedded; optionally the by-format / by-confidence breakdown);
  * a TABLE of the recovered files, one row each, with: #, type, offset
    (offset_hex), size, confidence, sha256 (a short prefix is fine), notes;
  * confidence shown as a colour-coded badge -- e.g. green for "high", amber for
    "medium", red for "low".

``data`` is the canonical summary from ``carver.report.report_data`` (see
carver/report_json.py for its full shape). Use ``html.escape`` on any text that
comes from the image (paths, notes) to avoid breaking the markup. You only edit
THIS file and tests/test_report_html.py.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_report_html.py)
--------------------------------------------------------------------------
The written file contains a <table>, has one row per recovered file (each
file's offset_hex appears), and shows the confidence values.
"""


def write_html(data: dict, path: str) -> None:
    """Write ``data`` to ``path`` as a self-contained HTML report.

    TODO(Task B): implement. This stub is a no-op (writes nothing), so the
    acceptance test fails until you implement it.
    """
    return
