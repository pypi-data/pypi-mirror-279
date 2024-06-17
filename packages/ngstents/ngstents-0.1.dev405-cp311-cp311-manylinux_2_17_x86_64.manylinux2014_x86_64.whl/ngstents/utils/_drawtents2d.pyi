from __future__ import annotations
from netgen.libngpy._meshing import Element2D
from netgen.libngpy._meshing import Element3D
from netgen.libngpy._meshing import FaceDescriptor
from netgen.libngpy._meshing import Mesh
from netgen.libngpy._meshing import MeshPoint
from netgen.libngpy._meshing import Pnt
import ngsolve as ng
import numpy as np
__all__ = ['DrawPitchedTents', 'Element2D', 'Element3D', 'FaceDescriptor', 'Mesh', 'MeshPoint', 'Pnt', 'ng', 'np']
def DrawPitchedTents(self, uptolevel = None):
    """
    
        Make a 2+1 dimensional mesh of spacetime tents, drawable using netgen.
        If uptolevel=L, then only tents of level L and lower are plotted,
        and if uptolevel is not given, all tents are included in the mesh.
    
        RETURNS:
          mesh3d: the spacetime mesh
          vertexlevels: tentlevels assigned to apex vertices (H1 function)
          tetlevels: tentlevels assigned to spacetime tetrahedra (DG function)
        
    """
