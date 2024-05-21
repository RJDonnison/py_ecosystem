import matplotlib.pyplot as plt
import numpy as np
import random

from classes.creature import Creature
from classes.point2d import Point2d

FILE_HEADER = "Population"

class Simulation:
    """Simulation instance"""
    current_turn = 0    
    def __init__(self, start_population: int, grid_size: int, filename: str):
        """Run the simulation"""
        self.population = start_population
        self.grid_size = grid_size
        self.grid = self.create_grid(grid_size)
        self.filename = filename
    
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Simulation({self.population}, {self.filename})"
    
    def __str__(self) -> str:
        """A human-friendly string represention"""
        return f"({self.population}, {self.filename}, {self.current_turn})"
    
    def start(self, turns: int):
        """Start simulation"""
        # TODO: Thread
        with open(self.filename, 'w') as outfile:
            outfile.write(FILE_HEADER)
        
        self.populate_grid(self.population)
        # Save turn 0 data
        self.save_turn_data()
           
        # Run for number of turns 
        self.current_turn = 1
        while self.current_turn <= turns:
            self.trun()
            self.current_turn += 1
    
    # TODO: add pause, continue, and end
    
    def create_grid(self, size: int):
        """Create grid of size"""
        return [[None for _ in range(size)] for _ in range(size)]        

    def populate_grid(self, count: int):
        """Populate grid with random positons"""
        placed_creatures = 0
        while placed_creatures < count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid[x][y] is None:
                self.grid[x][y] = Creature(Point2d(x,y))
                placed_creatures += 1

    def move(self, creature: Creature, new_pos: Point2d):
        """Move object to pos"""
        old_pos = creature.pos
        creature.move(new_pos)
        self.grid[old_pos.x][old_pos.y] = None
        self.grid[new_pos.y][new_pos.x] = creature

    def trun(self):
        """One turn of simulation"""
        self.population -= 1
        # TODO: make creatures get food
        # TODO: check creatures death
        # TODO: check mates
        # TODO: mate creatures 
          
        self.save_turn_data()
        
    def save_turn_data(self):
        """Save turn data to file"""
        with open(self.filename, 'a') as outfile:
            outfile.write(f'\n{self.population}')
         
    def show_data(self, title: str, data_index: int):
        """Show graph of data"""
        infile = open(self.filename)
        lines = infile.read().splitlines()
        infile.close()
        
        axes = plt.axes()
        axes.grid(True)
        
        xs = np.arange(0, len(lines[1:]), 1)
        ys = [int(data.split(',')[data_index]) for data in lines[1:]]
        
        
        axes.plot(xs, ys, linestyle='-', color='darkgreen')
        
        axes.set_title(title)
        axes.set_xlabel("Turns")
        axes.set_ylabel(lines[0].split(',')[data_index])
        
        # TODO: Add x labels
        # TODO: Add y labels that run from ceil round max y value to 0
        
        plt.tight_layout()
        plt.show()
    
    def plot_grid(self):
        """Visualize the grid of creatures"""
        grid_data = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] is not None:
                    grid_data[i][j] = 1
                    
        plt.imshow( grid_data , cmap = 'Greens' )
        
        plt.title("Creature Grid")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
sim = Simulation(10, 5, 'data/simulation.csv')
sim.start(5)
sim.show_data('Population over time', 0)
