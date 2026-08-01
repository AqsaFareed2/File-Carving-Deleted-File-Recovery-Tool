#!/usr/bin/env python3
"""
Build a synthetic raw disk image for testing the Phase 1 carver.

The image is filled with pseudo-random "unallocated" noise and real files are
written at known offsets, mimicking data left behind after the file table is
gone. It prints the ground-truth layout so it can be compared against what the
carver recovers.

Usage:  python make_test_image.py [output.dd] [--size-mb N]
"""

import argparse
import base64
import io
import random
import struct
import zipfile
import zlib

# A real 1x1 baseline JPEG (valid FF D8 ... FF D9), kept as a constant so the
# generator needs no imaging library.
_JPEG_1x1 = base64.b64decode(
    "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRof"
    "Hh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAAB"
    "AAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AfwD/2Q==")


def make_png(width=1, height=1, rgb=(220, 40, 40)) -> bytes:
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = b""
    for _ in range(height):
        raw += b"\x00" + bytes(rgb) * width
    idat = zlib.compress(raw, 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def make_pdf() -> bytes:
    objs = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] "
        b"/Contents 4 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 18 Tf 20 100 Td "
        b"(Recovered!) Tj ET\nendstream\nendobj\n",
    ]
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for obj in objs:
        offsets.append(out.tell())
        out.write(obj)
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1))
    for off in offsets:
        out.write(("%010d 00000 n \n" % off).encode())
    out.write(b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objs) + 1))
    out.write(b"startxref\n%d\n" % xref)
    out.write(b"%%EOF\n")  # write separately: '%%' in a %-formatted bytes is '%'
    return out.getvalue()


def make_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("readme.txt", "This ZIP was carved out of unallocated space.\n")
        zf.writestr("data/notes.txt", "Second entry to give the archive structure.\n")
    return buf.getvalue()


def make_docx() -> bytes:
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.'
          'openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body><w:p><w:r><w:t>Recovered Word document.</w:t></w:r></w:p></w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", ct)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", doc)
    return buf.getvalue()


def build(path, size_mb, quiet=False):
    size = size_mb * 1024 * 1024
    rnd = random.Random(1337)
    image = bytearray(rnd.getrandbits(8) for _ in range(size))

    jpeg, png, pdf = _JPEG_1x1, make_png(), make_pdf()
    zip_bytes, docx = make_zip(), make_docx()
    truncated_png = png[: len(png) // 2]

    layout = [
        ("PNG image",              png,           0x001000),
        ("JPEG image",             jpeg,          0x080000),
        ("PDF document",           pdf,           0x120000),
        ("ZIP archive",            zip_bytes,     0x1C0000),
        ("DOCX (Word)",            docx,          0x260000),
        ("JPEG image (DUPLICATE)", jpeg,          0x320000),
        ("PNG (TRUNCATED)",        truncated_png, 0x3C0000),
    ]
    placed = []
    for label, data, off in layout:
        if off + len(data) > size:
            raise SystemExit(f"image too small for {label}; use a larger --size-mb")
        image[off:off + len(data)] = data
        placed.append((label, off, len(data)))

    with open(path, "wb") as fh:
        fh.write(image)

    if quiet:
        return
    print(f"Wrote {path}  ({size_mb} MiB)")
    print("\nGround truth (what the carver should find):")
    print(f"  {'OFFSET':>12}  {'SIZE':>8}  DESCRIPTION")
    for label, off, ln in placed:
        print(f"  {off:>#12x}  {ln:>8}  {label}")


def main():
    ap = argparse.ArgumentParser(description="Generate a test disk image.")
    ap.add_argument("output", nargs="?", default="test_image.dd")
    ap.add_argument("--size-mb", type=int, default=8)
    args = ap.parse_args()
    build(args.output, args.size_mb)


if __name__ == "__main__":
    main()
