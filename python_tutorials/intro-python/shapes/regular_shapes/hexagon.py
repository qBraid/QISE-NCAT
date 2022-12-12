from .ngon import NGon

class Hexagon(NGon):
    
    def __init__(self):
        
        super().__init__(6)
        self.name = 'Hexagon'