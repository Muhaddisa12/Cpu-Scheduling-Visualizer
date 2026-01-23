"""
Priority Scheduling – Non-Preemptive.

At each decision point, choose the highest-priority process among those
already arrived (lower numeric value = higher priority). No preemption.
"""

from .base import BaseScheduler


class PriorityNonPreemptive(BaseScheduler):
    """
    Priority Non-Preemptive: run highest-priority arrived job to completion.

    OS Concept: Lower number = higher priority. Long high-priority jobs
    can delay lower-priority ones; starvation possible.
    """

    def _run(self, processes, **kwargs):
        """
        Execute non-preemptive priority scheduling.

        Requires 'priority' in each process. At each step, pick
        highest-priority (lowest value) among arrived, run to completion.

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
        gantt_data = []
        completion_times = {}
        current_time = 0.0
        n = len(procs)

        while len(completion_times) < n:
            arrived = [
                q for q in procs
                if q["arrival_time"] <= current_time
                and q["process_id"] not in completion_times
            ]

            if not arrived:
                next_arr = min(
                    q["arrival_time"] for q in procs
                    if q["process_id"] not in completion_times
                )
                gantt_data.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                continue

            # OS: Lower priority number = higher priority; no preemption.
            chosen = min(arrived, key=lambda q: (q["priority"], q["arrival_time"]))
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
