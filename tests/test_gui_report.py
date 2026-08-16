"""
ACCEPTANCE TEST for Phase 4 - Task B (Reports & Export panel).

RED until carver/gui/report_view.py::save_report is implemented.
Needs a display; skips automatically where Tk cannot open.
Run:  python tests/test_gui_report.py
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

import make_test_image as mti
from carver import DiskImage, scan
from carver.gui.app import AppState
from carver.gui.report_view import ReportView


def _result():
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "img.dd")
    mti.build(p, size_mb=8, quiet=True)
    with DiskImage(p) as img:
        return scan(img)


def _root():
    try:
        r = tk.Tk()
        r.withdraw()
        return r
    except tk.TclError as exc:
        raise unittest.SkipTest(f"no display: {exc}")


def test_report_view_writes_valid_json():
    root = _root()
    try:
        app = AppState()
        res = _result()
        app.set_result(res)
        view = ReportView(root, app)
        out = os.path.join(tempfile.mkdtemp(), "report.json")
        view.save_report("json", out)
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
        assert data["summary"]["recovered"] == len(res.recovered)
    finally:
        root.destroy()


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except unittest.SkipTest as e:
                print(f"SKIP  {name}: {e}")
            except Exception as e:
                failures += 1; print(f"FAIL  {name}: {e!r}")
    sys.exit(1 if failures else 0)
