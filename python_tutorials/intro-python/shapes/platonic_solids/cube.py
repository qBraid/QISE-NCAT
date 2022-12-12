from .platonicsolid
from ..regular_shapes.square import Square

def Cube(PlatonicSolid):
    
    def __init__(self):
        
        self.num_edges = 12
        self.num_faces = 6
        self.face_shape = 'square'
        
    def get_face_shape(self):
        
        return Square()