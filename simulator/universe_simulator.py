import random
import time
from .cell import Cell
from .quadtree import QuadTree, Rect
import math

class UniverseSimulator:
    def __init__(self, seed=None, max_grid_size=250):
        self.grid, self.seed = self.initialize_universe(seed)
        self.running = False
        self.time_step = 0
        self.speed = 2  # Default speed set lower for better observation
        self.speed_map = {1: 1.0, 2: 0.5, 3: 0.1, 4: 0.05, 5: 0.01, 6: 0.005}
        self.big_bang_delay = 50  # Delay before the Big Bang starts
        self.big_bang_occurred = False
        self.quad_tree = QuadTree(Rect(0, 0, 800, 800), 4)  # Initialize QuadTree
        self.max_grid_size = max_grid_size

        # Parameters for expansion and contraction phases
        self.initial_expansion_rate = 1  # Initial expansion rate
        self.expansion_rate = self.calculate_initial_expansion_rate()
        self.slowdown_factor = 0.99999  # Slowdown factor for gradual slowdown
        self.contraction_factor = 1.0001  # Factor for contraction
        self.stillness_duration = 5000  # Duration of virtual stillness

        # Total duration parameters for different phases
        self.big_bang_duration = 60
        self.phase_25_duration = 1000
        self.phase_50_duration = 5000
        self.phase_75_duration = 15000
        self.phase_100_duration = 30000
        self.phase_collapse_75_duration = 55000

    def initialize_universe(self, seed):
        seed = self.initialize_seed(seed)
        initial_tile = self.create_initial_tile()
        grid = {(initial_tile.x, initial_tile.y): initial_tile}
        return grid, seed

    def initialize_seed(self, seed=None):
        if seed is None:
            seed = random.randint(0, 1000000)
        random.seed(seed)
        return seed
    
    def create_initial_tile(self):
        return Cell(x=0, y=0, density=10.0, temperature=10000.0)
    
    def calculate_initial_expansion_rate(self):
        return self.initial_expansion_rate

    def update_universe(self):
        if self.running:
            if not self.big_bang_occurred:
                if self.time_step >= self.big_bang_delay:
                    self.big_bang_occurred = True
                else:
                    self.time_step += 1
                    return
            
            self.time_step += 1
            self.grid = self.expand_universe(self.grid, self.expansion_rate)
            self.expansion_rate = self.calculate_expansion_rate()
    
    def calculate_expansion_rate(self):
        # Calculate the current size of the universe
        total_cells = len(self.grid)
        universe_size = int(math.sqrt(total_cells))

        # Determine the phase of the expansion
        if self.time_step < self.big_bang_duration:  # Big bang phase
            return self.initial_expansion_rate
        elif self.time_step < self.big_bang_duration + self.phase_25_duration:  # 0-25% expansion
            progress = (self.time_step - self.big_bang_duration) / self.phase_25_duration
            return self.initial_expansion_rate * (1 - progress * 0.75)
        elif self.time_step < self.big_bang_duration + self.phase_25_duration + self.phase_50_duration:  # 25-50% expansion
            progress = (self.time_step - self.big_bang_duration - self.phase_25_duration) / self.phase_50_duration
            return self.initial_expansion_rate * 0.25 * (1 - progress * 0.5)
        elif self.time_step < self.big_bang_duration + self.phase_25_duration + self.phase_50_duration + self.phase_75_duration:  # 50-75% expansion
            progress = (self.time_step - self.big_bang_duration - self.phase_25_duration - self.phase_50_duration) / self.phase_75_duration
            return self.initial_expansion_rate * 0.125 * (1 - progress * 0.25)
        elif self.time_step < self.big_bang_duration + self.phase_25_duration + self.phase_50_duration + self.phase_75_duration + self.phase_100_duration:  # 75-100% expansion
            progress = (self.time_step - self.big_bang_duration - self.phase_25_duration - self.phase_50_duration - self.phase_75_duration) / self.phase_100_duration
            return self.initial_expansion_rate * 0.0625 * (1 - progress * 0.25)
        elif self.time_step < self.big_bang_duration + self.phase_25_duration + self.phase_50_duration + self.phase_75_duration + self.phase_100_duration + self.phase_collapse_75_duration:  # Collapse to 75%
            progress = (self.time_step - self.big_bang_duration - self.phase_25_duration - self.phase_50_duration - self.phase_75_duration - self.phase_100_duration) / self.phase_collapse_75_duration
            return self.initial_expansion_rate * 0.03125 * (1 - progress * 0.25)
        else:  # Post-collapse
            return 0.1  # Very slow expansion rate
    
    def expand_universe(self, grid, expansion_rate):
        new_grid = {}
        min_x = min(cell.x for cell in grid.values())
        max_x = max(cell.x for cell in grid.values())
        min_y = min(cell.y for cell in grid.values())
        max_y = max(cell.y for cell in grid.values())

        if max_x - min_x >= self.max_grid_size or max_y - min_y >= self.max_grid_size:
            return grid  # Don't expand if the grid size limit is reached

        int_expansion_rate = max(int(expansion_rate), 1)  # Convert expansion rate to an integer

        for x in range(min_x - int_expansion_rate, max_x + int_expansion_rate + 1):
            for y in range(min_y - int_expansion_rate, max_y + int_expansion_rate + 1):
                if (x, y) in grid:
                    cell = grid[(x, y)]
                    new_grid[(x, y)] = Cell(x, y, cell.density, cell.temperature)
                    self.quad_tree.insert((x, y))  # Insert into quadtree
                else:
                    neighbors = self.get_neighbors(grid, x, y)
                    new_grid[(x, y)] = self.generate_tile_from_neighbors(neighbors, x, y)
                    self.quad_tree.insert((x, y))  # Insert into quadtree

        for (x, y), cell in new_grid.items():
            if cell.density > 0:
                self.distribute_density(new_grid, x, y)
                
        return new_grid

    def get_neighbors(self, grid, x, y):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Adjacent cells
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid:
                neighbors.append(grid[(nx, ny)])
        return neighbors

    def generate_tile_from_neighbors(self, neighbors, x, y):
        if neighbors:
            density = sum(neighbor.density for neighbor in neighbors) / len(neighbors)
            temperature = sum(neighbor.temperature for neighbor in neighbors) / len(neighbors)
            density += random.uniform(-density * 0.1, density * 0.1)  # Small variation
            temperature += random.uniform(-temperature * 0.1, temperature * 0.1)  # Small variation
        else:
            density = random.uniform(0.1, 1.0)
            temperature = random.uniform(0.1, 1.0)
        return Cell(x=x, y=y, density=density, temperature=temperature)
    
    def distribute_density(self, grid, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        total_density = grid[(x, y)].density
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid:
                transfer_amount = total_density * 0.1  # Transfer 10% of density to each neighbor
                grid[(nx, ny)].density += transfer_amount
                grid[(x, y)].density -= transfer_amount

    def run(self):
        self.running = True
        while self.running:
            self.update_universe()
            time.sleep(self.speed_map[self.speed] * 2)  # Adjust time step duration to slow down simulation
    
    def pause(self):
        self.running = False

    def play(self):
        self.running = True
    
    def set_speed(self, speed):
        if speed in self.speed_map:
            self.speed = speed
