import argparse
import os
import re
import sys

from city import City, generate_cities
from organism import Organism
from utils import load_config
from population import Population
from sim_annealing import SimAnnealing


def main():
    # ---------------------- parse args ----------------------
    try:
        config_path = parse_args()
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)
    # --------------------------------------------------------

    # ------------------ reading config file -----------------
    # TODO: check config for correct types and missing values
    config = load_config(path=config_path)

    general_settings = config["general_settings"]
    map_size = general_settings["map_size"]
    number_of_cities = general_settings["number_of_cities"]
    overwrite_config = general_settings["overwrite_config"]
    algorithm = general_settings["algorithm"]

    ga_settings = config["ga_settings"]
    generations = ga_settings["generations"]
    parents_ratio = ga_settings["parents_ratio"]
    select_method = ga_settings["select_method"]
    mutate_prob = ga_settings["mutate_prob"]
    mutate_form = ga_settings["mutate_form"]
    gen_size = ga_settings["gen_size"]
    mut_inc_threshold = ga_settings["mut_inc_threshold"]
    draw_nth = ga_settings["draw_nth"]

    sa_settings = config["sa_settings"]
    epoch_duration = sa_settings["epoch_duration"]
    init_temperature = sa_settings["init_temperature"]
    cool_by_factor = sa_settings["cool_by_factor"]

    cities = list()
    if config.get("cities") is not None and len(config.get("cities")) > 0:
        for city, corr in config["cities"].items():
            corr = re.sub(pattern="\(", repl="", string=corr)
            corr = re.sub(pattern="\)", repl="", string=corr)
            corr = corr.split(",")
            cities.append(City(x=int(corr[0]), y=int(corr[1])))
    else:
        cities = generate_cities(length=number_of_cities,
                                 map_size=map_size,
                                 to_config=overwrite_config,
                                 config_path=config_path)
    # -----------------------------------------------------------

    if algorithm == "sa" or algorithm == "both":
        print("Running Simulated Annealing Algorithm:")
        sim_annealing = SimAnnealing(init_solution=Organism(cities))
        # result = sim_annealing.grid_search(epoch_durations=[100, 250, 500],
        #                                    init_temperatures=[30, 40, 50],
        #                                    cool_by_factors=[0.05, 0.025, 0.01, 0.005])
        # optimal_solution = result.get("best_result")
        optimal_solution = sim_annealing.run(epoch_duration=epoch_duration,
                                             cool_by_factor=cool_by_factor,
                                             init_temperature=init_temperature)
        print("Optimal solution:", optimal_solution, "| fitness:", optimal_solution.calc_fitness())
    if algorithm == "ga" or algorithm == "both":
        print("Running Genetic Algorithm:")
        population = Population()
        population.init_first_gen(gen_size=gen_size,
                                  cities=cities)  # if cities are defined, overwrite_config is ignored
        optimal_solution = population.evolve(generations=generations,
                                             parents_ratio=parents_ratio,
                                             select_method=select_method,
                                             mutate_prob=mutate_prob,
                                             mutate_form=mutate_form,
                                             gen_size=gen_size,
                                             mut_inc_threshold=mut_inc_threshold,
                                             draw_nth=draw_nth)
        print("Generations fitness:", population.get_all_gen_fitness())
        print("Generations worst fitness:", population.get_all_gen_worst_fitness())
        print("Generations best fitness:", population.get_all_gen_best_fitness())
        print("Optimal solution:", optimal_solution, "| fitness:", optimal_solution.calc_fitness())


def parse_args() -> str:
    args_parser = argparse.ArgumentParser(description="Find optimal solution for TSP problem")
    args_parser.add_argument("-f", "--file", nargs=1,
                             help="The path to configuration yaml file.",
                             default=None,
                             const=None,
                             required=True)
    args = args_parser.parse_args()
    file = args.file[0]
    if file is None or not os.path.exists(file):
        if file is None:
            message = "No value given to the -f/--file required argument."
        else:
            message = "The configuration file \"" + args.file + "\" does not exist."
        raise FileNotFoundError(message)

    return file


if __name__ == '__main__':
    main()
