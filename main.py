import matplotlib.pyplot as plt
import numpy as np

FILE_HEADER = "Population"

class Simulation:
    """Simulation instance"""
    current_turn = 0    
    def __init__(self, start_population, filename):
        """Run the simulation"""
        self.population = start_population
        self.filename = filename
    
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Simulation({self.population}, {self.filename})"
    
    def __str__(self):
        """A human-friendly string represention"""
        return f"({self.population}, {self.filename}, {self.current_turn})"
    
    def start(self, turns):
        """Start simulation"""
        # TODO: Thread
        with open(self.filename, 'w') as outfile:
            outfile.write(FILE_HEADER)
        
        # Save turn 0 data
        self.save_turn_data()
           
        # Run for number of turns 
        self.current_turn = 1
        while self.current_turn <= turns:
            self.trun()
            self.current_turn += 1
    
    # TODO: add pause, continue, and end
    
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
         
    def show_data(self, title, data_index):
        """Show graph of data"""
        infile = open(self.filename)
        lines = infile.read().splitlines()
        infile.close()
        
        axes = plt.axes()
        axes.grid(True)
        
        xs = np.arange(0, len(lines[1:]), 1)
        ys = [int(data.split(',')[data_index]) for data in lines[1:]]
        
        axes.plot(xs, ys, linestyle='-',color='darkgreen')
        
        axes.set_title(title)
        axes.set_xlabel("Turns")
        axes.set_ylabel(lines[0].split(',')[data_index])
        
        # TODO: Add x labels
        # TODO: Add y labels that run from ceil round max y value to 0
        
        plt.tight_layout()
        plt.show()
        
sim = Simulation(10, 'data/simulation.csv')
sim.start(5)
sim.show_data("Population over Turns", 0)