import math
import random
from typing import List, Optional, Literal
from city import City


class Organism:
    __chromosome: List[Optional["City"]]

    def __init__(self, chromosome: List[Optional["City"]]):
        self.__chromosome = chromosome

    def __str__(self) -> str:
        string = "{~"
        for gene in self.__chromosome:
            string += str(gene) + "~"
        return string[:-1] + "~}"

    def get_chromosome(self) -> List[Optional["City"]]:
        return self.__chromosome

    def mutate(self, form: Literal["random", "both", "swap", "inverse"] = "random", probability: float = 0.05) -> None:
        if probability < 0 or probability > 1:
            raise ValueError(f"Argument probability can only be from interval <0, 1> but is {probability}")
        random.seed(self)
        if not random.random() <= probability:
            return
        if form == "swap":
            self.__mutate_swap()
            print("  > swap")
        elif form == "inverse":
            self.__mutate_inverse()
            print("  > inverse")
        elif form == "both":
            self.__mutate_swap()
            self.__mutate_inverse()
            print("  > swap")
            print("  > inverse")
        elif form == "random":
            random.seed(tuple(self.__chromosome * 2))
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                self.__mutate_swap()
                print("  > random: swap")
            else:
                self.__mutate_inverse()
                print("  > random: inverse")
        else:
            raise ValueError(f"Argument \"form\" has invalid value: \"{form}\"")

    def __mutate_swap(self) -> None:
        random.seed(tuple(self.__chromosome))
        point = random.randrange(0, len(self.__chromosome))
        next_point = (point + 1) % len(self.__chromosome)

        temp = self.__chromosome[point]
        self.__chromosome[point] = self.__chromosome[next_point]
        self.__chromosome[next_point] = temp

    def __mutate_inverse(self) -> None:
        random.seed(tuple(self.__chromosome))
        inverse_len = random.randint(2, math.floor(len(self.__chromosome) / 2))  # The length of inversed string
        start_point = random.randint(0, len(self.__chromosome) - 1)
        end_point = (start_point + inverse_len - 1) % len(self.__chromosome)
        if end_point > start_point:
            selected_dna = self.__chromosome[start_point:end_point + 1]
            selected_dna.reverse()
            self.__chromosome = self.__chromosome[:start_point] + selected_dna + self.__chromosome[end_point + 1:]
        else:
            selected_dna = self.__chromosome[start_point:] + self.__chromosome[:end_point + 1]
            break_point = len(self.__chromosome) - start_point
            selected_dna.reverse()
            self.__chromosome = selected_dna[break_point:] + self.__chromosome[end_point + 1:start_point] \
                                + selected_dna[:break_point]

    def calc_fitness(self) -> float:
        distance = 0
        for i, city in enumerate(self.__chromosome):
            if city == self.__chromosome[-1]:
                distance += city.distance(self.__chromosome[0])
                break
            distance += city.distance(self.__chromosome[i + 1])
        return distance

    def reproduce(self, other: Optional["Organism"], mutate_prob: float = 0.05,
                  mutate_form: Literal["random", "both", "swap", "inverse"] = "random") -> List[Optional["Organism"]]:
        self_chromo = self.__chromosome
        other_chromo = other.get_chromosome()

        random.seed(tuple(self.__chromosome))
        path_len = random.randint(2, math.floor(len(self.__chromosome) * 0.6))  # The length of inversed string
        start_point = random.randint(0, math.floor(len(self.__chromosome) * 0.4))

        self_path = self_chromo[start_point:start_point + path_len]
        other_path = other_chromo[start_point:start_point + path_len]

        self_to_other = self_chromo[start_point + path_len:] + self_chromo[:start_point] + self_path
        self_to_other = [city for city in self_to_other if city not in other_path]
        self_to_other.reverse()

        other_to_self = other_chromo[start_point + path_len:] + other_chromo[:start_point] + other_path
        other_to_self = [city for city in other_to_self if city not in self_path]
        other_to_self.reverse()

        first_chunk = self_to_other[:start_point]
        last_chunk = self_to_other[start_point:]
        first_chunk.reverse()
        last_chunk.reverse()
        first_child = Organism(first_chunk + other_path + last_chunk)
        first_child.mutate(form=mutate_form, probability=mutate_prob)

        first_chunk = other_to_self[:start_point]
        last_chunk = other_to_self[start_point:]
        first_chunk.reverse()
        last_chunk.reverse()
        second_child = Organism(first_chunk + self_path + last_chunk)
        second_child.mutate(form=mutate_form, probability=mutate_prob)
        return [first_child, second_child]
