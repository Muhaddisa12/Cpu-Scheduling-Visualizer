# Contributing to CPU Scheduling Visualizer

Thank you for your interest in contributing to CPU Scheduling Visualizer! This document provides guidelines and instructions for contributing.

## 🎯 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title** describing the bug
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** (if applicable)
- **Python version** and **OS** information

### Suggesting Features

Feature suggestions are welcome! Please include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit with clear messages**: `git commit -m "Add: description of change"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## 📋 Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **88 characters** (Black formatter default)
- Use **type hints** where appropriate

### Code Structure

- **One class per file** (when possible)
- **Meaningful names** for variables, functions, and classes
- **Docstrings** for all functions and classes (Google style)
- **Comments** explaining OS concepts and complex logic

### Example Code Style

```python
def calculate_turnaround_time(completion_time: float, arrival_time: float) -> float:
    """
    Calculate turnaround time for a process.

    Args:
        completion_time: Time when process completes execution
        arrival_time: Time when process arrives in ready queue

    Returns:
        Turnaround time (completion - arrival)
    """
    return completion_time - arrival_time
```

## 🧪 Testing

Before submitting:

1. **Test with different inputs**:
   - Simple cases (2-3 processes)
   - Complex cases (many processes)
   - Edge cases (same arrival times, zero burst, etc.)

2. **Test all algorithms** if your change affects core scheduling logic

3. **Verify GUI** still works correctly

4. **Check for errors** in console output

## 📝 Documentation

- Update **README.md** if adding new features
- Add **docstrings** to new functions/classes
- Include **examples** in docstrings when helpful
- Update **algorithm descriptions** if behavior changes

## 🎨 UI/UX Guidelines

- **Consistent styling** with existing UI
- **Clear labels** and **helpful error messages**
- **Responsive layout** (works on different window sizes)
- **Accessibility**: Consider colorblind-friendly colors

## 🔍 Pull Request Process

1. **Update documentation** for any new features
2. **Ensure code follows style guidelines**
3. **Test on your system** before submitting
4. **Write clear PR description**:
   - What changes were made
   - Why they were made
   - How to test the changes

## 🚀 Feature Ideas

Areas where contributions would be valuable:

### Algorithms
- Multilevel Queue Scheduling
- Multilevel Feedback Queue
- Lottery Scheduling
- Fair Share Scheduling

### Features
- Export Gantt chart as PNG/PDF
- Export results to CSV/Excel
- Save/Load process configurations
- Dark mode theme
- Animation for step-by-step mode
- Process arrival animation
- Multiple time quantum support (for MLFQ)

### Improvements
- Performance optimizations
- Unit tests
- Integration tests
- Better error handling
- Internationalization (i18n)
- Accessibility improvements

## ❓ Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in Issues
- Contact maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CPU Scheduling Visualizer! 🎉
