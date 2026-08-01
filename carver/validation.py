"""
Phase 2 - Task 1: Validation & Confidence Scoring.

Owner:  <assign a teammate>
Tests:  tests/test_validation.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``assign_confidence(candidates, buf)`` so that every carved candidate
gets a ``.confidence`` of "high", "medium" or "low", based on how well its bytes
validate against the format's own structure. This pass also delivers the project
scope item "handle fragmentation gracefully": a truncated or footer-less file
must come out as "low" rather than being silently trusted.

You only edit THIS file and tests/test_validation.py. Do not touch engine.py or
cli.py -- the Candidate fields and the call site already exist.

Each candidate ``c`` has: c.fmt, c.start, c.end, c.size, c.note, and the field
you set here, c.confidence. Read the carved bytes with:

    data = bytes(buf[c.start:c.end])

Suggested rules (refine as you like, but keep three levels):

  PNG   chunk structure walks cleanly to IEND ................ high
        walk broke before IEND (truncated) .................. low
  JPG   starts FF D8 FF, ends FF D9, has APP0/APP1/DQT marker  high
        header + FF D9 only, no JFIF/EXIF/DQT ............... medium
        no FF D9 (see c.note) .............................. low
  PDF   %PDF ... %%EOF and contains 'startxref'/'xref' ...... high
        %PDF ... %%EOF but no xref ......................... medium
        no %%EOF (see c.note) .............................. low
  ZIP/DOCX/XLSX/PPTX
        zipfile opens and testzip() passes ................. high
        opens but a CRC fails (partial) .................... medium
        will not open ...................................... low

You may also append a short explanation to c.note.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_validation.py)
--------------------------------------------------------------------------
On the synthetic test image the five clean files (png/jpg/pdf/zip/docx) are
"high" and the truncated PNG at offset 0x3c0000 is "low".
"""

# NOTE: do not `import` Candidate from engine (that would be circular). The
# candidates are passed in; treat them by their attributes.

HIGH = "high"
MEDIUM = "medium"
LOW = "low"


def assign_confidence(candidates, buf) -> None:
    """Set ``c.confidence`` for every candidate in ``candidates`` (in place).

    ``buf`` is the searchable image buffer (supports slicing and len()).

    TODO(Task 1): implement per-format validation. This stub is a no-op, so
    every candidate keeps its default confidence of "unknown".
    """
    return
