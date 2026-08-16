"""
Phase 4 - Task B: Reports & Export panel.

Owner:  <assign a teammate>
Tests:  tests/test_gui_report.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Build the panel that turns the current scan result into files on disk:

  * an "Export carved files..." button that asks for a folder and writes the
    recovered files there (see the export logic in carver/cli.py);
  * "Save JSON / Save HTML / Save CSV" buttons, each asking for a path
    (tkinter.filedialog.asksaveasfilename) and writing that report;
  * an "Open HTML report" convenience that opens the saved HTML in the browser
    (webbrowser.open);
  * sensible disabling when there is no scan result yet
    (self.app.result is None), and a small status label.

Use the Phase 3 reporting code -- ``carver.report.write_report(result, kind,
path)`` already renders 'json' / 'html' / 'csv'. You only edit THIS file and
tests/test_gui_report.py. Do not touch app.py or the other panels.

--------------------------------------------------------------------------
CONTRACT (checked by tests/test_gui_report.py)
--------------------------------------------------------------------------
  * save_report(kind, path) -- write a report of `kind` ('json'|'html'|'csv')
    for self.app.result to `path`. (Delegate to carver.report.write_report;
    this is the function your Save buttons should call.)
"""

import tkinter as tk
from tkinter import ttk


class ReportView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app

        ttk.Label(self, text="Reports & Export  —  TODO (Task B)",
                  font=("", 11, "bold")).pack(anchor="w")
        ttk.Label(self, text="Add buttons to export the carved files and to save "
                             "JSON / HTML / CSV reports for the current scan "
                             "result. See the module docstring for the contract "
                             "(save_report()).",
                  foreground="#666", justify="left").pack(anchor="w", pady=(2, 8))

    def save_report(self, kind, path):
        """Write a `kind` report for self.app.result to `path`.

        TODO(Task B): implement, e.g. via carver.report.write_report. This stub
        does nothing, so the acceptance test fails.
        """
        return
