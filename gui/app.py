"""
Main Tkinter window for CPU Scheduling Visualizer.

Layout: Title (top), Left (input), Right (algorithm + run + Gantt),
Bottom (results). Algorithm selection enables/disables Priority and Time Quantum.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ensure project root is on path when running as script
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils.validator import validate_processes, validate_time_quantum, ValidationError
from utils.helpers import compute_metrics
from algorithms import ALGORITHMS
from .input_panel import InputPanel
from .result_panel import ResultPanel
from .gantt_chart import GanttChartPanel


# Algorithm names and which need priority / time quantum
ALGO_PRIORITY = {"Priority (Non-Preemptive)", "Priority (Preemptive)"}
ALGO_TQ = {"Round Robin"}
ALGO_NAMES = list(ALGORITHMS.keys())


class CPUSchedulerApp:
    """
    Main application window.

    Integrates input panel, algorithm selection, run/compare actions,
    Gantt chart, and results panel. Handles validation and updates.
    """

    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("CPU Scheduling Visualizer")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        self._algo_var = tk.StringVar(value=ALGO_NAMES[0])
        self._input_panel = None
        self._result_panel = None
        self._gantt_panel = None
        self._last_processes = []
        self._last_gantt = []
        self._last_completion = {}
        self._step_index = 0
        self._step_mode = False
        self._build_ui()

    def _build_ui(self):
        # Top: project title
        title_frame = tk.Frame(self.root, bg="#1a365d", height=56)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        tk.Label(
            title_frame,
            text="CPU Scheduling Visualizer",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#1a365d",
        ).pack(expand=True)

        # Main content: left (input) | right (algo + gantt)
        main = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=6, bg="#e2e8f0")
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left = tk.Frame(main, width=320, bg="white", relief=tk.RAISED, bd=1)
        left.pack_propagate(False)
        main.add(left, width=320)

        self._input_panel = InputPanel(left)
        self._input_panel.get_frame().pack(fill=tk.BOTH, expand=True)

        right = tk.Frame(main, bg="white", relief=tk.RAISED, bd=1)
        main.add(right, width=400)

        # Algorithm selection
        algo_frame = tk.LabelFrame(right, text="Algorithm Selection", font=("Segoe UI", 10, "bold"), padx=8, pady=8)
        algo_frame.pack(fill=tk.X, padx=8, pady=8)

        for name in ALGO_NAMES:
            rb = ttk.Radiobutton(
                algo_frame,
                text=name,
                variable=self._algo_var,
                value=name,
                command=self._on_algo_change,
            )
            rb.pack(anchor="w", pady=2)

        btn_frame = tk.Frame(right)
        btn_frame.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_frame, text="Run", command=self._on_run).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Compare All Algorithms", command=self._on_compare).pack(side=tk.LEFT, padx=2)

        # Step-by-step controls (educational feature)
        step_frame = tk.LabelFrame(right, text="Step-by-Step Mode", font=("Segoe UI", 9, "bold"), padx=6, pady=6)
        step_frame.pack(fill=tk.X, padx=8, pady=6)
        self._step_label = tk.Label(step_frame, text="Current time: — | Running: —", font=("Segoe UI", 9))
        self._step_label.pack(anchor="w", pady=2)
        step_btn_f = tk.Frame(step_frame)
        step_btn_f.pack(fill=tk.X, pady=4)
        ttk.Button(step_btn_f, text="Step", command=self._on_step).pack(side=tk.LEFT, padx=2)
        ttk.Button(step_btn_f, text="Reset", command=self._on_step_reset).pack(side=tk.LEFT, padx=2)

        # Gantt chart
        gantt_frame = tk.LabelFrame(right, text="Gantt Chart", font=("Segoe UI", 10, "bold"), padx=6, pady=6)
        gantt_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self._gantt_panel = GanttChartPanel(gantt_frame, width=500, height=280)
        self._gantt_panel.get_frame().pack(fill=tk.BOTH, expand=True)

        # Bottom: results
        bottom = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        bottom.pack(fill=tk.BOTH, expand=False, padx=8, pady=(0, 8))
        self._result_panel = ResultPanel(bottom)
        self._result_panel.get_frame().pack(fill=tk.BOTH, expand=True)

        self._on_algo_change()

    def _on_algo_change(self):
        """Update Priority and Time Quantum visibility based on selected algorithm."""
        algo = self._algo_var.get()
        self._input_panel.enable_priority(algo in ALGO_PRIORITY)
        self._input_panel.enable_time_quantum(algo in ALGO_TQ)
        if algo in ALGO_TQ:
            self._input_panel.set_time_quantum("2")

    def _get_processes(self):
        """Return list of process dicts from input panel."""
        return self._input_panel.get_processes()

    def _validate_and_run(self, algo_name=None):
        """
        Validate input, run selected (or given) algorithm, update UI.
        Returns (processes, gantt_data, completion_times) or None on error.
        """
        processes = self._get_processes()
        if not processes:
            messagebox.showerror("Validation", "Please add at least one process.")
            return None

        algo = algo_name or self._algo_var.get()
        require_priority = algo in ALGO_PRIORITY
        try:
            validate_processes(processes, require_priority=require_priority)
        except ValidationError as e:
            messagebox.showerror("Validation", str(e))
            return None

        tq = None
        if algo in ALGO_TQ:
            try:
                tq = validate_time_quantum(self._input_panel.get_time_quantum())
            except ValidationError as e:
                messagebox.showerror("Validation", str(e))
                return None

        klass = ALGORITHMS.get(algo)
        if not klass:
            messagebox.showerror("Error", f"Unknown algorithm: {algo}")
            return None

        scheduler = klass()
        kwargs = {}
        if tq is not None:
            kwargs["time_quantum"] = tq
        gantt_data, completion_times = scheduler.run(processes, **kwargs)

        return processes, gantt_data, completion_times, algo

    def _on_run(self):
        """Run selected algorithm and update Gantt + results."""
        out = self._validate_and_run()
        if out is None:
            return
        processes, gantt_data, completion_times, algo = out
        self._last_processes = processes
        self._last_gantt = gantt_data
        self._last_completion = completion_times
        self._step_index = 0
        self._step_mode = True

        self._result_panel.update_results(processes, completion_times)
        # Step-by-step: start with first segment only; Step adds more
        partial = gantt_data[:1] if gantt_data else []
        self._gantt_panel.update_chart(partial, processes, title=f"Gantt Chart — {algo} (Step-by-Step)")
        self._update_step_label()

    def _update_step_label(self):
        """Update step-by-step label (current time, running process)."""
        if not self._last_gantt:
            self._step_label.config(text="Current time: — | Running: —")
            return
        # Show latest segment in current step view
        idx = min(self._step_index, len(self._last_gantt) - 1)
        pid, start, end = self._last_gantt[idx]
        self._step_label.config(
            text=f"Current time: {start:.1f}–{end:.1f} | Running: {pid} | Step {self._step_index + 1}/{len(self._last_gantt)}"
        )

    def _on_step(self):
        """Advance one Gantt segment (step-by-step mode)."""
        if not self._last_gantt:
            return
        self._step_index = min(self._step_index + 1, len(self._last_gantt))
        partial = self._last_gantt[: self._step_index + 1]
        self._gantt_panel.update_chart(partial, self._last_processes, title="Gantt Chart (Step-by-Step)")
        self._update_step_label()

    def _on_step_reset(self):
        """Reset step-by-step to full Gantt."""
        self._step_index = len(self._last_gantt) if self._last_gantt else 0
        self._gantt_panel.update_chart(self._last_gantt, self._last_processes, title="Gantt Chart (Full)")
        self._update_step_label()

    def _on_compare(self):
        """Run all algorithms, show comparison bar graphs (avg WT, avg TT)."""
        processes = self._get_processes()
        if not processes:
            messagebox.showerror("Validation", "Please add at least one process.")
            return

        require_priority_algos = ALGO_PRIORITY
        try:
            validate_processes(processes, require_priority=False)
        except ValidationError as e:
            messagebox.showerror("Validation", str(e))
            return

        # For priority-based algorithms, ensure every process has a priority (default 0).
        for p in processes:
            if "priority" not in p:
                p["priority"] = 0

        tq = 2.0
        if "Round Robin" in ALGORITHMS:
            try:
                tq = validate_time_quantum(self._input_panel.get_time_quantum())
            except ValidationError:
                tq = 2.0

        results = {}
        for name, klass in ALGORITHMS.items():
            req_pri = name in require_priority_algos
            if req_pri:
                try:
                    validate_processes(processes, require_priority=True)
                except ValidationError:
                    results[name] = {"avg_waiting": None, "avg_turnaround": None}
                    continue
            kwargs = {"time_quantum": tq} if name == "Round Robin" else {}
            try:
                gantt, comp = klass().run(processes, **kwargs)
                m = compute_metrics(processes, comp)
                results[name] = {"avg_waiting": m["avg_waiting"], "avg_turnaround": m["avg_turnaround"]}
            except Exception:
                results[name] = {"avg_waiting": None, "avg_turnaround": None}

        self._show_comparison_window(results)

    def _show_comparison_window(self, results):
        """Open Toplevel with bar graphs: avg WT and avg TT per algorithm; highlight best."""
        win = tk.Toplevel(self.root)
        win.title("Compare All Algorithms")
        win.geometry("700x520")
        win.transient(self.root)

        valid = {k: v for k, v in results.items() if v["avg_waiting"] is not None}
        best_wt = min(valid.keys(), key=lambda x: valid[x]["avg_waiting"]) if valid else None
        best_tt = min(valid.keys(), key=lambda x: valid[x]["avg_turnaround"]) if valid else None
        # Fallback if no valid results
        if not valid:
            txt = tk.Text(win, wrap=tk.WORD, font=("Consolas", 10))
            txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            txt.insert("end", "No valid results. Ensure processes have required fields (e.g. Priority for Priority algorithms).\n")
            return

        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
        except ImportError:
            # Fallback: text-only comparison
            txt = tk.Text(win, wrap=tk.WORD, font=("Consolas", 10))
            txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            for name, r in results.items():
                wt = r["avg_waiting"]
                tt = r["avg_turnaround"]
                w = f"{wt:.2f}" if wt is not None else "N/A"
                t = f"{tt:.2f}" if tt is not None else "N/A"
                b = ""
                if name == best_wt and name == best_tt:
                    b = " (best both)"
                elif name == best_wt:
                    b = " (best avg WT)"
                elif name == best_tt:
                    b = " (best avg TT)"
                txt.insert("end", f"{name}: Avg WT = {w}, Avg TT = {t}{b}\n")
            return

        fig = Figure(figsize=(6.5, 4.5), dpi=100, facecolor="#fafafa")
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        names = list(results.keys())
        wt_vals = [results[n]["avg_waiting"] if results[n]["avg_waiting"] is not None else 0 for n in names]
        tt_vals = [results[n]["avg_turnaround"] if results[n]["avg_turnaround"] is not None else 0 for n in names]
        colors_wt = ["#2E86AB" if n != best_wt else "#048A81" for n in names]
        colors_tt = ["#A23B72" if n != best_tt else "#95C623" for n in names]

        x = range(len(names))
        ax1.bar(x, wt_vals, color=colors_wt, edgecolor="#333", linewidth=0.8)
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=15, ha="right")
        ax1.set_ylabel("Average Waiting Time")
        ax1.set_title("Average Waiting Time by Algorithm (green = best)")

        ax2.bar(x, tt_vals, color=colors_tt, edgecolor="#333", linewidth=0.8)
        ax2.set_xticks(x)
        ax2.set_xticklabels(names, rotation=15, ha="right")
        ax2.set_ylabel("Average Turnaround Time")
        ax2.set_title("Average Turnaround Time by Algorithm (green = best)")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.run()
