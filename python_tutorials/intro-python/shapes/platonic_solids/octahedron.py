from .platonicsolid
from ..regular_shapes import Triangle

def Octahedron(PlatonicSolid):
    
    def __init__(self):
        
        self.num_edges = 12
        self.num_faces = 8
        self.face_shape = 'triangle'
        
    def get_face_shape(self):
        
        return Triangle()