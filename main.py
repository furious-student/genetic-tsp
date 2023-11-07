import math
import random
import time

from city import City
from organism import Organism
from generation import Generation
from population import Population


def main():
    organisms = list()
    cities = list()

    # create cities on map
    for i in range(10):
        random.seed(str(i) + time.time().hex())
        rand_x = random.randint(0, 200)
        rand_y = random.randint(0, 200)
        cities.append(City(x=math.floor(rand_x), y=math.floor(rand_y)))

    # create first generation of organisms
    for i in range(40):
        random.seed(str(i) + time.time().hex())
        shuffled_cities = cities.copy()
        random.shuffle(shuffled_cities)
        organisms.append(Organism(chromosome=shuffled_cities))

    population = Population(Generation(organisms))
    population.evolve(generations=100,
                      parents_ratio=0.5,
                      elite_percentage=0.2,
                      mutate_prob=0.1,
                      mutate_form="random",
                      gen_size=40,
                      mut_inc_threshold=3)
    print("Generations fitness:", population.get_all_gen_fitness())


if __name__ == '__main__':
    main()

