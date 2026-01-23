"""
Results panel for CPU Scheduling Visualizer.

Displays per-process table (PID, Arrival, Burst, Completion, Turnaround, Waiting)
and summary metrics: Average Waiting Time, Average Turnaround Time.
"""

import tkinter as tk
from tkinter import ttk
from utils.helpers import compute_metrics


def _fmt(x):
    """Format number for display (2 decimal places if float)."""
    if isinstance(x, float):
        return f"{x:.2f}"
    return str(x)


RESULT_COLUMNS = (
    "Process ID",
    "Arrival Time",
    "Burst Time",
    "Completion Time",
    "Turnaround Time",
    "Waiting Time",
)


class ResultPanel:
    """
    Bottom-panel UI: results table and metrics.

    update_results(processes, completion_times) fills the table and
    displays average waiting and turnaround times.
    """

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.frame = tk.Frame(parent, **kwargs)
        self._tree = None
        self._scroll_y = None
        self._avg_wt_var = tk.StringVar(value="—")
        self._avg_tt_var = tk.StringVar(value="—")
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self.frame, text="Results & Metrics", font=("Segoe UI", 11, "bold"))
        title.pack(anchor="w", padx=8, pady=(8, 4))

        container = tk.Frame(self.frame)
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self._scroll_y = ttk.Scrollbar(container)
        self._scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree = ttk.Treeview(
            container,
            columns=RESULT_COLUMNS,
            show="headings",
            height=6,
            yscrollcommand=self._scroll_y.set,
        )
        for c in RESULT_COLUMNS:
            self._tree.heading(c, text=c)
            self._tree.column(c, width=100, minwidth=70)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scroll_y.config(command=self._tree.yview)

        metrics_frame = tk.Frame(self.frame)
        metrics_frame.pack(fill=tk.X, padx=8, pady=6)
        tk.Label(metrics_frame, text="Average Waiting Time:", font=("Segoe UI", 10, "bold")).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        tk.Label(metrics_frame, textvariable=self._avg_wt_var, font=("Segoe UI", 10)).pack(
            side=tk.LEFT, padx=(0, 20)
        )
        tk.Label(metrics_frame, text="Average Turnaround Time:", font=("Segoe UI", 10, "bold")).pack(
            side=tk.LEFT, padx=(0, 4)
        )
        tk.Label(metrics_frame, textvariable=self._avg_tt_var, font=("Segoe UI", 10)).pack(
            side=tk.LEFT
        )

    def update_results(self, processes, completion_times):
        """
        Update table and metrics from processes and completion times.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time).
            completion_times: Dict process_id -> completion time.
        """
        for iid in self._tree.get_children():
            self._tree.delete(iid)

        self._avg_wt_var.set("—")
        self._avg_tt_var.set("—")

        if not processes or not completion_times:
            return

        metrics = compute_metrics(processes, completion_times)
        for row in metrics["per_process"]:
            self._tree.insert("", "end", values=(
                row["process_id"],
                _fmt(row["arrival_time"]),
                _fmt(row["burst_time"]),
                _fmt(row["completion_time"]),
                _fmt(row["turnaround_time"]),
                _fmt(row["waiting_time"]),
            ))
        self._avg_wt_var.set(str(metrics["avg_waiting"]))
        self._avg_tt_var.set(str(metrics["avg_turnaround"]))

    def get_avg_waiting(self):
        """Return current average waiting time string."""
        return self._avg_wt_var.get()

    def get_avg_turnaround(self):
        """Return current average turnaround time string."""
        return self._avg_tt_var.get()

    def get_frame(self):
        return self.frame
