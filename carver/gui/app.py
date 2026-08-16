"""
Phase 4 - GUI shell (shared scaffolding).

``AppState`` is the small shared-state object every panel talks to: it holds the
current image path and scan result, and lets panels notify each other. Importing
this module does NOT open a window (only :func:`launch` does), so tests can use
``AppState`` headless.

``launch()`` builds the main window with three tabs, each a panel implemented by
a separate Phase 4 task:

    Scan      -> carver/gui/scan_view.py     (Task A)
    Reports   -> carver/gui/report_view.py   (Task B)
    Acquire   -> carver/gui/acquire_view.py  (Task C, + carver/acquire.py)

Each panel is a ``ttk.Frame`` subclass constructed as ``Panel(parent, app)``.
Do not change this contract -- the panels depend on it.
"""

from typing import Callable, List, Optional


class AppState:
    """Shared application state. Panels read/update it and subscribe to changes.

    Attributes:
        image_path: path of the disk image currently loaded (or None).
        result:     the most recent ``carver.engine.ScanResult`` (or None).
    """

    def __init__(self):
        self.image_path: Optional[str] = None
        self.result = None
        self._subscribers: List[Callable[[], None]] = []

    def subscribe(self, callback: Callable[[], None]) -> None:
        """Register ``callback`` to be called whenever the state changes."""
        self._subscribers.append(callback)

    def _notify(self) -> None:
        for cb in list(self._subscribers):
            cb()

    def set_image(self, path: Optional[str]) -> None:
        self.image_path = path
        self._notify()

    def set_result(self, result) -> None:
        self.result = result
        if result is not None:
            self.image_path = result.image_path
        self._notify()


def launch(argv=None) -> int:
    """Open the desktop GUI. ``argv[0]`` optionally pre-loads an image path."""
    import tkinter as tk
    from tkinter import ttk

    from .scan_view import ScanView
    from .report_view import ReportView
    from .acquire_view import AcquireView

    root = tk.Tk()
    root.title("Carver — File Carving & Deleted-File Recovery")
    root.geometry("1000x640")
    root.minsize(820, 520)
    try:
        ttk.Style().theme_use("vista")  # nicer on Windows; harmless elsewhere
    except tk.TclError:
        pass

    app = AppState()
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=6, pady=6)
    nb.add(ScanView(nb, app), text="  Scan  ")
    nb.add(ReportView(nb, app), text="  Reports  ")
    nb.add(AcquireView(nb, app), text="  Acquire  ")

    if argv and argv[0]:
        app.set_image(argv[0])

    root.mainloop()
    return 0


if __name__ == "__main__":
    launch()
