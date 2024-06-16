#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest

from pywaffle.waffle import array_resize, division, flip_lines, round_up_to_multiple


class TestUtilities(unittest.TestCase):
    def test_array_resize(self):
        self.assertEqual(array_resize(array=[1, 2, 3, 4, 5], length=2), [1, 2])
        self.assertEqual(array_resize(array=[1, 2, 3, 4, 5], length=2, array_len=5), [1, 2])
        self.assertEqual(array_resize(array=[1, 2], length=5, array_len=2), [1, 2, 1, 2, 1])
        # when a tuple is passed
        self.assertEqual(array_resize(array=(1, 2), length=5, array_len=2), (1, 2, 1, 2, 1))

    def test_round_up_to_multiple(self):
        self.assertEqual(round_up_to_multiple(x=12, base=5), 15)
        self.assertIsInstance(round_up_to_multiple(x=12, base=5), int)

    def test_flip_lines(self):
        self.assertEqual(
            list(flip_lines(matrix=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], base=3)),
            [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0)],
        )
        self.assertEqual(
            list(flip_lines(matrix=[], base=3)),
            [],
        )
        self.assertEqual(
            list(flip_lines(matrix=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], base=0)),
            [],
        )

    def test_division(self):
        self.assertEqual(division(x=2, y=3, method="float"), 2 / 3)
        self.assertIsInstance(division(x=2, y=3, method="float"), float)

        self.assertEqual(division(x=2, y=3, method="nearest"), 1)
        self.assertIsInstance(division(x=2, y=3, method="nearest"), int)

        self.assertEqual(division(x=2, y=3, method="ceil"), 1)
        self.assertIsInstance(division(x=2, y=3, method="ceil"), int)

        self.assertEqual(division(x=2, y=3, method="floor"), 0)
        self.assertIsInstance(division(x=2, y=3, method="floor"), int)


if __name__ == "__main__":
    unittest.main()
