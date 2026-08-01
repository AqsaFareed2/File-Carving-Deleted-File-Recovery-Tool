"""
ACCEPTANCE TEST for Phase 2 - Task 2 (De-duplication by SHA-256).

This test is RED until carver/dedup.py::deduplicate is implemented.
Run:  python tests/test_dedup.py    (or: python -m pytest -q tests/test_dedup.py)
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


def test_every_candidate_has_a_hash():
    res = _scan()
    assert all(len(c.sha256) == 64 for c in res.candidates), \
        "each candidate should have a 64-char hex SHA-256"


def test_duplicate_jpeg_is_flagged():
    by_off = {c.start: c for c in _scan().candidates}
    first = by_off[0x080000]        # original JPEG
    dup = by_off[0x320000]          # byte-for-byte duplicate
    assert first.sha256 == dup.sha256 and first.sha256 != ""
    assert first.duplicate_of is None
    assert dup.duplicate_of == 0x080000, dup.duplicate_of


def test_duplicate_dropped_from_recovered():
    res = _scan()
    starts = {c.start for c in res.recovered}
    assert 0x080000 in starts and 0x320000 not in starts


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except AssertionError as e:
                failures += 1; print(f"FAIL  {name}: {e}")
    sys.exit(1 if failures else 0)
