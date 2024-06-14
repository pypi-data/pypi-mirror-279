import unittest
from astraeus.integrator.runge_kutta import RungeKutta4
import numpy as np


class RungeKutta4Tests(unittest.TestCase):

    def test_ball_drop(self):
        """
        This example will be of numerical integration of a ball dropping.
        The state vector u = [position (x), velocity (v)]

        The analytical equation is x = x0 + (v0 * t) + ( 0.5 * a * t^2)
                                   v = v0 + (a * t)

        We should approach this as we decrease dt.

        """

        def du_function(u: np.ndarray) -> np.array:

            dx = u[1]
            dv = -9.81

            return np.array([dx, dv])

        u0 = np.array([10, 0])
        integrator = RungeKutta4(du_function)

        state = u0
        while state[0] >= 0:

            state = integrator.next(state, 0.5)

        self.assertTrue(state[0] <= 0)

        # ==============================================

        u0 = np.array([10, 0])
        integrator = RungeKutta4(du_function)

        state = u0
        dt = 0.001
        t = 0
        while state[0] >= 0:

            state = integrator.next(state, dt)
            t += dt

        # Time from analytical solution
        self.assertTrue(np.isclose(t, 1.427999, rtol=0.001))


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(RungeKutta4Tests))
    return test_suite


if __name__ == "__main__":
    unittest.main()
