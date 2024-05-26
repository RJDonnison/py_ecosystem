from classes.point2d import Point2d

class Creature:
    """Creature"""
    def __init__(self, pos: Point2d, energy:float=10):
        self.pos = pos # Grid position
        self.energy = energy  # Energy level or any other attribute
        self.food = False
        self.has_mated = False
    
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Creature({self.pos.x}, {self.pos.y}, {self.energy})"
    
    def move(self, new_pos: Point2d):
        """Move creature to new pos"""
        distance = self.pos.distance_to(new_pos)
        if distance > self.energy:
            return False
        
        self.energy -= distance
        self.pos = new_pos
        return True