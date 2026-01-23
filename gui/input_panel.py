"""
Process input panel for CPU Scheduling Visualizer.

Table-style input for Process ID, Arrival Time, Burst Time, Priority.
Add/Delete buttons. Priority and Time Quantum fields are enabled/disabled
based on selected algorithm.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import create_process_dict


# Default number of rows when empty
DEFAULT_ROWS = 4
# Column headers
COLUMNS = ("Process ID", "Arrival Time", "Burst Time", "Priority")


class InputPanel:
    """
    Left-panel UI: process table, Add/Delete, and optional Time Quantum.

    Callbacks: on_run(callback), on_compare(callback).
    Algorithm selection and priority/tq visibility are controlled externally
    via enable_priority( bool ), enable_time_quantum( bool ), set_time_quantum( str ).
    """

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.frame = tk.Frame(parent, **kwargs)
        self._enable_priority = False
        self._enable_tq = False
        self._process_entries = []  # list of dicts: pid, arr, burst, pri
        self._tq_var = tk.StringVar(value="2")
        self._tq_entry = None
        self._tq_label = None
        self._build_ui()

    def _build_ui(self):
        # Title
        title = tk.Label(self.frame, text="Process Input", font=("Segoe UI", 11, "bold"))
        title.pack(anchor="w", padx=8, pady=(8, 4))

        # Table-style input: grid of Entry widgets
        self._table_frame = tk.Frame(self.frame)
        self._table_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Header row
        for j, col in enumerate(COLUMNS):
            lbl = tk.Label(self._table_frame, text=col, font=("Segoe UI", 9, "bold"))
            lbl.grid(row=0, column=j, padx=2, pady=2, sticky="ew")
        self._table_frame.columnconfigure(1, weight=1)
        self._table_frame.columnconfigure(2, weight=1)
        self._table_frame.columnconfigure(3, weight=1)

        # Data rows - we'll add DEFAULT_ROWS and manage via Add/Delete
        self._rows_container = tk.Frame(self._table_frame)
        self._rows_container.grid(row=1, column=0, columnspan=4, sticky="nsew")
        self._table_frame.rowconfigure(1, weight=1)

        # Add some initial rows
        for _ in range(DEFAULT_ROWS):
            self._add_row()

        # Buttons
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(btn_frame, text="Add Row", command=self._on_add).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Last Row", command=self._on_delete).pack(side=tk.LEFT, padx=2)

        # Time Quantum (hidden by default)
        tq_frame = tk.Frame(self.frame)
        tq_frame.pack(fill=tk.X, padx=8, pady=4)
        self._tq_label = tk.Label(tq_frame, text="Time Quantum:", font=("Segoe UI", 9))
        self._tq_label.pack(side=tk.LEFT, padx=(0, 4))
        self._tq_entry = ttk.Entry(tq_frame, textvariable=self._tq_var, width=8)
        self._tq_entry.pack(side=tk.LEFT)
        self._tq_frame = tq_frame
        self._hide_tq()
        self.enable_priority(False)

    def _add_row(self):
        """Append one editable row (PID, Arrival, Burst, Priority)."""
        row_idx = len(self._process_entries)
        entries = {}
        vars = {}
        for j, key in enumerate(["pid", "arrival", "burst", "priority"]):
            default = "0" if key != "pid" else f"P{row_idx + 1}"
            v = tk.StringVar(value=default)
            e = ttk.Entry(self._rows_container, textvariable=v, width=12)
            e.grid(row=row_idx, column=j, padx=2, pady=2, sticky="ew")
            entries[key] = e
            vars[key] = v
        self._process_entries.append({"entries": entries, "vars": vars, "row": row_idx})

    def _on_add(self):
        n = len(self._process_entries)
        self._add_row()
        self._process_entries[-1]["vars"]["pid"].set(f"P{n + 1}")

    def _remove_row(self, index):
        """Remove row at index and re-grid remaining."""
        for w in self._process_entries[index]["entries"].values():
            w.destroy()
        self._process_entries.pop(index)
        for i, row in enumerate(self._process_entries):
            row["row"] = i
            for j, key in enumerate(["pid", "arrival", "burst", "priority"]):
                row["entries"][key].grid(row=i, column=j, padx=2, pady=2, sticky="ew")

    def _on_delete(self):
        # Simple: delete last row if more than 1
        if len(self._process_entries) > 1:
            self._remove_row(len(self._process_entries) - 1)
        else:
            if self.parent.winfo_exists():
                messagebox.showinfo("Delete", "At least one process row is required.")

    def _hide_tq(self):
        self._tq_frame.pack_forget()

    def _show_tq(self):
        self._tq_frame.pack(fill=tk.X, padx=8, pady=4)

    def enable_priority(self, enabled):
        """Show/enable or hide/disable Priority column."""
        self._enable_priority = enabled
        for row in self._process_entries:
            e = row["entries"]["priority"]
            if enabled:
                e.config(state="normal")
            else:
                e.config(state="disabled")

    def enable_time_quantum(self, enabled):
        """Show/enable or hide Time Quantum field."""
        self._enable_tq = enabled
        if enabled:
            self._show_tq()
            self._tq_entry.config(state="normal")
        else:
            self._hide_tq()

    def set_time_quantum(self, value):
        """Set Time Quantum entry value."""
        self._tq_var.set(str(value))

    def get_time_quantum(self):
        """Get Time Quantum string from entry."""
        return self._tq_var.get().strip()

    def get_processes(self):
        """
        Parse table into list of process dicts.

        Returns:
            list: [{"process_id", "arrival_time", "burst_time"[, "priority"]}, ...]
        """
        out = []
        for row in self._process_entries:
            pid = row["vars"]["pid"].get().strip()
            arr = row["vars"]["arrival"].get().strip()
            burst = row["vars"]["burst"].get().strip()
            pri = row["vars"]["priority"].get().strip() if self._enable_priority else None
            if not pid:
                continue
            try:
                a = float(arr) if arr else 0.0
                b = float(burst) if burst else 0.0
                p = int(pri) if pri is not None and pri else 0
            except ValueError:
                continue
            d = create_process_dict(pid, a, b, p if self._enable_priority else None)
            out.append(d)
        return out

    def get_frame(self):
        return self.frame
