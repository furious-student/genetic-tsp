import copy
import random
from typing import List, Optional, Dict, Literal
from time import time_ns

from organism import Organism


class Generation:
    __organisms: List[Optional["Organism"]]
    __eval_organisms: Dict[Optional["Organism"], int]
    __parents: List[Optional["Organism"]]

    def __init__(self, organisms: List[Optional["Organism"]]):
        self.__organisms = organisms

    def get_organisms(self) -> List[Optional["Organism"]]:
        return self.__organisms

    def get_total_fitness(self) -> float:
        fitness = 0
        for organism in self.__organisms:
            fitness += organism.calc_fitness()
        return round(fitness, 2)

    def get_avg_fitness(self) -> float:
        return round(self.get_total_fitness() / len(self.__organisms), 2)

    def evaluate(self, organisms: List[Optional["Organism"]] = None, assign_to_self=True) -> \
            Dict[Optional["Organism"], float]:
        if assign_to_self:
            organisms = self.__organisms
        eval_organisms = {key: key.calc_fitness() for key in organisms}
        eval_organisms = dict(sorted(eval_organisms.items(), key=lambda organism: organism[1]))
        if assign_to_self:
            self.__eval_organisms = eval_organisms
        return eval_organisms

    def pick_elite(self, elite_percentage: float = 0.2) -> List[Optional["Organism"]]:
        if elite_percentage < 0 or elite_percentage > 1:
            raise ValueError(f"Argument elite_percentage can be only from interval <0, 1> but is {elite_percentage}")

        elite_size = round(len(self.__organisms) * elite_percentage)
        elite = list()
        for organism in self.__eval_organisms:
            if elite_size > 0:
                elite.append(organism)
                elite_size -= 1
        return elite

    def select_parents(self, parents_percentage: float = 0.5, method: Literal["tournament", "roulette"] = "tournament",
                       tournament_size_percentage: float = 0.33):
        if method == "tournament":
            self.__select_by_tournament(parents_percentage=parents_percentage,
                                        tournament_size_percentage=tournament_size_percentage)
        elif method == "roulette":
            self.__select_by_roulette(parents_percentage=parents_percentage)

    def __select_by_tournament(self, parents_percentage: float = 0.5, tournament_size_percentage: float = 0.33) -> None:
        if parents_percentage < 0 or parents_percentage > 1:
            raise ValueError(f"Argument parents_percentage can only be from interval <0, 1> "
                             f"but is {parents_percentage}")
        if tournament_size_percentage < 0 or tournament_size_percentage > 1:
            raise ValueError(f"Argument tournament_size_percentage can only be from interval <0, 1> "
                             f"but is {tournament_size_percentage}")

        parents_size = round(len(self.__organisms) * parents_percentage)
        if parents_size % 2 == 1:
            parents_size += 1
        tournament_size = round(len(self.__organisms) * tournament_size_percentage)
        parents = set()
        while len(parents) < parents_size:
            parents.add(self.__tournament(tournament_size))
        self.__parents = list(parents)

    def __tournament(self, t_size: int) -> Optional["Organism"]:
        champions = dict(random.sample(self.__eval_organisms.items(), t_size))
        return min(champions, key=champions.get)

    def __select_by_roulette(self, parents_percentage: float = 0.5):
        if parents_percentage < 0 or parents_percentage > 1:
            raise ValueError(f"Argument parents_percentage can only be from interval <0, 1> "
                             f"but is {parents_percentage}")

        parents_size = round(len(self.__organisms) * parents_percentage)
        if parents_size % 2 == 1:
            parents_size += 1
        parents = set()
        fitness_sum = 1/self.get_total_fitness()
        sorted_organisms = sorted(self.__organisms, key=lambda o: 1/o.calc_fitness())
        while len(parents) < parents_size:
            random.seed(str(self.__organisms) + str(time_ns()))
            roulette_point = random.uniform(0, fitness_sum)
            current_fitness_sum = 0
            for organism in sorted_organisms:
                if current_fitness_sum >= roulette_point:
                    parents.add(organism)
                current_fitness_sum += 1/organism.calc_fitness()
        self.__parents = list(parents)

    def reproduce(self, mutate_prob: float = 0.05,
                  mutate_form: Literal["random", "both", "swap", "inverse"] = "random") -> List[Optional["Organism"]]:
        children = list()
        for i in range(0, len(self.__parents), 2):
            parent1 = self.__parents[i]
            parent2 = self.__parents[2]
            children += (parent1.reproduce(parent2, mutate_prob=mutate_prob, mutate_form=mutate_form))
        return children

    def create_next_gen(self, parents_ratio: float = 0.5, mutate_prob: float = 0.05, next_gen_size: int = 30,
                        select_method: Literal["tournament", "roulette"] = "tournament",
                        mutate_form: Literal["random", "both", "swap", "inverse"] = "random"):
        self.evaluate()
        self.select_parents(parents_percentage=parents_ratio, method=select_method, tournament_size_percentage=0.33)
        children = self.reproduce(mutate_prob=mutate_prob, mutate_form=mutate_form)
        all_organisms = copy.deepcopy(self.__organisms) + children

        all_eval = self.evaluate(organisms=all_organisms, assign_to_self=False)
        next_gen_organisms = list()

        for organism, fitness in all_eval.items():
            if next_gen_size > 0:
                next_gen_organisms.append(organism)
                next_gen_size -= 1

        return Generation(next_gen_organisms)
