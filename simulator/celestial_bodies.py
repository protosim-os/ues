# simulator/celestial_bodies.py

class CelestialBody:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Nebula(CelestialBody):
    def __init__(self, x, y, size, density):
        super().__init__(x, y)
        self.size = size
        self.density = density

class Star(CelestialBody):
    def __init__(self, x, y, mass, temperature):
        super().__init__(x, y)
        self.mass = mass
        self.temperature = temperature

class Planet(CelestialBody):
    def __init__(self, x, y, star, distance, size, atmosphere):
        super().__init__(x, y)
        self.star = star
        self.distance = distance
        self.size = size
        self.atmosphere = atmosphere

class Moon(CelestialBody):
    def __init__(self, x, y, planet, distance, size):
        super().__init__(x, y)
        self.planet = planet
        self.distance = distance
        self.size = size

class Asteroid(CelestialBody):
    def __init__(self, x, y, size, composition):
        super().__init__(x, y)
        self.size = size
        self.composition = composition

class Comet(CelestialBody):
    def __init__(self, x, y, size, composition, orbit):
        super().__init__(x, y)
        self.size = size
        self.composition = composition
        self.orbit = orbit

class BlackHole(CelestialBody):
    def __init__(self, x, y, mass):
        super().__init__(x, y)
        self.mass = mass

class Galaxy(CelestialBody):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size
