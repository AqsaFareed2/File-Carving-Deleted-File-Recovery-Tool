"""
Phase 4 - Task C: Drive acquisition backend (READ-ONLY).

Owner:  <assign a teammate>   (same person as carver/gui/acquire_view.py)
Tests:  tests/test_acquire.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement two functions.

1) list_drives() -> list
   Return the machine's drives available for imaging. Each item should carry at
   least a device path, a human name and a size in bytes (a small dataclass or a
   dict is fine). On Windows you can enumerate physical disks and volumes with
   WMI via PowerShell; on Linux read /sys/block. On an unsupported platform or
   on any error, return an EMPTY LIST -- never raise.

2) image_source(source, out_path, max_bytes=None, block=1<<20,
                progress=None, cancel=None) -> int
   Copy `source` READ-ONLY to `out_path` and return the number of bytes written.
   `source` may be a device path (e.g. \\\\.\\PhysicalDrive1) OR a regular file
   (handy for testing).
     * open the source read-only; NEVER write to it;
     * read in `block`-sized chunks until end-of-source or `max_bytes` reached;
     * if `progress` is given, call progress(bytes_written, target_or_None);
     * if `cancel` (a threading.Event) is set, stop early;
     * opening a physical drive/volume usually needs Administrator (Windows) /
       root (Linux) -- raise a clear error message, do not crash the app.

You edit this file, carver/gui/acquire_view.py and tests/test_acquire.py.

--------------------------------------------------------------------------
CONTRACT (checked by tests/test_acquire.py)
--------------------------------------------------------------------------
  * list_drives() returns a list.
  * image_source(src_file, out, max_bytes=N) writes exactly N bytes, equal to
    the first N bytes of the source.
"""


def list_drives() -> list:
    """Enumerate drives available for imaging.

    TODO(Task C): implement. This stub returns an empty list.
    """
    return []


def image_source(source, out_path, max_bytes=None, block=1 << 20,
                 progress=None, cancel=None) -> int:
    """Read-only copy ``source`` -> ``out_path``; return bytes written.

    TODO(Task C): implement. This stub does nothing and returns 0, so the
    acceptance test fails.
    """
    return 0
