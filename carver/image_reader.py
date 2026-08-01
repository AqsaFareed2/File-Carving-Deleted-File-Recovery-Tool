"""
Disk image reader (Phase 1).

Presents a raw ``.dd``/``.img``/``.raw`` image or an EnCase ``.E01`` image
through one simple interface: a ``buf`` object that supports slicing, ``len()``
and ``find()`` (so the engine does not care which kind it got).

* Raw images are memory-mapped, so multi-gigabyte images can be scanned without
  loading them into RAM.
* E01 images are read through the optional ``pyewf`` library. When it is not
  installed the tool degrades with a clear message rather than a stack trace.
"""

import mmap
import os
from typing import Union

RAW_EXTS = {".dd", ".img", ".raw", ".bin", ".001", ""}
EWF_EXTS = {".e01", ".ex01", ".s01", ".l01"}


class SearchableBuffer:
    """A thin wrapper over an ``mmap`` (or ``bytes``) that supports slicing,
    ``len()`` and ``find()``.

    Why it exists: on some Windows CPython builds ``mmap.find()`` triggers an
    access violation, whereas *slicing* an mmap is safe. So we implement
    ``find()`` ourselves by copying bounded windows out of the underlying buffer
    and using the rock-solid ``bytes.find()`` on them -- keeping mmap's low
    memory use while avoiding the broken C path.
    """

    __slots__ = ("_d", "_len", "_window")

    def __init__(self, data, window: int = 1 << 22):  # 4 MiB search windows
        self._d = data
        self._len = len(data)
        self._window = window

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        return self._d[key]

    def find(self, sub: bytes, start: int = 0, end=None) -> int:
        if end is None or end > self._len:
            end = self._len
        if start < 0:
            start = 0
        n = len(sub)
        if n == 0:
            return start if start <= end else -1
        pos = start
        overlap = n - 1
        while pos < end:
            stop = min(pos + self._window, end)
            chunk = bytes(self._d[pos:stop])          # safe: slicing, not .find
            idx = chunk.find(sub)
            if idx != -1:
                return pos + idx
            if stop >= end:
                break
            pos = stop - overlap                       # keep straddling matches
        return -1


class DiskImage:
    def __init__(self, path: str):
        self.path = path
        self.size = 0
        self.kind = "raw"
        self._file = None
        self._mmap = None
        self._buf: Union[SearchableBuffer, None] = None

    def open(self) -> "DiskImage":
        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"Image not found: {self.path}")
        ext = os.path.splitext(self.path)[1].lower()
        if ext in EWF_EXTS:
            self._open_ewf()
        else:
            self._open_raw()
        return self

    def _open_raw(self):
        self.kind = "raw"
        self._file = open(self.path, "rb")
        size = os.fstat(self._file.fileno()).st_size
        if size == 0:
            raise ValueError("Image file is empty")
        self._mmap = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        self._buf = SearchableBuffer(self._mmap)
        self.size = size

    def _open_ewf(self):
        self.kind = "ewf"
        try:
            import pyewf  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "This looks like an E01 (EnCase) image but the 'pyewf' library "
                "is not installed.\n"
                "Either install libewf/pyewf, or convert the image to raw first:\n"
                "    ewfexport -t out image.E01      # produces out.dd\n"
                "and then run the carver against the .dd file."
            ) from exc

        filenames = pyewf.glob(self.path)
        handle = pyewf.handle()
        handle.open(filenames)
        self.size = handle.get_media_size()
        handle.seek(0)
        self._buf = SearchableBuffer(handle.read(self.size))
        handle.close()

    def close(self):
        if self._mmap is not None:
            self._mmap.close()
        if self._file is not None:
            self._file.close()
        self._buf = None
        self._mmap = None
        self._file = None

    @property
    def buf(self):
        if self._buf is None:
            raise RuntimeError("Image is not open; call open() first")
        return self._buf

    def read(self, offset: int, length: int) -> bytes:
        return bytes(self.buf[offset:offset + length])

    def __enter__(self):
        return self.open()

    def __exit__(self, *exc):
        self.close()
        return False
