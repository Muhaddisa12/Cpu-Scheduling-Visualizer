"""
Helper utilities for CPU Scheduling Visualizer.

Provides shared colors for Gantt charts, process normalization,
and common data transformations.
"""

# Distinct colors for Gantt chart process blocks (one per process).
# Using a palette that works well for both light and dark themes.
COLORS = [
    "#2E86AB",  # Steel blue
    "#A23B72",  # Magenta
    "#F18F01",  # Orange
    "#C73E1D",  # Red
    "#3B1F2B",  # Dark purple
    "#95C623",  # Lime
    "#048A81",  # Teal
    "#D4A373",  # Tan
    "#6A4C93",  # Purple
    "#4ECDC4",  # Turquoise
    "#FF6B6B",  # Coral
    "#45B7D1",  # Sky blue
]


def get_color_for_process(process_id, color_map=None):
    """
    Return a consistent color for a process ID.

    Uses COLORS list; cycles if more processes than colors.
    Optional color_map can override (pid -> color).

    Args:
        process_id: Process identifier (e.g. 'P1', 'P2').
        color_map: Optional dict mapping process_id -> hex color.

    Returns:
        str: Hex color string.
    """
    if color_map and process_id in color_map:
        return color_map[process_id]
    pid_str = str(process_id)
    # Simple hash: use character codes to get reproducible index
    idx = sum(ord(c) for c in pid_str) % len(COLORS)
    return COLORS[idx]


def create_process_dict(process_id, arrival_time, burst_time, priority=None):
    """
    Build a normalized process dict from raw input.

    Args:
        process_id: Process ID (string or number).
        arrival_time: Arrival time (numeric).
        burst_time: Burst time (numeric).
        priority: Optional priority (int); used for priority-based algorithms.

    Returns:
        dict: Keys process_id, arrival_time, burst_time; priority if given.
    """
    out = {
        "process_id": str(process_id).strip(),
        "arrival_time": float(arrival_time),
        "burst_time": float(burst_time),
    }
    if priority is not None:
        out["priority"] = int(priority)
    return out


def compute_metrics(processes, completion_times):
    """
    Compute turnaround time, waiting time per process, and averages.

    Turnaround Time = Completion Time - Arrival Time
    Waiting Time = Turnaround Time - Burst Time

    Args:
        processes: List of dicts with process_id, arrival_time, burst_time.
        completion_times: Dict mapping process_id -> completion time.

    Returns:
        dict: {
            "per_process": [{process_id, arrival, burst, completion, turnaround, waiting}, ...],
            "avg_waiting": float,
            "avg_turnaround": float,
        }
    """
    per_process = []
    total_wt = 0.0
    total_tt = 0.0
    n = 0

    for p in processes:
        pid = p["process_id"]
        at = p["arrival_time"]
        bt = p["burst_time"]
        ct = completion_times.get(pid)
        if ct is None:
            continue
        tt = ct - at
        wt = tt - bt
        # Clamp waiting time to non-negative (edge case: burst 0, etc.)
        wt = max(0.0, wt)
        total_wt += wt
        total_tt += tt
        n += 1
        per_process.append({
            "process_id": pid,
            "arrival_time": at,
            "burst_time": bt,
            "completion_time": ct,
            "turnaround_time": tt,
            "waiting_time": wt,
        })

    avg_wt = total_wt / n if n else 0.0
    avg_tt = total_tt / n if n else 0.0

    return {
        "per_process": per_process,
        "avg_waiting": round(avg_wt, 2),
        "avg_turnaround": round(avg_tt, 2),
    }
