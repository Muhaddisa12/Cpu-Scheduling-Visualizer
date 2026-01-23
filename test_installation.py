"""
Quick installation and functionality test for CPU Scheduling Visualizer.

Run this script to verify that all dependencies are installed correctly
and that the algorithms work as expected.

Usage:
    python test_installation.py
"""

import sys
import os

# Add project root to path
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import tkinter
        print("  ✓ Tkinter imported successfully")
    except ImportError:
        print("  ✗ Tkinter not found (usually included with Python)")
        return False
    
    try:
        import matplotlib
        print(f"  ✓ Matplotlib imported successfully (version {matplotlib.__version__})")
    except ImportError:
        print("  ✗ Matplotlib not found. Install with: pip install matplotlib")
        return False
    
    try:
        from algorithms import ALGORITHMS
        print(f"  ✓ Algorithms module imported ({len(ALGORITHMS)} algorithms)")
    except ImportError as e:
        print(f"  ✗ Algorithms module import failed: {e}")
        return False
    
    try:
        from utils.validator import validate_processes, validate_time_quantum
        print("  ✓ Utils module imported successfully")
    except ImportError as e:
        print(f"  ✗ Utils module import failed: {e}")
        return False
    
    try:
        from gui.app import CPUSchedulerApp
        print("  ✓ GUI module imported successfully")
    except ImportError as e:
        print(f"  ✗ GUI module import failed: {e}")
        return False
    
    return True


def test_algorithms():
    """Test that all algorithms can run with sample data."""
    print("\nTesting algorithms...")
    
    from algorithms import ALGORITHMS
    from utils.helpers import compute_metrics
    
    # Sample processes
    processes = [
        {"process_id": "P1", "arrival_time": 0, "burst_time": 4},
        {"process_id": "P2", "arrival_time": 1, "burst_time": 3},
        {"process_id": "P3", "arrival_time": 2, "burst_time": 2},
    ]
    
    # Processes with priority for priority algorithms
    processes_priority = [
        {"process_id": "P1", "arrival_time": 0, "burst_time": 4, "priority": 2},
        {"process_id": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
        {"process_id": "P3", "arrival_time": 2, "burst_time": 2, "priority": 3},
    ]
    
    success_count = 0
    total_count = len(ALGORITHMS)
    
    for name, Klass in ALGORITHMS.items():
        try:
            # Use priority processes for priority algorithms
            procs = processes_priority if "Priority" in name else processes
            
            # Round Robin needs time quantum
            kwargs = {"time_quantum": 2} if name == "Round Robin" else {}
            
            scheduler = Klass()
            gantt_data, completion_times = scheduler.run(procs, **kwargs)
            
            # Verify results
            if not completion_times:
                print(f"  ✗ {name}: No completion times returned")
                continue
            
            if len(completion_times) != len(procs):
                print(f"  ✗ {name}: Incomplete results ({len(completion_times)}/{len(procs)})")
                continue
            
            # Calculate metrics
            metrics = compute_metrics(procs, completion_times)
            
            print(f"  ✓ {name}: {len(gantt_data)} segments, "
                  f"Avg WT={metrics['avg_waiting']:.2f}, "
                  f"Avg TT={metrics['avg_turnaround']:.2f}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ {name}: Error - {e}")
    
    print(f"\nAlgorithm tests: {success_count}/{total_count} passed")
    return success_count == total_count


def test_validation():
    """Test input validation functions."""
    print("\nTesting validation...")
    
    from utils.validator import validate_processes, validate_time_quantum, ValidationError
    
    # Test valid processes
    try:
        valid_procs = [
            {"process_id": "P1", "arrival_time": 0, "burst_time": 4},
            {"process_id": "P2", "arrival_time": 1, "burst_time": 3},
        ]
        validate_processes(valid_procs)
        print("  ✓ Valid processes accepted")
    except ValidationError as e:
        print(f"  ✗ Valid processes rejected: {e}")
        return False
    
    # Test invalid processes (negative burst time)
    try:
        invalid_procs = [
            {"process_id": "P1", "arrival_time": 0, "burst_time": -1},
        ]
        validate_processes(invalid_procs)
        print("  ✗ Invalid processes (negative burst) accepted (should fail)")
        return False
    except ValidationError:
        print("  ✓ Invalid processes (negative burst) rejected correctly")
    
    # Test time quantum validation
    try:
        tq = validate_time_quantum(2.5)
        if tq == 2.5:
            print("  ✓ Time quantum validation works")
        else:
            print(f"  ✗ Time quantum validation returned wrong value: {tq}")
            return False
    except ValidationError as e:
        print(f"  ✗ Time quantum validation failed: {e}")
        return False
    
    # Test invalid time quantum
    try:
        validate_time_quantum(-1)
        print("  ✗ Invalid time quantum (negative) accepted (should fail)")
        return False
    except ValidationError:
        print("  ✓ Invalid time quantum (negative) rejected correctly")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("CPU Scheduling Visualizer - Installation Test")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies.")
        all_passed = False
    else:
        # Test algorithms
        if not test_algorithms():
            print("\n❌ Algorithm tests failed.")
            all_passed = False
        
        # Test validation
        if not test_validation():
            print("\n❌ Validation tests failed.")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Installation is correct.")
        print("\nYou can now run the application with:")
        print("  python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
