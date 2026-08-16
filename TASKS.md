# Phase 4 — Task Assignments

Phase 4 puts a **desktop GUI** on the carver and lets it **acquire a live drive**,
so the whole workflow — pick or image a disk → scan → review → report — runs from
one window. It is split into **three independent tasks**. The GUI shell (the main
window, the shared `AppState`, and the tabs) is already in place on this branch,
so **each task only edits its own panel file** — the pull requests will not
conflict.

*(Phase 3 — JSON / HTML / CSV reporting — is complete and merged.)*

## How the pieces fit together

`carver/gui/app.py` builds the main window: a tabbed notebook with three panels
and a shared state object, `AppState`, that holds the current image path and
scan result and lets panels notify each other:

```python
app.image_path          # currently loaded image (or None)
app.result              # latest carver ScanResult (or None)
app.set_image(path)     # load an image (Acquire tab -> Scan tab)
app.set_result(result)  # publish a scan result (Scan tab -> Reports tab)
app.subscribe(callback) # be told when the above change
```

Each panel is a `ttk.Frame` built as `Panel(parent, app)` and mounted as a tab.
**Do not edit `app.py`** — just fill in your panel. Launch the app any time with:

```bash
python -m carver gui        # or:  python gui.py
```

| # | Task | Edit only |
|---|------|-----------|
| A | Scan & Results panel | `carver/gui/scan_view.py`, `tests/test_gui_scan.py` |
| B | Reports & Export panel | `carver/gui/report_view.py`, `tests/test_gui_report.py` |
| C | Drive acquisition | `carver/acquire.py`, `carver/gui/acquire_view.py`, `tests/test_acquire.py` |

The full brief for each task is in the docstring at the top of its file.

## Task A — Scan & Results panel
Pick a disk image, run `carver.scan` on a background thread (responsive UI, with
progress + cancel), and show the recovered files in a colour-coded table; publish
the result with `app.set_result(...)`. **Done when** `tests/test_gui_scan.py`
passes (the table has one row per recovered file).

## Task B — Reports & Export panel
Buttons to export the carved files and to save JSON / HTML / CSV reports for the
current result (reusing `carver.report.write_report`). **Done when**
`tests/test_gui_report.py` passes (`save_report("json", path)` writes a valid
report).

## Task C — Drive acquisition
A read-only backend in `carver/acquire.py` (`list_drives()` and
`image_source(...)`) plus a thin panel to drive it. **Done when**
`tests/test_acquire.py` passes (a read-only copy of N bytes produces exactly N
bytes). This test is pure logic — no display or Administrator rights needed.

## Workflow

```bash
# 1. Fork this repo on GitHub, then clone your fork:
git clone https://github.com/<you>/File-Carving-Deleted-File-Recovery-Tool
cd File-Carving-Deleted-File-Recovery-Tool

# 2. Implement your file(s) until your test is green:
python tests/test_gui_scan.py     # (or test_gui_report.py / test_acquire.py)

# 3. Commit and push to your fork:
git commit -am "Phase 4: <task>"
git push
```

Then **open a Pull Request** from your fork to this repo's `main` branch.

Before opening the PR, make sure the whole suite still passes:

```bash
python -m pytest -q      # or run each tests/test_*.py file directly
```

The GUI tests need a display (they skip on a headless machine); run them on your
own PC. All earlier tests (Phases 1–3) must stay green.
