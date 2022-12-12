from .ngon import NGon

class Octagon(NGon):
    
    def __init__(self):
        
        super().__init__(8)
        self.name = 'Octagon'