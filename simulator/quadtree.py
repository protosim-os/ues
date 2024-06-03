class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        px, py = point
        return self.x <= px < self.x + self.w and self.y <= py < self.y + self.h

    def intersects(self, range):
        return not (range.x > self.x + self.w or 
                    range.x + range.w < self.x or 
                    range.y > self.y + self.h or 
                    range.y + range.h < self.y)

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rect object
        self.capacity = capacity  # Max points per quad
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h
        nw = Rect(x, y, w / 2, h / 2)
        ne = Rect(x + w / 2, y, w / 2, h / 2)
        sw = Rect(x, y + h / 2, w / 2, h / 2)
        se = Rect(x + w / 2, y + h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            
            if self.northwest.insert(point):
                return True
            elif self.northeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True

        return False

    def query(self, range, found):
        if not self.boundary.intersects(range):
            return
        
        for p in self.points:
            if range.contains(p):
                found.append(p)
        
        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)
