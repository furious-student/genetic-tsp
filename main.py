import math
import random
import time

from city import City
from organism import Organism
from generation import Generation


def main():
    organisms = list()
    cities = list()
    for i in range(10):
        random.seed(str(i) + time.time().hex())
        rand_x = random.randint(0, 200)
        rand_y = random.randint(0, 200)
        cities.append(City(x=math.floor(rand_x), y=math.floor(rand_y)))
    for i in range(30):
        random.seed(str(i) + time.time().hex())
        shuffled_cities = cities.copy()
        random.shuffle(shuffled_cities)
        organisms.append(Organism(chromosome=shuffled_cities))

    generation = Generation(organisms)
    gen2 = generation.create_next_gen()
    gen3 = gen2.create_next_gen()
    gen4 = gen3.create_next_gen()

    print("=================")
    generation.evaluate()
    print(generation.get_avg_fitness(), "\n")
    gen2.evaluate()
    print(gen2.get_avg_fitness(), "\n")
    gen3.evaluate()
    print(gen3.get_avg_fitness(), "\n")
    gen4.evaluate()
    print(gen4.get_avg_fitness(), "\n")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
