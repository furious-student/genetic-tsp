import math
import random
import time

from city import City
from organism import Organism
from generation import Generation
from population import Population


def main():
    population = Population()
    population.init_first_gen(map_size=200,
                              chromosome_len=10,
                              gen_size=30)
    optimal_solution = population.evolve(generations=1000,
                                         parents_ratio=0.5,
                                         select_method="tournament",
                                         elite_percentage=0.2,
                                         mutate_prob=0.1,
                                         mutate_form="random",
                                         gen_size=30,
                                         mut_inc_threshold=3)
    print("Generations fitness:", population.get_all_gen_fitness())
    print("Generations worst fitness:", population.get_all_gen_worst_fitness())
    print("Generations best fitness:", population.get_all_gen_best_fitness())
    print("Optimal solution:", optimal_solution, "| fitness:", optimal_solution.calc_fitness())


if __name__ == '__main__':
    main()
