"""CPU Scheduling Algorithm implementations."""

from .fcfs import FCFS
from .sjf_np import SJFNonPreemptive
from .sjf_p import SJFPreemptive
from .priority_np import PriorityNonPreemptive
from .priority_p import PriorityPreemptive
from .round_robin import RoundRobin

ALGORITHMS = {
    "FCFS": FCFS,
    "SJF (Non-Preemptive)": SJFNonPreemptive,
    "SJF (Preemptive)": SJFPreemptive,
    "Priority (Non-Preemptive)": PriorityNonPreemptive,
    "Priority (Preemptive)": PriorityPreemptive,
    "Round Robin": RoundRobin,
}

__all__ = [
    "FCFS",
    "SJFNonPreemptive",
    "SJFPreemptive",
    "PriorityNonPreemptive",
    "PriorityPreemptive",
    "RoundRobin",
    "ALGORITHMS",
]
