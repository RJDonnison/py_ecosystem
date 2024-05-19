import unittest
from math import sqrt

from classes.point2d import Point2d

class Test_Point2d(unittest.TestCase):
    """Test point2d class"""
    def setUp(self):
        self.p1 = Point2d(1, 2)
        self.p2 = Point2d(3, 4)
        self.p3 = Point2d(-1, -2)
        
    def test_initialization(self):
        self.assertEqual(self.p1.x, 1)
        self.assertEqual(self.p1.y, 2)  
        
    def test_repr(self):
        self.assertEqual(repr(self.p1), "Point2d(1, 2)")
        
    def test_str(self):
        self.assertEqual(str(self.p1), "(1, 2)")

    def test_addition(self):
        p = self.p1 + self.p2
        self.assertEqual(p.x, 4)
        self.assertEqual(p.y, 6)
        
    def test_subtraction(self):
        p = self.p1 - self.p2
        self.assertEqual(p.x, -2)
        self.assertEqual(p.y, -2)
        
    def test_distance(self):
        dist = self.p1.distance(self.p2)
        self.assertAlmostEqual(dist, sqrt(8))
        
    def test_midpoint(self):
        mid = self.p1.midpoint(self.p2)
        self.assertEqual(mid.x, 2)
        self.assertEqual(mid.y, 3)
        
    def test_add_type_error(self):
        with self.assertRaises(TypeError):
            self.p1 + "not a point"

    def test_sub_type_error(self):
        with self.assertRaises(TypeError):
            self.p1 - "not a point"

    def test_distance_type_error(self):
        with self.assertRaises(TypeError):
            self.p1.distance("not a point")

    def test_midpoint_type_error(self):
        with self.assertRaises(TypeError):
            self.p1.midpoint("not a point")
    
class Test_Creature(unittest.TestCase):
    """Test creature class"""