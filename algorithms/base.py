"""
Base class for CPU scheduling algorithms.

Provides common interface: run(processes, **kwargs) -> (gantt_data, completion_times).
All algorithms inherit from this and implement _run().
"""

from abc import ABC, abstractmethod


class BaseScheduler(ABC):
    """Abstract base for all CPU scheduling algorithms."""

    @abstractmethod
    def _run(self, processes, **kwargs):
        """
        Algorithm-specific execution logic.

        Args:
            processes: List of dicts with process_id, arrival_time, burst_time[, priority].
            **kwargs: Algorithm-specific args (e.g. time_quantum for RR).

        Returns:
            tuple: (gantt_data, completion_times)
                - gantt_data: List of (process_id, start_time, end_time).
                - completion_times: Dict process_id -> completion time.
        """
        pass

    def run(self, processes, **kwargs):
        """
        Run the scheduler on given processes.

        Validates input, delegates to _run, and returns normalized output.

        Args:
            processes: List of process dicts.
            **kwargs: Algorithm-specific parameters.

        Returns:
            tuple: (gantt_data, completion_times) as in _run.
        """
        if not processes:
            return [], {}
        return self._run(processes, **kwargs)
