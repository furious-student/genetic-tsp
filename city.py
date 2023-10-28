import math
import random
import time
from typing import Tuple, Optional


class City:
    __location: Tuple[float, float]

    def __init__(self,
                 x: float = 0,
                 y: float = 0):
        self.__location = (x, y)

    def __str__(self):
        return "(" + str(self.__location[0]) + ", " + str(self.__location[1]) + ")"

    def get_location(self) -> Tuple[float, float]:
        return self.__location

    def distance(self, other: Optional["City"]) -> float:
        if not isinstance(other, City):
            raise TypeError("other is not an instance of the City class.")
        other_loc = other.get_location()
        return math.sqrt(pow(self.__location[0] - other_loc[0], 2) + pow(self.__location[1] - other_loc[1], 2))
