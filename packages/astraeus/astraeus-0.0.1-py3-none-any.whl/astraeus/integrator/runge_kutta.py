from astraeus.integrator.integrator import Integrator
import numpy as np
from abc import ABC
from typing import Callable


class RungeKutta(Integrator, ABC):
    def __init__(self, du: Callable[[np.ndarray], np.ndarray]) -> None:
        super().__init__(du)

        self.a: np.ndarray = np.array([])
        self.b: np.ndarray = np.array([])
        self.c: np.ndarray = np.array([])

    def next(self, state, dt):

        f = np.zeros((len(state), (len(self.b))))

        for i in range(len(self.b)):

            u = np.array(state, copy=True)

            for j in range(i):

                u = np.add(u, dt * self.a[i][j] * f[:, j])

            f[:, i] = self.du(u)

        u = np.array(state, copy=True)

        for j in range(len(self.b)):
            u = np.add(u, dt * self.b[j] * f[:, j])

        return u


class RungeKutta4(RungeKutta):
    def __init__(self, du: Callable[[np.ndarray], np.ndarray]) -> None:
        super().__init__(du)

        self.a = np.array([[0, 0, 0, 0], [0.5, 0, 0, 0], [0, 0.5, 0, 0], [0, 0, 1, 0]])
        self.b = np.array([1, 2, 2, 1]) / 6
        self.c = np.array([])
