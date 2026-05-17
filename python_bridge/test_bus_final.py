import unittest
import random
from bus_manager import BusLibrary, BusManager, SortType

class TestBusSorting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Look for the library in the parent directory
        cls.lib = BusLibrary("../libbus.so")
        cls.manager = BusManager(cls.lib)

    def setUp(self):
        self.manager = BusManager(self.lib)

    # --- 1. Security & Validation ---
    def test_security_vulnerabilities(self):
        # UTF-8 byte length overflow
        long_name = "a" * 15 + "א" * 5 # UTF-8 multi-byte characters
        success, msg = self.manager.add_bus_line(long_name, 100, 20, 5)
        self.assertFalse(success)
        self.assertIn("Security Error", msg)

        # Null Byte injection
        success, msg = self.manager.add_bus_line("bus\0name", 100, 20, 5)
        self.assertFalse(success)
        
        # Control Characters
        success, msg = self.manager.add_bus_line("bus\nline", 100, 20, 5)
        self.assertFalse(success)

    def test_range_validation_extended(self):
        # Distance limits
        self.assertFalse(self.manager.add_bus_line("b", -1, 20, 5)[0])
        self.assertFalse(self.manager.add_bus_line("b", 1001, 20, 5)[0])
        # Duration limits
        self.assertFalse(self.manager.add_bus_line("b", 100, 9, 5)[0])
        self.assertFalse(self.manager.add_bus_line("b", 100, 101, 5)[0])
        # Frequency limits
        self.assertFalse(self.manager.add_bus_line("b", 100, 20, 0)[0])
        self.assertFalse(self.manager.add_bus_line("b", 100, 20, 51)[0])

    # --- 2. Sorting Tests ---
    def test_large_random_sort(self):
        random_distances = list(range(1, 1000, 50))
        random.shuffle(random_distances)
        
        for i, d in enumerate(random_distances):
            self.manager.add_bus_line(f"bus{i}", d, 20, 5)
        
        results = self.manager.sort_and_get_results(SortType.DISTANCE)
        sorted_distances = [r['distance'] for r in results]
        self.assertEqual(sorted_distances, sorted(random_distances))

    def test_reverse_sorted_input(self):
        for i in range(10, 0, -1):
            self.manager.add_bus_line(f"bus{i}", 100, 20, i)
        
        results = self.manager.sort_and_get_results(SortType.FREQUENCY)
        frequencies = [r['frequency'] for r in results]
        self.assertEqual(frequencies, list(range(1, 11)))

    def test_already_sorted_input(self):
        for i in range(1, 11):
            self.manager.add_bus_line(f"bus{i}", i * 10, 20, 5)
        
        results = self.manager.sort_and_get_results(SortType.DISTANCE)
        distances = [r['distance'] for r in results]
        self.assertEqual(distances, [i * 10 for i in range(1, 11)])

    def test_identical_values(self):
        for i in range(5):
            self.manager.add_bus_line(f"bus{i}", 100, 50, 10)
        
        results = self.manager.sort_and_get_results(SortType.DURATION)
        self.assertEqual(len(results), 5)
        for res in results:
            self.assertEqual(res['duration'], 50)

    # --- 3. Edge Cases ---
    def test_max_limits(self):
        success, _ = self.manager.add_bus_line("maxbus", 1000, 100, 50)
        self.assertTrue(success)
        
        results = self.manager.sort_and_get_results(SortType.DISTANCE)
        self.assertEqual(results[0]['distance'], 1000)

    def test_min_limits(self):
        success, _ = self.manager.add_bus_line("minbus", 0, 10, 1)
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
