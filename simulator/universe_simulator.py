import random
import math
import time
from .cell import Cell
from .quadtree import QuadTree, Rect

class UniverseSimulator:
    def __init__(self, seed=None, max_grid_size=250):
        self.seed = seed
        self.grid, self.seed = self.initialize_universe(seed)
        self.running = False
        self.time_step = 0
        self.speed = 1  # Default speed set for better observation
        self.speed_map = {
            1: 5.0,     # 5x slower than current speed 2
            2: 2.5,     # 2.5x slower than current speed 2
            3: 1.0,     # Same as current speed 2
            4: 0.5,     # Slightly faster than current speed 2
            5: 0.25,    # Faster
            6: 0.1      # Fastest, as the current speed 2
        }
        self.big_bang_delay = 50  # Delay before the Big Bang starts
        self.big_bang_occurred = False
        self.quad_tree = QuadTree(Rect(0, 0, 800, 800), 4)  # Initialize QuadTree
        self.max_grid_size = max_grid_size
        self.current_cell = None  # For cell view

        self.expansion_duration = 15000
        self.collapse_duration = 15000

    def initialize_universe(self, seed):
        seed = self.initialize_seed(seed)
        initial_tile = self.create_initial_tile(seed)
        grid = {(initial_tile.x, initial_tile.y): initial_tile}
        return grid, seed

    def initialize_seed(self, seed=None):
        if seed is None:
            seed = random.randint(0, 1000000)
        random.seed(seed)
        return seed
    
    def create_initial_tile(self, seed):
        return Cell(x=0, y=0, density=10.0, temperature=10000.0, seed=seed)
    
    def update_universe(self):
        if self.running:
            if not self.big_bang_occurred:
                if self.time_step >= self.big_bang_delay:
                    self.big_bang_occurred = True
                else:
                    self.time_step += 1
                    return
            
            self.time_step += int(self.speed_map[self.speed])  # Increment time_step based on the speed
            self.grid = self.expand_universe(self.grid)
    
    def expand_universe(self, grid):
        new_grid = {}
        min_x = min(cell.x for cell in grid.values())
        max_x = max(cell.x for cell in grid.values())
        min_y = min(cell.y for cell in grid.values())
        max_y = max(cell.y for cell in grid.values())

        if max_x - min_x >= self.max_grid_size or max_y - min_y >= self.max_grid_size:
            return grid  # Don't expand if the grid size limit is reached

        # Calculate expansion/contraction rate based on time_step
        if self.time_step <= self.expansion_duration:
            expansion_phase = self.time_step / self.expansion_duration
            expansion_rate = max(1, int((self.max_grid_size / 2) * expansion_phase))
        else:
            contraction_phase = (self.time_step - self.expansion_duration) / self.collapse_duration
            expansion_rate = max(1, int((self.max_grid_size / 2) * (1 - contraction_phase)))

        for x in range(min_x - expansion_rate, max_x + expansion_rate + 1):
            for y in range(min_y - expansion_rate, max_y + expansion_rate + 1):
                if (x, y) in grid:
                    cell = grid[(x, y)]
                    new_grid[(x, y)] = Cell(x, y, cell.density, cell.temperature, seed=self.seed)
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
        return Cell(x=x, y=y, density=density, temperature=temperature, seed=self.seed)
    
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
            time.sleep(self.speed_map[self.speed] * 0.05)  # Adjust time step duration to slow down simulation
    
    def pause(self):
        self.running = False

    def play(self):
        self.running = True
    
    def set_speed(self, speed):
        if speed in self.speed_map:
            self.speed = speed

    def open_cell_view(self, cell):
        self.current_cell = cell

    def close_cell_view(self):
        self.current_cell = None
