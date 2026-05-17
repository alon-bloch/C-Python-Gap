from bus_manager import BusLibrary, BusManager, SortType

def main():
    try:
        # 1. אתחול הספריה והמנהל
        lib = BusLibrary("./libbus.so")
        manager = BusManager(lib)
        
        print("--- Testing Validation ---")
        
        # ניסיון להוסיף קו עם אותיות גדולות (ייכשל בגלל ה-C)
        success, msg = manager.add_bus_line("Bus-Line-A", 100, 20, 5)
        if not success: print(f"Caught expected error: {msg}")
        
        # ניסיון להוסיף קו עם מרחק לא תקין (ייכשל בגלל ה-Python)
        success, msg = manager.add_bus_line("bus-line-b", 5000, 20, 5)
        if not success: print(f"Caught expected error: {msg}")

        print("\n--- Adding Valid Lines ---")
        manager.add_bus_line("green-line", 500, 40, 10)
        manager.add_bus_line("blue-line", 200, 15, 30)
        manager.add_bus_line("red-line", 800, 60, 5)
        print("Added 3 lines successfully.")

        # 2. מיון לפי שם (Bubble Sort)
        print("\n--- Sorting by Name (Bubble Sort) ---")
        results = manager.sort_and_get_results() # ברירת מחדל היא Bubble Sort
        for res in results:
            print(f"Name: {res['name']:<12} | Dist: {res['distance']:<5}")

        # 3. מיון לפי מרחק (Quick Sort)
        print("\n--- Sorting by Distance (Quick Sort) ---")
        results = manager.sort_and_get_results(SortType.DISTANCE)
        for res in results:
            print(f"Name: {res['name']:<12} | Dist: {res['distance']:<5}")

        # 4. מיון לפי תדירות (Quick Sort)
        print("\n--- Sorting by Frequency (Quick Sort) ---")
        results = manager.sort_and_get_results(SortType.FREQUENCY)
        for res in results:
            print(f"Name: {res['name']:<12} | Freq: {res['frequency']:<5}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
