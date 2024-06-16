import unittest
from src.sort.quick_sort import quick_sort

class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        self.assertEqual(quick_sort([4, 2, 7, 1, 3]), [1, 2, 3, 4, 7])
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(quick_sort([5]), [5])

if __name__ == '__main__':
    unittest.main()
