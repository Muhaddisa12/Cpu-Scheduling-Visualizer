# CPU Scheduling Visualizer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![Status](https://img.shields.io/badge/Status-Stable-success.svg)

**An interactive CPU Scheduling Algorithm Visualizer for Operating Systems courses**

Visualize and compare 6 different CPU scheduling algorithms with Gantt charts, metrics, and step-by-step execution.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Algorithms](#-algorithms) • [Examples](#-examples)

</div>

---

##  Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Algorithms](#-algorithms)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

##  Overview

**CPU Scheduling Visualizer** is a comprehensive desktop application designed for students and educators in Operating Systems courses. It provides an intuitive graphical interface to:

- **Input processes** with arrival times, burst times, and priorities
- **Visualize execution** using interactive Gantt charts
- **Calculate metrics** including waiting time, turnaround time, and their averages
- **Compare algorithms** side-by-side with bar graphs
- **Learn step-by-step** how each algorithm schedules processes

Built with **Python 3**, **Tkinter** (GUI), and **Matplotlib** (visualization), this tool is perfect for:
- OS lab submissions
- Viva presentations
- Understanding scheduling concepts
- Algorithm performance comparison

---

##  Features

### Core Functionality

-  **6 Scheduling Algorithms**
  - First Come First Serve (FCFS)
  - Shortest Job First - Non-Preemptive (SJF-NP)
  - Shortest Job First - Preemptive / SRTF (SJF-P)
  - Priority Scheduling - Non-Preemptive
  - Priority Scheduling - Preemptive
  - Round Robin (RR) with configurable time quantum

-  **Interactive Process Input**
  - Table-style input with Add/Delete rows
  - Dynamic Priority field (enabled only for priority algorithms)
  - Time Quantum input (enabled only for Round Robin)
  - Input validation with clear error messages

-  **Gantt Chart Visualization**
  - Color-coded process blocks
  - Start and end times displayed on each block
  - Idle CPU periods shown in gray
  - Multiple slices for preemptive algorithms (context switches)
  - Real-time updates

-  **Comprehensive Metrics**
  - Per-process: Completion Time, Turnaround Time, Waiting Time
  - System-wide: Average Waiting Time, Average Turnaround Time
  - Formatted results table

-  **Algorithm Comparison**
  - Run all 6 algorithms on the same input simultaneously
  - Side-by-side bar graphs for Average Waiting Time and Average Turnaround Time
  - Best-performing algorithm highlighted in green
  - Easy performance comparison

-  **Step-by-Step Mode**
  - Educational feature for understanding algorithm execution
  - Advance one Gantt segment at a time
  - Display current time and running process
  - Visual context switch highlighting

### User Experience

-  **Clean, Modern UI** with organized panels
-  **Dynamic Field Enabling** based on selected algorithm
-  **Input Validation** with helpful error messages
-  **Professional Visualizations** with Matplotlib
-  **Educational Comments** explaining OS concepts in code

---

##  Screenshots

> **Note:** Screenshots can be added here. The application features:
> - Left panel: Process input table with Add/Delete buttons
> - Right panel: Algorithm selection, Run/Compare buttons, Gantt chart
> - Bottom panel: Results table with metrics
> - Comparison window: Bar graphs showing algorithm performance

---

##  Installation

### Prerequisites

- **Python 3.8 or higher** (Python 3.9+ recommended)
- **pip** (Python package manager)
- **Tkinter** (usually included with Python)

### Step-by-Step Installation

1. **Clone or download the repository**

   ```bash
   git clone <repository-url>
   cd cpu_scheduling_visualizer
   ```

   Or download and extract the ZIP file.

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `matplotlib` (>=3.5.0) - For Gantt chart visualization

3. **Verify installation** (optional but recommended)

   ```bash
   python test_installation.py
   ```

   This will test:
   - All required modules are installed
   - All algorithms work correctly
   - Input validation functions properly

   Or manually verify:

   ```bash
   python -c "import matplotlib; print('Matplotlib installed successfully')"
   ```

### Troubleshooting Installation

**Issue: `ModuleNotFoundError: No module named 'matplotlib'`**

```bash
pip install matplotlib
```

**Issue: Tkinter not found (Linux)**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

**Issue: Python version too old**

- Ensure Python 3.8+ is installed: `python --version`
- Use `python3` instead of `python` if needed

---

##  Usage Guide

### Starting the Application

```bash
python main.py
```

Or from the project root directory:

```bash
cd cpu_scheduling_visualizer
python main.py
```

### Basic Workflow

#### 1. Enter Process Details

In the **left panel**:

- **Process ID**: Enter unique identifiers (e.g., `P1`, `P2`, `ProcessA`)
- **Arrival Time**: When the process arrives (non-negative, can be 0)
- **Burst Time**: CPU time required (non-negative)
- **Priority**: Only visible when Priority algorithms are selected
  - Lower number = Higher priority (e.g., 1 is higher priority than 5)

**Actions:**
- Click **Add Row** to add a new process
- Click **Delete Last Row** to remove the last process (at least one required)

**Example Input:**
```
Process ID | Arrival Time | Burst Time | Priority
-----------|--------------|------------|----------
P1         | 0            | 4          | 2
P2         | 1            | 3          | 1
P3         | 2            | 2          | 3
```

#### 2. Select Algorithm

In the **right panel**, choose one of six algorithms:

- **FCFS**: First Come First Serve
- **SJF (Non-Preemptive)**: Shortest Job First
- **SJF (Preemptive)**: Shortest Remaining Time First
- **Priority (Non-Preemptive)**: Priority-based scheduling
- **Priority (Preemptive)**: Preemptive priority scheduling
- **Round Robin**: Time-sliced scheduling

**Note:**
- Selecting **Priority** algorithms enables the Priority column
- Selecting **Round Robin** shows the Time Quantum input field
- Time Quantum default is 2 (can be changed)

#### 3. Run Algorithm

Click the **Run** button to:

1. Validate input (checks for errors)
2. Execute the selected algorithm
3. Display Gantt chart in the right panel
4. Show results table at the bottom with:
   - Per-process metrics
   - Average Waiting Time
   - Average Turnaround Time

#### 4. Step-by-Step Mode

After running an algorithm:

- **Step**: Click to advance one Gantt segment at a time
- **Reset**: Show the complete Gantt chart
- **Label**: Shows current time range and running process

**Educational Use:**
- Understand how processes are scheduled over time
- See context switches in preemptive algorithms
- Observe CPU idle periods

#### 5. Compare All Algorithms

Click **Compare All Algorithms** to:

1. Run all 6 algorithms on the same input
2. Open a comparison window with:
   - Bar graph: Average Waiting Time per algorithm
   - Bar graph: Average Turnaround Time per algorithm
   - Best algorithm highlighted in green

**Use Cases:**
- Performance analysis
- Algorithm selection for specific workloads
- Educational comparison

### Input Validation Rules

The application validates:

-  **At least one process** required
-  **Unique Process IDs** (no duplicates)
-  **Non-negative values** for Arrival Time, Burst Time
-  **Priority required** when Priority algorithms are selected
-  **Time Quantum > 0** required for Round Robin
- **Numeric values** only (no text in numeric fields)

**Error Messages:**
- Clear, descriptive error dialogs guide users to fix issues

---

##  Algorithms

### 1. First Come First Serve (FCFS)

**Type:** Non-Preemptive

**Description:**
- Processes are executed in the order they arrive
- No priority or burst-time consideration
- Simplest scheduling algorithm

**Characteristics:**
-  Simple to implement
-  Poor average waiting time (convoy effect)
-  No preemption

**When to Use:**
- Simple systems
- Batch processing
- Educational purposes

**Example:**
```
Processes: P1(AT=0, BT=4), P2(AT=1, BT=3), P3(AT=2, BT=2)
Gantt: [P1:0-4][P2:4-7][P3:7-9]
```

---

### 2. Shortest Job First - Non-Preemptive (SJF-NP)

**Type:** Non-Preemptive

**Description:**
- At each decision point, select the process with the smallest burst time among arrived processes
- Process runs to completion once selected

**Characteristics:**
-  Optimal average waiting time (when all arrive at once)
-  Starvation possible for long jobs
-  Requires knowledge of burst times

**When to Use:**
- Batch systems with known job lengths
- Minimizing average waiting time

**Example:**
```
Processes: P1(AT=0, BT=4), P2(AT=1, BT=3), P3(AT=2, BT=2)
Gantt: [P1:0-4][P3:4-6][P2:6-9]  (P3 selected before P2 due to shorter burst)
```

---

### 3. Shortest Job First - Preemptive (SRTF)

**Type:** Preemptive

**Description:**
- Always run the process with the shortest remaining time
- Preempts current process when a shorter job arrives
- Also called Shortest Remaining Time First (SRTF)

**Characteristics:**
-  Better average waiting time than SJF-NP
-  Responsive to new arrivals
-  More context switches (overhead)
-  Starvation possible

**When to Use:**
- Interactive systems
- When minimizing waiting time is critical

**Example:**
```
Processes: P1(AT=0, BT=4), P2(AT=1, BT=3), P3(AT=2, BT=2)
Gantt: [P1:0-1][P2:1-2][P3:2-4][P2:4-5][P1:5-6]
       (P1 preempted by P2, then P2 preempted by P3)
```

---

### 4. Priority Scheduling - Non-Preemptive

**Type:** Non-Preemptive

**Description:**
- Select the highest-priority process (lowest priority number)
- Process runs to completion once selected
- Tie-breaking: earlier arrival time

**Characteristics:**
-  Respects priority levels
-  Starvation for low-priority processes
-  No preemption

**Priority Convention:**
- **Lower number = Higher priority** (e.g., 1 > 2 > 3)

**When to Use:**
- Systems with priority-based requirements
- Real-time systems (with aging to prevent starvation)

**Example:**
```
Processes: P1(AT=0, BT=4, PR=2), P2(AT=1, BT=3, PR=1), P3(AT=2, BT=2, PR=3)
Gantt: [P1:0-4][P2:4-7][P3:7-9]  (P2 has highest priority but arrives after P1 starts)
```

---

### 5. Priority Scheduling - Preemptive

**Type:** Preemptive

**Description:**
- Always run the highest-priority process
- Preempts current process when a higher-priority process arrives

**Characteristics:**
-  Immediate response to high-priority tasks
-  Suitable for real-time systems
-  Severe starvation for low-priority processes
-  More context switches

**When to Use:**
- Real-time operating systems
- Systems with critical tasks

**Example:**
```
Processes: P1(AT=0, BT=4, PR=2), P2(AT=1, BT=3, PR=1), P3(AT=2, BT=2, PR=3)
Gantt: [P1:0-1][P2:1-4][P1:4-6][P3:6-8]
       (P1 preempted by P2, then P2 completes, then P1 resumes)
```

---

### 6. Round Robin (RR)

**Type:** Preemptive

**Description:**
- Each process gets a fixed time quantum
- If not completed, process is preempted and moved to the back of the ready queue
- Fair CPU sharing among all processes

**Characteristics:**
-  No starvation (fair scheduling)
-  Good for time-sharing systems
-  Performance depends on time quantum size
  - Too large → behaves like FCFS
  - Too small → excessive context switching overhead

**Time Quantum:**
- Configurable (default: 2)
- Should be larger than context switch time

**When to Use:**
- Interactive systems
- Time-sharing environments
- When fairness is important

**Example (Time Quantum = 2):**
```
Processes: P1(AT=0, BT=4), P2(AT=1, BT=3), P3(AT=2, BT=2)
Gantt: [P1:0-2][P2:2-4][P3:4-6][P1:6-8][P2:8-9]
       (Each process runs for up to 2 time units, then rotates)
```

---

##  Project Structure

```
cpu_scheduling_visualizer/
│
├── main.py                    # Application entry point
│
├── gui/                       # GUI components
│   ├── __init__.py
│   ├── app.py                 # Main Tkinter window and application logic
│   ├── input_panel.py         # Process input table UI
│   ├── result_panel.py        # Results table and metrics display
│   └── gantt_chart.py         # Matplotlib Gantt chart visualization
│
├── algorithms/                # Scheduling algorithm implementations
│   ├── __init__.py            # Algorithm registry and exports
│   ├── base.py                # Base scheduler abstract class
│   ├── fcfs.py                # First Come First Serve
│   ├── sjf_np.py              # Shortest Job First (Non-Preemptive)
│   ├── sjf_p.py               # Shortest Job First (Preemptive / SRTF)
│   ├── priority_np.py         # Priority Scheduling (Non-Preemptive)
│   ├── priority_p.py          # Priority Scheduling (Preemptive)
│   └── round_robin.py         # Round Robin
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── validator.py           # Input validation functions
│   └── helpers.py             # Helper functions (colors, metrics, etc.)
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Architecture Overview

**MVC-like Structure:**
- **Model**: Algorithm classes in `algorithms/`
- **View**: GUI components in `gui/`
- **Controller**: Application logic in `gui/app.py`

**Key Design Patterns:**
- **Strategy Pattern**: Each algorithm is a separate class inheriting from `BaseScheduler`
- **Observer Pattern**: GUI updates when algorithm results change
- **Factory Pattern**: Algorithm selection creates appropriate scheduler instance

---

##  Examples

### Example 1: Basic FCFS Scheduling

**Input:**
```
Process ID | Arrival Time | Burst Time
-----------|--------------|------------
P1         | 0            | 4
P2         | 1            | 3
P3         | 2            | 2
```

**Steps:**
1. Select **FCFS** algorithm
2. Click **Run**
3. View Gantt chart: `[P1:0-4][P2:4-7][P3:7-9]`

**Results:**
```
Process | Arrival | Burst | Completion | Turnaround | Waiting
--------|---------|-------|------------|------------|--------
P1      | 0       | 4     | 4          | 4          | 0
P2      | 1       | 3     | 7          | 6          | 3
P3      | 2       | 2     | 9          | 7          | 5

Average Waiting Time: 2.67
Average Turnaround Time: 5.67
```

---

### Example 2: Round Robin with Time Quantum

**Input:**
```
Process ID | Arrival Time | Burst Time
-----------|--------------|------------
P1         | 0            | 5
P2         | 1            | 3
P3         | 2            | 2
```

**Steps:**
1. Select **Round Robin**
2. Set **Time Quantum** to 2
3. Click **Run**

**Gantt Chart:**
```
[P1:0-2][P2:2-4][P3:4-6][P1:6-8][P2:8-9][P1:9-10]
```

**Observations:**
- Each process gets 2 time units per turn
- Processes rotate in the ready queue
- Fair CPU sharing

---

### Example 3: Priority Preemptive Scheduling

**Input:**
```
Process ID | Arrival Time | Burst Time | Priority
-----------|--------------|------------|----------
P1         | 0            | 4          | 2
P2         | 1            | 3          | 1
P3         | 2            | 2          | 3
```

**Steps:**
1. Select **Priority (Preemptive)**
2. Click **Run**

**Gantt Chart:**
```
[P1:0-1][P2:1-4][P1:4-6][P3:6-8]
```

**Observations:**
- P2 (priority 1) preempts P1 (priority 2) at time 1
- P1 resumes after P2 completes
- P3 (priority 3) runs last

---

### Example 4: Algorithm Comparison

**Input:**
```
Process ID | Arrival Time | Burst Time | Priority
-----------|--------------|------------|----------
P1         | 0            | 4          | 2
P2         | 1            | 3          | 1
P3         | 2            | 2          | 3
```

**Steps:**
1. Enter processes
2. Click **Compare All Algorithms**
3. View comparison window

**Results Summary:**
- **Best Avg Waiting Time**: SJF (Preemptive) or SJF (Non-Preemptive)
- **Best Avg Turnaround Time**: SJF algorithms
- **Most Fair**: Round Robin (no starvation)

---

##  Technical Details

### Dependencies

- **Python 3.8+**: Core language
- **Tkinter**: GUI framework (standard library)
- **Matplotlib 3.5.0+**: Gantt chart visualization

### Algorithm Implementation Details

**Data Structures:**
- Processes stored as dictionaries with keys: `process_id`, `arrival_time`, `burst_time`, `priority` (optional)
- Gantt data: List of tuples `(process_id, start_time, end_time)`
- Completion times: Dictionary mapping `process_id → completion_time`

**Time Complexity:**
- **FCFS**: O(n log n) - sorting by arrival time
- **SJF-NP**: O(n²) - selection sort at each step
- **SJF-P**: O(n log n) - event-based with sorting
- **Priority**: O(n²) - similar to SJF
- **Round Robin**: O(n × total_time / quantum) - queue operations

**Space Complexity:**
- All algorithms: O(n) - storing process data and results

### Metrics Calculation

**Turnaround Time (TT):**
```
TT = Completion Time - Arrival Time
```

**Waiting Time (WT):**
```
WT = Turnaround Time - Burst Time
```

**Average Waiting Time:**
```
Avg WT = (Sum of all WT) / Number of processes
```

**Average Turnaround Time:**
```
Avg TT = (Sum of all TT) / Number of processes
```

### Edge Cases Handled

-  **Zero burst time**: Process completes instantly at arrival
-  **Same arrival times**: Tie-breaking by process ID or input order
-  **Idle CPU**: Gray blocks shown when no process is ready
-  **Preemption**: Multiple Gantt slices for preemptive algorithms
-  **Empty input**: Validation prevents running with no processes

---

##  Troubleshooting

### Common Issues

**Problem: Application won't start**

```
ModuleNotFoundError: No module named 'matplotlib'
```

**Solution:**
```bash
pip install matplotlib
```

---

**Problem: GUI window doesn't appear**

- Check if Tkinter is installed: `python -m tkinter`
- On Linux, install `python3-tk` package
- Ensure display server is running (X11/Wayland)

---

**Problem: Gantt chart not displaying**

- Verify matplotlib is installed: `python -c "import matplotlib; print(matplotlib.__version__)"`
- Check for error messages in console
- Try running with a simple input (e.g., one process)

---

**Problem: "At least one process is required" error**

- Ensure at least one row has a non-empty Process ID
- Check that Process ID field is not just whitespace

---

**Problem: Priority field not appearing**

- Priority field is only visible when a Priority algorithm is selected
- Select "Priority (Non-Preemptive)" or "Priority (Preemptive)"

---

**Problem: Time Quantum field not appearing**

- Time Quantum is only visible for Round Robin
- Select "Round Robin" algorithm

---

**Problem: Comparison window shows "N/A" for some algorithms**

- Ensure all processes have Priority values when comparing Priority algorithms
- Check that input is valid for all algorithms

---

##  Contributing

Contributions are welcome! This project is designed for educational purposes.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- Additional scheduling algorithms (e.g., Multilevel Queue, Multilevel Feedback Queue)
- Export functionality (save Gantt chart as image, export results to CSV)
- Dark mode theme
- Animation for step-by-step mode
- Performance optimizations
- Unit tests
- Documentation improvements

### Code Style

- Follow **PEP 8** Python style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Include comments explaining OS concepts

---

##  License

This project is provided for **educational and academic purposes**. Feel free to use, modify, and distribute for learning and teaching.

---

##  Author

**CPU Scheduling Visualizer**  
Developed for Operating Systems academic courses

---

##  Acknowledgments

- **Operating Systems** course curriculum
- **Python Tkinter** documentation
- **Matplotlib** visualization library
- Educational resources on CPU scheduling algorithms

---

##  References

- Operating System Concepts (Silberschatz, Galvin, Gagne)
- CPU Scheduling Algorithms - GeeksforGeeks
- Python Tkinter Documentation
- Matplotlib Documentation

---

##  Educational Use

This tool is ideal for:

- **Students**: Understanding CPU scheduling concepts visually
- **Instructors**: Demonstrating algorithms in lectures
- **Labs**: Completing OS lab assignments
- **Viva**: Explaining algorithm behavior with visual aids

**Tips for Students:**
1. Start with simple examples (2-3 processes)
2. Use step-by-step mode to understand execution flow
3. Compare algorithms to see performance differences
4. Experiment with different time quanta for Round Robin
5. Try edge cases (same arrival times, zero burst, etc.)

---

<div align="center">

** If you find this project helpful, please consider giving it a star! **

Made with  for Operating Systems education

</div>
