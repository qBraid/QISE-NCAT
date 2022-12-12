from .platonicsolid
from ..regular_shapes.pentagon import Pentagon

def Dodecahedron(PlatonicSolid):
    
    def __init__(self):
        
        self.num_edges = 30
        self.num_faces = 12
        self.face_shape = 'pentagon'
        
    def get_face_shape(self):
        
        return Pentagon()