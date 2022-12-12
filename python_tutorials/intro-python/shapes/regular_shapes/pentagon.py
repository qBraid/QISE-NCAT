from .ngon import NGon

class Pentagon(NGon):
    
    def __init__(self):
        
        super().__init__(5)
        self.name = 'Pentagon'