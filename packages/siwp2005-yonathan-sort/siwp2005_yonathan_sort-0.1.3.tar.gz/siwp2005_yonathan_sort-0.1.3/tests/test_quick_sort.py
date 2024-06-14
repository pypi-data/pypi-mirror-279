import unittest
from sort.quick_sort import QuickSort

class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        QuickSort.sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

if __name__ == "__main__":
    unittest.main()