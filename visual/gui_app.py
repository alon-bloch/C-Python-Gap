import os
import sys
import time
from flask import Flask, render_template, jsonify, request

# Explicitly set the template and static folders
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')

# Adding bridge directory to path to import bus_manager
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'python_bridge')))
from bus_manager import BusLibrary, BusManager, SortType

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# --- Default Dataset (13 lines) ---
DEFAULT_BUSES = [
    {"name": "101", "distance": 150, "duration": 20, "frequency": 15},
    {"name": "42", "distance": 800, "duration": 60, "frequency": 5},
    {"name": "303", "distance": 120, "duration": 15, "frequency": 40},
    {"name": "12", "distance": 500, "duration": 40, "frequency": 10},
    {"name": "99", "distance": 900, "duration": 70, "frequency": 2},
    {"name": "7", "distance": 200, "duration": 18, "frequency": 30},
    {"name": "505", "distance": 350, "duration": 30, "frequency": 12},
    {"name": "22", "distance": 600, "duration": 50, "frequency": 8},
    {"name": "88", "distance": 450, "duration": 35, "frequency": 20},
    {"name": "15", "distance": 100, "duration": 12, "frequency": 50},
    {"name": "202", "distance": 700, "duration": 55, "frequency": 6},
    {"name": "33", "distance": 250, "duration": 22, "frequency": 25},
    {"name": "66", "distance": 400, "duration": 32, "frequency": 18}
]

# --- Sorting Engines ---

def get_bubble_sort_steps(data, criteria='name', optimized=False):
    start_time = time.time()
    steps = []
    arr = [dict(item) for item in data]
    n = len(arr)
    comparisons, swaps = 0, 0
    
    for i in range(n):
        swapped_in_pass = False
        for j in range(n - 1):
            comparisons += 1
            steps.append({
                "array": [dict(item) for item in arr],
                "cur": j, "next": j + 1, "current_pass": i,
                "action": "compare", "swap": False
            })
            
            if arr[j][criteria] > arr[j+1][criteria]:
                swaps += 1
                swapped_in_pass = True
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({
                    "array": [dict(item) for item in arr],
                    "cur": j, "next": j + 1, "current_pass": i,
                    "action": "swap", "swap": True
                })
        if optimized and not swapped_in_pass:
            steps.append({"array": [dict(item) for item in arr], "action": "early_exit", "current_pass": i})
            break
            
    execution_time = (time.time() - start_time) * 1000
    return {"steps": steps, "metrics": {"comparisons": comparisons, "swaps": swaps, "time": round(execution_time, 4)}}

def get_quick_sort_steps(data, criteria):
    start_time = time.time()
    steps = []
    arr = [dict(item) for item in data]
    metrics = {"comparisons": 0, "swaps": 0}
    
    def partition(low, high):
        pivot_idx = high
        pivot_val = arr[pivot_idx][criteria]
        small = low
        for current in range(low, high):
            metrics["comparisons"] += 1
            steps.append({"array": [dict(item) for item in arr], "low": low, "high": high, "small": small, "current": current, "pivot": pivot_idx, "action": "partition_compare", "swap": False})
            if arr[current][criteria] <= pivot_val:
                metrics["swaps"] += 1
                arr[current], arr[small] = arr[small], arr[current]
                steps.append({"array": [dict(item) for item in arr], "low": low, "high": high, "small": small, "current": current, "pivot": pivot_idx, "action": "partition_swap", "swap": True})
                small += 1
        metrics["swaps"] += 1
        arr[small], arr[high] = arr[high], arr[small]
        steps.append({"array": [dict(item) for item in arr], "low": low, "high": high, "small": small, "current": high, "pivot": small, "action": "pivot_placed", "swap": True})
        return small

    def quick_sort(low, high):
        if low < high:
            p = partition(low, high)
            quick_sort(low, p - 1)
            quick_sort(p + 1, high)

    quick_sort(0, len(arr) - 1)
    execution_time = (time.time() - start_time) * 1000
    return {"steps": steps, "metrics": {"comparisons": metrics["comparisons"], "swaps": metrics["swaps"], "time": round(execution_time, 4)}}

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/default_data')
def get_default_data():
    return jsonify(DEFAULT_BUSES)

@app.route('/api/sort_steps', methods=['POST'])
def sort_steps():
    data = request.json.get('data', [])
    if len(data) > 50:
        return jsonify({"error": "Data exceeds maximum limit (50 lines)"}), 400
    
    # Robust validation for each bus line
    for bus in data:
        name = str(bus.get('name', ''))
        dist = bus.get('distance')
        dur = bus.get('duration')
        freq = bus.get('frequency')
        
        if not (1 <= len(name) <= 20):
            return jsonify({"error": f"Invalid name length: {name}"}), 400
        if not isinstance(dist, int) or not (0 <= dist <= 1000):
            return jsonify({"error": f"Invalid distance: {dist}"}), 400
        if not isinstance(dur, int) or not (10 <= dur <= 100):
            return jsonify({"error": f"Invalid duration: {dur}"}), 400
        if not isinstance(freq, int) or not (1 <= freq <= 50):
            return jsonify({"error": f"Invalid frequency: {freq}"}), 400
            
    criteria = request.json.get('criteria', 'name')
    algo_type = request.json.get('algo_type', 'standard')
    
    if criteria == 'name':
        result = get_bubble_sort_steps(data, criteria, optimized=(algo_type == 'aborted'))
        algo = f"{'Aborted' if algo_type == 'aborted' else 'Standard'} Bubble Sort"
    else:
        result = get_quick_sort_steps(data, criteria)
        algo = "Quick Sort"
        
    return jsonify({"steps": result["steps"], "metrics": result["metrics"], "algo": algo})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
