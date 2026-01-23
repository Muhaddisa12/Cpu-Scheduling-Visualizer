"""
Input validation for CPU Scheduling Visualizer.

Validates process data (PID, arrival time, burst time, priority)
and time quantum. Rejects negative values and malformed input.
"""


class ValidationError(Exception):
    """Raised when process or parameter validation fails."""

    pass


def validate_processes(processes, require_priority=False):
    """
    Validate a list of process dictionaries.

    Each process must have: process_id, arrival_time, burst_time.
    If require_priority is True, priority must also be present and valid.

    Args:
        processes: List of dicts with keys process_id, arrival_time, burst_time[, priority]
        require_priority: If True, each process must have a valid priority.

    Returns:
        None

    Raises:
        ValidationError: If any process is invalid or list is empty.
    """
    if not processes:
        raise ValidationError("At least one process is required.")

    seen_pids = set()
    for i, p in enumerate(processes):
        if not isinstance(p, dict):
            raise ValidationError(f"Process {i + 1}: expected dict, got {type(p).__name__}.")

        pid = p.get("process_id")
        if pid is None or (isinstance(pid, str) and not pid.strip()):
            raise ValidationError(f"Process {i + 1}: Process ID cannot be empty.")
        pid_str = str(pid).strip()
        if pid_str in seen_pids:
            raise ValidationError(f"Process {i + 1}: Duplicate Process ID '{pid_str}'.")
        seen_pids.add(pid_str)

        try:
            at = float(p.get("arrival_time", p.get("arrival", 0)))
        except (TypeError, ValueError):
            raise ValidationError(f"Process {i + 1}: Invalid arrival time '{p.get('arrival_time')}'.")
        if at < 0:
            raise ValidationError(f"Process {i + 1}: Arrival time cannot be negative.")

        try:
            bt = float(p.get("burst_time", p.get("burst", 0)))
        except (TypeError, ValueError):
            raise ValidationError(f"Process {i + 1}: Invalid burst time '{p.get('burst_time')}'.")
        if bt < 0:
            raise ValidationError(f"Process {i + 1}: Burst time cannot be negative.")
        # Zero burst is an edge case: process completes instantly at arrival
        # We allow it; algorithms must handle it.

        if require_priority:
            pr = p.get("priority")
            if pr is None:
                raise ValidationError(f"Process {i + 1}: Priority is required for this algorithm.")
            try:
                pr_val = int(pr)
            except (TypeError, ValueError):
                raise ValidationError(f"Process {i + 1}: Invalid priority '{pr}'.")
            # Allow any integer; "lower = higher priority" is algorithm convention


def validate_time_quantum(tq):
    """
    Validate time quantum for Round Robin.

    Args:
        tq: Value to check (int or float).

    Returns:
        float: Valid time quantum.

    Raises:
        ValidationError: If tq is missing, not numeric, or <= 0.
    """
    if tq is None:
        raise ValidationError("Time quantum is required for Round Robin.")
    try:
        val = float(tq)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid time quantum '{tq}'.")
    if val <= 0:
        raise ValidationError("Time quantum must be positive.")
    return val
