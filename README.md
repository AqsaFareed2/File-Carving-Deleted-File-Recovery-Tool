# Carver — Phase 1: Core Carving Engine

Phase 1 of the **File Carving & Deleted-File Recovery Tool**. This folder is a
self-contained implementation of just the first phase: read a disk image
without a file system, scan it for known file signatures, carve each candidate
file, and report its **byte offset and size**.

> Later phases (validation & confidence scoring, fragmentation handling,
> de-duplication by hash, rich reports, GUI, and live drive acquisition) are
> **not** part of this folder — they build on top of this engine.

## Scope of Phase 1

- Read a **raw** (`.dd` / `.img` / `.raw`) or **E01** (EnCase) disk image,
  independently of any file system.
- Scan the whole image for the header signatures of **JPG, PNG, PDF, ZIP** and
  **DOCX**.
- Determine each file's true end (format-aware) and **carve + export** it,
  reporting **offset and size**.

## How it works

| Format | Header (hex) | How the end is found |
|--------|--------------|----------------------|
| JPG    | `FF D8 FF`   | first `FF D9` (End of Image) |
| PNG    | `89 50 4E 47 …` | chunk-walked to the `IEND` chunk |
| PDF    | `25 50 44 46` (`%PDF`) | last `%%EOF` trailer |
| ZIP    | `50 4B 03 04` | End-of-Central-Directory (`50 4B 05 06`) |
| DOCX   | `50 4B 03 04` (a ZIP) | detected by `word/document.xml` inside |

The ZIP pass runs first and records each archive's byte range so the many
internal `PK\x03\x04` headers (and any media) inside an archive are not
mistaken for separate files.

## Requirements

- **Python 3.8+**, standard library only. No third-party packages are needed for
  raw images or any supported format.
- **E01 images** additionally need the optional `pyewf` library; without it the
  tool tells you to convert the image to raw with `ewfexport` instead.

## Usage

```bash
# 1. (optional) build a synthetic test image with known contents
python make_test_image.py test_image.dd --size-mb 8

# 2. scan it and export the carved files
python -m carver scan test_image.dd -o recovered/
```

Options:

```
python -m carver scan IMAGE [-o DIR] [--formats jpg,png,pdf,zip]
```

- `-o DIR`        write carved files here (omit to only print the summary)
- `--formats`     restrict the search; `docx` comes from `zip`

Carved files are named `NNNN_<type>_<offset-hex>.<ext>` (e.g.
`0003_pdf_120000.pdf`) so the filename records where the data was found.

## Project layout

```
carver/
  __init__.py       package exports
  signatures.py     the signature catalogue (headers/footers/limits)
  image_reader.py   raw (mmap) and E01 (pyewf) image access
  engine.py         header scanning, format-aware carving, offset/size
  cli.py            the `python -m carver scan` command line
  __main__.py       entry point
make_test_image.py  builds a synthetic image with known ground truth
tests/test_phase1.py  end-to-end test (carve the test image, check results)
```

## Testing

```bash
python tests/test_phase1.py      # or:  python -m pytest -q
```

The test builds the synthetic image and asserts that the five target files are
carved at their exact offset and size, that the DOCX is classified from its ZIP
container, and that Phase 1 reports raw candidates (the duplicate and truncated
files both appear — de-duplication and fragmentation handling come later).
```
