import astropy.units as u
import portion as P
from astropy.time import Time


class Interval(P.Interval):
    def __init__(self, *intervals):
        super().__init__(*intervals)

    @property
    def length(self) -> u.Quantity[u.s]:
        """
        Returns the total length of the interval in seconds.
        """

        windows = [
            (Time(i.upper) - Time(i.lower)).datetime.total_seconds() for i in self
        ]

        return sum(windows) * u.s

    def within(self, t: Time) -> bool:
        """
        Determines if t is within the interval.
        """
        raise NotImplementedError("Not Implemented")
