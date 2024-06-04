# simulator/cell.py

import random
from .celestial_bodies import Nebula, Star, Planet, Moon, Asteroid, Comet, BlackHole, Galaxy

class Cell:
    def __init__(self, x, y, density=0.0, temperature=0.0, seed=None):
        self.x = x
        self.y = y
        self.density = density
        self.temperature = temperature
        self.seed = seed
        self.celestial_bodies = []

        if seed is not None:
            random.seed(seed)
            self.generate_celestial_bodies()

    def generate_celestial_bodies(self):
        # Probabilities based on temperature and density
        if self.temperature > 5000 and self.density > 5:
            if random.random() < 0.1:
                self.celestial_bodies.append(Star(self.x, self.y, mass=random.uniform(0.5, 50), temperature=self.temperature))
        if self.temperature < 3000 and self.density > 2:
            if random.random() < 0.05:
                self.celestial_bodies.append(Nebula(self.x, self.y, size=random.uniform(5, 15), density=self.density))
        # Add more conditions for other celestial bodies
