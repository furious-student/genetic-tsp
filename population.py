from typing import List, Optional, Literal

from generation import Generation


class Population:
    __all_gen_fitness: List[float]
    __current_gen: Optional["Generation"]

    def __init__(self, init_gen: Optional["Generation"]):
        self.__all_gen_fitness = list()
        self.__current_gen = init_gen

    def get_all_gen_fitness(self) -> List[float]:
        return self.__all_gen_fitness

    def is_stagnating(self, threshold: int = 3) -> bool:
        if threshold < 2:
            raise ValueError(f"Argument 'threshold' must be greater then 2 but is {threshold}")
        gen_fitness_evolution = self.__all_gen_fitness
        if len(gen_fitness_evolution) < threshold:
            return False
        return len(set(gen_fitness_evolution[-threshold:])) == 1

    def evolve(self, generations: int = 10, parents_ratio: float = 0.5, elite_percentage: float = 0.2,
               mutate_prob: float = 0.05, mutate_form: Literal["random", "both", "swap", "inverse"] = "random",
               gen_size: int = 30, mut_inc_threshold: int = 3):
        init_mutate_prob = mutate_prob
        for i in range(generations):
            print("gen", i, "avg_fitness:", self.__current_gen.get_avg_fitness())
            self.__all_gen_fitness.append(self.__current_gen.get_avg_fitness())
            self.__current_gen = self.__current_gen.create_next_gen(parents_ratio=parents_ratio,
                                                                    elite_percentage=elite_percentage,
                                                                    mutate_prob=mutate_prob,
                                                                    mutate_form=mutate_form,
                                                                    next_gen_size=gen_size)
            if self.is_stagnating(threshold=mut_inc_threshold):
                mutate_prob = min(mutate_prob*2, 1.0)
            else:
                mutate_prob = max(mutate_prob/2, init_mutate_prob)
