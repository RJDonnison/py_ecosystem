import matplotlib.pyplot as plt
import numpy as np
import random

from classes.creature import Creature
from classes.point2d import Point2d
from classes.tree import Tree

FILE_HEADER = "Population, Food eaten, New creatures"

class Simulation:
    """Simulation instance"""
    current_turn = 0    
    food_eaten = 0
    new_creatures = 0
    default_energy = 10
    def __init__(self, start_population: int, num_trees:int, grid_size: int, filename: str):
        """Run the simulation"""
        self.population = start_population
        self.num_trees = num_trees
        self.grid_size = grid_size
        self.grid = self.create_grid(grid_size)
        self.filename = filename
    
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Simulation({self.population}, {self.num_trees}, {self.grid_size}, {self.filename})"
    
    def __str__(self) -> str:
        """A human-friendly string represention"""
        return f"({self.population}, {self.num_trees}, {self.grid_size}, {self.filename}, {self.current_turn})"
    
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
            self.turn()
    
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

    def turn(self):
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
                        self.distribute_food(creature.pos)
                        
                        if not creature.food:
                            self.death(creature)
                            continue

                        # Move creature to closest mate
                        closest_mate_pos = self.find_closest_mate(creature.pos)
                        if closest_mate_pos and not creature.has_mated:
                            self.move(creature, closest_mate_pos)
                            self.mate_creatures(creature)
        
        self.current_turn += 1
        self.save_turn_data()
        self.reset()
        
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
    
    def distribute_food(self, pos: Point2d):
        """Distributes the food in a cell"""
        cell = self.grid[pos.x][pos.y]
        highest_energy_creatures = []
        tree = None

        for obj in cell:
            if isinstance(obj, Tree):
                tree = obj
                
        # Collect creatures in the cell
        for obj in cell:
            if isinstance(obj, Creature):
                highest_energy_creatures.append(obj)
                
        # Sort creatures by energy in descending order
        highest_energy_creatures.sort(key=lambda c: c.energy, reverse=True)
        
        # Feed the highest energy creatures
        for creature_to_feed in highest_energy_creatures:
            if tree and tree.food > 0:
                tree.food -= 1
                creature_to_feed.food = True
                self.food_eaten += 1
            else:
                break
    
    def find_closest_mate(self, pos: Point2d):
        """Find the closest posible mate to the given position"""
        min_distance = float('inf')
        closest_mate_pos = None
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                for obj in self.grid[i][j]:
                    if isinstance(obj, Creature) and not obj.has_mated:
                        mate_pos = obj.pos
                        distance = pos.distance_to(mate_pos)
                        if distance < min_distance:
                            min_distance = distance
                            closest_mate_pos = mate_pos
    
        return closest_mate_pos
    
    def mate_creatures(self, creature:Creature):
        """Mate creatures"""
        cell = self.grid[creature.pos.x][creature.pos.y]
        for obj in cell:
            if isinstance(obj, Creature) and not obj.has_mated and obj != creature:
                obj.has_mated = True
                creature.has_mated = True
                self.new_creatures += 1
                
                cell.append(Creature(creature.pos))
                self.population += 1
                break

    def death(self, creature:Creature):
        """Remove instance of given Creature"""   
        self.grid[creature.pos.x][creature.pos.y].remove(creature)
        self.population -= 1
        
    def reset(self):
        """Reset trees and creature states"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.grid[i][j]
                for obj in cell:
                    if isinstance(obj, Creature):
                        obj.energy = self.default_energy
                        obj.food = False  # Reset creature's food state
                    if isinstance(obj, Tree):
                        self.grid[i][j].remove(obj) # Remove all trees
        
        self.new_creatures = 0
        self.food_eaten = 0
        self.add_trees()    
        
    def save_turn_data(self):
        """Save turn data to file"""                                     
        with open(self.filename, 'a') as outfile:
            outfile.write(f'\n{self.population}, {self.food_eaten}, {self.new_creatures}')
         
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
                for obj in cell:
                    if isinstance(obj, Creature):
                        grid_data[i][j] += 1
                    if isinstance(obj, Tree):
                        grid_data[i][j] += 0.5
        
        plt.imshow(grid_data, cmap='Greens')
        
        plt.title("Creature and Tree Grid")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        
sim = Simulation(50, 40, 10, 'data/simulation.csv')
sim.start(100)
sim.show_data("Population over time", 0)