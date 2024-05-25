from classes.point2d import Point2d

class Tree:
    """Tree that holds food"""
    def __init__(self, pos:Point2d, food:int = 3) -> None:
        self.pos = pos
        self.food = food
        
    def __repr__(self) -> str:
        """A string representation of the self object"""
        return f"Tree({self.pos.x}, {self.pos.y}, {self.food})"