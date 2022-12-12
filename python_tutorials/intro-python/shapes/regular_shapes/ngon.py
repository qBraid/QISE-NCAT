from ..shape import Shape

class NGon(Shape):
    
    def __init__(self, num_sides):
        
        name = str(num_sides) + 'gon'
        super().__init__(num_sides, name = name)
        
    def get_interior_angles(self):
        
        n = self.num_sides
        return 180*(n-2)/n
        
    def get_exterior_angles(self):
        
        n = self.num_sides
        return 360/n
        
