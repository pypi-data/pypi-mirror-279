import astropy.coordinates
import astropy.time
from astraeus.perturbation.perturbation import Perturbation
import astropy
from astraeus import constants
import numpy as np
from datetime import timedelta


class GravityPerturbation(Perturbation):
    def __init__(
        self, body: str, gravitation_parameter: float, t0: astropy.time.Time
    ) -> None:
        super().__init__()

        self.body: str = body
        self.gravitation_parameter: float = gravitation_parameter
        self.t0: astropy.time.Time = t0

    def acceleration(self, state: np.ndarray) -> np.ndarray:

        t = self.t0 + timedelta(seconds=state[0])

        body_position = astropy.coordinates.get_body_barycentric(self.body, t)  # icrs

        position = state[1:4]

        return np.array()

    @classmethod
    def EARTH(cls, t0: astropy.time.Time):

        perturbation = cls(
            "earth", constants.EARTH_STANDARD_GRAVITATIONAL_PARAMETER, t0
        )

        return perturbation

    # @classmethod
    # def SUN(cls):
    #     perturbation = cls()
    #     return perturbation

    # @classmethod
    # def MOON(cls):
    #     perturbation = cls()
    #     return perturbation
