import unittest
from src.sort.bubble_sort import bubble_sort

class TestBubbleSort(unittest.TestCase):
    def test_bubble_sort(self):
        self.assertEqual(bubble_sort([4, 2, 7, 1, 3]), [1, 2, 3, 4, 7])
        self.assertEqual(bubble_sort([]), [])
        self.assertEqual(bubble_sort([5]), [5])

if __name__ == '__main__':
    unittest.main()
