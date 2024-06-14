import unittest
from sort.insertion_sort import InsertionSort

class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        InsertionSort.sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

if __name__ == "__main__":
    unittest.main()