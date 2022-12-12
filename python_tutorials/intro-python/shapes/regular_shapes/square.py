from .ngon import NGon

class Square(NGon):
    
    def __init__(self):
        
        super().__init__(4)
        self.name = 'Square'