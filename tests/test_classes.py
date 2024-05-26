# Add the parent directory (app) to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from math import sqrt

from classes.point2d import Point2d
from classes.creature import Creature
from classes.tree import Tree

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
        
    def test_distance_to(self):
        dist = self.p1.distance_to(self.p2)
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
            self.p1.distance_to("not a point")

    def test_midpoint_type_error(self):
        with self.assertRaises(TypeError):
            self.p1.midpoint("not a point")
    
class Test_Creature(unittest.TestCase):
    """Test creature class"""
    def setUp(self):
        """Set up test fixtures"""
        self.initial_pos = Point2d(2, 3)
        self.new_pos = Point2d(5, 6)
        self.energy = 15
        self.creature = Creature(self.initial_pos, self.energy)

    def test_initialization(self):
        """Test the initialization of a Creature"""
        self.assertEqual(self.creature.pos, self.initial_pos)
        self.assertEqual(self.creature.energy, self.energy)

    def test_repr(self):
        """Test the string representation of a Creature"""
        expected_repr = f"Creature({self.initial_pos.x}, {self.initial_pos.y}, {self.energy})"
        self.assertEqual(repr(self.creature), expected_repr)

    def test_move(self):
        """Test the move method of a Creature"""
        moved = self.creature.move(self.new_pos)
        self.assertTrue(moved)
        self.assertEqual(self.creature.pos, self.new_pos)
        expected_energy = self.energy - self.initial_pos.distance_to(self.new_pos)
        self.assertEqual(self.creature.energy, expected_energy)

    def test_move_insufficient_energy(self):
        """Test the move method of a Creature with insufficient energy"""
        self.creature.energy = 1  # Set low energy
        moved = self.creature.move(self.new_pos)
        self.assertFalse(moved)
        self.assertEqual(self.creature.pos, self.initial_pos)  # Position should not change
        
class Test_Tree(unittest.TestCase):
    """Test tree class"""
    def test_initialization(self):
        """Test the initialization of a Tree"""
        pos = Point2d(2, 3)
        food = 5
        tree = Tree(pos, food)
        
        self.assertEqual(tree.pos, pos)
        self.assertEqual(tree.food, food)

    def test_repr(self):
        """Test the string representation of a Tree"""
        pos = Point2d(2, 3)
        food = 5
        tree = Tree(pos, food)
        
        expected_repr = f"Tree({pos.x}, {pos.y}, {food})"
        self.assertEqual(repr(tree), expected_repr)