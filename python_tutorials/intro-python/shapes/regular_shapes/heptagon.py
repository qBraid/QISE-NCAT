from .ngon import NGon

class Heptagon(NGon):
    
    def __init__(self):
        
        super().__init__(7)
        self.name = 'Heptagon'