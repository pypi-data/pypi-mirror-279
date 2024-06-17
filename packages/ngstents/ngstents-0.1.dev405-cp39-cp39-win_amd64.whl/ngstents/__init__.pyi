from __future__ import annotations
import ngsolve as ngsolve
import pyngcore.pyngcore
import typing
from . import conslaw
from . import utils
__all__: list = ['TentSlab', 'Tent', 'conslaw', 'utils']
class Tent:
    """
    Tent structure
    """
    def MaxSlope(self) -> float:
        ...
    @property
    def els(self) -> pyngcore.pyngcore.Array_I_S:
        ...
    @property
    def internal_facets(self) -> pyngcore.pyngcore.Array_I_S:
        ...
    @property
    def level(self) -> int:
        ...
    @property
    def nbtime(self) -> pyngcore.pyngcore.Array_D_S:
        ...
    @property
    def nbv(self) -> pyngcore.pyngcore.Array_I_S:
        ...
    @property
    def tbot(self) -> float:
        ...
    @property
    def ttop(self) -> float:
        ...
    @property
    def vertex(self) -> int:
        ...
class TentSlab:
    """
    Tent pitched slab in D + 1 time dimensions
    """
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
    def DrawPitchedTentsPlt(self, showtentnums = False):
        """
        
            Draw 1D tents using Matplotlib
            
        """
    def DrawPitchedTentsVTK(self, vtkfilename: str = 'vtkoutput') -> None:
        """
                 Export the mesh of tents and intermediate advancing fronts
                 to VTK file format for visualization in Paraview.
        """
    def GetNLayers(self) -> int:
        ...
    def GetNTents(self) -> int:
        ...
    def GetSlabHeight(self) -> float:
        ...
    def GetTent(self, arg0: int) -> Tent:
        ...
    def MaxSlope(self) -> float:
        ...
    def PitchTents(self, dt: float, local_ct: bool = False, global_ct: float = 1.0) -> bool:
        """
                 Parameters:--
                   dt: spacetime slab's height in time.
                   local_ct: if True, constrain tent slope by scaling 1/wavespeed
                     with a further local mesh-dependent factor.
                   global_ct: an additional factor to constrain tent slope, which
                     gives flatter tents for smaller values.
        
                 Returns True upon successful tent meshing.
                 -------------
        """
    def SetMaxWavespeed(self, arg0: typing.Any) -> None:
        ...
    def TentData1D(self) -> list:
        ...
    def __init__(self, mesh: ngsolve.comp.Mesh, method: str = 'edge', heapsize: int = 1000000) -> None:
        ...
    @property
    def gradphi(self) -> ngsolve.fem.CoefficientFunction:
        ...
    @property
    def mesh(self) -> ngsolve.comp.Mesh:
        ...
_pytents = 
