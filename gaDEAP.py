import array
import time
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from learningUtils import LearningUtils, LearningRule
from create_rules import create_rules

utils = LearningUtils()
utils.setType('sqli')

from fuzzy_logic import FuzzySystem

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
#creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
# toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 18)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def init_individual(creator, levels):
    rule = LearningRule()
    rule.set_from_levels(levels)
    return creator(rule.chromosome)

def init_population(pcls, ind_init):
    return pcls(ind_init(x) for x in create_rules(utils.type))


toolbox.register("individual_guess", init_individual, creator.Individual)
toolbox.register("population_guess", init_population, list, toolbox.individual_guess)

toolbox.register("evaluate", utils.fitness_function)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def ga():
    #random.seed(time.time())

    pop = toolbox.population_guess()
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
    while True:
        res = ga()
        rule = LearningRule()
        rule.set_from_chromosome(res.items[0])
        print(rule.levels)
        if not rule in rules:
            fs.add_rule(rule.levels, utils.type)
            fs.start_system(utils.type)
            lastLen = len(utils.attack_data[utils.type])
            delete_attack_check(fs, utils.attack_data[utils.type])
            newLen = len(utils.attack_data[utils.type])
            if lastLen != newLen:
                rules.append(rule)
            print(newLen)
            if not len(utils.attack_data[utils.type]):
                break
    for rule in rules:
        print(rule.levels)