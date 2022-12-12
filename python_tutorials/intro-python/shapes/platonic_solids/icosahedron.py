from .platonicsolid
from ..regular_shapes.Triangle import Triangle 

def Icosahedron(PlatonicSolid):
    
    def __init__(self):
        
        self.num_edges = 30
        self.num_faces = 20
        self.face_shape = 'triangle'
        
    def get_face_shape(self):
        
        return Triangle()