import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from learningUtils import LearningUtils

utils = LearningUtils()
utils.setType('xss')

from fuzzy_logic import FuzzySystem

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 18)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



toolbox.register("evaluate", utils.fitness_function_for_one_rule)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def ga():
    random.seed(64)

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10,
                                   stats=stats, halloffame=hof, verbose=False)

    return hof #pop, log, hof


def delete_attack_check(fs, data):
    i = 0
    while i < len(data):
        try:
            res = fs.compute(data[i])
            if res > 50:
                del data[i]
                i = i - 1
        except ValueError:
            pass
        i = i + 1



if __name__ == "__main__":
    rules = []
    fs = FuzzySystem()
    allLine = len(utils.attack_data[utils.type])
    detectedLine = 0
    while True:
        res = ga()
        print(res.items)
        x = 0
        for bit in res.items[0]:
            x = (x << 1) | bit
        if not x in rules:
            rules.append(x)
            levels = utils.chromosome_to_rule(rules[-1])
            fs.add_rule(levels, utils.type)
            fs.start_system(utils.type)
            delete_attack_check(fs, utils.attack_data[utils.type])
            print(len(utils.attack_data[utils.type]))
            if not utils.attack_data[utils.type]:
                break
    for rule in rules:
        print(utils.chromosome_to_rule(rule))