import unittest
import numpy as np
from astraeus.perturbation.gravity_perturbation import GravityPerturbation
from astropy.time import Time
from astropy.coordinates import SkyCoord
import astropy
from astropy.coordinates import ICRS, CartesianRepresentation, CartesianDifferential
import astropy.units as u


class GravityPerturbationTests(unittest.TestCase):

    def test_earth_graivity(self):

        t0 = Time("2021-01-01T00:00:00.00", format="isot", scale="utc")

        u0 = ICRS(
            x=-0.185782 * u.au,
            y=-0.892517 * u.au,
            z=0.387018 * u.au,
            v_x=5 * u.km / u.s,
            v_y=5 * u.km / u.s,
            v_z=5 * u.km / u.s,
            representation_type=CartesianRepresentation,
            differential_type=CartesianDifferential,
        )

        print(u0)

        earth_gravity = GravityPerturbation.EARTH(t0)

        self.assertTrue(True)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(GravityPerturbationTests))
    return test_suite


if __name__ == "__main__":
    unittest.main()
