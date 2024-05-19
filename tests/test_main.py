# Add the parent directory (app) to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import mock_open, patch

from main import Simulation

class Test_Simulation(unittest.TestCase):
    """Test simulation"""
    def setUp(self):
        self.file = 'data/simulation.csv'
        self.start_population = 10
        self.turns = 5
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
        self.assertEqual(self.sim.population, self.start_population - self.turns + 1)
        self.assertEqual(self.sim.current_turn, self.turns)
        self.assertEqual(mock_file().write.call_count, self.turns + 1)