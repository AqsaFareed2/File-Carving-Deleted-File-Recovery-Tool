"""
ACCEPTANCE TEST for Phase 2 - Task 1 (Validation & Confidence Scoring).

This test is RED until carver/validation.py::assign_confidence is implemented.
Run:  python tests/test_validation.py    (or: python -m pytest -q tests/test_validation.py)
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_test_image as mti
from carver import DiskImage, scan


def _scan():
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "img.dd")
    mti.build(path, size_mb=8, quiet=True)
    with DiskImage(path) as img:
        return scan(img)


def test_clean_files_are_high_confidence():
    by_off = {c.start: c for c in _scan().candidates}
    for off in (0x001000, 0x080000, 0x120000, 0x1C0000, 0x260000):  # png jpg pdf zip docx
        assert by_off[off].confidence == "high", \
            (hex(off), by_off[off].fmt, by_off[off].confidence)


def test_truncated_png_is_low_confidence():
    by_off = {c.start: c for c in _scan().candidates}
    assert by_off[0x3C0000].confidence == "low", by_off[0x3C0000].confidence


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except AssertionError as e:
                failures += 1; print(f"FAIL  {name}: {e}")
    sys.exit(1 if failures else 0)
