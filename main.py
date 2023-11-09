import re

from city import City
from utils import load_config
from population import Population


def main():

    # ------------------ reading config file ------------------
    # TODO: check config for correct types and missing values
    config = load_config()
    cities = list()
    alg_settings = config["algorithm_settings"]
    if cities is not None and len(cities) > 0:
        for city, corr in config["cities"].items():
            corr = re.sub(pattern="\(", repl="", string=corr)
            corr = re.sub(pattern="\)", repl="", string=corr)
            corr = corr.split(",")
            cities.append(City(x=int(corr[0]), y=int(corr[1])))
    else:
        cities = None
    map_size = alg_settings["map_size"]
    chromosome_len = alg_settings["chromosome_len"]
    overwrite_config = alg_settings["overwrite_config"]
    generations = alg_settings["generations"]
    parents_ratio = alg_settings["parents_ratio"]
    select_method = alg_settings["select_method"]
    elite_percentage = alg_settings["elite_percentage"]
    mutate_prob = alg_settings["mutate_prob"]
    mutate_form = alg_settings["mutate_form"]
    gen_size = alg_settings["gen_size"]
    mut_inc_threshold = alg_settings["mut_inc_threshold"]
    draw_nth = alg_settings["draw_nth"]
    # -----------------------------------------------------------

    population = Population()
    population.init_first_gen(map_size=map_size,
                              chromosome_len=chromosome_len,
                              gen_size=gen_size,
                              cities=cities,
                              overwrite_config=overwrite_config)  # if cities are defined, overwrite_config is ignored
    optimal_solution = population.evolve(generations=generations,
                                         parents_ratio=parents_ratio,
                                         select_method=select_method,
                                         elite_percentage=elite_percentage,
                                         mutate_prob=mutate_prob,
                                         mutate_form=mutate_form,
                                         gen_size=gen_size,
                                         mut_inc_threshold=mut_inc_threshold,
                                         draw_nth=draw_nth)
    # optimal_solution.draw()
    print("Generations fitness:", population.get_all_gen_fitness())
    print("Generations worst fitness:", population.get_all_gen_worst_fitness())
    print("Generations best fitness:", population.get_all_gen_best_fitness())
    print("Optimal solution:", optimal_solution, "| fitness:", optimal_solution.calc_fitness())


if __name__ == '__main__':
    main()
