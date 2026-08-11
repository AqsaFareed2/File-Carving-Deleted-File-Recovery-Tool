"""
Phase 3 - Task C: CSV evidence log.

Tests:  tests/test_report_csv.py   (currently RED -- make them pass)
"""

def write_csv(data: dict, path: str) -> None:
    """Write the recovered files in ``data`` to ``path`` as CSV."""
    import csv

    columns = [
        "index",
        "type",
        "offset",
        "size",
        "confidence",
        "sha256",
        "filename",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        for index, file_data in enumerate(data["files"], start=1):
            writer.writerow([
                index,
                file_data.get("format", ""),
                file_data.get("offset_hex", ""),
                file_data.get("size", ""),
                file_data.get("confidence", ""),
                file_data.get("sha256", ""),
                file_data.get("filename", ""),
            ])