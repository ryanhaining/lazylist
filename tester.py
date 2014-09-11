#!/usr/bin/env python3

import unittest

import lazylist

class TestGetItem(unittest.TestCase):
    def setUp(self):
        pass
        #self.lazy = lazylist.List(range(20, 30))
    
    def test_incremental(self):
        range_size = 10
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i]
            self.assertEqual(len(lazy._list), i + 1)
        self.assertEqual(len(lazy), range_size)


if __name__ == '__main__':
    unittest.main()
