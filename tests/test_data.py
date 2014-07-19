# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import unittest
import math

import data


class TestPoint(unittest.TestCase):

    def setUp(self):
        
        pass

    def test_test(self):
        
        self.assertEqual(True, True)

    def test_chunk_distance(self):

        p1 = data.Point(0, 0, 0)
        p2 = data.Point(0, 0, 0)
        result = p1.chunk_distance(p2)
        self.assertAlmostEqual(result, 0)

        p1 = data.Point(0, 0, 0)
        p2 = data.Point(0, 150, 0)
        result = p1.chunk_distance(p2)
        self.assertAlmostEqual(result, 0)

        p1 = data.Point(-10, 0, 0)
        p2 = data.Point(10, 0, 0)
        result = p1.chunk_distance(p2)
        self.assertAlmostEqual(result, 20)

        p1 = data.Point(0, 0, 10)
        p2 = data.Point(0, 0, -10)
        result = p1.chunk_distance(p2)
        self.assertAlmostEqual(result, 20)

        p1 = data.Point(-10, 0, 10)
        p2 = data.Point(10, 0, -10)
        result = p1.chunk_distance(p2)
        self.assertAlmostEqual(result, math.sqrt(pow(20, 2) + pow(-20, 2)))

