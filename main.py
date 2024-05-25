import matplotlib.pyplot as plt
import numpy as np
import random

from classes.creature import Creature
from classes.point2d import Point2d
from classes.tree import Tree

FILE_HEADER = "Population"

class Simulation:
    """Simulation instance"""
    current_turn = 0    
    def __init__(self, start_population: int, num_trees:int, grid_size: int, filename: str):
        """Run the simulation"""
        self.population = start_population
        self.num_trees = num_trees
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
        self.add_trees()  # Add some trees with food
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
        return [[[] for _ in range(size)] for _ in range(size)]          

    def populate_grid(self, count: int):
        """Populate grid with random positons"""
        placed_creatures = 0
        while placed_creatures < count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            creature = Creature(Point2d(x, y))
            self.grid[x][y].append(creature)
            placed_creatures += 1

    def add_trees(self):
        """Add trees with food at random positions"""
        placed_trees = 0
        while placed_trees < self.num_trees:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            tree = Tree(Point2d(x, y))
            self.grid[x][y].append(tree)
            placed_trees += 1

    def move(self, creature: Creature, new_pos: Point2d):
        """Move object to pos"""
        old_pos = creature.pos
        if creature.move(new_pos):
            self.grid[old_pos.x][old_pos.y].remove(creature)
            self.grid[new_pos.x][new_pos.y].append(creature)

    def trun(self):
        """One turn of simulation"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.grid[i][j]
                for obj in cell:
                    if isinstance(obj, Creature):
                        creature = obj
                        # Move creature to closest food
                        closest_food_pos = self.find_closest_food(creature.pos)
                        if closest_food_pos:
                            self.move(creature, closest_food_pos)
                        
                        # Get food if there is a tree at the new position
                        # TODO: if num creatures at cell is more than tree food give food to higher energy cretures
                        new_pos_cell = self.grid[creature.pos.x][creature.pos.y]
                        for new_obj in new_pos_cell:
                            if isinstance(new_obj, Tree):
                                tree = new_obj
                                tree.food -= 1
                                creature.food = True
                        
                        if not creature.food:
                            self.death(creature)
                
        # TODO: check mates
        # TODO: mate creatures 
          
        self.save_turn_data()
        self.reset()
           
    def reset(self):
        """Reset trees and creature states"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.grid[i][j]
                for obj in cell:
                    if isinstance(obj, Creature):
                        obj.food = False  # Reset creature's food state
        self.add_trees()
        
    def find_closest_food(self, pos: Point2d):
        """Find the closest food source to the given position"""
        min_distance = float('inf')
        closest_food_pos = None
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                for obj in self.grid[i][j]:
                    if isinstance(obj, Tree) and obj.food > 0:
                        food_pos = obj.pos
                        distance = pos.distance_to(food_pos)
                        if distance < min_distance:
                            min_distance = distance
                            closest_food_pos = food_pos
    
        return closest_food_pos
    
    def death(self, creature:Creature):
        """Remove instance of given Creature"""   
        self.grid[creature.pos.x][creature.pos.y].remove(creature)
        self.population -= 1
        
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
                cell = self.grid[i][j]
                if any(isinstance(obj, Creature) for obj in cell):
                    grid_data[i][j] += 1
                if any(isinstance(obj, Tree) for obj in cell):
                    grid_data[i][j] += 0.5
        
        plt.imshow(grid_data, cmap='Greens')
        
        plt.title("Creature and Tree Grid")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
sim = Simulation(50, 30, 100, 'data/simulation.csv')
sim.start(50)
sim.show_data('Population over time', 0)
