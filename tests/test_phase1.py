"""
Phase 1 end-to-end test: build the synthetic image, carve it, and check that
the planted files are recovered at their exact offset and size.

Run with:  python tests/test_phase1.py   (or:  python -m pytest -q)
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


def test_known_files_recovered_at_exact_offset_and_size():
    res = _scan()
    by_off = {c.start: c for c in res.candidates}
    expected = {
        0x001000: ("png", 69),
        0x080000: ("jpg", 160),
        0x120000: ("pdf", 456),
        0x1C0000: ("zip", 312),
        0x260000: ("docx", 912),
    }
    for off, (fmt, size) in expected.items():
        assert off in by_off, f"missing file at {off:#x}"
        assert by_off[off].fmt == fmt, (off, by_off[off].fmt)
        assert by_off[off].size == size, (off, by_off[off].size)


def test_docx_classified_from_zip():
    res = _scan()
    assert any(c.fmt == "docx" for c in res.candidates)


def test_phase1_does_not_deduplicate_or_drop():
    # Phase 1 reports raw candidates: the duplicate JPEG and the truncated PNG
    # both appear (de-dup and fragmentation handling are later phases).
    res = _scan()
    assert 0x320000 in {c.start for c in res.candidates}, "duplicate JPEG missing"
    assert 0x3C0000 in {c.start for c in res.candidates}, "truncated PNG missing"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL  {name}: {e}")
    sys.exit(1 if failures else 0)
