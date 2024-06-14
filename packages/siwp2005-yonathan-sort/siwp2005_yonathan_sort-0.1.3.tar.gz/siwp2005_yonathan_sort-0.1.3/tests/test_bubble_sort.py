import unittest
from sort.bubble_sort import BubbleSort

class TestBubbleSort(unittest.TestCase):
    def test_bubble_sort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        BubbleSort.sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])

if __name__ == "__main__":
    unittest.main()
