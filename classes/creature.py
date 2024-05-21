from classes.point2d import Point2d

class Creature:
    """Creature"""
    def __init__(self, pos: Point2d, energy=10):
        self.pos = pos # Grid position
        self.energy = energy  # Energy level or any other attribute
    
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Creature({self.pos.x}, {self.pos.y}, {self.energy})"
    
    def move(self, pos: Point2d):
        """Move creature to new pos"""
        self.pos = pos
        # return if posible
