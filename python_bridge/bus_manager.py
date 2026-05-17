import ctypes
import os
from enum import IntEnum

# --- Constants (Matching C defines) ---
MAX_NAME_LEN = 20
MIN_DUR = 10
MAX_DUR = 100
MAX_DIS = 1000
MIN_FREQ = 1
MAX_FREQ = 50

class SortType(IntEnum):
    DISTANCE = 0
    DURATION = 1
    FREQUENCY = 2

# --- Data Layer ---
class BusLine(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 21),
        ("distance", ctypes.c_int),
        ("duration", ctypes.c_int),
        ("frequency", ctypes.c_int)
    ]

# --- C Library Bridge ---
class BusLibrary:
    def __init__(self, lib_name="./libbus.so"):
        lib_path = os.path.abspath(lib_name)
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Library not found: {lib_path}")
        
        try:
            self.lib = ctypes.CDLL(lib_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load library: {e}")
            
        self._setup_prototypes()

    def _setup_prototypes(self):
        self.lib.bus_bubble_sort.argtypes = [ctypes.POINTER(BusLine), ctypes.POINTER(BusLine)]
        self.lib.bus_quick_sort.argtypes = [ctypes.POINTER(BusLine), ctypes.POINTER(BusLine), ctypes.c_int]
        self.lib.has_uppercase.argtypes = [ctypes.c_char_p]
        self.lib.has_uppercase.restype = ctypes.c_int

    def is_name_valid_in_c(self, name_bytes):
        """Calls C has_uppercase validation."""
        return self.lib.has_uppercase(name_bytes) == 0

# --- Management Layer ---
class BusManager:
    def __init__(self, library: BusLibrary):
        self.lib = library
        self.bus_lines = []

    def add_bus_line(self, name, distance, duration, frequency):
        """Validates and adds a bus line. Returns (success, error_msg)."""
        
        # 1. Input sanitization
        if '\0' in name:
            return False, "Security Error: Null characters not allowed"
        
        if any(ord(c) < 32 for c in name):
            return False, "Security Error: Control characters not allowed"

        # 2. Byte length validation (Buffer Overflow protection)
        try:
            encoded_name = name.encode('utf-8')
        except UnicodeEncodeError:
            return False, "Error: Invalid character encoding"

        if len(encoded_name) > 20:
            return False, f"Security Error: Name too long ({len(encoded_name)} bytes). Max 20."

        # 3. Content validation via C library
        if not self.lib.is_name_valid_in_c(encoded_name):
            return False, "Error: Bus name cannot contain uppercase letters"

        # 4. Range validation
        try:
            distance, duration, frequency = int(distance), int(duration), int(frequency)
        except (ValueError, TypeError):
            return False, "Error: Numeric fields must be integers"

        if not (0 <= distance <= MAX_DIS):
            return False, f"Error: distance {distance} out of range"
        
        if not (MIN_DUR <= duration <= MAX_DUR):
            return False, f"Error: duration {duration} out of range"
            
        if not (MIN_FREQ <= frequency <= MAX_FREQ):
            return False, f"Error: frequency {frequency} out of range"

        # 5. Object creation
        new_line = BusLine()
        new_line.name = encoded_name
        new_line.distance = distance
        new_line.duration = duration
        new_line.frequency = frequency
        
        self.bus_lines.append(new_line)
        return True, None

    def sort_and_get_results(self, sort_type: SortType = None):
        """Performs sorting via C binding and returns list of dictionaries."""
        n = len(self.bus_lines)
        if n == 0: return []

        BusArray = BusLine * n
        c_array = BusArray(*self.bus_lines)
        
        end_ptr = ctypes.cast(ctypes.addressof(c_array) + ctypes.sizeof(c_array), ctypes.POINTER(BusLine))

        if sort_type is None:
            self.lib.lib.bus_bubble_sort(c_array, end_ptr)
        else:
            self.lib.lib.bus_quick_sort(c_array, end_ptr, int(sort_type))

        return [
            {"name": line.name.decode('utf-8'), "distance": line.distance, 
             "duration": line.duration, "frequency": line.frequency}
            for line in c_array
        ]
