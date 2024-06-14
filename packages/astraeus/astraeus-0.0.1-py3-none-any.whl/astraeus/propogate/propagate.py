from astraeus.integrator.integrator import Integrator
from astraeus.perturbation.perturbation import Perturbation
from typing import List
from astraeus.orbit import Orbit
import astropy.units as u


class Propagate:
    def __init__(self) -> None:
        pass

    def propagate(
        self,
        orbit: Orbit,
        integrator: Integrator,
        dt: u.Quantity[u.s],
        frame: str,
        *pertubations: Perturbation
    ):
        pass
