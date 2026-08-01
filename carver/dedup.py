"""
Phase 2 - Task 2: De-duplication by SHA-256.

Owner:  <assign a teammate>
Branch: feature/dedup
Tests:  tests/test_dedup.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``deduplicate(candidates, buf)`` so that:

  * every candidate gets its content hash in ``c.sha256`` (hex SHA-256 of the
    carved bytes, i.e. hashlib.sha256(bytes(buf[c.start:c.end])).hexdigest());
  * when two carved files have the same hash, the *later* one (by offset) is
    marked as a duplicate of the first by setting
        c.duplicate_of = <start offset of the first copy>.
    The first copy keeps c.duplicate_of = None.

You only edit THIS file and tests/test_dedup.py. Do not touch engine.py or
cli.py -- the Candidate fields and the call site already exist. Once
duplicate_of is set, the CLI/report automatically drops duplicates from the
recovered set (see ScanResult.recovered).

Tip: hash large files in chunks to avoid copying the whole thing at once, e.g.

    import hashlib
    h = hashlib.sha256()
    pos = c.start
    while pos < c.end:
        chunk = bytes(buf[pos:min(pos + (1 << 20), c.end)])
        h.update(chunk); pos += len(chunk)
    c.sha256 = h.hexdigest()

Process candidates in offset order so "first copy" is deterministic.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_dedup.py)
--------------------------------------------------------------------------
On the synthetic test image the duplicate JPEG at 0x320000 gets the same
sha256 as the file at 0x80000 and duplicate_of == 0x80000; the file at
0x80000 has duplicate_of is None.
"""


def deduplicate(candidates, buf) -> None:
    """Set ``c.sha256`` for every candidate and mark repeats with
    ``c.duplicate_of`` (in place).

    TODO(Task 2): implement hashing + duplicate detection. This stub is a
    no-op, so every candidate keeps sha256 == "" and duplicate_of == None.
    """
    return
