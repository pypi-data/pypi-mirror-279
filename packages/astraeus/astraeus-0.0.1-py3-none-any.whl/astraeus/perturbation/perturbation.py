from abc import abstractmethod, ABC
import numpy as np


class Perturbation(ABC):

    @abstractmethod
    def acceleration(self, state: np.ndarray) -> np.ndarray: ...
