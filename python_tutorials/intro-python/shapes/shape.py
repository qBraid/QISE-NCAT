"""Contains Shape class and other relevant functions."""

import random

class Shape:
    
    """Shape: base class for storing attributes/methods related to shapes
    
    Args:
        num_sides: sides of the shape
        name (optional): None
        kwargs: any
    """
    
    def __init__(self, num_sides, name=None, **kwargs):
        
        self.num_sides = num_sides

        self.name = name        
        self.__dict__.update(kwargs)
        
        print("You've created an instance of the shape class.")
        
        
def get_random_polygon():
    
    num_sides = random.randint(1,10)
    name = "random polygon with {} sides".format(num_sides)
    
    return Shape(num_sides, name = name)