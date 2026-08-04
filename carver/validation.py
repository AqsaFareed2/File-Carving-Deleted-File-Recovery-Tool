import io
import zipfile

# NOTE: do not `import` Candidate from engine (that would be circular). The
# candidates are passed in; treat them by their attributes.

HIGH = "high"
MEDIUM = "medium"
LOW = "low"


def _validate_png(data):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return LOW

    pos = 8
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], "big")
        chunk = data[pos + 4:pos + 8]
        nxt = pos + 12 + length

        if nxt > len(data):
            return LOW

        if chunk == b"IEND":
            return HIGH

        pos = nxt

    return LOW


def _validate_jpg(data):
    if not data.startswith(b"\xff\xd8\xff"):
        return LOW

    if not data.endswith(b"\xff\xd9"):
        return LOW

    if b"JFIF" in data or b"Exif" in data or b"\xff\xdb" in data:
        return HIGH

    return MEDIUM


def _validate_pdf(data):
    if not data.startswith(b"%PDF"):
        return LOW

    if b"%%EOF" not in data:
        return LOW

    if b"xref" in data or b"startxref" in data:
        return HIGH

    return MEDIUM


def _validate_zip(data):
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))

        if zf.testzip() is None:
            return HIGH

        return MEDIUM

    except Exception:
        return LOW


def assign_confidence(candidates, buf):
    """
    Set confidence for every carved candidate.
    """

    for c in candidates:

        data = bytes(buf[c.start:c.end])

        if c.fmt == "png":
            c.confidence = _validate_png(data)

        elif c.fmt == "jpg":
            c.confidence = _validate_jpg(data)

        elif c.fmt == "pdf":
            c.confidence = _validate_pdf(data)

        elif c.fmt in ("zip", "docx", "xlsx", "pptx"):
            c.confidence = _validate_zip(data)

        else:
            c.confidence = LOW