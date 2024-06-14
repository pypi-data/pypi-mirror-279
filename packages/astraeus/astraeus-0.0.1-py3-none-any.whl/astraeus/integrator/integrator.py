from abc import abstractmethod, ABC
import numpy as np
from typing import Callable


class Integrator(ABC):
    def __init__(self, du: Callable[[np.ndarray], np.ndarray]) -> None:
        super().__init__()

        self.du = du

    @abstractmethod
    def next(self): ...
