🚌 Bus Sorting System & Visualizer
A hybrid C-Python system for implementing, managing, and visualizing sorting algorithms on bus-line datasets.

This project combines low-level C programming, Python interoperability, and a Flask-based visualization interface to create an interactive educational and algorithm-analysis platform.

The project began as a university assignment focused on implementing sorting algorithms in C, and later evolved into a full hybrid C-Python system with an interactive visualization layer.

The goal was not only to implement sorting algorithms, but also to explore:
- low-level memory manipulation,
- Python-C interoperability,
- algorithm visualization,
- and modular software design.

The project combines systems programming concepts with practical tooling and interactive visualization.

🚀 Features
Core Algorithm Engine (C)
Implemented Bubble Sort and Quick Sort in C
Used pointer arithmetic and direct memory manipulation
Added robust input-validation utilities
Designed low-level sorting logic for performance and correctness
Python Integration Layer
Built a Python-C bridge using ctypes
Enabled Python-based orchestration of native C sorting functions
Added automated integration testing and execution management
Interactive Visualization Dashboard
Developed a Flask-based web interface for algorithm visualization
Added real-time pointer tracking:
cur
next
pivot
small
Implemented animated swap visualization using JavaScript and CSS
Displayed execution metrics:
comparisons
swaps
execution time

🧠 Technical Concepts Demonstrated
Low-level memory management
Pointer arithmetic
Sorting algorithms
Python-C interoperability
Backend development with Flask
Automated testing
Algorithm visualization
Input validation and defensive programming

🛠️ Technologies Used
Technology	Purpose
C	Core sorting engine
Python	Integration & orchestration
Flask	Web visualization backend
ctypes	Python-C bridge
HTML/CSS/JavaScript	Interactive frontend
GCC	Shared library compilation

📁 Project Structure

.

├── sort_bus_lines.c/h      # Core C sorting logic

├── main.c                  # Original CLI application

├── test_bus_lines.c/h      # C unit/integration tests

├── libbus.so               # Compiled shared library

│
├── python_bridge/

│   ├── bus_manager.py      # Python-C integration layer

│   └── test_bus_final.py   # Python integration tests

│
├── visual/

│   ├── gui_app.py          # Flask visualization server

│   ├── templates/          # HTML templates

│   └── static/             # CSS & JavaScript assets
│
└── README.md


https://github.com/alon-bloch/C-Python-Gap
