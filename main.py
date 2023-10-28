import math
import random
import time

from city import City
from organism import Organism


def main():
    cities = list()
    for i in range(10):
        random.seed(str(i) + time.time().hex())
        rand_x = random.randint(0, 200)
        rand_y = random.randint(0, 200)
        cities.append(City(x=math.floor(rand_x), y=math.floor(rand_y)))
    organism = Organism(chromosome=cities)
    print(organism)
    print(organism.calc_fitness())

    print("=========")
    # organism.mutate_swap()
    organism.mutate_inverse()
    print("=========")

    print(organism)
    print(organism.calc_fitness())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
