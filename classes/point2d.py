import math

class Point2d:
    """A point in 2-space"""
    def __init__(self, x, y):
        """Initialises a new Point object"""
        self.x = x
        self.y = y

    def __repr__(self):
        """A string representation of the self object"""
        return f"Point2d({self.x}, {self.y})"

    def __str__(self):
        """A human-friendly string represention"""
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        """Allow the use of '+' on points"""
        if not isinstance(other, Point2d):
            raise TypeError
        return Point2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Allow the use of '-' on points"""
        if not isinstance(other, Point2d):
            raise TypeError
        return Point2d(self.x - other.x, self.y - other.y)
    
    def distance_to(self, pos):
        """Calculate Euclidean distance between two positions."""
        if not isinstance(pos, Point2d):
            raise TypeError
        return math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2)
    
    def midpoint(self, pos):
        """Calculate the midpoint between two positions."""
        if not isinstance(pos, Point2d):
            raise TypeError
        mid_x = (self.x + pos.x) / 2
        mid_y = (self.y + pos.y) / 2
        return Point2d(mid_x, mid_y)