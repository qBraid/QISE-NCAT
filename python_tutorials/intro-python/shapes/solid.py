class Solid:
    
    """Solid class, to hold properties of solids. 
    
    Args:
        name (optional): name of the solid
        kwargs
    
    This class supports arbitrary keyword arguments. For example:
        my solid = Solid(color='blue', hardness =10, edge_width = '2px')
    """
    
    def __init__(self, name = None, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
        
        print("You've created an instance of the solid class.")