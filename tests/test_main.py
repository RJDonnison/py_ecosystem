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

class Test_Simulation(unittest.TestCase):
    """Test simulation"""
    def setUp(self):
        self.file = 'data/simulation.csv'
        self.start_population = 10
        self.turns = 7
        self.grid_size = 5
        self.sim = Simulation(self.start_population, self.grid_size, self.file)
        
    def test_initialization(self):
        self.assertEqual(self.sim.population, self.start_population)
        self.assertEqual(self.sim.filename, self.file)
        self.assertEqual(self.sim.grid_size, self.grid_size)
        self.assertEqual(self.sim.current_turn, 0)
        self.assertEqual(len(self.sim.grid), self.grid_size)
        self.assertEqual(len(self.sim.grid[0]), self.grid_size)

    def test_repr(self):
        self.assertEqual(repr(self.sim), f"Simulation({self.start_population}, {self.file})")

    def test_str(self):
        self.assertEqual(str(self.sim), f"({self.start_population}, {self.file}, 0)")

    def test_create_grid(self):
        grid = self.sim.create_grid(self.grid_size)
        self.assertEqual(len(grid), self.grid_size)
        self.assertEqual(len(grid[0]), self.grid_size)
        self.assertTrue(all(cell is None for row in grid for cell in row))

    def test_populate_grid(self):
        self.sim.populate_grid(self.start_population)
        count = sum(1 for row in self.sim.grid for cell in row if isinstance(cell, Creature))
        self.assertEqual(count, self.start_population)
        
    def test_move_creature(self):
        creature = Creature(Point2d(0, 0))
        self.sim.grid[0][0] = creature
        new_pos = Point2d(1, 1)
        self.sim.move(creature, new_pos)
        self.assertIsNone(self.sim.grid[0][0])
        self.assertEqual(self.sim.grid[1][1], creature)
        self.assertEqual(creature.pos, new_pos)

    @patch('builtins.open', new_callable=mock_open)
    def test_trun(self, mock_file):
        self.sim.trun()
        self.assertEqual(self.sim.population, 9)
        mock_file.assert_called_once_with(self.file, 'a')
        mock_file().write.assert_called_once_with('\n9')

    @patch('builtins.open', new_callable=mock_open)
    def test_start(self, mock_file):
        self.sim.start(self.turns)
        self.assertEqual(self.sim.population, self.start_population - self.turns)
        self.assertEqual(self.sim.current_turn, self.turns + 1) # plus 1 for end of loop
        self.assertEqual(mock_file().write.call_count, self.turns + 2) # plus 2 for header and turn 0
        
    @patch('builtins.open', new_callable=mock_open)
    def test_save_turn_data(self, mock_file):
        self.sim.save_turn_data()
        mock_file.assert_called_once_with(self.file, 'a')
        mock_file().write.assert_called_once_with(f'\n{self.start_population}')
        
    @patch('builtins.open', new_callable=mock_open, read_data="Population\n10\n9\n8\n7\n6")
    @patch('matplotlib.pyplot.show')
    def test_show_data(self, mock_show, mock_file): # TODO: Check graph dispalys propperly
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
        self.sim.grid[0][0] = Creature(Point2d(0, 0))
        self.sim.grid[2][3] = Creature(Point2d(2, 3))

        # Call the plot_grid method
        self.sim.plot_grid()

        # Check if imshow was called once
        mock_imshow.assert_called_once()
        args, kwargs = mock_imshow.call_args

        # Extract the grid_data passed to imshow
        grid_data = args[0]

        # Expected grid data with creatures at (0, 0) and (2, 3)
        expected_grid_data = np.zeros((self.grid_size, self.grid_size))
        expected_grid_data[0][0] = 1
        expected_grid_data[2][3] = 1

        # Assert the grid data is as expected
        np.testing.assert_array_equal(grid_data, expected_grid_data)
        
        # Check if imshow was called with the correct colormap
        self.assertEqual(kwargs['cmap'], 'Greens')

        # Check if show was called once
        mock_show.assert_called_once()

        # Check if the plot has correct labels and title
        self.assertEqual(plt.gca().get_title(), "Creature Grid")
        self.assertEqual(plt.gca().get_xlabel(), 'x')
        self.assertEqual(plt.gca().get_ylabel(), 'y')
            
if __name__ == '__main__':
    unittest.main()