# Changelog

All notable changes to CPU Scheduling Visualizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-23

### Added
- Initial release of CPU Scheduling Visualizer
- **6 Scheduling Algorithms**:
  - First Come First Serve (FCFS)
  - Shortest Job First - Non-Preemptive (SJF-NP)
  - Shortest Job First - Preemptive / SRTF (SJF-P)
  - Priority Scheduling - Non-Preemptive
  - Priority Scheduling - Preemptive
  - Round Robin with configurable time quantum
- **Interactive GUI** with Tkinter:
  - Process input table with Add/Delete functionality
  - Dynamic Priority and Time Quantum fields
  - Algorithm selection via radio buttons
  - Run and Compare All buttons
- **Gantt Chart Visualization**:
  - Color-coded process blocks
  - Start and end times on each block
  - Idle CPU visualization
  - Support for preemptive algorithms (multiple slices)
- **Results Panel**:
  - Per-process metrics table
  - Average Waiting Time and Average Turnaround Time
  - Formatted numerical display
- **Step-by-Step Mode**:
  - Advance one Gantt segment at a time
  - Current time and running process display
  - Reset to full Gantt chart
- **Algorithm Comparison**:
  - Run all 6 algorithms simultaneously
  - Bar graphs for Average Waiting Time and Average Turnaround Time
  - Best algorithm highlighting
- **Input Validation**:
  - Non-negative value checks
  - Unique Process ID validation
  - Priority requirement for priority algorithms
  - Time Quantum validation for Round Robin
- **Educational Features**:
  - Inline comments explaining OS concepts
  - Step-by-step execution visualization
  - Context switch highlighting
- **Documentation**:
  - Comprehensive README.md
  - CONTRIBUTING.md guidelines
  - CHANGELOG.md
  - LICENSE file
  - .gitignore for Python projects

### Technical Details
- Python 3.8+ support
- Modular architecture (MVC-like)
- Base scheduler abstract class for algorithm implementations
- Utility modules for validation and helpers
- Error handling and user-friendly error messages

### Known Limitations
- No export functionality (Gantt chart as image, results as CSV)
- No save/load process configurations
- Single time quantum for Round Robin (no MLFQ support)
- No animation in step-by-step mode

---

## [Unreleased]

### Planned Features
- Export Gantt chart as PNG/PDF
- Export results to CSV/Excel
- Save/Load process configurations
- Dark mode theme
- Animation for step-by-step mode
- Additional algorithms (Multilevel Queue, MLFQ)
- Unit tests
- Performance optimizations

---

## Version History

- **1.0.0** (2025-01-23): Initial release

---

For detailed information about each version, see the [GitHub Releases](https://github.com/yourusername/cpu-scheduling-visualizer/releases) page.
