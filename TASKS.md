# Phase 3 — Task Assignments

Phase 3 adds **reporting**: turn the scan results into shareable reports that
summarise the recovered files and their confidence. It is split into **three
independent tasks**. The shared plumbing (a canonical report data builder and
the CLI flags) is already in place on this branch, so **each task only edits one
module and one test file** — the three pull requests will not conflict.

*(Phase 2 — confidence scoring, de-duplication and containment — is complete and
merged.)*

## How the pieces fit together

`carver/report.py` builds ONE canonical, JSON-safe summary from a scan result:

```python
from carver.report import report_data
data = report_data(result)     # dict: image, summary counts, and file records
```

Every report format renders from this same `data` dict, so the renderers are
independent of each other. Each task fills in one renderer:

```python
write_json(data, "report.json")   # Task A -> carver/report_json.py
write_html(data, "report.html")   # Task B -> carver/report_html.py
write_csv(data,  "report.csv")    # Task C -> carver/report_csv.py
```

The CLI flags already exist and call your renderer:

```bash
python -m carver scan test_image.dd --json out.json --html out.html --csv out.csv
```

**Do not edit `report.py` or `cli.py`** — just fill in your one renderer. The
`data` shape is documented at the top of `carver/report_json.py`.

| # | Task | Edit only |
|---|------|-----------|
| A | JSON report | `carver/report_json.py`, `tests/test_report_json.py` |
| B | HTML report | `carver/report_html.py`, `tests/test_report_html.py` |
| C | CSV evidence log | `carver/report_csv.py`, `tests/test_report_csv.py` |

## Task A — JSON report
Write the `data` dict to a valid, pretty-printed JSON file (machine-readable).
**Done when** `tests/test_report_json.py` passes.

## Task B — HTML report
Write a single self-contained HTML page (inline CSS) with the summary and a
colour-coded table of the recovered files (green/amber/red confidence badges).
**Done when** `tests/test_report_html.py` passes.

## Task C — CSV evidence log
Write the recovered files as a CSV: a header row plus one row per file (index,
type, offset, size, confidence, sha256, filename).
**Done when** `tests/test_report_csv.py` passes.

## Workflow

```bash
# 1. Fork this repo on GitHub, then clone your fork:
git clone https://github.com/<you>/File-Carving-Deleted-File-Recovery-Tool
cd File-Carving-Deleted-File-Recovery-Tool

# 2. Implement your carver/report_<fmt>.py until your test is green:
python tests/test_report_<fmt>.py     # <fmt> = json | html | csv

# 3. Commit and push to your fork:
git commit -am "Phase 3: <fmt> report"
git push
```

Then **open a Pull Request** from your fork to this repo's `main` branch.

Before opening the PR, make sure the whole suite still passes:

```bash
python -m pytest -q      # or run each tests/test_*.py file directly
```

Your test starts **red** (the renderer is a no-op stub). Implement it to turn it
green. All earlier tests (Phase 1 and Phase 2) must stay green.
