"""
ACCEPTANCE TEST for Phase 3 - Task B (HTML report).

RED until carver/report_html.py::write_html is implemented.
Run:  python tests/test_report_html.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_test_image as mti
from carver import DiskImage, scan
from carver.report import report_data
from carver.report_html import write_html


def _data():
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "img.dd")
    mti.build(p, size_mb=8, quiet=True)
    with DiskImage(p) as img:
        return report_data(scan(img))


def test_html_has_table_and_one_row_per_file():
    data = _data()
    out = os.path.join(tempfile.mkdtemp(), "report.html")
    write_html(data, out)
    html = open(out, encoding="utf-8").read().lower()
    assert "<table" in html, "report should contain a table"
    for f in data["files"]:
        assert f["offset_hex"] in html, f"missing row for {f['offset_hex']}"
    assert any(level in html for level in ("high", "medium", "low")), \
        "confidence levels should be shown"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except Exception as e:
                failures += 1; print(f"FAIL  {name}: {e!r}")
    sys.exit(1 if failures else 0)
