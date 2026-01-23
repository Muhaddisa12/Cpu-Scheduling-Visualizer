"""
Shortest Job First (SJF) – Preemptive / Shortest Remaining Time First (SRTF).

At each time unit, run the process with smallest remaining burst time among
those already arrived. Preemption occurs when a shorter (remaining) job arrives.
"""

from .base import BaseScheduler


class SJFPreemptive(BaseScheduler):
    """
    SJF Preemptive (SRTF): always run job with shortest remaining time.

    OS Concept: Preemption on arrival of shorter job; minimizes average
    waiting time. Multiple Gantt slices per process possible.
    """

    def _run(self, processes, **kwargs):
        """
        Execute preemptive SJF (SRTF).

        Event-based: at each arrival or completion, choose shortest-remaining
        among arrived, run until next event. Handle idle CPU.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time).

        Returns:
            tuple: (gantt_data, completion_times).
        """
        procs = [
            {
                "process_id": p["process_id"],
                "arrival_time": p["arrival_time"],
                "burst_time": p["burst_time"],
                "remaining": p["burst_time"],
            }
            for p in processes
        ]
        arrivals = sorted([(p["arrival_time"], p["process_id"]) for p in procs])
        proc_map = {p["process_id"]: p for p in procs}
        gantt_data = []
        completion_times = {}
        current_time = 0.0
        arr_idx = 0
        n = len(procs)

        def arrived_by(t):
            return [proc_map[pid] for _, pid in arrivals if _ <= t]

        while len(completion_times) < n:
            # All arrived by current_time
            while arr_idx < len(arrivals) and arrivals[arr_idx][0] <= current_time:
                arr_idx += 1

            candidates = [
                q for q in procs
                if q["process_id"] not in completion_times
                and q["arrival_time"] <= current_time
                and q["remaining"] > 0
            ]

            if not candidates:
                if arr_idx >= len(arrivals):
                    break
                next_t = arrivals[arr_idx][0]
                gantt_data.append(("IDLE", current_time, next_t))
                current_time = next_t
                continue

            # OS: SRTF = preempt when shorter (remaining) job arrives; multiple slices per process.
            chosen = min(candidates, key=lambda q: (q["remaining"], q["arrival_time"]))
            pid = chosen["process_id"]

            # Next event: either completion of current job or arrival of a new one
            run_duration = chosen["remaining"]
            next_arrival = None
            if arr_idx < len(arrivals):
                next_arrival = arrivals[arr_idx][0]
                if next_arrival > current_time:
                    delta = next_arrival - current_time
                    if delta < run_duration:
                        run_duration = delta
                        next_event = next_arrival
                    else:
                        next_event = current_time + run_duration
                else:
                    next_event = current_time + run_duration
            else:
                next_event = current_time + run_duration

            start = current_time
            end = next_event
            gantt_data.append((pid, start, end))
            chosen["remaining"] -= (end - start)
            if chosen["remaining"] <= 0:
                completion_times[pid] = end
            current_time = end

        return gantt_data, completion_times
