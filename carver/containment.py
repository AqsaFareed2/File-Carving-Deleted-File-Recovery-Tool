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

    A candidate ``inner`` is embedded when some other candidate ``outer`` fully
    covers its byte range and is strictly larger:

        outer.start <= inner.start  and  inner.end <= outer.end
        and outer.size > inner.size

    When several candidates contain ``inner`` (nesting), we record the
    outermost one -- the largest container -- so the field points at the
    top-level file. A standalone file keeps ``embedded_in = None``.
    """
    for inner in candidates:
        container_start = None
        container_size = -1
        for outer in candidates:
            if outer is inner:
                continue
            if (outer.start <= inner.start and inner.end <= outer.end
                    and outer.size > inner.size):
                # keep the largest (outermost) container
                if outer.size > container_size:
                    container_size = outer.size
                    container_start = outer.start
        if container_start is not None:
            inner.embedded_in = container_start
