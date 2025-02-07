import random
import time
from typing import List, Optional, Literal

from city import City, generate_cities
from generation import Generation
from organism import Organism


class Population:
    __all_gen_fitness: List[float]
    __all_gen_worst_fitness: List[float]
    __all_gen_best_fitness: List[float]
    __current_gen: Optional["Generation"]
    __optimal_solution: Optional["Organism"]

    def __init__(self, init_gen: Optional["Generation"] = None):
        self.__all_gen_fitness = list()
        self.__all_gen_worst_fitness = list()
        self.__all_gen_best_fitness = list()
        self.__current_gen = init_gen

    def get_all_gen_fitness(self) -> List[float]:
        return self.__all_gen_fitness

    def get_all_gen_worst_fitness(self) -> List[float]:
        return self.__all_gen_worst_fitness

    def get_all_gen_best_fitness(self) -> List[float]:
        return self.__all_gen_best_fitness

    def init_first_gen(self, gen_size: int = 20, cities: List[Optional["City"]] = None):
        if cities is None:
            raise ValueError(f"Argument 'cities' must not be 'None' but is {cities}")

        # create first generation of organisms
        organisms = list()
        for i in range(gen_size):
            random.seed(str(i) + time.time().hex())
            shuffled_cities = cities.copy()
            random.shuffle(shuffled_cities)
            organisms.append(Organism(chromosome=shuffled_cities))

        self.__current_gen = Generation(organisms)

    def is_stagnating(self, threshold: int = 3) -> bool:
        if threshold < 2:
            raise ValueError(f"Argument 'threshold' must be greater then 2 but is {threshold}")
        gen_fitness_evolution = self.__all_gen_fitness
        if len(gen_fitness_evolution) < threshold:
            return False
        return len(set(gen_fitness_evolution[-threshold:])) == 1

    def evolve(self, generations: int = 10, parents_ratio: float = 0.5, elite_percentage: float = 0.2,
               select_method: Literal["tournament", "roulette"] = "tournament",
               mutate_prob: float = 0.05, mutate_form: Literal["random", "both", "swap", "inverse"] = "random",
               gen_size: int = 30, mut_inc_threshold: int = 3, draw_nth: int = -1) -> Optional["Organism"]:
        init_mutate_prob = mutate_prob
        for i in range(generations):
            # print("gen", i, "| avg_fitness:", self.__current_gen.get_avg_fitness(),
            #       "| mutation probability:", mutate_prob)
            curr_best = min(self.__current_gen.get_organisms(),
                            key=lambda organism: organism.calc_fitness())
            if draw_nth > 0 and i % draw_nth == 0:
                curr_best.display(f"Generation {i}, fitness(): {curr_best.calc_fitness()}")
                # time.sleep(3)  # needed when you want to generate more than 30 images in PyCharm
            self.__all_gen_fitness.append(self.__current_gen.get_avg_fitness())
            self.__all_gen_worst_fitness.append(max(self.__current_gen.get_organisms(),
                                                    key=lambda organism: organism.calc_fitness()).calc_fitness())
            self.__all_gen_best_fitness.append(curr_best.calc_fitness())
            self.__current_gen = self.__current_gen.create_next_gen(parents_ratio=parents_ratio,
                                                                    select_method=select_method,
                                                                    mutate_prob=mutate_prob,
                                                                    mutate_form=mutate_form,
                                                                    next_gen_size=gen_size)
            if self.is_stagnating(threshold=mut_inc_threshold):
                mutate_prob = min(mutate_prob * 2, 1.0)
            else:
                mutate_prob = max(mutate_prob / 2, init_mutate_prob)
        self.__optimal_solution = min(self.__current_gen.get_organisms(), key=lambda organism: organism.calc_fitness())
        if draw_nth > 0:
            self.__optimal_solution.display(f"Generation {generations}, "
                                            f"fitness(): {self.__optimal_solution.calc_fitness()}")
        return self.__optimal_solution
