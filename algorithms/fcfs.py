"""
First Come First Serve (FCFS) CPU Scheduling Algorithm.

Non-preemptive: processes are executed in order of arrival.
No priority or burst-time consideration; first arrived runs until completion.
"""

from .base import BaseScheduler


class FCFS(BaseScheduler):
    """
    FCFS Scheduler: serve processes in arrival order.

    OS Concept: Simplest scheduling; no context switches except at completion.
    Poor for turnaround when short jobs arrive after long ones (convoy effect).
    """

    def _run(self, processes, **kwargs):
        """
        Execute FCFS on processes.

        Processes sorted by arrival time; ties broken by input order.
        Idle CPU: if next process arrives after current time, add idle slice.

        Args:
            processes: List of dicts (process_id, arrival_time, burst_time).

        Returns:
            tuple: (gantt_data, completion_times).
        """
        # OS: FCFS = no preemption; order of service = order of arrival.
        # Sort by arrival time; preserve order for same arrival (FCFS among ties)
        sorted_procs = sorted(
            enumerate(processes),
            key=lambda x: (x[1]["arrival_time"], x[0])
        )
        gantt_data = []
        completion_times = {}
        current_time = 0.0

        for _, p in sorted_procs:
            pid = p["process_id"]
            at = p["arrival_time"]
            bt = p["burst_time"]

            # OS: Idle CPU when no process has arrived yet (CPU wait).
            if at > current_time:
                gantt_data.append(("IDLE", current_time, at))
                current_time = at

            # Edge case: zero burst — process completes at arrival
            if bt <= 0:
                completion_times[pid] = current_time
                continue

            start = current_time
            end = current_time + bt
            gantt_data.append((pid, start, end))
            completion_times[pid] = end
            current_time = end

        return gantt_data, completion_times
