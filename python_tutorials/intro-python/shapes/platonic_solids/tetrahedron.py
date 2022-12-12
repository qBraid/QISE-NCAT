from .platonicsolid
from ..regular_shapes.triangle import Triangle

def Tetrahedron(PlatonicSolid):
    
    def __init__(self):
        
        self.num_edges = 4
        self.num_faces = 4
        self.face_shape = 'triangle'
        
    def get_face_shape(self):
        
        return Triangle()