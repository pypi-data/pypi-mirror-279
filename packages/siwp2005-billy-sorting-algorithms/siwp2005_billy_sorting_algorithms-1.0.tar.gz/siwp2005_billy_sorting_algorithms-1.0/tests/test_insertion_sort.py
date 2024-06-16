import unittest
from src.sort.insertion_sort import insertion_sort

class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort(self):
        self.assertEqual(insertion_sort([4, 2, 7, 1, 3]), [1, 2, 3, 4, 7])
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(insertion_sort([5]), [5])

if __name__ == '__main__':
    unittest.main()
