"""
ACCEPTANCE TEST for Phase 2 - Task 3 (Containment / embedded-object resolution).

This test is RED until carver/containment.py::resolve_containment is implemented.
Run:  python tests/test_containment.py  (or: python -m pytest -q tests/test_containment.py)
"""

import os
import random
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import make_test_image as mti
from carver import DiskImage, scan


def _image_with_jpeg_inside_pdf():
    """A 1 MiB image whose only planted object is a PDF that embeds a JPEG, so
    the JPEG's byte range sits fully inside the PDF's byte range."""
    jpeg = mti._JPEG_1x1
    blob = (b"%PDF-1.4\n% a JPEG is embedded just below\n"
            + jpeg + b"\nstartxref\n0\n%%EOF\n")
    rnd = random.Random(5)
    data = bytearray(rnd.getrandbits(8) for _ in range(1024 * 1024))
    off = 0x1000
    data[off:off + len(blob)] = blob
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "img.dd")
    with open(path, "wb") as fh:
        fh.write(bytes(data))
    return path


def test_jpeg_inside_pdf_is_flagged_embedded():
    with DiskImage(_image_with_jpeg_inside_pdf()) as img:
        res = scan(img)
    pdfs = [c for c in res.candidates if c.fmt == "pdf"]
    jpgs = [c for c in res.candidates if c.fmt == "jpg"]
    assert pdfs and jpgs, "expected both a PDF and a JPEG candidate"
    pdf, jpg = pdfs[0], jpgs[0]
    # sanity: the JPEG really is inside the PDF
    assert pdf.start <= jpg.start and jpg.end <= pdf.end
    assert jpg.embedded_in == pdf.start, jpg.embedded_in
    assert pdf.embedded_in is None


def test_embedded_dropped_from_recovered():
    with DiskImage(_image_with_jpeg_inside_pdf()) as img:
        res = scan(img)
    fmts = {c.fmt for c in res.recovered}
    assert "pdf" in fmts and "jpg" not in fmts


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"PASS  {name}")
            except AssertionError as e:
                failures += 1; print(f"FAIL  {name}: {e}")
    sys.exit(1 if failures else 0)
