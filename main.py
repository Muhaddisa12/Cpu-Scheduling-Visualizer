"""
CPU Scheduling Visualizer – Application entry point.

Run from project root: python main.py
"""

import sys
import os

# Ensure project root is on path
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from gui.app import CPUSchedulerApp
except ModuleNotFoundError as e:
    if "matplotlib" in str(e).lower():
        print("Matplotlib is required. Install with: pip install -r requirements.txt")
    else:
        print(f"Missing module: {e}")
    sys.exit(1)


def main():
    """Launch the CPU Scheduling Visualizer GUI."""
    app = CPUSchedulerApp()
    app.run()


if __name__ == "__main__":
    main()
