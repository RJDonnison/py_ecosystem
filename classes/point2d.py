class Point2d:
    """A point in 2-space"""
    def __init__(self, x, y):
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
            raise TypeError(f"Unsupported operand type(s) for +: 'Point2d' and '{type(other).__name__}'")
        return Point2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Allow the use of '-' on points"""
        if not isinstance(other, Point2d):
            raise TypeError(f"Unsupported operand type(s) for -: 'Point2d' and '{type(other).__name__}'")
        return Point2d(self.x - other.x, self.y - other.y)
    
    def distance(self, other):
        """Returns the distance between two points"""
        if not isinstance(other, Point2d):
            raise TypeError(f"Unsupported type(s):'{type(other).__name__}'")
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5
    
    def midpoint(self, other):
        """Returns the midpoint between two points"""
        if not isinstance(other, Point2d):
            raise TypeError(f"Unsupported type(s):'{type(other).__name__}'")
        x = (self.x + other.x) / 2
        y = (self.y + other.y) / 2
        return Point2d(x, y)