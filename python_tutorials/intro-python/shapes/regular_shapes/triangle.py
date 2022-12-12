from .ngon import NGon

class Triangle(NGon):
    
    def __init__(self):
        
        super().__init__(3)
        self.name = 'Triangle'