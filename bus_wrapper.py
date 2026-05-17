import ctypes
from enum import IntEnum

# 1. הגדרת ה-Enum של סוגי המיון (מקביל ל-SortType ב-C)
class SortType(IntEnum):
    DISTANCE = 0
    DURATION = 1
    FREQUENCY = 2

# 2. הגדרת המבנה של קו אוטובוס (מקביל ל-struct BusLine ב-C)
class BusLine(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 21),    # מערך תווים בגודל 21
        ("distance", ctypes.c_int),     # מרחק (שלם)
        ("duration", ctypes.c_int),     # משך זמן (שלם)
        ("frequency", ctypes.c_int)     # תדירות (שלם)
    ]

def setup_library(lib_path):
    """
    מטעינה את הספריה ומגדירה את חתימות הפונקציות.
    """
    lib = ctypes.CDLL(lib_path)
    
    # הגדרת פונקציית ה-Bubble Sort (מיון לפי שם)
    # void bus_bubble_sort (BusLine *start, BusLine *end);
    lib.bus_bubble_sort.argtypes = [ctypes.POINTER(BusLine), ctypes.POINTER(BusLine)]
    lib.bus_bubble_sort.restype = None
    
    # הגדרת פונקציית ה-Quick Sort (מיון לפי סוג)
    # void bus_quick_sort (BusLine *start, BusLine *end, SortType sort_type);
    lib.bus_quick_sort.argtypes = [
        ctypes.POINTER(BusLine), 
        ctypes.POINTER(BusLine), 
        ctypes.c_int # SortType הוא למעשה Integer
    ]
    lib.bus_quick_sort.restype = None
    
    return lib

def sort_bus_lines(lib, data_list, sort_type=None):
    """
    פונקציית מעטפת:
    1. מקבלת רשימת נתונים מפייתון.
    2. מקצה זיכרון למערך C.
    3. קוראת לפונקציית ה-C המתאימה לביצוע המיון בפועל.
    4. מחזירה את הנתונים הממוינים.
    """
    n = len(data_list)
    if n == 0:
        return []

    # א. הקצאת מערך C רציף בזיכרון
    BusLineArray = BusLine * n
    c_array = BusLineArray()

    # ב. מילוי המערך בנתונים (המרה מ-Python ל-C)
    for i, item in enumerate(data_list):
        c_array[i].name = item['name'].encode('utf-8')
        c_array[i].distance = item['distance']
        c_array[i].duration = item['duration']
        c_array[i].frequency = item['frequency']

    # ג. חישוב המצביעים (Start ו-End)
    # ב-C של הפרויקט הזה, end מצביע לתא שאחרי האחרון
    start_ptr = ctypes.pointer(c_array[0])
    end_ptr = ctypes.pointer(c_array[n-1])
    # ליתר דיוק, המצביע לסוף הוא הכתובת של האיבר הראשון + מספר האיברים
    # ctypes מאפשר לנו לקבל את זה בקלות:
    end_ptr = ctypes.cast(ctypes.addressof(c_array) + ctypes.sizeof(c_array), ctypes.POINTER(BusLine))

    # ד. קריאה לפונקציית ה-C (המיון מתבצע בתוך הזיכרון של c_array)
    if sort_type is None:
        # אם לא נבחר סוג, נשתמש ב-Bubble Sort (לפי שם)
        lib.bus_bubble_sort(c_array, end_ptr)
    else:
        # אחרת, נשתמש ב-Quick Sort לפי הסוג שנבחר
        lib.bus_quick_sort(c_array, end_ptr, int(sort_type))

    # ה. החזרת התוצאות כרשימה פייתונית נקייה
    result = []
    for i in range(n):
        result.append({
            'name': c_array[i].name.decode('utf-8'),
            'distance': c_array[i].distance,
            'duration': c_array[i].duration,
            'frequency': c_array[i].frequency
        })
    
    return result
