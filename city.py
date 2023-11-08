import math
import random
import time
from typing import Tuple, Optional, List
from utils import load_config, write_config


class City:
    __location: Tuple[float, float]

    def __init__(self,
                 x: float = 0,
                 y: float = 0):
        self.__location = (x, y)

    def __str__(self):
        return "(" + str(self.__location[0]) + ", " + str(self.__location[1]) + ")"

    def __hash__(self):
        return hash(self.__location)

    def __eq__(self, other: Optional["City"]):
        if not isinstance(other, City):
            return False
        self_loc = self.__location
        other_loc = other.get_location()
        return self_loc[0] == other_loc[0] and self_loc[1] == other_loc[1]

    def get_location(self) -> Tuple[float, float]:
        return self.__location

    def distance(self, other: Optional["City"]) -> float:
        if not isinstance(other, City):
            raise TypeError("other is not an instance of the City class.")
        other_loc = other.get_location()
        return round(math.sqrt(pow(self.__location[0] - other_loc[0], 2) + pow(self.__location[1] - other_loc[1], 2)))


def generate_cities(length: int = 20, map_size: int = 200, to_config: bool = False) -> List[Optional["City"]]:
    cities = list()

    # create cities on map
    for i in range(length):
        random.seed(str(i) + time.time().hex())
        rand_x = random.randint(0, map_size + 1)
        rand_y = random.randint(0, map_size + 1)
        cities.append(City(x=math.floor(rand_x), y=math.floor(rand_y)))

    if to_config:
        __to_config(cities)
    return cities


def __to_config(cities: List[Optional["City"]]):
    config = load_config()
    yaml_cities = dict()
    for index,city in enumerate(cities):
        yaml_cities.update({str(index): f"{city.get_location()}"})
    config["cities"] = yaml_cities
    write_config("config/config.yaml", config)

