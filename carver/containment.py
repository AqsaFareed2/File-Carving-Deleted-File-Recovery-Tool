"""
Phase 2 - Task 3: Containment / embedded-object resolution.

Owner:  <assign a teammate>
Tests:  tests/test_containment.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Signature scanning finds files that are physically stored inside other files --
for example a JPEG thumbnail inside a PDF, or media inside an Office document.
Those should not be reported as standalone recoveries.

Implement ``resolve_containment(candidates)`` so that any candidate whose byte
range [start, end) lies fully inside a larger, different candidate is flagged:

    inner.embedded_in = <start offset of the containing candidate>

Rules:
  * "fully inside" means  outer.start <= inner.start  and  inner.end <= outer.end
    and outer.size > inner.size (the container is strictly bigger).
  * Only the *outermost* container needs to be recorded; a top-level file keeps
    embedded_in = None.
  * Do not flag a candidate as embedded in itself.

You only edit THIS file and tests/test_containment.py. Do not touch engine.py or
cli.py -- the Candidate field and the call site already exist. Once embedded_in
is set, the CLI/report drops embedded objects from the recovered set (see
ScanResult.recovered).

Note: this pass needs only the offsets/sizes already on each candidate, so it
does not require the image buffer.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_containment.py)
--------------------------------------------------------------------------
Given an image with a JPEG stored inside a PDF, the JPEG candidate is flagged
embedded_in == <the PDF's start offset> and the PDF candidate keeps
embedded_in is None.
"""


def resolve_containment(candidates) -> None:
    """Flag candidates contained within a larger candidate by setting
    ``c.embedded_in`` (in place).

    TODO(Task 3): implement containment detection. This stub is a no-op, so
    every candidate keeps embedded_in == None.
    """
    return
