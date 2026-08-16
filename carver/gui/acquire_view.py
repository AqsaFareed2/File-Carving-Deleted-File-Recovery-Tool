"""
Phase 4 - Task C: Drive Acquisition panel (UI half).

Owner:  <assign a teammate>   (same person as the carver/acquire.py backend)
Tests:  tests/test_acquire.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Build the panel that images a live drive so it can be carved:

  * a "Refresh" button + a list (ttk.Treeview) of drives from
    ``carver.acquire.list_drives()`` (kind, device, size, removable, name);
  * an output-file chooser and an optional "limit to N MB" for quick tests;
  * an "Image" button that runs ``carver.acquire.image_source(device, out, ...)``
    on a BACKGROUND THREAD with a progress bar and Cancel;
  * on success, call ``self.app.set_image(out)`` so the Scan tab can open it.

The real logic lives in carver/acquire.py (also Task C) -- keep this panel thin.
You edit this file, carver/acquire.py and tests/test_acquire.py.

Safety: acquisition is READ-ONLY -- never write to the source drive. Imaging a
physical drive/volume needs Administrator rights; the size limit keeps test runs
quick.
"""

import tkinter as tk
from tkinter import ttk


class AcquireView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app

        ttk.Label(self, text="Drive Acquisition  —  TODO (Task C)",
                  font=("", 11, "bold")).pack(anchor="w")
        ttk.Label(self, text="List drives (carver.acquire.list_drives) and image "
                             "a selected one read-only "
                             "(carver.acquire.image_source), then load the image "
                             "into the app for scanning. The backend lives in "
                             "carver/acquire.py.",
                  foreground="#666", justify="left").pack(anchor="w", pady=(2, 8))
