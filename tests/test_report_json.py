"""
ACCEPTANCE TEST for Phase 3 - Task A (JSON report).

RED until carver/report_json.py::write_json is implemented.
Run:  python tests/test_report_json.py
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_test_image as mti
from carver import DiskImage, scan
from carver.report import report_data
from carver.report_json import write_json


def _data():
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "img.dd")
    mti.build(p, size_mb=8, quiet=True)
    with DiskImage(p) as img:
        return report_data(scan(img))


def test_json_is_valid_and_complete():
    data = _data()
    out = os.path.join(tempfile.mkdtemp(), "report.json")
    write_json(data, out)
    with open(out, encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["summary"]["recovered"] == data["summary"]["recovered"]
    assert len(loaded["files"]) == len(data["files"])
    assert all(len(f["sha256"]) == 64 for f in loaded["files"])


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except Exception as e:
                failures += 1; print(f"FAIL  {name}: {e!r}")
    sys.exit(1 if failures else 0)
