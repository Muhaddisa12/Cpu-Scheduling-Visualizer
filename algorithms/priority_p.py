"""
Priority Scheduling – Preemptive.

Always run the highest-priority process among those arrived (lower value =
higher priority). Preemption when a higher-priority process arrives.
"""

from .base import BaseScheduler


class PriorityPreemptive(BaseScheduler):
    """
    Priority Preemptive: run highest-priority job; preempt on new arrival.

    OS Concept: Ensures high-priority tasks get CPU quickly. Risk of
    starvation for low-priority processes.
    """

    def _run(self, processes, **kwargs):
        """
        Execute preemptive priority scheduling.

        Event-based: at each arrival or completion, pick highest-priority
        among arrived, run until next event. Multiple Gantt slices per process.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time, priority).

        Returns:
            tuple: (gantt_data, completion_times).
        """
        procs = [
            {
                "process_id": p["process_id"],
                "arrival_time": p["arrival_time"],
                "burst_time": p["burst_time"],
                "priority": p["priority"],
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

        while len(completion_times) < n:
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

            # OS: Preempt when higher-priority process arrives; context switch per slice.
            chosen = min(candidates, key=lambda q: (q["priority"], q["arrival_time"]))
            pid = chosen["process_id"]
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
