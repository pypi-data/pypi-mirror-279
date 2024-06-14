from abc import abstractmethod, ABC
import numpy as np
from typing import Tuple
import astropy.units as u
from scipy.spatial.transform import Rotation


class Frame(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.base = "ECEF"

    @abstractmethod
    def frame(self, t: float) -> Rotation: ...

    @abstractmethod
    def look_angles(self, t: float) -> Tuple[u.deg, u.deg]: ...
