from abc import abstractmethod, ABC
from typing import Tuple
import astropy.units as u


class BaseBody(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def position(
        self, t
    ) -> Tuple[u.Quantity[u.m], u.Quantity[u.m], u.Quantity[u.m]]: ...

    @abstractmethod
    def velocity(
        self, t
    ) -> Tuple[u.Quantity[u.m / u.s], u.Quantity[u.m / u.s], u.Quantity[u.m / u.s]]: ...
