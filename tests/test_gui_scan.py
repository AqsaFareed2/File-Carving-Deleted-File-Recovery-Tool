"""
ACCEPTANCE TEST for Phase 4 - Task A (Scan & Results panel).

RED until carver/gui/scan_view.py fills its results table.
Needs a display; skips automatically where Tk cannot open (e.g. headless CI).
Run:  python tests/test_gui_scan.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk

import make_test_image as mti
from carver import DiskImage, scan
from carver.gui.app import AppState
from carver.gui.scan_view import ScanView


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


def test_results_table_has_one_row_per_recovered_file():
    root = _root()
    try:
        app = AppState()
        res = _result()
        app.set_result(res)
        view = ScanView(root, app)
        view.refresh()
        rows = view.tree.get_children()
        assert len(rows) == len(res.recovered), (len(rows), len(res.recovered))
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
