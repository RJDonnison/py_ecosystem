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

class Test_Simulation(unittest.TestCase):
    """Test simulation"""
    def setUp(self):
        self.file = 'data/simulation.csv'
        self.start_population = 10
        self.turns = 7
        self.sim = Simulation(self.start_population, self.file)
        
    def test_initialization(self):
        self.assertEqual(self.sim.population, self.start_population)
        self.assertEqual(self.sim.filename, self.file)
        self.assertEqual(self.sim.current_turn, 0)

    def test_repr(self):
        self.assertEqual(repr(self.sim), f"Simulation({self.start_population}, {self.file})")

    def test_str(self):
        self.assertEqual(str(self.sim), f"({self.start_population}, {self.file}, 0)")

    @patch('builtins.open', new_callable=mock_open)
    def test_save_turn_data(self, mock_file):
        self.sim.save_turn_data()
        mock_file.assert_called_once_with(self.file, 'a')
        mock_file().write.assert_called_once_with(f'\n{self.start_population}')

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
        
    @patch('builtins.open', new_callable=mock_open, read_data="Population\n10\n9\n8\n7\n6")
    @patch('matplotlib.pyplot.show')
    def test_show_data(self, mock_show, mock_file):
        self.sim.show_data("Population over Turns", 0)
        
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
        
        # Check x and y values for actual data
        expected_xs = np.arange(0, self.turns - 2, 1)
        expected_ys = [self.start_population - i for i in range(self.turns - 2)]
        self.assertTrue(np.array_equal(actual_line.get_xdata(), expected_xs))
        self.assertTrue(np.array_equal(actual_line.get_ydata(), expected_ys))
        
        mock_file.assert_called_with('data/simulation.csv')
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()