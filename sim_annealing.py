import copy
import itertools
import random

from time import time_ns

from organism import Organism
from typing import Optional, List, Dict, Any


class SimAnnealing:
    __current_solution: Optional["Organism"]
    __init_temperature: int

    def __init__(self, init_solution: Optional["Organism"]):
        self.__current_solution = init_solution

    def __generate_next(self) -> Optional["Organism"]:
        next_solution = copy.deepcopy(self.__current_solution)
        next_solution.mutate(form="swap", probability=1.0)  # swap two cities in the organism (current solution)
        return next_solution

    def __try_accept(self, descendant: Optional["Organism"], curr_temperature: float) -> bool:
        if descendant.calc_fitness() < self.__current_solution.calc_fitness():
            self.__current_solution = descendant
            return True
        random.seed(str(self.__current_solution) + str(time_ns()))
        if random.uniform(0, self.__init_temperature) < curr_temperature:
            self.__current_solution = descendant
            return True
        return False

    def run(self, epoch_duration: int = 1000, cool_by_factor: float = 0.025, init_temperature: int = 30)\
            -> Optional["Organism"]:
        if cool_by_factor < 0 or cool_by_factor >= 1:
            raise ValueError(f"Argument 'cool_by_factor' must be a float in range <0,1) but is {cool_by_factor}.")

        self.__init_temperature = init_temperature
        curr_temperature = self.__init_temperature
        while curr_temperature > 0:
            for _ in range(epoch_duration):
                # print(f"fitness: {self.__current_solution.calc_fitness()} | temperature: {curr_temperature} | "
                #      f"{self.__current_solution}")
                self.__try_accept(self.__generate_next(), curr_temperature=curr_temperature)
            curr_temperature -= cool_by_factor*init_temperature
        return self.__current_solution

    def grid_search(self, epoch_durations: List[int], init_temperatures, cool_by_factors) -> Dict[str, Any]:
        best_result = None
        best_params = None

        for params in itertools.product(epoch_durations, init_temperatures, cool_by_factors):
            epoch_duration, init_temperature, cool_by_factor = params
            result = self.run(epoch_duration=epoch_duration,
                              init_temperature=init_temperature,
                              cool_by_factor=cool_by_factor)

            # Evaluate and compare results
            if best_result is None or result.calc_fitness() < best_result.calc_fitness():
                best_result = result
                best_params = params
            print(f"Done searching for params configuration: "
                  f"[epoch_duration, temperature, cool_by_factor, stop_temperature] {params}")

        print(f"Best Parameters: {best_params}")
        print(f"Best Result Fitness: {best_result.calc_fitness()}")
        print(f"Best Result: {best_result}")
        return {
            "best_result": best_result,
            "best_params": best_params
        }
