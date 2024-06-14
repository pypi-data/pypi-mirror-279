# tests/test_bubble_sort.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sort.bubble_sort import bubble_sort

class TestBubbleSort(unittest.TestCase):
    def test_bubble(self):
        arr = [0, 50, 7, 34, 66, 85]
        print('this is the unsorted list:')
        print(arr)
        result = bubble_sort.bubble_sort(arr)
        print('this is the (bubble) sorted list:')
        print(result)

if __name__ == "__main__":
    unittest.main()
