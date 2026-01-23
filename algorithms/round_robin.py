"""
Round Robin (RR) CPU Scheduling.

Each process gets a fixed time quantum. If not completed, it is preempted
and moved to the back of the ready queue. Fair CPU sharing.
"""

from .base import BaseScheduler


class RoundRobin(BaseScheduler):
    """
    Round Robin: run each process for up to time_quantum, then rotate.

    OS Concept: Preemption by time slice; prevents starvation. Performance
    depends on quantum size (too large → FCFS-like; too small → overhead).
    """

    def _run(self, processes, **kwargs):
        """
        Execute Round Robin with given time quantum.

        Ready queue is FIFO. Process runs for min(remaining, TQ), then
        is requeued if remaining > 0. Handle idle when queue empty.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time).
            time_quantum: Max CPU time per turn (required for RR).

        Returns:
            tuple: (gantt_data, completion_times).
        """
        tq = float(kwargs.get("time_quantum", 1.0))
        if tq <= 0:
            tq = 1.0

        procs = [
            {
                "process_id": p["process_id"],
                "arrival_time": p["arrival_time"],
                "burst_time": p["burst_time"],
                "remaining": p["burst_time"],
            }
            for p in processes
        ]
        proc_map = {p["process_id"]: p for p in procs}
        # Sort by arrival for initial order; FCFS among same-time arrivals
        procs_sorted = sorted(procs, key=lambda x: (x["arrival_time"], x["process_id"]))
        gantt_data = []
        completion_times = {}
        current_time = 0.0
        n = len(procs)
        next_idx = 0
        queue = []

        def enqueue_arrived(now):
            nonlocal next_idx
            while next_idx < n and procs_sorted[next_idx]["arrival_time"] <= now:
                p = procs_sorted[next_idx]
                if p["process_id"] not in completion_times and p["remaining"] > 0:
                    queue.append(p)
                next_idx += 1

        enqueue_arrived(current_time)

        while len(completion_times) < n:
            if not queue:
                if next_idx >= n:
                    break
                next_arr = procs_sorted[next_idx]["arrival_time"]
                gantt_data.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                enqueue_arrived(current_time)
                continue

            # OS: Round Robin = fixed time quantum; preempt and requeue; fair, no starvation.
            chosen = queue.pop(0)
            pid = chosen["process_id"]
            run = min(chosen["remaining"], tq)
            start = current_time
            end = current_time + run
            gantt_data.append((pid, start, end))
            chosen["remaining"] -= run
            current_time = end
            enqueue_arrived(current_time)

            if chosen["remaining"] <= 0:
                completion_times[pid] = end
            else:
                queue.append(chosen)

        return gantt_data, completion_times
