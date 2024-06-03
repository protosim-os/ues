import random
import time
from .cell import Cell

class UniverseSimulator:
    def __init__(self, seed=None):
        self.grid, self.seed = self.initialize_universe(seed)
        self.running = False
        self.time_step = 0
        self.expansion_rate = self.calculate_initial_expansion_rate()
        self.speed = 2  # Default speed set lower for better observation
        self.speed_map = {1: 1.0, 2: 0.5, 3: 0.1, 4: 0.05, 5: 0.01, 6: 0.005}
        self.big_bang_delay = 50  # Delay before the Big Bang starts
        self.big_bang_occurred = False
    
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
        return 10  # Initial expansion rate, adjust as needed

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
        # Implement realistic expansion rate adjustment
        if self.time_step < 100:  # Rapid initial expansion
            return self.expansion_rate * 0.98  # Slowing down
        elif self.time_step < 200:  # Gradual slow down
            return self.expansion_rate * 0.99
        elif self.time_step < 300:  # Halting expansion
            return max(self.expansion_rate * 0.999, 0.1)
        else:  # Begin contraction
            return self.expansion_rate * 1.01
    
    def expand_universe(self, grid, expansion_rate):
        new_grid = {}
        min_x = min(cell.x for cell in grid.values())
        max_x = max(cell.x for cell in grid.values())
        min_y = min(cell.y for cell in grid.values())
        max_y = max(cell.y for cell in grid.values())

        int_expansion_rate = int(expansion_rate)  # Convert expansion rate to an integer

        for x in range(min_x - int_expansion_rate, max_x + int_expansion_rate + 1):
            for y in range(min_y - int_expansion_rate, max_y + int_expansion_rate + 1):
                if (x, y) in grid:
                    cell = grid[(x, y)]
                    new_grid[(x, y)] = Cell(x, y, cell.density, cell.temperature)
                else:
                    neighbors = self.get_neighbors(grid, x, y)
                    new_grid[(x, y)] = self.generate_tile_from_neighbors(neighbors, x, y)

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
            time.sleep(self.speed_map[self.speed])  # Adjust time step duration based on speed
    
    def pause(self):
        self.running = False

    def play(self):
        self.running = True
    
    def set_speed(self, speed):
        if speed in self.speed_map:
            self.speed = speed
