# Bus Sorting System & Visualizer
**Contest Participation: I would like to take part in the sorting competition.**

A hybrid C-Python system for managing and visualizing bus line sorting algorithms. This project integrates legacy C sorting logic with a modern, secure Python interface and a high-end web-based visualization tool.

## i. Implemented Features
*   **C Core**: Implementation of `Bubble Sort` (lexicographical) and `Quick Sort` (numerical) using pointer arithmetic.
*   **Pointer-Based Logic**: Direct memory manipulation consistent with low-level C management.
*   **Input Validation**: Robust C utility to ensure data integrity.

## ii. Extensions & Enhancements
*   **Modern Web GUI**: A Flask-based dashboard with:
    *   **Real-time Pointer Tracking**: Visual simulation of `cur`, `next`, `pivot`, and `small` pointers.
    *   **Swap Animations**: Smooth CSS transitions for swap operations.
    *   **Performance Metrics**: Tracking comparisons, swaps, and execution time.
    *   **Aborted Bubble Sort**: Optimized variant for early exit.
*   **Security Hardening**: Patched buffer overflows (sscanf), XSS protection, and DoS mitigation.

## iii. Project Structure
```text
.
├── sort_bus_lines.c/h      # Core C sorting logic
├── main.c                  # Original C CLI
├── test_bus_lines.c/h      # Original C tests
├── libbus.so               # Compiled shared library
│
├── python_bridge/          # Management & Security Layer
│   ├── bus_manager.py      # Python-C Bridge (ctypes)
│   └── test_bus_final.py   # Comprehensive integration tests
│
├── visual/                 # Visualization Extension
│   ├── gui_app.py          # Flask backend & Step Engine
│   ├── templates/          # HTML5 UI
│   └── static/             # CSS (Aesthetics) & JS (Animation)
│
└── README.md               # Documentation
```

## iv. How to Run
### Compilation (WSL/Linux)
```bash
gcc -fPIC -shared -o libbus.so sort_bus_lines.c main.c test_bus_lines.c
```

### Running the GUI Visualizer
1. Install dependencies: `pip install flask`
2. Run the server (inside WSL): `python3 visual/gui_app.py`
3. Open browser: `http://127.0.0.1:5000`

### Running Tests
```bash
cd python_bridge
python3 test_bus_final.py
```

## v. Repository
Git URL: https://github.com/alon-bloch/project2a
