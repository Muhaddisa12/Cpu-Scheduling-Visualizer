"""
Gantt Chart visualization for CPU Scheduling.

Uses Matplotlib to draw process execution timeline. Each block shows
Process ID, start and end time. Idle CPU and context switches (multiple
slices per process) are supported.
"""

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

from utils.helpers import get_color_for_process

# Idle CPU block color (light gray)
IDLE_COLOR = "#E0E0E0"


def build_gantt_figure(gantt_data, processes, title="Gantt Chart", figsize=(10, 4)):
    """
    Build a Matplotlib Figure for the Gantt chart.

    Args:
        gantt_data: List of (process_id, start, end) tuples.
        processes: List of process dicts (for color mapping).
        title: Chart title.
        figsize: (width, height) in inches.

    Returns:
        matplotlib.figure.Figure
    """
    fig = Figure(figsize=figsize, dpi=100, facecolor="#fafafa")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#ffffff")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Time")
    ax.set_ylabel("Process")

    if not gantt_data:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.5)
        return fig

    has_idle = any(p[0] == "IDLE" for p in gantt_data)
    pid_set = sorted({p[0] for p in gantt_data if p[0] != "IDLE"})
    if has_idle:
        pid_set.append("IDLE")
    y_pos = {pid: i for i, pid in enumerate(pid_set)}

    y_min = -0.5
    y_max = len(pid_set) + 0.5
    x_max = 0.0

    for pid, start, end in gantt_data:
        y = y_pos.get(pid, 0)
        width = max(end - start, 0.01)
        color = IDLE_COLOR if pid == "IDLE" else get_color_for_process(pid)
        rect = mpatches.Rectangle((start, y - 0.35), width, 0.7, facecolor=color, edgecolor="#333", linewidth=0.8)
        ax.add_patch(rect)
        label = f"{pid}\n[{start:.1f}-{end:.1f}]"
        ax.text(start + width / 2, y, label, ha="center", va="center", fontsize=8, fontweight="bold")
        x_max = max(x_max, end)

    ax.set_xlim(0, x_max * 1.02 + 0.5)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks([i for i in range(len(pid_set))])
    ax.set_yticklabels(pid_set)
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    return fig


class GanttChartPanel:
    """
    Tkinter panel that embeds a Matplotlib Gantt chart.

    Updates dynamically when new gantt_data is set via update_chart().
    """

    def __init__(self, parent, width=700, height=320, **kwargs):
        self.parent = parent
        self.width = width
        self.height = height
        self.frame = tk.Frame(parent, **kwargs)
        self.fig = None
        self.canvas = None
        self._gantt_data = []
        self._processes = []
        self._title = "Gantt Chart"

    def update_chart(self, gantt_data, processes, title=None):
        """
        Redraw the Gantt chart with new data.

        Args:
            gantt_data: List of (process_id, start, end).
            processes: List of process dicts.
            title: Optional chart title override.
        """
        self._gantt_data = gantt_data or []
        self._processes = processes or []
        if title is not None:
            self._title = title

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.fig:
            plt.close(self.fig)

        self.fig = build_gantt_figure(
            self._gantt_data,
            self._processes,
            title=self._title,
            figsize=(self.width / 100, self.height / 100),
        )
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_frame(self):
        """Return the Tk frame for packing/placing."""
        return self.frame

    def clear(self):
        """Clear the chart (empty data)."""
        self.update_chart([], [], title="Gantt Chart")
