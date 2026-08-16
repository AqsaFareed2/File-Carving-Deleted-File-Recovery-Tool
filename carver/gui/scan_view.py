"""
Phase 4 - Task A: Scan & Results panel.

Owner:  <assign a teammate>
Tests:  tests/test_gui_scan.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Build the panel that drives a scan and shows the results:

  * a control to pick a disk image (tkinter.filedialog.askopenfilename), shown
    in an entry -- pre-fill it from self.app.image_path if already set;
  * a "Scan" button that runs ``carver.scan`` on a BACKGROUND THREAD so the
    window stays responsive, with a progress bar / status and a Cancel option
    (use a queue + self.after(...) to talk back to the UI thread -- never touch
    widgets from the worker thread);
  * a results TABLE (ttk.Treeview) of the recovered files, with columns:
    #, type, offset, size, confidence, sha256 -- colour the rows by confidence
    (green/amber/red for high/medium/low);
  * when the scan finishes, call ``self.app.set_result(result)`` so the other
    tabs can use it.

You only edit THIS file and tests/test_gui_scan.py. Read the image with
``carver.DiskImage`` and scan with ``carver.scan`` (see carver/cli.py for the
pattern). Do not touch app.py or the other panels.

--------------------------------------------------------------------------
CONTRACT (checked by tests/test_gui_scan.py)
--------------------------------------------------------------------------
  * self.tree  -- a ttk.Treeview listing the recovered files.
  * refresh()  -- (re)fills self.tree from self.app.result.recovered,
                  one row per recovered file (empty if no result yet).
"""

import tkinter as tk
from tkinter import ttk


class ScanView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app

        ttk.Label(self, text="Scan & Results  —  TODO (Task A)",
                  font=("", 11, "bold")).pack(anchor="w")
        ttk.Label(self, text="Build the image picker, the threaded scan, and the "
                             "results table here. See the module docstring for "
                             "the contract (self.tree + refresh()).",
                  foreground="#666", justify="left").pack(anchor="w", pady=(2, 8))

        # Placeholder so the contract's self.tree exists -- replace with a real,
        # populated, colour-coded table.
        cols = ("idx", "type", "offset", "size", "conf", "sha")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, w in zip(cols, (36, 60, 90, 70, 80, 160)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True)

        self.app.subscribe(self.refresh)

    def refresh(self):
        """Fill self.tree from self.app.result.

        TODO(Task A): implement. This stub does nothing, so the results table
        stays empty and the acceptance test fails.
        """
        return
