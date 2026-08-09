"""
ACCEPTANCE TEST for Phase 3 - Task C (CSV evidence log).

RED until carver/report_csv.py::write_csv is implemented.
Run:  python tests/test_report_csv.py
"""

import csv
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_test_image as mti
from carver import DiskImage, scan
from carver.report import report_data
from carver.report_csv import write_csv


def _data():
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "img.dd")
    mti.build(p, size_mb=8, quiet=True)
    with DiskImage(p) as img:
        return report_data(scan(img))


def test_csv_header_and_one_row_per_file():
    data = _data()
    out = os.path.join(tempfile.mkdtemp(), "report.csv")
    write_csv(data, out)
    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) == 1 + len(data["files"]), \
        f"expected header + {len(data['files'])} rows, got {len(rows)}"
    header = " ".join(rows[0]).lower()
    for col in ("offset", "size", "confidence", "sha256"):
        assert col in header, f"header missing '{col}' column"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except Exception as e:
                failures += 1; print(f"FAIL  {name}: {e!r}")
    sys.exit(1 if failures else 0)
