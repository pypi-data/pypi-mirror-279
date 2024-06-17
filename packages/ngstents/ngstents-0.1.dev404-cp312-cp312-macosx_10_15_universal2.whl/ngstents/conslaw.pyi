from __future__ import annotations
import ngsolve.comp
import ngsolve.fem
import ngstents
from ngstents import conslaw as _pyconslaw
import typing
__all__ = ['Advection', 'Burgers', 'ConservationLaw', 'Euler', 'Maxwell', 'Wave']
class Advection(ConservationLaw):
    def __init__(self, gfu, tentslab, **kwargs):
        """
        
                INPUTS:
        
                gridfunction : GridFunction
                tentslab     : TentSlab
                outflow      : Optional[Region]
                inflow       : Optional[Region]
                reflect      : Optional[Region]
                transparent  : Optional[Region]
                
        """
class Burgers(ConservationLaw):
    def __init__(self, gfu, tentslab, **kwargs):
        """
        
                INPUTS:
        
                gridfunction : GridFunction
                tentslab     : TentSlab
                outflow      : Optional[Region]
                inflow       : Optional[Region]
                reflect      : Optional[Region]
                
        """
class ConservationLaw:
    """
    Conservation Law
    """
    def Propagate(self, hdgf: ngsolve.comp.GridFunction = None) -> None:
        """
        GridFunction vector for visualization on 3D mesh
        """
    @typing.overload
    def SetBoundaryCF(self, arg0: ngsolve.comp.Region, arg1: ngsolve.fem.CoefficientFunction) -> None:
        ...
    @typing.overload
    def SetBoundaryCF(self, arg0: ngsolve.fem.CoefficientFunction) -> None:
        ...
    def SetIdx3d(self, idx3d: list) -> None:
        """
        Set index for visualization on a 3D mesh
        """
    def SetInitial(self, arg0: ngsolve.fem.CoefficientFunction) -> None:
        ...
    def SetMaterialParameters(self, mu: ngsolve.fem.CoefficientFunction, eps: ngsolve.fem.CoefficientFunction) -> None:
        ...
    def SetNumEntropyFlux(self, arg0: ngsolve.fem.CoefficientFunction) -> None:
        ...
    def SetTentSolver(self, method: str = 'SARK', stages: int = 2, substeps: int = 1) -> None:
        """
                 Parameters:--
                   method: SARK (Structure-Aware Runge Kutta), or 
                           SAT  (Structure-Aware Taylor).
                   stages: determines the order of time stepper.
                   substeps: number of subtents each tent should be divided into
                     before applying the tent solver method.
                   ----------- 
        """
    def SetVectorField(self, arg0: ngsolve.fem.CoefficientFunction) -> None:
        ...
    @typing.overload
    def __init__(self, gridfunction: ngsolve.comp.GridFunction, tentslab: ngstents.TentSlab, equation: str, outflow: ngsolve.comp.Region | None = None, inflow: ngsolve.comp.Region | None = None, reflect: ngsolve.comp.Region | None = None, transparent: ngsolve.comp.Region | None = None) -> None:
        ...
    @typing.overload
    def __init__(self, gridfunction: ngsolve.comp.GridFunction, tentslab: ngstents.TentSlab, flux: typing.Any, numflux: typing.Any, inversemap: typing.Any, compile: bool = False, entropy: typing.Any | None = None, entropyflux: typing.Any | None = None, numentropyflux: typing.Any | None = None, visccoeff: typing.Any | None = None) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def nu(self) -> ngsolve.comp.GridFunction:
        """
        entropy viscosity for nonlinear hyperbolic eq
        """
    @property
    def res(self) -> ngsolve.comp.GridFunction:
        """
        entropy residual for nonlinear hyperbolic eq
        """
    @property
    def sol(self) -> ngsolve.comp.GridFunction:
        """
        returns grid function representing the solution
        """
    @property
    def space(self) -> ngsolve.comp.FESpace:
        """
        returns finite element space
        """
    @property
    def tentslab(self) -> ngstents.TentSlab:
        """
        returns the tent pitched time slab
        """
    @property
    def time(self) -> ngsolve.fem.CoefficientFunction:
        """
        the time coordinate of a spacetime point in an advancing front
        """
    @property
    def u_minus(self) -> ngsolve.comp.ProxyFunction:
        """
        returns trial function u(x-s*n) for s->0^+ and the normal vector n
        """
class Euler(ConservationLaw):
    def __init__(self, gfu, tentslab, **kwargs):
        """
        
                INPUTS:
        
                gridfunction : GridFunction
                tentslab     : TentSlab
                outflow      : Optional[Region]
                inflow       : Optional[Region]
                reflect      : Optional[Region]
                
        """
class Maxwell(ConservationLaw):
    def __init__(self, gfu, tentslab, **kwargs):
        """
        
                INPUTS:
        
                gridfunction : GridFunction
                tentslab     : TentSlab
                outflow      : Optional[Region]
                inflow       : Optional[Region]
                reflect      : Optional[Region]
                
        """
class Wave(ConservationLaw):
    def __init__(self, gfu, tentslab, **kwargs):
        """
        
                INPUTS:
        
                gridfunction : GridFunction
                tentslab     : TentSlab
                outflow      : Optional[Region]
                inflow       : Optional[Region]
                reflect      : Optional[Region]
                transparent  : Optional[Region]
                
        """
