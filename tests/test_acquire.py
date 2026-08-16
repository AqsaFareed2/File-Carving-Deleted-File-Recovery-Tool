"""
ACCEPTANCE TEST for Phase 4 - Task C (drive acquisition backend).

RED until carver/acquire.py::image_source is implemented. This test is pure
logic (no display): it images a regular file read-only, which needs no drive or
Administrator rights.
Run:  python tests/test_acquire.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from carver import acquire


def test_list_drives_returns_a_list():
    assert isinstance(acquire.list_drives(), list)


def test_image_source_copies_exact_bytes():
    data = os.urandom(300 * 1024)
    src = os.path.join(tempfile.mkdtemp(), "src.bin")
    with open(src, "wb") as f:
        f.write(data)
    out = os.path.join(tempfile.mkdtemp(), "out.dd")

    n = acquire.image_source(src, out, max_bytes=200 * 1024)
    assert n == 200 * 1024, f"expected 204800 bytes, got {n}"
    with open(out, "rb") as f:
        assert f.read() == data[:200 * 1024], "copied bytes do not match source"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except Exception as e:
                failures += 1; print(f"FAIL  {name}: {e!r}")
    sys.exit(1 if failures else 0)
