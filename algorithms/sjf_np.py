"""
Shortest Job First (SJF) – Non-Preemptive CPU Scheduling.

At each decision point, choose the process with smallest burst time among
those already arrived. No preemption; selected process runs to completion.
"""

from .base import BaseScheduler


class SJFNonPreemptive(BaseScheduler):
    """
    SJF Non-Preemptive: always run shortest available job.

    OS Concept: Minimizes average waiting time when all arrive together.
    Starvation possible for long jobs if short jobs keep arriving.
    """

    def _run(self, processes, **kwargs):
        """
        Execute non-preemptive SJF.

        Simulate time; at each step pick shortest-burst among arrived,
        run to completion. Handle idle CPU when no process has arrived.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time).

        Returns:
            tuple: (gantt_data, completion_times).
        """
        # Working copy: track remaining burst (all run to completion here)
        procs = [
            {
                "process_id": p["process_id"],
                "arrival_time": p["arrival_time"],
                "burst_time": p["burst_time"],
                "remaining": p["burst_time"],
            }
            for p in processes
        ]
        gantt_data = []
        completion_times = {}
        current_time = 0.0
        n = len(procs)

        while len(completion_times) < n:
            # Candidates: arrived by current_time, not yet completed
            arrived = [
                q for q in procs
                if q["arrival_time"] <= current_time
                and q["process_id"] not in completion_times
            ]

            if not arrived:
                # Idle: advance to next arrival
                next_arr = min(q["arrival_time"] for q in procs if q["process_id"] not in completion_times)
                gantt_data.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                continue

            # OS: SJF minimizes avg waiting when all arrive together; no preemption.
            # Choose smallest burst (then smallest arrival for tie).
            chosen = min(arrived, key=lambda q: (q["burst_time"], q["arrival_time"]))
            pid = chosen["process_id"]
            bt = chosen["burst_time"]

            if bt <= 0:
                completion_times[pid] = current_time
                continue

            start = current_time
            end = current_time + bt
            gantt_data.append((pid, start, end))
            completion_times[pid] = end
            current_time = end

        return gantt_data, completion_times
