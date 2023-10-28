import math
import random
from typing import List, Optional, Literal
from city import City


class Organism:
    __chromosome: List[Optional["City"]]

    def __init__(self, chromosome: List[Optional["City"]]):
        self.__chromosome = chromosome
        self.mutate()

    def __str__(self) -> str:
        string = "{"
        for gene in self.__chromosome:
            string += str(gene) + "~"
        return string[:-1] + "}"

    def get_chromosome(self) -> List[Optional["City"]]:
        return self.__chromosome

    def mutate(self, form: Literal["random", "both", "swap", "inverse"] = "random") -> None:
        pass

    def mutate_swap(self) -> None:
        random.seed(tuple(self.__chromosome))
        point = random.randrange(0, len(self.__chromosome))
        next_point = (point + 1) % len(self.__chromosome)

        print("Mutate point", point, "-", next_point)

        temp = self.__chromosome[point]
        self.__chromosome[point] = self.__chromosome[next_point]
        self.__chromosome[next_point] = temp

    def mutate_inverse(self) -> None:
        random.seed(tuple(self.__chromosome))
        inverse_len = random.randint(2, math.floor(len(self.__chromosome) / 2))  # The length of inversed string
        start_point = random.randint(0, len(self.__chromosome) - 1)
        end_point = (start_point + inverse_len - 1) % len(self.__chromosome)
        if end_point > start_point:
            selected_dna = self.__chromosome[start_point:end_point + 1]
            selected_dna.reverse()
            self.__chromosome = self.__chromosome[:start_point] + selected_dna + self.__chromosome[end_point+1:]
        else:
            selected_dna = self.__chromosome[start_point:] + self.__chromosome[:end_point + 1]
            break_point = len(self.__chromosome)-start_point
            selected_dna.reverse()
            for dna in selected_dna:
                print(dna)
            self.__chromosome = selected_dna[break_point:] + self.__chromosome[end_point + 1:start_point] + \
                                selected_dna[:break_point]
        print("Inverse length", inverse_len, "| start point", start_point, "| end point", end_point)

    def calc_fitness(self) -> float:
        distance = 0
        for i, city in enumerate(self.__chromosome):
            if city == self.__chromosome[-1]:
                break
            distance += city.distance(self.__chromosome[i + 1])
        return distance
