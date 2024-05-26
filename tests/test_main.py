# Add the parent directory (app) to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot

import unittest
from unittest.mock import mock_open, patch

import numpy as np
import matplotlib.pyplot as plt

from main import Simulation
from classes.point2d import Point2d
from classes.creature import Creature
from classes.tree import Tree

class Test_Simulation(unittest.TestCase):
    """Test simulation"""
    def setUp(self):
        self.file = 'data/simulation.csv'
        self.start_population = 10
        self.num_trees = 5
        self.turns = 7
        self.grid_size = 10
        self.sim = Simulation(self.start_population, self.num_trees, self.grid_size, self.file)

        
    def test_initialization(self):
        self.assertEqual(self.sim.population, self.start_population)
        self.assertEqual(self.sim.filename, self.file)
        self.assertEqual(self.sim.grid_size, self.grid_size)
        self.assertEqual(self.sim.current_turn, 0)
        self.assertEqual(len(self.sim.grid), self.grid_size)
        self.assertEqual(len(self.sim.grid[0]), self.grid_size)

    def test_repr(self):
        self.assertEqual(repr(self.sim), f"Simulation({self.start_population}, {self.num_trees}, {self.grid_size}, {self.file})")

    def test_str(self):
        self.assertEqual(str(self.sim), f"({self.start_population}, {self.num_trees}, {self.grid_size}, {self.file}, 0)")

    def test_create_grid(self):
        grid = self.sim.create_grid(self.grid_size)
        self.assertEqual(len(grid), self.grid_size)
        self.assertEqual(len(grid[0]), self.grid_size)
        self.assertTrue(all(isinstance(cell, list) for row in grid for cell in row))

    def test_populate_grid(self):
        self.sim.populate_grid(self.start_population)
        count = sum(len(cell) for row in self.sim.grid for cell in row if any(isinstance(obj, Creature) for obj in cell))
        self.assertEqual(count, self.start_population)
        
    def test_add_trees(self):
        self.sim.add_trees()
        count = sum(len(cell) for row in self.sim.grid for cell in row if any(isinstance(obj, Tree) for obj in cell))
        self.assertEqual(count, self.num_trees)
        
    def test_move_creature(self):
        creature = Creature(Point2d(0, 0))
        self.sim.grid[0][0].append(creature)
        new_pos = Point2d(1, 1)
        self.sim.move(creature, new_pos)
        self.assertNotIn(creature, self.sim.grid[0][0])
        self.assertIn(creature, self.sim.grid[1][1])
        self.assertEqual(creature.pos, new_pos)

    def test_find_closest_food(self):
        tree1 = Tree(Point2d(0, 0))
        tree2 = Tree(Point2d(4, 4))
        self.sim.grid[0][0].append(tree1)
        self.sim.grid[4][4].append(tree2)
        creature_pos = Point2d(2, 2)

        closest_food = self.sim.find_closest_food(creature_pos)
        self.assertEqual(closest_food, Point2d(0, 0))

    def test_distribute_food(self):
        tree = Tree(Point2d(0, 0))
        tree.food = 3
        creature1 = Creature(Point2d(0, 0))
        creature2 = Creature(Point2d(0, 0))
        creature3 = Creature(Point2d(0, 0))
        creature1.energy = 5
        creature2.energy = 10
        creature3.energy = 2

        self.sim.grid[0][0].extend([tree, creature1, creature2, creature3])
        self.sim.distribute_food(Point2d(0, 0))

        self.assertTrue(creature2.food)
        self.assertTrue(creature1.food)
        self.assertTrue(creature3.food)
        self.assertEqual(tree.food, 0)
        
    def test_find_closest_mate(self):
        """Test finding closest mate"""
        creature1 = Creature(Point2d(0, 2))
        creature2 = Creature(Point2d(0, 1))
        self.sim.grid[0][2].append(creature1)
        self.sim.grid[0][1].append(creature2)
        closest_mate = self.sim.find_closest_mate(Point2d(0, 0))
        self.assertEqual(closest_mate, Point2d(0, 1))
        
    def test_mate_creatures(self):
        """Test mating"""
        creature1 = Creature(Point2d(0, 0))
        creature2 = Creature(Point2d(0, 0))
        self.sim.grid[0][0].append(creature1)
        self.sim.grid[0][0].append(creature2)
        self.sim.mate_creatures(creature1)
        self.assertEqual(self.sim.population, 11)
        self.assertTrue(creature1.has_mated)
        self.assertTrue(creature2.has_mated)
        
    def test_death(self):
        creature = Creature(Point2d(0, 0))
        self.sim.grid[0][0].append(creature)
        self.sim.death(creature)
        self.assertNotIn(creature, self.sim.grid[0][0])
        self.assertEqual(self.sim.population, self.start_population - 1)
        
    def test_reset(self):
        creature = Creature(Point2d(0, 0))
        tree = Tree(Point2d(2, 3))
        self.sim.grid[0][0].append(creature)
        self.sim.grid[2][3].append(tree)
        creature.food = True

        self.sim.turn()
        self.sim.reset()

        self.assertFalse(creature.food)
        tree_count = sum(len(cell) for row in self.sim.grid for cell in row if any(isinstance(obj, Tree) for obj in cell))
        self.assertEqual(tree_count, self.num_trees)
        self.assertEqual(self.sim.food_eaten, 0)
        self.assertEqual(self.sim.new_creatures, 0)

    @patch('builtins.open', new_callable=mock_open)
    def test_turn(self, mock_file):
        self.sim.populate_grid(self.start_population)
        self.sim.add_trees()
        self.sim.turn()
        self.assertEqual(self.sim.current_turn, 1)

    @patch('builtins.open', new_callable=mock_open)
    def test_start(self, mock_file):
        self.sim.start(self.turns)
        self.assertEqual(self.sim.current_turn, self.turns + 1) # plus 1 for end of loop
        mock_file.assert_called()
        
    @patch('builtins.open', new_callable=mock_open)
    def test_save_turn_data(self, mock_file):
        self.sim.save_turn_data()
        mock_file.assert_called_once_with(self.file, 'a')
        mock_file().write.assert_called_once_with(f'\n{self.sim.population}, {self.sim.food_eaten}, {self.sim.new_creatures}')
        
    @patch('builtins.open', new_callable=mock_open, read_data="Population\n10\n9\n8\n7\n6")
    @patch('matplotlib.pyplot.show')
    def test_show_data(self, mock_show, mock_file): 
        self.sim.show_data('Population over Turns', 0)

        # Get the current axes after showing the plot
        actual_fig, actual_ax = plt.gcf(), plt.gca()

        # Check the title
        self.assertEqual(actual_ax.get_title(), "Population over Turns")

        # Check x and y labels
        self.assertEqual(actual_ax.get_xlabel(), "Turns")
        self.assertEqual(actual_ax.get_ylabel(), "Population")

        # Check gridlines
        self.assertTrue(actual_ax.get_xgridlines())
        self.assertTrue(actual_ax.get_ygridlines())

        # Check the line properties
        lines = actual_ax.get_lines()
        self.assertEqual(len(lines), 1)  # Ensure there is one line

        # Check actual data line properties
        actual_line = lines[0]
        self.assertEqual(actual_line.get_linestyle(), '-')  # Line style
        self.assertEqual(actual_line.get_color(), 'darkgreen')  # Line color

        mock_file.assert_called_with('data/simulation.csv')
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.imshow')
    def test_plot_grid(self, mock_imshow, mock_show): #TODO: fix
        # Set up the grid with some creatures
        # Set up the grid with some creatures and trees
        self.sim.grid[0][0] = [Creature(Point2d(0, 0)), Tree(Point2d(0, 0))]
        self.sim.grid[2][3] = [Creature(Point2d(2, 3)), Creature(Point2d(2, 3))]

        # Call the plot_grid method
        self.sim.plot_grid()

        # Check if imshow was called once
        mock_imshow.assert_called_once()

        # Extract the grid_data passed to imshow
        args, kwargs = mock_imshow.call_args
        grid_data = args[0]

        # Expected grid data with creatures at (0, 0) and (2, 3) and trees at (0, 0)
        expected_grid_data = np.zeros((self.grid_size, self.grid_size))
        expected_grid_data[0][0] = 1.5  # 1 for Creature, 0.5 for Tree
        expected_grid_data[2][3] = 2  # Two Creatures

        # Assert the grid data is as expected
        np.testing.assert_array_equal(grid_data, expected_grid_data)

        # Check if imshow was called with the correct colormap
        self.assertEqual(kwargs['cmap'], 'Greens')

        # Check if show was called once
        mock_show.assert_called_once()

        # Get the current axes after showing the plot
        actual_fig, actual_ax = plt.gcf(), plt.gca()
        
        # Check the title
        self.assertEqual(actual_ax.get_title(), 'Creature and Tree Grid')
        
        # Check x and y labels
        self.assertEqual(actual_ax.get_xlabel(), 'x')
        self.assertEqual(actual_ax.get_ylabel(), 'y')
            
if __name__ == '__main__':
    unittest.main()