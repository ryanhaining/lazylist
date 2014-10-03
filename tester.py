#!/usr/bin/env python3

import unittest
import itertools

import lazylist

range_size = 10


class TestGetItem(unittest.TestCase):
    def test_incremental(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i]
            self.assertEqual(len(lazy._list), i + 1)
        self.assertEqual(len(lazy), range_size)
        for a, b in zip(lazy._list, range(range_size)):
            self.assertEqual(a, b)
            

    def test_all_at_once(self):
        lazy = lazylist.List(range(range_size))
        lazy[range_size - 1]
        self.assertEqual(len(lazy._list), range_size)

    def test_negative_index(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            self.assertEqual(lazy[-(i + 1)], range_size - i - 1)

class TestSetItem(unittest.TestCase):
    def test_zero_out(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy[i] = 0
        for i in range(range_size):
            self.assertEqual(lazy[i], 0)

    def test_slice_assign(self):
        lazy = lazylist.List(range(range_size))
        seq = list(range(range_size))
        lazy[2:5] = [10,20,30,40,50,60]
        seq[2:5] = [10,20,30,40,50,60]
        for i, e in enumerate(seq):
            self.assertEqual(lazy[i], e) 

    def test_negative_slice_assign(self):
        lazy = lazylist.List(range(range_size))
        seq = list(range(range_size))
        lazy[-2:-5] = [10,20,30,40,50,60]
        seq[-2:-5] = [10,20,30,40,50,60]
        for i, e in enumerate(seq):
            self.assertEqual(lazy[i], e) 
        

class TestDelItem(unittest.TestCase):
    def test_remove_middle(self):
        lazy = lazylist.List(range(range_size))
        del lazy[4]
        self.assertEqual(lazy[3] + 2, lazy[4])


class TestLen(unittest.TestCase):
    def test_lens(self):
        seq = list(range(10))
        self.assertEqual(len(seq), len(lazylist.List(seq)))


class TestContains(unittest.TestCase):
    def test_range(self):
        range_min = 10
        range_max = 20
        lazy = lazylist.List(range(range_min, range_max))
        for i in range(range_min, range_max):
            self.assertTrue(i in lazy)
        for i in range(0, range_min):
            self.assertFalse(i in lazy)
        for i in range(range_max, range_max + 10):
            self.assertFalse(i in lazy)

class TestBool(unittest.TestCase):
    def test_for_false(self):
        self.assertFalse(lazylist.List(range(0)))
        self.assertFalse(lazylist.List([]))

    def test_for_true(self):
        self.assertTrue(lazylist.List(range(1)))
        self.assertTrue(lazylist.List([1]))

class TestExtend(unittest.TestCase):
    def test_two_range(self):
        lazy = lazylist.List(range(10))
        lazy[3]
        lazy.extend(range(10, 20))
        for i in range(20):
            self.assertEqual(lazy[i], i)

    def test_iadd(self):
        lazy = lazylist.List(range(10))
        lazy[3]
        lazy += range(10, 20)
        for i in range(20):
            self.assertEqual(lazy[i], i)

class TestRepr(unittest.TestCase):
    def test_simple(self):
        lazy = lazylist.List(range(3))
        self.assertEqual(repr(lazy), '[0, 1, 2]')

class TestEquality(unittest.TestCase):
    def test_should_equal(self):
        a = lazylist.List(range(3))
        b = lazylist.List(range(3))
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_totally_different(self):
        a = lazylist.List(range(3))
        b = lazylist.List(range(3, 10))
        self.assertFalse(a == b)
        self.assertEqual(len(a._list), 1)
        self.assertEqual(len(b._list), 1)
        self.assertTrue(a != b)

    def test_different_length(self):
        a = lazylist.List(range(range_size))
        b = lazylist.List(range(range_size + 1))
        self.assertFalse(a == b)
        self.assertTrue(a != b)

    def test_with_list(self):
        a = lazylist.List(range(range_size))
        b = list(range(range_size))
        self.assertTrue(a == b)
        self.assertFalse(a != b)

class TestReversed(unittest.TestCase):
    def test_backwards_range(self):
        lazy = lazylist.List(range(range_size))
        for i, v in zip(range(9, -1, -1), reversed(lazy)):
            self.assertEqual(i, v)

    def test_in_place(self):
        lazy = lazylist.List(range(range_size))
        lazy.reverse()
        for i, v in zip(range(9, -1, -1), lazy):
            self.assertEqual(i, v)


class TestSort(unittest.TestCase):
    def test_sort(self):
        lazy = lazylist.List(range(range_size))
        lazy.sort()
        for i in range(len(lazy) - 1):
            self.assertLess(lazy[i], lazy[i] + 1) 

class TestPop(unittest.TestCase):
    def test_pop_default(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            self.assertEqual(len(lazy), range_size - i)
            self.assertEqual(lazy.pop(), range_size - i - 1)
            self.assertEqual(len(lazy), range_size - i - 1)


class TestIndex(unittest.TestCase):
    def test_index(self):
        lazy = lazylist.List(range(range_size))
        self.assertEqual(lazy.index(5), 5)
        self.assertEqual(len(lazy._list), 6)
        self.assertRaises(ValueError, lazy.index, 10)
        self.assertRaises(ValueError, lazy.index, -1)

    def test_index_with_bounds(self):
        lazy = lazylist.List(range(range_size))
        self.assertEqual(lazy.index(9, 5), 9)
        self.assertEqual(lazy.index(2, 0, -2), 2)
        self.assertEqual(lazy.index(5, -7, -2), 5)
        

class TestCount(unittest.TestCase):
    def test_count(self):
        lazy = lazylist.List(
            itertools.chain.from_iterable([i]*i for i in range(range_size)))
        for i in range(range_size):
            self.assertEqual(i, lazy.count(i))

class TestRemove(unittest.TestCase):
    def test_remove(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size):
            lazy.remove(i)
        self.assertEqual(len(lazy), 0)

    def test_remove_fails(self):
        lazy = lazylist.List(range(range_size))
        for i in range(range_size, range_size*2):
            self.assertRaises(ValueError, lazy.remove, i)

class TestInsert(unittest.TestCase):
    def test_insert(self):
        lazy = lazylist.List(range(range_size))
        lazy.insert(2, 'a')
        self.assertEqual(lazy[2], 'a')
        lazy.insert(10, 'b')
        self.assertEqual(lazy[10], 'b')

    def test_insert_negative(self):
        lazy = lazylist.List(range(range_size))
        lazy.insert(-1, 'c')
        self.assertEqual(lazy[-2], 'c')


class TestAppend(unittest.TestCase):
    def test_append(self):
        lazy = lazylist.List(range(range_size // 2))
        for i in range(range_size // 2, range_size):
            lazy.append(i)
        for i, j in zip(lazy, range(range_size)):
            self.assertEqual(i, j)

class TestClear(unittest.TestCase):
    def test_unevaluated(self):
        lazy = lazylist.List(range(range_size))
        lazy.clear()
        self.assertEqual(len(lazy), 0)

    def test_evaluated(self):
        lazy = lazylist.List(range(range_size))
        len(lazy)
        lazy.clear()
        self.assertEqual(len(lazy), 0)

    def test_clear_and_add(self):
        lazy = lazylist.List(range(range_size))
        lazy.clear()
        self.assertEqual(len(lazy), 0)
        lazy.extend(range(range_size))
        self.assertEqual(len(lazy), range_size)

class TestLessThan(unittest.TestCase):
    def test_simple(self):
        a = lazylist.List(range(1, range_size + 1))
        b = lazylist.List(range(range_size))
        self.assertTrue(b < a)
        self.assertFalse(a < b)

    def test_uneven(self):
        a = lazylist.List(range(range_size))
        b = lazylist.List(range(range_size - 1))
        self.assertTrue(b < a)
        self.assertFalse(a < b)

    def test_unordered(self):
        a = lazylist.List([1,9])
        b = lazylist.List([2, -1])
        self.assertTrue(a < b)
        self.assertFalse(b < a)




if __name__ == '__main__':
    unittest.main()
