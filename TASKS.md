# Phase 2 — Task Assignments

Phase 2 turns the raw Phase 1 candidates into **trustworthy, ranked results**.
It is split into **three independent tasks**. The shared plumbing (the new
`Candidate` fields, the call sites in `engine.py`, and the CLI display) is
already in place on this branch, so **each task only edits one module and one
test file** — the three pull requests will not conflict.

## How the pieces fit together

`carver/engine.py::scan()` builds the candidate list and then calls three
post-processing passes:

```python
assign_confidence(candidates, buf)   # Task 1 -> c.confidence
resolve_containment(candidates)      # Task 3 -> c.embedded_in
deduplicate(candidates, buf)         # Task 2 -> c.sha256, c.duplicate_of
```

Each pass mutates the candidates in place. The `Candidate` dataclass already has
the fields `confidence`, `sha256`, `duplicate_of`, `embedded_in`, and
`ScanResult` already exposes `.recovered`, `.duplicates`, `.embedded`, which the
CLI uses. **Do not edit `engine.py` or `cli.py`** — just fill in your module.

| # | Task | Edit only | Branch |
|---|------|-----------|--------|
| 1 | Validation & confidence scoring | `carver/validation.py`, `tests/test_validation.py` | `feature/validation` |
| 2 | De-duplication by SHA-256 | `carver/dedup.py`, `tests/test_dedup.py` | `feature/dedup` |
| 3 | Containment / embedded objects | `carver/containment.py`, `tests/test_containment.py` | `feature/containment` |

The full brief for each task is in the docstring at the top of its module.

## Task 1 — Validation & Confidence Scoring
Give every candidate a `.confidence` of `high` / `medium` / `low` by validating
its bytes against the format structure (this also covers "handle fragmentation
gracefully": truncated files become `low`). **Done when** `tests/test_validation.py`
passes.

## Task 2 — De-duplication by SHA-256
Hash each candidate's bytes into `.sha256` and mark later identical carves with
`.duplicate_of = <first offset>`. **Done when** `tests/test_dedup.py` passes.

## Task 3 — Containment / Embedded-object Resolution
Flag any candidate fully inside a larger different candidate with
`.embedded_in = <container start>`. **Done when** `tests/test_containment.py`
passes.

## Workflow

```bash
# 1. Fork this repo on GitHub, then clone your fork:
git clone https://github.com/<you>/File-Carving-Deleted-File-Recovery-Tool
cd File-Carving-Deleted-File-Recovery-Tool

# 2. Branch for your task:
git checkout -b feature/<task>

# 3. Implement carver/<module>.py until your test is green:
python tests/test_<task>.py

# 4. Commit and push to your fork, then open a PR against the main repo:
git commit -am "Phase 2: <task>"
git push origin feature/<task>
```

Before opening the PR, make sure the whole suite still passes:

```bash
python -m pytest -q      # or run each tests/test_*.py file directly
```

Your test starts **red** (the module is a no-op stub). Implement the module to
turn it green. The Phase 1 test (`tests/test_phase1.py`) must stay green.
