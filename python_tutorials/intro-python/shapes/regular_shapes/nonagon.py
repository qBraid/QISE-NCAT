from .ngon import NGon

class Nonagon(NGon):
    
    def __init__(self):
        
        super().__init__(9)
        self.name = 'Nonagon'